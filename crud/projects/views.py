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
def projects(request):
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
# @can_edit_project
def project(request, code, project=None):
    """
    modifica dati progetto
    """
    form = ProgettoDatiBaseForm(instance=project)

    researchers = ProgettoRicercatore.objects.filter(id_progetto=project)
    scientific_directors = ProgettoResponsabileScientifico.objects.filter(
        id_progetto=project)

    structure_data = get_object_or_404(ProgettoDatiBase, pk=code)

    if request.POST:
        form = ProgettoDatiBaseForm(instance=project, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            project.user_mod = request.user
            project.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            if changed_field_labels:
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
                   'researchers': researchers,
                   'scientific_directors': scientific_directors,
                   'structure_data': structure_data})


@login_required
@can_manage_projects
def project_new(request):
    """
    nuovo progetto
    """
    # tre form
    # dati progetto, direttore e struttura
    form = ProgettoDatiBaseForm()
    structure_form = ProgettoStrutturaForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque la struttura senza doverli cercare
    # nuovamente dall'elenco
    structure = None

    if request.POST.get('choosen_structure', ''):
        structure = get_object_or_404(UnitaOrganizzativa,
                                      uo=(request.POST['choosen_structure']))

    if request.POST:
        form = ProgettoDatiBaseForm(data=request.POST)
        structure_form = ProgettoStrutturaForm(data=request.POST)

        # se tutti i form sono validi
        if form.is_valid() and structure_form.is_valid():

            project = form.save(commit=False)
            # struttura del progetto
            project.uo = structure
            project.save()

            log_action(user=request.user,
                       obj=project,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Project created successfully"))
            return redirect("crud_projects:crud_projects")

        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

            for k, v in structure_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{structure_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   '#': _('New')}

    return render(request,
                  'project_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_structure': f'{structure.denominazione}' if structure else '',
                   'form': form,
                   'structures_api': reverse('ricerca:structureslist'),
                   'structure_form': structure_form,
                   })


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_projects
# # @can_edit_project
def project_delete(request, code, project=None):
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


@login_required
@can_manage_projects
# @can_edit_project
def project_director_new(request, code, project=None):
    """
    nuovo direttore scientifico
    """
    external_form = ProgettoResponsabileScientificoForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoResponsabileScientificoForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                director_code = decrypt(form.cleaned_data['choosen_person'])
                director = get_object_or_404(
                    Personale, matricola=director_code)
                nome_origine = f'{director.cognome} {director.nome}'
            else:
                director = None
                nome_origine = form.cleaned_data['nome_origine']

            p = ProgettoResponsabileScientifico.objects.create(
                id_progetto=project,
                matricola=director,
                nome_origine=nome_origine
            )

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo direttore scientifico {p}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director added successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:
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
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
# @can_edit_project
def project_director_edit(request, code, director_id, project=None):
    """
    dettaglio direttore scientifico
    """
    project_director = get_object_or_404(ProgettoResponsabileScientifico.objects.select_related('matricola'),
                                         pk=director_id,
                                         id_progetto=project)
    old_label = project_director.nome_origine
    director = project_director.matricola
    initial = {}
    director_data = ''
    if director:
        director_data = f'{director.cognome} {director.nome}'
        initial = {'choosen_person': encrypt(director.matricola)}

    external_form = ProgettoResponsabileScientificoForm(
        instance=project_director)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoResponsabileScientificoForm(instance=project_director,
                                                       data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                director_code = decrypt(form.cleaned_data['choosen_person'])
                director = get_object_or_404(
                    Personale, matricola=director_code)
                project_director.matricola = director
                project_director.nome_origine = f'{director.cognome} {director.nome}'
            else:
                project_director.matricola = None
                project_director.nome_origine = form.cleaned_data['nome_origine']

            project_director.save()

            if old_label != project_director.nome_origine:
                log_action(user=request.user,
                           obj=project,
                           flag=CHANGE,
                           msg=f'Sostituito direttore scientifico {old_label} con {project_director}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director data edited successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': f'{_("Director")} {project_director}'
                   }

    return render(request,
                  'project_director.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': director_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
# @can_edit_project
def project_director_delete(request, code, director_id, project=None):
    """
    elimina dati direttore scientifico
    """
    director_project = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id,
                                         id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'Rimosso direttore scientifico {director_project}')

    director_project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Director removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_new(request, code, project=None):
    """
    nuovo ricercatore
    """
    external_form = ProgettoRicercatoreForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoRicercatoreForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                researcher_code = decrypt(form.cleaned_data['choosen_person'])
                researcher = get_object_or_404(
                    Personale, matricola=researcher_code)
                nome_origine = f'{researcher.cognome} {researcher.nome}'
            else:
                researcher = None
                nome_origine = form.cleaned_data['nome_origine']

            p = ProgettoRicercatore.objects.create(
                id_progetto=project,
                matricola=researcher,
                nome_origine=nome_origine
            )
            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo ricercatore {p}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher added successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:
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
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_edit(request, code, researcher_id, project=None):
    """
    dettaglio ricercatore
    """
    project_researcher = get_object_or_404(ProgettoRicercatore.objects.select_related('matricola'),
                                           pk=researcher_id,
                                           id_progetto=project)
    old_label = project_researcher.nome_origine
    researcher = project_researcher.matricola
    initial = {}
    researcher_data = ''
    if researcher:
        researcher_data = f'{researcher.cognome} {researcher.nome}'
        initial = {'choosen_person': encrypt(researcher.matricola)}

    external_form = ProgettoRicercatoreForm(instance=project_researcher)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoRicercatoreForm(instance=project_researcher,
                                           data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                researcher_code = decrypt(form.cleaned_data['choosen_person'])
                researcher = get_object_or_404(
                    Personale, matricola=researcher_code)
                project_researcher.matricola = researcher
                project_researcher.nome_origine = f'{researcher.cognome} {researcher.nome}'
            else:
                project_researcher.matricola = None
                project_researcher.nome_origine = form.cleaned_data['nome_origine']

            project_researcher.save()

            if old_label != project_director.nome_origine:
                log_action(user=request.user,
                           obj=project,
                           flag=CHANGE,
                           msg=f'Sostituito ricercatore {old_label} con {project_researcher}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher data edited successfully"))
            return redirect('crud_projects:crud_project_edit',
                            code=code)
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_projects:crud_projects'): _('Projects'),
                   reverse('crud_projects:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': f'{_("Researcher")} {project_researcher}'
                   }

    return render(request,
                  'project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': researcher_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_delete(request, code, researcher_id, project=None):
    """
    elimina ricercatore
    """
    researcher = get_object_or_404(ProgettoRicercatore,
                                   pk=researcher_id,
                                   id_progetto=project)

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'Rimosso ricercatore {researcher}')

    researcher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Researcher removed successfully"))
    return redirect('crud_projects:crud_project_edit', code=code)


@login_required
@can_manage_projects
# @can_edit_project
def project_structure_data_edit(request, code, data_id, project=None):
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

            if structure != new_structure:
                log_action(user=request.user,
                           obj=project,
                           flag=CHANGE,
                           msg=f'Sostituita struttura {structure} con {new_structure}')

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
                  'project_structure.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'choosen_structure': structure.denominazione,
                   'url': reverse('ricerca:structureslist')})
