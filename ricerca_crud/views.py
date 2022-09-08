import requests

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructure

from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *
from . utils import log_action


@login_required
def home(request):
    return render(request, 'dashboard.html')


@login_required
@can_manage_researchgroups
def researchgroups(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Research groups')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:researchgroups')}
    return render(request, 'researchgroups.html', context)


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup(request, code,
                  my_offices=None, rgroup=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_researchgroups'): _('Research groups'),
                   '#': rgroup.nome}
    form = RicercaGruppoForm(instance=rgroup)
    if request.POST:
        form = RicercaGruppoForm(instance=rgroup, data=request.POST)
        if form.is_valid():
            rgroup.user_mod = request.user
            rgroup.nome = form.cleaned_data['nome']
            rgroup.descrizione = form.cleaned_data['descrizione']
            rgroup.ricerca_erc1 = form.cleaned_data['ricerca_erc1']
            rgroup.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=rgroup,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research group edited successfully"))

            return redirect('ricerca_crud:crud_researchgroup_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(rgroup).pk,
                                   object_id=rgroup.pk)

    return render(request,
                  'researchgroup.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'rgroup': rgroup,
                   'teachers': teachers})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_delete(request, code,
                         my_offices=None, rgroup=None, teachers=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    rgroup.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Research group removed successfully"))
    return redirect('ricerca_crud:crud_researchgroups')


@login_required
@can_manage_researchgroups
def researchgroup_new(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_researchgroups'): _('Research groups'),
                   '#': _('New')}
    form = RicercaGruppoForm()
    teacher_form = RicercaGruppoDocenteForm()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = RicercaGruppoForm(data=request.POST)
        teacher_form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_RESEARCHGROUPS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            rgroup = RicercaGruppo.objects.create(user_ins=request.user,
                                                  nome = form.cleaned_data['nome'],
                                                  descrizione = form.cleaned_data['descrizione'],
                                                  ricerca_erc1 = form.cleaned_data['ricerca_erc1'])
            RicercaDocenteGruppo.objects.create(user_ins=request.user,
                                                ricerca_gruppo = rgroup,
                                                dt_inizio = teacher_form.cleaned_data['dt_inizio'],
                                                dt_fine = teacher_form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rgroup,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research group created successfully"))
            return redirect("ricerca_crud:crud_researchgroups")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")

    return render(request,
                  'researchgroup_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_teacher_new(request, code,
                              my_offices=None, rgroup=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_researchgroups'): _('Research groups'),
                   reverse('ricerca_crud:crud_researchgroup_edit', kwargs={'code': code}): rgroup.nome,
                   '#': _('New teacher')}
    form = RicercaGruppoDocenteForm()
    if request.POST:
        form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)
            RicercaDocenteGruppo.objects.create(user_ins=request.user,
                                                ricerca_gruppo = rgroup,
                                                dt_inizio = form.cleaned_data['dt_inizio'],
                                                dt_fine = form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rgroup,
                       flag=CHANGE,
                       msg=f'{_("Added teacher")} {teacher.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher added successfully"))
            return redirect('ricerca_crud:crud_researchgroup_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'researchgroup_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rgroup,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_teacher_edit(request, code, teacher_rgroup_id,
                               my_offices=None, rgroup=None, teachers=None):
    teacher_rgroup = get_object_or_404(RicercaDocenteGruppo,
                                       pk=teacher_rgroup_id)
    teacher = teacher_rgroup.personale
    teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
    form = RicercaGruppoDocenteForm(instance=teacher_rgroup,
                                    initial={'choosen_person': teacher_data[0]})

    if request.POST:
        form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_rgroup.user_mod = request.user
            teacher_rgroup.dt_inizio = form.cleaned_data['dt_inizio']
            teacher_rgroup.dt_fine = form.cleaned_data['dt_fine']
            teacher_rgroup.personale = new_teacher
            teacher_rgroup.save()

            log_msg = f'{_("Changed teacher")} {teacher.__str__()}' \
                      if teacher == new_teacher \
                      else f'{teacher} {_("substituted with")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=rgroup,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('ricerca_crud:crud_researchgroup_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_researchgroups'): _('Research groups'),
                   reverse('ricerca_crud:crud_researchgroup_edit', kwargs={'code': code}): rgroup.nome,
                   '#': f'{teacher.cognome} {teacher.nome}'}

    return render(request,
                  'researchgroup_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rgroup,
                   'teacher_rgroup_id': teacher_rgroup_id,
                   'choosen_person': teacher_data[1],
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_teacher_delete(request, code, teacher_rgroup_id,
                                 my_offices=None, rgroup=None, teachers=None):
    teacher_rgroup = get_object_or_404(RicercaDocenteGruppo,
                                       ricerca_gruppo=rgroup,
                                       pk=teacher_rgroup_id)

    if RicercaDocenteGruppo.objects.filter(ricerca_gruppo=rgroup).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=rgroup,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {teacher_rgroup.personale.__str__()}')

    teacher_rgroup.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_researchgroup_edit', code=code)



@login_required
@can_manage_researchlines
def base_researchlines(request,
                   my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Base Research lines')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:allresearchlines')+'?exclude_applied=1'}
    return render(request, 'base_researchlines.html', context)


@login_required
@can_manage_researchlines
def applied_researchlines(request,
                   my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Applied Research lines')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:allresearchlines')+'?exclude_base=1'}
    return render(request, 'applied_researchlines.html', context)


@login_required
@can_manage_researchlines
def researchline_new_applied(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_applied_researchlines'): _('Applied Research lines'),
                   '#': _('New')}
    form = RicercaLineaApplicataForm()
    teacher_form = RicercaDocenteLineaApplicataForm()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = RicercaLineaApplicataForm(data=request.POST)
        teacher_form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_RESEARCHLINES,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            rline = RicercaLineaApplicata.objects.create(user_ins=request.user,
                                                         descrizione = form.cleaned_data['descrizione'],
                                                         descr_pubblicaz_prog_brevetto = form.cleaned_data['descr_pubblicaz_prog_brevetto'],
                                                         anno = form.cleaned_data['anno'],
                                                         ricerca_aster2=form.cleaned_data['ricerca_aster2']

                                                         )
            RicercaDocenteLineaApplicata.objects.create(user_ins=request.user,
                                                ricerca_linea_applicata = rline,
                                                dt_inizio = teacher_form.cleaned_data['dt_inizio'],
                                                dt_fine = teacher_form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rline,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research line created successfully"))
            return redirect("ricerca_crud:crud_applied_researchlines")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")

    return render(request,
                  'researchline_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})


@login_required
@can_manage_researchlines
def researchline_new_base(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_base_researchlines'): _('Base Research lines'),
                   '#': _('New')}
    form = RicercaLineaBaseForm()
    teacher_form = RicercaDocenteLineaBaseForm()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = RicercaLineaBaseForm(data=request.POST)
        teacher_form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_RESEARCHLINES,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            rline = RicercaLineaBase.objects.create(user_ins=request.user,
                                                         descrizione = form.cleaned_data['descrizione'],
                                                         descr_pubblicaz_prog_brevetto = form.cleaned_data['descr_pubblicaz_prog_brevetto'],
                                                         anno = form.cleaned_data['anno'],
                                                         ricerca_erc2=form.cleaned_data['ricerca_erc2']

                                                         )
            RicercaDocenteLineaBase.objects.create(user_ins=request.user,
                                                ricerca_linea_base = rline,
                                                dt_inizio = teacher_form.cleaned_data['dt_inizio'],
                                                dt_fine = teacher_form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rline,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research line created successfully"))
            return redirect("ricerca_crud:crud_base_researchlines")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")

    return render(request,
                  'researchline_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})



@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline(request, code, my_offices=None, rline=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_base_researchlines'): _('Base Research lines'),
                   '#': rline.descrizione}
    form = RicercaLineaBaseForm(instance=rline)
    if request.POST:
        form = RicercaLineaBaseForm(instance=rline, data=request.POST)
        if form.is_valid():
            rline.user_mod = request.user
            rline.descrizione = form.cleaned_data['descrizione']
            rline.descr_pubblicaz_prog_brevetto = form.cleaned_data['descr_pubblicaz_prog_brevetto']
            rline.ricerca_erc2 = form.cleaned_data['ricerca_erc2']
            rline.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research line edited successfully"))

            return redirect('ricerca_crud:crud_base_researchline_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(rline).pk,
                                   object_id=rline.pk)

    return render(request,
                  'base_researchline.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'rline': rline,
                   'teachers': teachers})

@login_required
@can_manage_researchlines
@can_edit_applied_researchline
def applied_researchline(request, code,
                  my_offices=None, rline=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_applied_researchlines'): _('Applied Research lines'),
                   '#': rline.descrizione}
    form = RicercaLineaApplicataForm(instance=rline)
    if request.POST:
        form = RicercaLineaApplicataForm(instance=rline, data=request.POST)
        if form.is_valid():
            rline.user_mod = request.user
            rline.descrizione = form.cleaned_data['descrizione']
            rline.descr_pubblicaz_prog_brevetto = form.cleaned_data['descr_pubblicaz_prog_brevetto']
            rline.ricerca_aster2 = form.cleaned_data['ricerca_aster2']
            rline.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research line edited successfully"))

            return redirect('ricerca_crud:crud_applied_researchline_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(rline).pk,
                                   object_id=rline.pk)

    return render(request,
                  'applied_researchline.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'rline': rline,
                   'teachers': teachers})




@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline_delete(request, code,
                         my_offices=None, rline=None, teachers=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    rline.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Research group removed successfully"))
    return redirect('ricerca_crud:crud_base_researchlines')


@login_required
@can_manage_researchlines
@can_edit_applied_researchline
def applied_researchline_delete(request, code,
                         my_offices=None, rline=None, teachers=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    rline.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Research group removed successfully"))
    return redirect('ricerca_crud:crud_applied_researchlines')


@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline_teacher_new(request, code,
                              my_offices=None, rline=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_base_researchlines'): _('Research lines'),
                   reverse('ricerca_crud:crud_base_researchline_edit', kwargs={'code': code}): rline.descrizione,
                   '#': _('New teacher')}
    form = RicercaDocenteLineaBaseForm()
    if request.POST:
        form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)
            RicercaDocenteLineaBase.objects.create(user_ins=request.user,
                                                ricerca_linea_base = rline,
                                                dt_inizio = form.cleaned_data['dt_inizio'],
                                                dt_fine = form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=f'{_("Added teacher")} {teacher.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher added successfully"))
            return redirect('ricerca_crud:crud_base_researchline_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'base_researchline_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rline,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_researchlines
@can_edit_applied_researchline
def applied_researchline_teacher_new(request, code,
                              my_offices=None, rline=None, teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_applied_researchlines'): _('Research lines'),
                   reverse('ricerca_crud:crud_applied_researchline_edit', kwargs={'code': code}): rline.descrizione,
                   '#': _('New teacher')}
    form = RicercaDocenteLineaApplicataForm()
    if request.POST:
        form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)
            RicercaDocenteLineaApplicata.objects.create(user_ins=request.user,
                                                ricerca_linea_applicata = rline,
                                                dt_inizio = form.cleaned_data['dt_inizio'],
                                                dt_fine = form.cleaned_data['dt_fine'],
                                                personale = teacher)

            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=f'{_("Added teacher")} {teacher.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher added successfully"))
            return redirect('ricerca_crud:crud_applied_researchline_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'base_researchline_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rline,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline_teacher_edit(request, code, teacher_rline_id,
                               my_offices=None, rline=None, teachers=None):
    teacher_rline = get_object_or_404(RicercaDocenteLineaBase,
                                       pk=teacher_rline_id)
    teacher = teacher_rline.personale
    teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
    form = RicercaDocenteLineaBaseForm(instance=teacher_rline,
                                    initial={'choosen_person': teacher_data[0]})

    if request.POST:
        form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_rline.user_mod = request.user
            teacher_rline.dt_inizio = form.cleaned_data['dt_inizio']
            teacher_rline.dt_fine = form.cleaned_data['dt_fine']
            teacher_rline.personale = new_teacher
            teacher_rline.save()

            log_msg = f'{_("Changed teacher")} {teacher.__str__()}' \
                      if teacher == new_teacher \
                      else f'{teacher} {_("substituted with")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('ricerca_crud:crud_base_researchline_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_base_researchlines'): _('Research groups'),
                   reverse('ricerca_crud:crud_base_researchline_edit', kwargs={'code': code}): rline.descrizione,
                   '#': f'{teacher.cognome} {teacher.nome}'}

    return render(request,
                  'base_researchline_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rline': rline,
                   'teacher_rline_id': teacher_rline_id,
                   'choosen_person': teacher_data[1],
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_researchlines
@can_edit_applied_researchline
def applied_researchline_teacher_edit(request, code, teacher_rline_id,
                               my_offices=None, rline=None, teachers=None):
    teacher_rline = get_object_or_404(RicercaDocenteLineaApplicata,
                                       pk=teacher_rline_id)
    teacher = teacher_rline.personale
    teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
    form = RicercaDocenteLineaApplicataForm(instance=teacher_rline,
                                    initial={'choosen_person': teacher_data[0]})

    if request.POST:
        form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_rline.user_mod = request.user
            teacher_rline.dt_inizio = form.cleaned_data['dt_inizio']
            teacher_rline.dt_fine = form.cleaned_data['dt_fine']
            teacher_rline.personale = new_teacher
            teacher_rline.save()

            log_msg = f'{_("Changed teacher")} {teacher.__str__()}' \
                      if teacher == new_teacher \
                      else f'{teacher} {_("substituted with")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=rline,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('ricerca_crud:crud_applied_researchline_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_applied_researchlines'): _('Research groups'),
                   reverse('ricerca_crud:crud_applied_researchline_edit', kwargs={'code': code}): rline.descrizione,
                   '#': f'{teacher.cognome} {teacher.nome}'}

    return render(request,
                  'base_researchline_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rline': rline,
                   'teacher_rline_id': teacher_rline_id,
                   'choosen_person': teacher_data[1],
                   'url': reverse('ricerca:teacherslist')})



@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline_teacher_delete(request, code, teacher_rline_id,
                                 my_offices=None, rline=None, teachers=None):
    teacher_rline = get_object_or_404(RicercaDocenteLineaBase,
                                       ricerca_linea_base=rline,
                                       pk=teacher_rline_id)

    if RicercaDocenteLineaBase.objects.filter(ricerca_linea_base=rline).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=rline,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {teacher_rline.personale.__str__()}')

    teacher_rline.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_base_researchline_edit', code=code)



@login_required
@can_manage_researchlines
@can_edit_applied_researchline
def applied_researchline_teacher_delete(request, code, teacher_rline_id,
                                 my_offices=None, rline=None, teachers=None):
    teacher_rline = get_object_or_404(RicercaDocenteLineaApplicata,
                                       ricerca_linea_applicata=rline,
                                       pk=teacher_rline_id)

    if RicercaDocenteLineaApplicata.objects.filter(ricerca_linea_applicata=rline).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=rline,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {teacher_rline.personale.__str__()}')

    teacher_rline.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_applied_researchline_edit', code=code)



@login_required
@can_manage_cds
def cds(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Cds')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist')}
    return render(request, 'cds.html', context)


@login_required
@can_manage_cds
@can_edit_cds
def cds_detail(request, code,
               my_offices=None, cds=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   '#': cds.nome_cds_it}

    regolamento = DidatticaRegolamento.objects.filter(cds=cds).first()
    other_data = DidatticaCdsAltriDati.objects.filter(cds_id=cds.pk)
    office_data = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=cds.pk)



    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds).pk,
                                   object_id=cds.pk)


    return render(request,
                  'cds_detail.html',
                  {'breadcrumbs': breadcrumbs,
                   'logs': logs,
                   'cds': cds,
                   'other_data': other_data,
                   'office_data': office_data,
                   'regolamento': regolamento})



