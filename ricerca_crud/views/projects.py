import logging

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. decorators import *
from .. forms import *
from .. utils import log_action


logger = logging.getLogger(__name__)


@login_required
@can_manage_projects
def projects(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Projects')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:projects')}
    return render(request, 'projects/projects.html', context)


@login_required
@can_manage_projects
def project_new(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   '#': _('New')}
    form = ProgettoDatiBaseForm()
    director_form = ProgettoResponsabileScientificoForm()
    structure_form = ProgettoDatiBaseFormWithoutFields()

    query_filter = Q()

    # already choosen before form fails
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
        structure_form = ProgettoDatiBaseFormWithoutFields(data=request.POST)

        if form.is_valid() and director_form.is_valid() and structure_form.is_valid():
            director_code = decrypt(
                director_form.cleaned_data['choosen_person'])
            director = get_object_or_404(Personale, matricola=director_code)

            structure_code = structure_form.cleaned_data['choosen_structure']
            structure = get_object_or_404(
                UnitaOrganizzativa, uo=structure_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:

                query_filter = Q(
                    office__organizational_structure__unique_code=director.cd_uo_aff_org_id)

                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(query_filter,
                                                                                        employee=request.user,
                                                                                        office__name=OFFICE_PROJECTS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True
                                                                                        )
                if not structure_afforg:
                    raise Exception(
                        _("Add director belonging to your structure"))

            project = ProgettoDatiBase.objects.create(
                titolo=form.cleaned_data['titolo'],
                anno_avvio=form.cleaned_data['anno_avvio'],
                descr_breve=form.cleaned_data['descr_breve'],
                id_ambito_territoriale=form.cleaned_data['id_ambito_territoriale'],
                id_tipologia_programma=form.cleaned_data['id_tipologia_programma'],
                id_area_tecnologica=form.cleaned_data['id_area_tecnologica'],
                url_immagine=form.cleaned_data['url_immagine'],
                abstract_ita=form.cleaned_data['abstract_ita'],
                abstract_eng=form.cleaned_data['abstract_eng'],
                url_sito_web=form.cleaned_data['url_sito_web'],
                call=form.cleaned_data['call'],
            )

            if director:
                ProgettoResponsabileScientifico.objects.create(id_progetto=project,
                                                               nome_origine=f'{director.cognome} {director.nome}',
                                                               matricola=director)
            else:
                ProgettoResponsabileScientifico.objects.create(id_progetto=project,
                                                               nome_origine=form.cleaned_data['nome_origine'])
                director = ProgettoResponsabileScientifico.objects.values(
                    'nome_origine')

            if structure:
                project.uo = structure
                project.save()

            log_action(user=request.user,
                       obj=project,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Project created successfully"))
            return redirect("ricerca_crud:crud_projects")

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

    return render(request,
                  'projects/project_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{director.cognome} {director.nome}' if director else '',
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
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   '#': project.titolo}
    form = ProgettoDatiBaseForm(instance=project)

    structure_data = get_object_or_404(ProgettoDatiBase,
                                       pk=code)

    if request.POST:
        form = ProgettoDatiBaseForm(instance=project, data=request.POST)

        if form.is_valid():
            project.user_mod = request.user
            project.anno_avvio = form.cleaned_data['anno_avvio']
            project.id_ambito_territoriale = form.cleaned_data['id_ambito_territoriale']
            project.id_tipologia_programma = form.cleaned_data['id_tipologia_programma']
            project.id_area_tecnologica = form.cleaned_data['id_area_tecnologica']
            project.titolo = form.cleaned_data['titolo']
            project.decr_breve = form.cleaned_data['decr_breve']
            project.url_immagine = form.cleaned_data['url_immagine']
            project.abstract_ita = form.cleaned_data['abstract_ita']
            project.abstract_eng = form.cleaned_data['abstract_eng']
            project.url_sito_web = form.cleaned_data['url_sito_web']
            project.call = form.cleaned_data['call']
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

            return redirect('ricerca_crud:crud_project_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(project).pk,
                                   object_id=project.pk)
    return render(request,
                  'projects/project.html',
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
def project_director_data(request, code, director_id, project=None, researchers=None, scientific_director=None, my_offices=None):

    director_data = get_object_or_404(ProgettoResponsabileScientifico,
                                      pk=director_id, id_progetto=code)

    form = ProgettoResponsabileScientificoForm(instance=director_data)

    if request.POST:
        form = ProgettoResponsabileScientificoForm(instance=director_data,
                                                   data=request.POST)
        if form.is_valid():
            director_data.user_mod = request.user
            director_data.nome_origine = form.cleaned_data['nome_origine']
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

            return redirect('ricerca_crud:crud_project_director_data',
                            code=code,
                            director_id=director_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   reverse('ricerca_crud:crud_project_director_data_edit', kwargs={'code': code, 'director_id': director_id}): _('Project director data')
                   }

    return render(request,
                  'projects/project_director_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'director_data': director_data})


@login_required
@can_manage_projects
@can_edit_project
def project_structure_data_edit(request, code, data_id,
                                my_offices=None, project=None, researchers=None, scientific_director=None):

    structure_project = get_object_or_404(ProgettoDatiBase,
                                          pk=data_id)

    structure = structure_project.uo

    structure_data = (structure.uo, f'{structure.denominazione}')
    form = ProgettoDatiBaseFormWithoutFields(instance=structure_project,
                                             initial={'choosen_structure': structure_data[0]})

    if request.POST:
        form = ProgettoDatiBaseFormWithoutFields(data=request.POST)
        if form.is_valid():

            structure_code = form.cleaned_data['choosen_structure']
            new_structure = get_object_or_404(
                UnitaOrganizzativa, uo=structure_code)
            structure_project.user_mod = request.user
            structure_project.uo = new_structure
            structure_project.save()

            log_msg = f'{_("Changed structure")} {structure.__str__()}' \
                      if structure == new_structure \
                      else f'{structure} {_("substituted with")} {new_structure.__str__()}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Structure edited successfully"))
            return redirect('ricerca_crud:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Companies'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': f'{structure.denominazione}'}

    return render(request,
                  'projects/project_structure_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'choosen_structure': structure_data[1] if structure_data else None,
                   'url': reverse('ricerca:structureslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_data_edit(request, code, director_id, researchers=None, scientific_director=None,
                               my_offices=None, project=None):

    director_project = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id, id_progetto=code)

    director = director_project.matricola
    director_data = ()

    if director:
        director_data = (encrypt(director.matricola),
                         f'{director.cognome} {director.nome}')
        form = ProgettoResponsabileScientificoWithoutFieldsForm(
            initial={'choosen_person': director_data[0]})
    else:
        form = ProgettoResponsabileScientificoWithoutFieldsForm()

    if request.POST:
        form = ProgettoResponsabileScientificoWithoutFieldsForm(
            data=request.POST)
        if form.is_valid():
            director_code = decrypt(form.cleaned_data['choosen_person'])
            new_director = get_object_or_404(
                Personale, matricola=director_code)
            director_project.matricola = new_director
            director_project.nome_origine = f'{new_director.cognome} {new_director.nome}'
            director_project.save()

            if director and director == new_director:
                log_msg = f'{_("Changed director")} {director.__str__()}'
            elif director and director != new_director:
                log_msg = f'{director} {_("substituted with")} {new_director.__str__()}'
            else:
                log_msg = f'{_("Changed director")} {new_director.__str__()}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director edited successfully"))
            return redirect('ricerca_crud:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('Scientific Director')}
    return render(request,
                  'projects/project_director_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'director_id': director_id,
                   'choosen_person': director_data[1] if director_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_delete(request, code, director_id,
                            my_offices=None, project=None, researchers=None, scientific_director=None):
    director_project = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id, id_progetto=code)

    if ProgettoResponsabileScientifico.objects.filter(id_progetto=code).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted director")} {director_project.nome_origine}')

    director_project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Director removed successfully"))
    return redirect('ricerca_crud:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_director_new(request, code, my_offices=None, project=None, researchers=None, scientific_director=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('New director')}
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
                director = get_object_or_404(
                    Personale, matricola=director_code)
                p.matricola = director
                p.nome_origine = f'{director.cognome} {director.nome}'
                p.save()

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'{_("Added director")} {p.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Director added successfully"))
            return redirect('ricerca_crud:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'projects/project_director.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_director_delete(request, code, director_id,
                            my_offices=None, project=None, researchers=None, scientific_director=None):
    project_director = get_object_or_404(ProgettoResponsabileScientifico,
                                         pk=director_id, id_progetto=code)

    if ProgettoResponsabileScientifico.objects.filter(id_progetto=code).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted director")} {project_director.nome_origine}')

    project_director.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Director removed successfully"))
    return redirect('ricerca_crud:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_data(request, code, researcher_id, researchers, scientific_director=None,
                            my_offices=None, project=None):
    researcher_data = get_object_or_404(ProgettoRicercatore,
                                        pk=researcher_id, id_progetto=code)

    form = ProgettoRicercatoreForm(instance=researcher_data)

    if request.POST:
        form = ProgettoRicercatoreForm(instance=researcher_data,
                                       data=request.POST)
        if form.is_valid():
            researcher_data.user_mod = request.user
            researcher_data.nome_origine = form.cleaned_data['nome_origine']
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

            return redirect('ricerca_crud:crud_project_researcher_data',
                            code=code,
                            researcher_id=researcher_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Companies'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   reverse('ricerca_crud:crud_project_director_data_edit',
                           kwargs={'code': code, 'director_id': researcher_id}): _('Project researcher data')
                   }

    return render(request,
                  'projects/project_researcher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'researcher_data': researcher_data})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_data_edit(request, code, researcher_id, researchers, scientific_director=None,
                                 my_offices=None, project=None):

    researcher_project = get_object_or_404(ProgettoRicercatore,
                                           pk=researcher_id, id_progetto=code)

    researcher = researcher_project.matricola
    researcher_data = ()

    if researcher:
        researcher_data = (encrypt(researcher.matricola),
                           f'{researcher.cognome} {researcher.nome}')
        form = ProgettoRicercatoreWithoutFieldsForm(
            initial={'choosen_person': researcher_data[0]})
    else:
        form = ProgettoRicercatoreWithoutFieldsForm()

    if request.POST:
        form = ProgettoRicercatoreWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            researcher_code = decrypt(form.cleaned_data['choosen_person'])
            new_researcher = get_object_or_404(
                Personale, matricola=researcher_code)
            researcher_project.matricola = new_researcher
            researcher_project.nome_origine = f'{new_researcher.cognome} {new_researcher.nome}'
            researcher_project.save()

            if researcher and researcher == new_researcher:
                log_msg = f'{_("Changed inventor")} {researcher.__str__()}'
            elif researcher and researcher != new_researcher:
                log_msg = f'{researcher} {_("substituted with")} {new_researcher.__str__()}'
            else:
                log_msg = f'{_("Changed researcher")} {new_researcher.__str__()}'

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher edited successfully"))
            return redirect('ricerca_crud:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('Researcher')}
    return render(request,
                  'projects/project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'researcher_id': researcher_id,
                   'choosen_person': researcher_data[1] if researcher_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_new(request, code, my_offices=None, project=None, researchers=None, scientific_director=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_projects'): _('Projects'),
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code}): project.titolo,
                   '#': _('New researcher')}
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
                researcher = get_object_or_404(
                    Personale, matricola=researcher_code)
                p.matricola = researcher
                p.nome_origine = f'{researcher.cognome} {researcher.nome}'
                p.save()

            log_action(user=request.user,
                       obj=project,
                       flag=CHANGE,
                       msg=f'{_("Added researcher")} {p.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Researcher added successfully"))
            return redirect('ricerca_crud:crud_project_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'projects/project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_projects
@can_edit_project
def project_researcher_delete(request, code, researcher_id,
                              my_offices=None, project=None, researchers=None, scientific_director=None):
    researcher_project = get_object_or_404(ProgettoRicercatore,
                                           pk=researcher_id, id_progetto=code)

    # if ProgettoRicercatore.objects.filter(id_progetto=code).count() == 1:
    #     raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=project,
               flag=CHANGE,
               msg=f'{_("Deleted researcher")} {researcher_project.nome_origine}')

    researcher_project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Researcher removed successfully"))
    return redirect('ricerca_crud:crud_project_edit', code=code)


@login_required
@can_manage_projects
@can_edit_project
def project_delete(request, code,
                   my_offices=None, project=None, researchers=None, scientific_director=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Project removed successfully"))

    return redirect('ricerca_crud:crud_projects')
