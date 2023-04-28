import logging

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. utils.forms import *
from .. utils.utils import log_action

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_projects
def projects(request, my_offices=None):
    """
    lista dei progetti
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Projects')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:projects')}
    return render(request, 'projects.html', context)


@login_required
@can_manage_projects
def project_new(request, my_offices=None):
    """
    nuovo progetto
    """
    # tre form
    # dati progetto, direttore e struttura
    form = ProgettoDatiBaseForm()
    director_form = ProgettoResponsabileScientificoForm()
    structure_form = ProgettoStrutturaForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque direttore e struttura scelti senza doverli cercare
    # nuovamente dall'elenco
    director = None
    structure = None
    if request.POST.get('choosen_person', ''):
        director = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST.get('choosen_structure', ''):
        structure = get_object_or_404(UnitaOrganizzativa,
                                      uo=(request.POST['choosen_structure']))

    if request.POST:
        form = ProgettoDatiBaseForm(data=request.POST)
        director_form = ProgettoResponsabileScientificoForm(data=request.POST)
        structure_form = ProgettoStrutturaForm(data=request.POST)

        # se tutti i form sono validi
        if form.is_valid() and director_form.is_valid() and structure_form.is_valid():

            # controlla se l'utente ha il diritto di
            # associare il progetto alla struttura
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(office__organizational_structure__unique_code=structure.uo,
                                                                                        employee=request.user,
                                                                                        office__name=OFFICE_PROJECTS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True)
                if not structure_afforg:
                    raise Exception(
                        _("Add director belonging to your structure"))

            project = form.save(commit=False)
            # struttura del progetto
            project.uo = structure
            project.save()

            # responsabile del progetto
            p = ProgettoResponsabileScientifico.objects.create(id_progetto=project,
                                                               nome_origine=director_form.cleaned_data['nome_origine'],
                                                               matricola=director)
            if director and not director_form.cleaned_data['nome_origine']:
                p.nome_origine = f'{director.nome} {director.cognome}'
                p.save()

            log_action(user=request.user,
                       obj=project,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Project created successfully"))
            return redirect("crud_projects:crud_projects")

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in director_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{director_form.fields[k].label}</b>: {v}")

            for k, v in structure_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{structure_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   '#': _('New')}

    return render(request,
                  'project_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{director.nome} {director.cognome}' if director else '',
                   'choosen_structure': f'{structure.denominazione}' if structure else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'structures_api': reverse('ricerca:structureslist'),
                   'director_form': director_form,
                   'structure_form': structure_form,
                   })


@login_required
@can_manage_projects
@can_edit_project
def project(request, code,
            my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    modifica dati progetto
    """
    form = ProgettoDatiBaseForm(instance=project)

    structure_data = get_object_or_404(ProgettoDatiBase, pk=code)

    if request.POST:
        form = ProgettoDatiBaseForm(instance=project, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            project.user_mod = request.user
            project.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Project edited successfully"))

            return redirect('crud_projects:crud_project_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(project).pk,
                                   object_id=project.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   '#': project.titolo}

    return render(request,
                  'project.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'project': project,
                   'structure_data': structure_data,
                   'researchers': researchers,
                   'scientific_director': scientific_director})