@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_edit(request, code, data_id, cds=None,
                               my_offices=None ):
    breadcrumbs = {
        reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
        reverse('ricerca_crud:crud_cds'): _('Cds'),
        reverse('ricerca_crud:crud_cds_detail', kwargs={'code': code}): cds.nome_cds_it,
        reverse('ricerca_crud:crud_cds_other_data_edit', kwargs={'code': code,'data_id': data_id}): _("Other data")
    }


    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                       pk=data_id, cds=cds)
    form = DidatticaCdsAltriDatiForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsAltriDatiForm(data=request.POST)
        if form.is_valid():
            other_data.user_mod = request.user
            other_data.num_posti = form.cleaned_data['num_posti']
            other_data.modalita_iscrizione = form.cleaned_data['modalita_iscrizione']
            other_data.nome_origine_coordinatore = form.cleaned_data['nome_origine_coordinatore']
            other_data.nome_origine_vice_coordinatore = form.cleaned_data['nome_origine_vice_coordinatore']
            other_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=cds,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Other data edited successfully"))

            return redirect('ricerca_crud:crud_cds_detail',
                            code=code)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'cds_other_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'cds': cds,
                   'other_data': other_data})



@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator(request, code, data_id,
                               my_offices=None, cds=None):


    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                       pk=data_id, cds=cds)

    teacher = other_data.matricola_coordinatore
    teacher_data = ()

    if teacher:
        teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
        form = DidatticaCdsAltriDatiCoordinatorForm(initial={'choosen_person': teacher_data[0]})
    else:
        form = DidatticaCdsAltriDatiCoordinatorForm()

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_coordinatore= new_teacher
            other_data.nome_origine_coordinatore = f'{new_teacher.cognome} {new_teacher.nome}'
            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed coordinator")} {teacher.__str__()}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher.__str__()}'
            else:
                log_msg = f'{_("Changed coordinator")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=cds,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_other_data_edit',
                            code=code, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('Cds'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'code': code}): cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_other_data_edit',
                           kwargs={'code': code, 'data_id':data_id}): 'Modifica Dati',
                   '#': _('Edit Coordinator')}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'cds': cds,
                   'data_id':data_id,
                   'choosen_person': teacher_data[1] if teacher_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible_delete(request, code, data_id, my_offices=None, cds=None):
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=cds)
    office_data.matricola_riferimento = None
    office_data.save()

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Deleted responsible data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Responsible data removed successfully"))
    return redirect('ricerca_crud:crud_cds_office_data_edit',
                    code=code,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator(request, code, data_id,
                               my_offices=None, cds=None):


    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                       pk=data_id, cds=cds)

    teacher = other_data.matricola_vice_coordinatore
    teacher_data = ()

    if teacher:
        teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
        form = DidatticaCdsAltriDatiCoordinatorForm(initial={'choosen_person': teacher_data[0]})
    else:
        form = DidatticaCdsAltriDatiCoordinatorForm()

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_vice_coordinatore= new_teacher
            other_data.nome_origine_vice_coordinatore = f'{new_teacher.cognome} {new_teacher.nome}'
            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed deputy coordinator")} {teacher.__str__()}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher.__str__()}'
            else:
                log_msg = f'{_("Changed deputy coordinator")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=cds,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Deputy Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_other_data_edit',
                            code=code, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('Cds'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'code': code}): cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_other_data_edit',
                           kwargs={'code': code, 'data_id':data_id}): 'Modifica Dati',
                   '#': 'Edit Coordinator'}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'cds': cds,
                   'data_id':data_id,
                   'choosen_person': teacher_data[1] if teacher_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_delete(request, code, data_id, my_offices=None, cds=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, cds=cds)

    other_data.delete()

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Deleted other data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data removed successfully"))
    return redirect('ricerca_crud:crud_cds_detail', code=code)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_new(request, code, my_offices=None, cds=None):
    other_data = DidatticaCdsAltriDati.objects.filter(cds=cds)

    if other_data:
        raise Exception(_('Other data set already existent for this cds'))

    DidatticaCdsAltriDati.objects.create(cds=cds)

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Created other data set")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data created successfully"))
    return redirect('ricerca_crud:crud_cds_detail', code=code)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_delete(request, code, data_id, my_offices=None, cds=None):
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=cds)

    office_data.delete()

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Deleted office data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data removed successfully"))
    return redirect('ricerca_crud:crud_cds_detail', code=code)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator_delete(request, code, data_id,
                                 my_offices=None, cds=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, cds=cds)
    other_data.matricola_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Deleted coordinator data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Coordinator data removed successfully"))
    return redirect('ricerca_crud:crud_cds_other_data_edit',
                    code=code,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator_delete(request, code, data_id,
                                 my_offices=None, cds=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, cds=cds)

    other_data.matricola_vice_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Deleted deputy coordinator data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Deputy coordinator data removed successfully"))
    return redirect('ricerca_crud:crud_cds_other_data_edit',
                    code=code,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_edit(request, code, data_id, cds=None, my_offices=None):

    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=cds)

    form = DidatticaCdsAltriDatiUfficioForm(instance=office_data)

    if request.POST:
        form = DidatticaCdsAltriDatiUfficioForm(data=request.POST)
        if form.is_valid():
            office_data.user_mod = request.user
            office_data.ordine = form.cleaned_data['ordine']
            office_data.nome_ufficio = form.cleaned_data['nome_ufficio']
            office_data.nome_origine_riferimento = form.cleaned_data['nome_origine_riferimento']
            office_data.telefono = form.cleaned_data['telefono']
            office_data.email = form.cleaned_data['email']
            office_data.edificio = form.cleaned_data['edificio']
            office_data.piano = form.cleaned_data['piano']
            office_data.orari = form.cleaned_data['orari']
            office_data.sportello_online = form.cleaned_data['sportello_online']
            office_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=cds,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Office data edited successfully"))

            return redirect('ricerca_crud:crud_cds_detail',
                            code=code)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds).pk,
                                   object_id=cds.pk)

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('Cds'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _('Edit office data')
                   }

    return render(request,
                  'cds_office_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'cds': cds,
                   'office_data': office_data})


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_new(request, code, my_offices=None, cds=None):

    # la relazione a other data deve assolutamente cambiare
    other_data = get_object_or_404(DidatticaCdsAltriDati, cds=cds)

    DidatticaCdsAltriDatiUfficio.objects.create(cds=other_data,
                                                ordine=10)

    log_action(user=request.user,
               obj=cds,
               flag=CHANGE,
               msg=f'{_("Created office data set")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data created successfully"))

    return redirect('ricerca_crud:crud_cds_detail', code=code)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible(request, code, data_id, my_offices=None, cds=None):

    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=cds)

    person = office_data.matricola_riferimento
    person_data = ()

    if person:
        person_data = (encrypt(person.matricola), f'{person.cognome} {person.nome}')
        form = DidatticaCdsAltriDatiCoordinatorForm(initial={'choosen_person': person_data[0]})
    else:
        form = DidatticaCdsAltriDatiCoordinatorForm()

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            person_code = decrypt(form.cleaned_data['choosen_person'])
            new_person = get_object_or_404(Personale, matricola=person_code)
            office_data.matricola_riferimento= new_person
            office_data.nome_origine_riferimento = f'{new_person.cognome} {new_person.nome}'
            office_data.save()

            if person and person == new_person:
                log_msg = f'{_("Changed responsible")} {person.__str__()}'
            elif person and person!=new_person:
                log_msg = f'{person} {_("substituted with")} {new_person.__str__()}'
            else:
                log_msg = f'{_("Changed coordinator")} {new_person.__str__()}'

            log_action(user=request.user,
                       obj=cds,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_office_data_edit',
                            code=code, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('Cds'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'code': code}): cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_office_data_edit',
                           kwargs={'code': code, 'data_id':data_id}): 'Modifica Dati',
                   '#': _('Edit Responsible')}

    return render(request,
                  'cds_office_data_responsible.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'cds': cds,
                   'data_id':data_id,
                   'choosen_person': person_data[1] if person_data else None,
                   'url': reverse('ricerca:addressbooklist')})