@login_required
@can_manage_projects
@can_edit_project
def project_director_data(request, code, director_id, project=None,
                          researchers=None, scientific_director=None, my_offices=None):
    """
    dettaglio direttore scientifico
    """
    director_data = get_object_or_404(ProgettoResponsabileScientifico.objects.select_related('matricola'),
                                      pk=director_id,
                                      id_progetto=project)
    matricola = director_data.matricola

    form = ProgettoResponsabileScientificoForm(instance=director_data)

    if request.POST:
        form = ProgettoResponsabileScientificoForm(instance=director_data,
                                                   data=request.POST)
        if form.is_valid():
            director_data.user_mod = request.user
            director_data.nome_origine = form.cleaned_data['nome_origine']

            if matricola and not form.cleaned_data['nome_origine']:
                director_data.nome_origine = f'{matricola.nome} {matricola.cognome}'

            director_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director data edited successfully"))

            return redirect('crud_projects:crud_project_director_data',
                            code=code,
                            director_id=director_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   reverse('crud_projects:crud_project_director_data_edit', kwargs={'code': code, 'director_id': director_id}): _('Director')
                   }

    return render(request,
                  'project_director_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'director_data': director_data})


@login_required
@can_manage_projects
@can_edit_project
def project_structure_data_edit(request, code, data_id,
                                my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    modifica struttura
    """
    structure_project = get_object_or_404(ProgettoDatiBase.objects.select_related('uo'),
                                          pk=data_id)

    structure = structure_project.uo
    form = ProgettoStrutturaForm(initial={'choosen_structure': structure.uo})

    if request.POST:
        form = ProgettoStrutturaForm(data=request.POST)
        if form.is_valid():
            structure_code = form.cleaned_data['choosen_structure']
            new_structure = get_object_or_404(UnitaOrganizzativa,
                                              uo=structure_code)
            structure_project.user_mod = request.user
            structure_project.uo = new_structure
            structure_project.save()

            log_msg = f'{_("Changed structure")} {structure}' \
                      if structure == new_structure \
                      else f'{structure} {_("substituted with")} {new_structure}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Structure edited successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Companies'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('Structure')}

    return render(request,
                  'project_structure_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'choosen_structure': structure.denominazione,
                   'url': reverse('ricerca:structureslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_data_edit(request, code, director_id, researchers=None, scientific_director=None,
                               my_offices=None, project=None):

    director_project = get_object_or_404(ProgettoResponsabileScientifico.objects.select_related('matricola'),
                                         pk=director_id,
                                         id_progetto=project)

    director = director_project.matricola
    initial = {}
    director_data = ''

    if director:
        director_data = f'{director.cognome} {director.nome}'
        initial={'choosen_person': encrypt(director.matricola)}

    form = ChoosenPersonForm(initial=initial)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST)
        if form.is_valid():
            director_code = decrypt(form.cleaned_data['choosen_person'])
            new_director = get_object_or_404(Personale,
                                             matricola=director_code)
            director_project.matricola = new_director
            director_project.nome_origine = f'{new_director.nome} {new_director.cognome}'
            director_project.save()

            if director and director == new_director:
                log_msg = f'{_("Changed director")} {director}'
            elif director and director != new_director:
                log_msg = f'{director} {_("substituted with")} {new_director}'
            else:
                log_msg = f'{_("Changed director")} {new_director}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director edited successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   reverse('crud_projects:crud_project_director_data',
                           kwargs={'code': code,
                                   'director_id': director_id}): _('Director'),
                   '#': _('Edit')}
    return render(request,
                  'project_director_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'director_id': director_id,
                   'choosen_person': director_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_delete(request, code, director_id,
                            my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    elimina dati direttore scientifico
    """
    director_project = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id,
                                         id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted director")} {director_project.nome_origine}')

    director_project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Director removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_director_new(request, code, my_offices=None, project=None,
                         researchers=None, scientific_director=None):
    """
    nuovo direttore scientifico
    """
    form = ProgettoResponsabileScientificoForm()
    if request.POST:
        form = ProgettoResponsabileScientificoForm(data=request.POST)
        if form.is_valid():

            p = ProgettoResponsabileScientifico.objects.create(
                id_progetto=project,
                nome_origine=form.cleaned_data['nome_origine']
            )
            director_code = decrypt(form.cleaned_data['choosen_person'])
            if director_code:
                director = get_object_or_404(Personale, matricola=director_code)
                p.matricola = director
                if not form.cleaned_data['nome_origine']:
                    p.nome_origine = f'{director.nome} {director.cognome}'
                p.save()

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'{_("Added director")} {p.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director added successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('New director')}

    return render(request,
                  'project_director.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_delete_link(request, code, director_id,
                            my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    elimina direttore scientifico
    """
    project_director = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id,
                                         id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted director link")} {project_director.nome_origine}')

    project_director.matricola = None
    inventor.save()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Director link removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_data(request, code, researcher_id, researchers, scientific_director=None,
                            my_offices=None, project=None):
    """
    dettaglio ricercatore
    """
    researcher_data = get_object_or_404(ProgettoRicercatore.objects.select_related('matricola'),
                                        pk=researcher_id,
                                        id_progetto=project)
    matricola = researcher_data.matricola

    form = ProgettoRicercatoreForm(instance=researcher_data)

    if request.POST:
        form = ProgettoRicercatoreForm(instance=researcher_data,
                                       data=request.POST)
        if form.is_valid():
            researcher_data.user_mod = request.user
            researcher_data.nome_origine = form.cleaned_data['nome_origine']

            if matricola and not form.cleaned_data['nome_origine']:
                researcher_data.nome_origine = f'{matricola.nome} {matricola.cognome}'

            researcher_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher data edited successfully"))

            return redirect('crud_projects:crud_project_researcher_data',
                            code=code,
                            researcher_id=researcher_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Companies'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   "#": _('Researcher')
                   }

    return render(request,
                  'project_researcher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'researcher_data': researcher_data})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_data_edit(request, code, researcher_id, researchers, scientific_director=None,
                                 my_offices=None, project=None):
    """
    modifica dati ricercatore
    """
    researcher_project = get_object_or_404(ProgettoRicercatore.objects.select_related('matricola'),
                                           pk=researcher_id,
                                           id_progetto=project)

    researcher = researcher_project.matricola
    initial = {}
    researcher_data = ''

    if researcher:
        researcher_data = f'{researcher.cognome} {researcher.nome}'
        initial={'choosen_person': encrypt(researcher.matricola)}

    form = ChoosenPersonForm(initial=initial)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST)
        if form.is_valid():
            researcher_code = decrypt(form.cleaned_data['choosen_person'])
            new_researcher = get_object_or_404(Personale, matricola=researcher_code)
            researcher_project.matricola = new_researcher
            researcher_project.nome_origine = f'{new_researcher.nome} {new_researcher.cognome}'
            researcher_project.save()

            if researcher and researcher == new_researcher:
                log_msg = f'{_("Changed inventor")} {researcher}'
            elif researcher and researcher != new_researcher:
                log_msg = f'{researcher} {_("substituted with")} {new_researcher}'
            else:
                log_msg = f'{_("Changed researcher")} {new_researcher}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher edited successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Companies'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   reverse('crud_projects:crud_project_researcher_data',
                           kwargs={'code': code,
                                   'researcher_id': researcher_id}): _('Researcher'),
                   "#": _('Edit')
                   }

    return render(request,
                  'project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'researcher_id': researcher_id,
                   'choosen_person': researcher_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_new(request, code, my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    nuovo ricercatore
    """
    form = ProgettoRicercatoreForm()
    if request.POST:
        form = ProgettoRicercatoreForm(data=request.POST)
        if form.is_valid():
            p = ProgettoRicercatore.objects.create(
                id_progetto=project,
                nome_origine=form.cleaned_data['nome_origine']
            )
            researcher_code = decrypt(form.cleaned_data['choosen_person'])
            if researcher_code:
                researcher = get_object_or_404(Personale,
                                               matricola=researcher_code)
                p.matricola = researcher

                if not form.cleaned_data['nome_origine']:
                    p.nome_origine = f'{researcher.nome} {researcher.cognome}'

                p.save()

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'{_("Added researcher")} {p}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher added successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('New researcher')}

    return render(request,
                  'project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_delete(request, code, researcher_id,
                              my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    elimina ricercatore
    """
    researcher_project = get_object_or_404(ProgettoRicercatore,
                                           pk=researcher_id,
                                           id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted researcher")} {researcher_project.nome_origine}')

    researcher_project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Researcher removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_delete_link(request, code, researcher_id,
                              my_offices=None, project=None, researchers=None, scientific_director=None):
    """
    elimina ricercatore
    """
    researcher_project = get_object_or_404(ProgettoRicercatore,
                                           pk=researcher_id,
                                           id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted researcher link")} {researcher_project.nome_origine}')

    researcher_project.matricola = None
    researcher_project.save()

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Researcher link removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_projects
# @can_edit_project
def project_delete(request, code,
                   my_offices=None, project=None, researchers=None, scientific_director=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    project = get_object_or_404(ProgettoDatiBase, pk=code)
    project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Project removed successfully"))

    return redirect('crud_projects:crud_projects')
