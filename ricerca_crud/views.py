import os

import requests

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField, Q, Value, F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructure

from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *
from . utils import log_action
import logging


logger = logging.getLogger(__name__)


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
                   '#': _('CdS')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist')}
    return render(request, 'cds.html', context)


@login_required
@can_manage_cds
@can_edit_cds
def cds_detail(request, regdid_id, my_offices=None, regdid=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   '#': regdid.cds.nome_cds_it}

    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id)
    office_data = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=regdid.cds.pk)

    logs_regdid = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(regdid).pk,
                                          object_id=regdid.pk)

    logs_cds = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(regdid.cds).pk,
                                       object_id=regdid.cds.pk)

    return render(request,
                  'cds_detail.html',
                  {'breadcrumbs': breadcrumbs,
                   'logs_regdid': logs_regdid,
                   'logs_cds': logs_cds,
                   'other_data': other_data,
                   'office_data': office_data,
                   'regdid': regdid,})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):

    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, regdid_id=regdid_id)
    form = DidatticaCdsAltriDatiForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsAltriDatiForm(instance=other_data,
                                         data=request.POST)
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
                       obj=regdid,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Other data edited successfully"))

            return redirect('ricerca_crud:crud_cds_other_data_edit',
                            regdid_id=regdid_id,
                            data_id=data_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {
        reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
        reverse('ricerca_crud:crud_cds'): _('CdS'),
        reverse('ricerca_crud:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
        reverse('ricerca_crud:crud_cds_other_data_edit', kwargs={'regdid_id': regdid_id,'data_id': data_id}): _("Other data")
    }

    return render(request,
                  'cds_other_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'other_data': other_data})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator(request, regdid_id, data_id,
                               my_offices=None, regdid=None):


    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                    pk=data_id, regdid_id=regdid_id)

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
                       obj=regdid,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_other_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_other_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id':data_id}): _('Other data'),
                   '#': _('Coordinator')}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id':data_id,
                   'choosen_person': teacher_data[1] if teacher_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator(request, regdid_id, data_id,
                               my_offices=None, regdid=None):


    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)

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
                       obj=regdid,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Deputy Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_other_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_other_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id':data_id}): _('Other data'),
                   '#': _('Deputy coordinator')}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id':data_id,
                   'choosen_person': teacher_data[1] if teacher_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)

    other_data.delete()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg=f'{_("Deleted other data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data removed successfully"))
    return redirect('ricerca_crud:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_new(request, regdid_id, my_offices=None, regdid=None):
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id)

    if other_data:
        raise Exception(_('Other data set already existent for this cds'))

    DidatticaCdsAltriDati.objects.create(regdid_id=regdid)

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg=f'{_("Created other data set")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data created successfully"))
    return redirect('ricerca_crud:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator_delete(request, regdid_id, data_id,
                                 my_offices=None, regdid=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, regdid_id=regdid_id)
    other_data.matricola_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg=f'{_("Deleted coordinator data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Coordinator data removed successfully"))
    return redirect('ricerca_crud:crud_cds_other_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator_delete(request, regdid_id, data_id,
                                 my_offices=None, regdid=None):
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id, regdid_id=regdid_id)

    other_data.matricola_vice_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg=f'{_("Deleted deputy coordinator data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Deputy coordinator data removed successfully"))
    return redirect('ricerca_crud:crud_cds_other_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=regdid.cds)

    office_data.delete()

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg=f'{_("Deleted office data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data removed successfully"))
    return redirect('ricerca_crud:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):

    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=regdid.cds)

    form = DidatticaCdsAltriDatiUfficioForm(instance=office_data)

    if request.POST:
        form = DidatticaCdsAltriDatiUfficioForm(instance=office_data,
                                                data=request.POST)
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
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Office data edited successfully"))

            return redirect('ricerca_crud:crud_cds_office_data_edit',
                            regdid_id=regdid_id,
                            data_id=data_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   '#': _('Office data')
                   }

    return render(request,
                  'cds_office_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'office_data': office_data})


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_new(request, regdid_id, my_offices=None, regdid=None):
    DidatticaCdsAltriDatiUfficio.objects.create(cds=regdid.cds, ordine=10)

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg=f'{_("Created office data set")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data created successfully"))

    return redirect('ricerca_crud:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible(request, regdid_id, data_id, my_offices=None, regdid=None):

    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=regdid.cds)

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
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('ricerca_crud:crud_cds_office_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_cds'): _('CdS'),
                   reverse('ricerca_crud:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('ricerca_crud:crud_cds_office_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id':data_id}): _('Office data'),
                   '#': _('Responsible')}

    return render(request,
                  'cds_office_data_responsible.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id':data_id,
                   'choosen_person': person_data[1] if person_data else None,
                   'url': reverse('ricerca:addressbooklist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=regdid.cds)
    office_data.matricola_riferimento = None
    office_data.save()

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg=f'{_("Deleted responsible data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Responsible data removed successfully"))
    return redirect('ricerca_crud:crud_cds_office_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)



@login_required
@can_manage_patents
def patents(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Patents')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:patents')}
    return render(request, 'patents.html', context)


@login_required
@can_manage_patents
def patent_new(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   '#': _('New')}
    form = BrevettoDatiBaseForm()
    inventor_form = BrevettoInventoriForm()

    # already choosen before form fails
    inventor = None
    if request.POST.get('choosen_person', ''):
        inventor = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = BrevettoDatiBaseForm(data=request.POST, files=request.FILES)
        inventor_form = BrevettoInventoriForm(data=request.POST)

        if form.is_valid() and inventor_form.is_valid():
            inventor_code = decrypt(inventor_form.cleaned_data['choosen_person'])
            inventor = get_object_or_404(Personale, matricola=inventor_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_PATENTS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=inventor.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(_("Add inventor belonging to your structure"))

            patent = BrevettoDatiBase.objects.create(
                                                     id_univoco = form.cleaned_data['id_univoco'],
                                                     titolo = form.cleaned_data['titolo'],
                                                     url_immagine = form.cleaned_data['url_immagine'],
                                                     breve_descrizione=form.cleaned_data['breve_descrizione'],
                                                     id_area_tecnologica=form.cleaned_data['id_area_tecnologica'],
                                                     url_knowledge_share=form.cleaned_data['url_knowledge_share'],
                                                     applicazioni=form.cleaned_data['applicazioni'],
                                                     vantaggi=form.cleaned_data['vantaggi'],
                                                     trl_aggiornato=form.cleaned_data['trl_aggiornato'],
                                                     proprieta=form.cleaned_data['proprieta'],
                                                     id_status_legale=form.cleaned_data['id_status_legale'],
                                                     data_priorita=form.cleaned_data['data_priorita'],
                                                     territorio=form.cleaned_data['territorio'],
                                                     id_diritto_commerciale=form.cleaned_data['id_diritto_commerciale'],
                                                     id_disponibilita=form.cleaned_data['id_disponibilita'],
                                                     area_ks=form.cleaned_data['area_ks'],
                                                     nome_file_logo=form.cleaned_data['nome_file_logo'],
                                                     )

            if inventor:
                BrevettoInventori.objects.create(id_brevetto = patent,
                                             cognomenome_origine = f'{inventor.cognome} {inventor.nome}',
                                             matricola_inventore = inventor)
            else:
                BrevettoInventori.objects.create(id_brevetto=patent,
                                                cognomenome_origine = form.cleaned_data['cognomenome_origine'])
                inventor = BrevettoInventori.objects.values('cognomenome_origine')

            log_action(user=request.user,
                       obj=patent,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent created successfully"))
            return redirect("ricerca_crud:crud_patents")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in inventor_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{inventor_form.fields[k].label}</b>: {v}")
    return render(request,
                  'patent_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{inventor.cognome} {inventor.nome}' if inventor else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'inventor_form': inventor_form})


@login_required
@can_manage_patents
@can_edit_patent
def patent(request, code,
                  my_offices=None, patent=None, inventors=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   '#': patent.titolo}
    form = BrevettoDatiBaseForm(instance=patent)


    if request.POST:
        form = BrevettoDatiBaseForm(instance=patent, data=request.POST, files=request.FILES)

        if form.is_valid():
            patent.user_mod = request.user
            patent.titolo = form.cleaned_data['titolo']
            patent.id_univoco = form.cleaned_data['id_univoco']
            patent.url_immagine = form.cleaned_data['url_immagine']
            patent.breve_descrizione = form.cleaned_data['breve_descrizione']
            patent.id_area_tecnologica = form.cleaned_data['id_area_tecnologica']
            patent.url_knowledge_share = form.cleaned_data['url_knowledge_share']
            patent.applicazioni = form.cleaned_data['applicazioni']
            patent.vantaggi = form.cleaned_data['vantaggi']
            patent.trl_aggiornato = form.cleaned_data['trl_aggiornato']
            patent.proprieta = form.cleaned_data['proprieta']
            patent.id_status_legale = form.cleaned_data['id_status_legale']
            patent.data_priorita = form.cleaned_data['data_priorita']
            patent.territorio = form.cleaned_data['territorio']
            patent.id_diritto_commerciale = form.cleaned_data['id_diritto_commerciale']
            patent.id_disponibilita = form.cleaned_data['id_disponibilita']
            patent.area_ks = form.cleaned_data['area_ks']
            patent.nome_file_logo = form.cleaned_data['nome_file_logo'] if form.cleaned_data.get('nome_file_logo') else None
            patent.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent edited successfully"))

            return redirect('ricerca_crud:crud_patent_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(patent).pk,
                                   object_id=patent.pk)
    return render(request,
                  'patent.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'patent': patent,
                   'inventors': inventors})


@login_required
@can_manage_patents
@can_edit_patent
def patent_inventor_data(request, code, inventor_id, patent=None, inventors=None, my_offices=None):

    inventor_data = get_object_or_404(BrevettoInventori,
                                    pk=inventor_id, id_brevetto=code)

    form = BrevettoInventoriForm(instance=inventor_data)

    if request.POST:
        form = BrevettoInventoriForm(instance=inventor_data,
                                                data=request.POST)
        if form.is_valid():
            inventor_data.user_mod = request.user
            inventor_data.cognomenome_origine = form.cleaned_data['cognomenome_origine']
            inventor_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor data edited successfully"))

            return redirect('ricerca_crud:crud_project_inventor_data',
                            code=code,
                            inventor_id=inventor_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code }): patent.titolo,
                   reverse('ricerca_crud:crud_patent_inventor_data_edit', kwargs={'code': code, 'inventor_id': inventor_id}): _('Patent inventor data')
                   }

    return render(request,
                  'patent_inventor_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_data': inventor_data})



@login_required
@can_manage_patents
@can_edit_patent
def patent_inventor_data_edit(request, code, inventor_id, inventors,
                               my_offices=None, patent=None):


    inventor_patent = get_object_or_404(BrevettoInventori,
                                    pk=inventor_id, id_brevetto=code)

    inventor = inventor_patent.matricola_inventore
    inventor_data = ()

    if inventor:
        inventor_data = (encrypt(inventor.matricola), f'{inventor.cognome} {inventor.nome}')
        form = BrevettoInventoriWithoutFieldsForm(initial={'choosen_person': inventor_data[0]})
    else:
        form = BrevettoInventoriWithoutFieldsForm()

    if request.POST:
        form = BrevettoInventoriWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            inventor_code = decrypt(form.cleaned_data['choosen_person'])
            new_inventor = get_object_or_404(Personale, matricola=inventor_code)
            inventor_patent.matricola_inventore = new_inventor
            inventor_patent.cognomenome_origine = f'{new_inventor.cognome} {new_inventor.nome}'
            inventor_patent.save()

            if inventor and inventor == new_inventor:
                log_msg = f'{_("Changed inventor")} {inventor.__str__()}'
            elif inventor and inventor!=new_inventor:
                log_msg = f'{inventor} {_("substituted with")} {new_inventor.__str__()}'
            else:
                log_msg = f'{_("Changed inventor")} {new_inventor.__str__()}'

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor edited successfully"))
            return redirect('ricerca_crud:crud_patent_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   '#': _('Inventor')}
    return render(request,
                  'patent_inventor_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_id': inventor_id,
                   'choosen_person': inventor_data[1] if inventor_data  else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
@can_edit_patent
def patent_inventor_new(request, code, my_offices=None, patent=None, inventors=None):
        breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                       reverse('ricerca_crud:crud_patents'): _('Patents'),
                       reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                       '#': _('New inventor')}
        form = BrevettoInventoriForm()
        if request.POST:
            form = BrevettoInventoriForm(data=request.POST)
            if form.is_valid():

                b = BrevettoInventori.objects.create(
                    id_brevetto=patent,
                    cognomenome_origine=form.cleaned_data['cognomenome_origine']
                )
                inventor_code = decrypt(form.cleaned_data['choosen_person'])
                if inventor_code:
                    inventor = get_object_or_404(Personale, matricola=inventor_code)
                    b.matricola_inventore = inventor
                    b.cognomenome_origine = f'{inventor.cognome} {inventor.nome}'
                    b.save()

                log_action(user=request.user,
                           obj=patent,
                           flag=CHANGE,
                           msg=f'{_("Added inventor")} {b.__str__()}')

                messages.add_message(request,
                                     messages.SUCCESS,
                                     _("Inventor added successfully"))
                return redirect('ricerca_crud:crud_patent_edit',
                                code=code)
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        return render(request,
                      'patent_inventor_data_edit.html',
                      {'breadcrumbs': breadcrumbs,
                       'form': form,
                       'patent': patent,
                       'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
@can_edit_patent
def patent_inventor_delete(request, code, inventor_id,
                                 my_offices=None, patent=None, inventors=None):
    inventor_patent = get_object_or_404(BrevettoInventori,
                                        pk=inventor_id, id_brevetto=code)

    if BrevettoInventori.objects.filter(id_brevetto=code).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=patent,
               flag=CHANGE,
               msg=f'{_("Deleted inventor")} {inventor_patent.cognomenome_origine}')

    inventor_patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Inventor removed successfully"))
    return redirect('ricerca_crud:crud_patent_edit', code=code)



@login_required
@can_manage_patents
@can_edit_patent
def patent_delete(request, code,
                         my_offices=None, patent=None, inventors=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))
    logo = patent.nome_file_logo.path

    patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Patent removed successfully"))
    try:
        os.remove(logo)
    except Exception:  # pragma: no cover
        logger.warning(f'File {logo} not found')

    return redirect('ricerca_crud:crud_patents')


@login_required
@can_manage_companies
def companies(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Companies')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:companies')}
    return render(request, 'companies.html', context)


@login_required
@can_manage_companies
def company_new(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   '#': _('New')}
    form = SpinoffStartupDatiBaseForm()
    department_form = SpinoffStartupDipartimentoForm()

    # already choosen before form fails
    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                    dip_id=request.POST['choosen_department'])

    if request.POST:
        form = SpinoffStartupDatiBaseForm(data=request.POST, files=request.FILES)
        department_form = SpinoffStartupDipartimentoForm(data=request.POST)

        if form.is_valid() and department_form.is_valid():
            department_code = department_form.cleaned_data['choosen_department']
            department = get_object_or_404(DidatticaDipartimento, dip_id=department_code)

            # # check if user can manage teacher structure
            # if not request.user.is_superuser:
            #     structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
            #                                                                             office__name=OFFICE_COMPANIES,
            #                                                                             office__is_active=True,
            #                                                                             office__organizational_structure__is_active=True,
            #                                                                             office__organizational_structure__unique_code=inventor.cd_uo_aff_org_id)
            #     if not structure_afforg:
            #         raise Exception(_("Add inventor belonging to your structure"))

            company = SpinoffStartupDatiBase.objects.create(
                                                     piva = form.cleaned_data['piva'],
                                                     nome_azienda = form.cleaned_data['nome_azienda'],
                                                     descrizione_ita = form.cleaned_data['descrizione_ita'],
                                                     descrizione_eng=form.cleaned_data['descrizione_eng'],
                                                     url_sito_web=form.cleaned_data['url_sito_web'],
                                                     ceo=form.cleaned_data['ceo'],
                                                     id_area_tecnologica=form.cleaned_data['id_area_tecnologica'],
                                                     id_area_innovazione_s3_calabria=form.cleaned_data['id_area_innovazione_s3_calabria'],
                                                     is_startup=form.cleaned_data['is_startup'],
                                                     is_spinoff=form.cleaned_data['is_spinoff'],
                                                     nome_file_logo=form.cleaned_data['nome_file_logo']
                                                     )

            if department:
                SpinoffStartupDipartimento.objects.create(id_spinoff_startup_dati_base = company,
                                             nome_origine_dipartimento = f'{department.dip_des_it}',
                                             id_didattica_dipartimento = department)

            log_action(user=request.user,
                       obj=company,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company created successfully"))
            return redirect("ricerca_crud:crud_companies")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")
    return render(request,
                  'company_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_department': f'{department.dip_des_it}' if department else '',
                   'form': form,
                   'departments_api': reverse('ricerca:departmentslist'),
                   'department_form': department_form})



@login_required
@can_manage_companies
@can_edit_company
def company(request, code,
                  my_offices=None, company=None, departments=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   '#': company.nome_azienda}
    form = SpinoffStartupDatiBaseForm(instance=company)

    referent_data = get_object_or_404(SpinoffStartupDatiBase,
                                   pk=code)

    if request.POST:
        form = SpinoffStartupDatiBaseForm(instance=company, data=request.POST, files=request.FILES)

        if form.is_valid():
            company.user_mod = request.user
            company.piva = form.cleaned_data['piva']
            company.nome_azienda = form.cleaned_data['nome_azienda']
            company.nome_file_logo = form.cleaned_data['nome_file_logo'] if form.cleaned_data.get('nome_file_logo') else None
            company.descrizione_ita = form.cleaned_data['descrizione_ita']
            company.descrizione_eng = form.cleaned_data['descrizione_eng']
            company.url_sito_web = form.cleaned_data['url_sito_web']
            company.ceo = form.cleaned_data['ceo']
            company.id_area_tecnologica = form.cleaned_data['id_area_tecnologica']
            company.id_area_innovazione_s3_calabria = form.cleaned_data['id_area_innovazione_s3_calabria']
            company.is_startup = form.cleaned_data['is_startup']
            company.is_spinoff = form.cleaned_data['is_spinoff']
            company.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company edited successfully"))

            return redirect('ricerca_crud:crud_company_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(company).pk,
                                   object_id=company.pk)
    return render(request,
                  'company.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'company': company,
                   'referent_data': referent_data,
                   'departments': departments})



@login_required
@can_manage_companies
@can_edit_company
def  company_unical_referent_data(request, code, data_id, company=None, departments=None, my_offices=None):

    referent_data = get_object_or_404(SpinoffStartupDatiBase,
                                    pk=data_id)

    form = SpinoffStartupDatiBaseReferentForm(instance=referent_data)

    if request.POST:
        form = SpinoffStartupDatiBaseReferentForm(instance=referent_data,
                                                data=request.POST)
        if form.is_valid():
            referent_data.user_mod = request.user
            referent_data.referente_unical = form.cleaned_data['referente_unical']
            referent_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Office data edited successfully"))

            return redirect('ricerca_crud:crud_company_unical_referent_data',
                            code=code,
                            data_id=data_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code }): company.nome_azienda,
                   reverse('ricerca_crud:crud_company_unical_referent_data', kwargs={'code': code, 'data_id': data_id}): _('Unical Referent data')
                   }

    return render(request,
                  'company_unical_referent_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'referent_data': referent_data})



@login_required
@can_manage_companies
@can_edit_company
def company_unical_referent_data_edit(request, code, data_id,
                  my_offices=None, company=None, departments=None):
    unical_referent  = get_object_or_404(SpinoffStartupDatiBase,
                                        pk=code)

    referent = unical_referent.matricola_referente_unical
    referent_data = ()

    if referent:
        referent_data = (encrypt(referent.matricola), f'{referent.cognome} {referent.nome}')
        form = SpinoffStartupDatiBaseReferentWithoutIDForm(initial={'choosen_person': referent_data[0]})
    else:
        form = SpinoffStartupDatiBaseReferentWithoutIDForm()

    if request.POST:
        form = SpinoffStartupDatiBaseReferentWithoutIDForm(data=request.POST)
        if form.is_valid():
            referent_code = decrypt(form.cleaned_data['choosen_person'])
            new_referent = get_object_or_404(Personale, matricola=referent_code)
            unical_referent.matricola_referente_unical = new_referent
            unical_referent.save()

            if referent and referent == new_referent:
                log_msg = f'{_("Changed referent")} {referent.__str__()}'
            elif referent and referent != new_referent:
                log_msg = f'{referent} {_("substituted with")} {new_referent.__str__()}'
            else:
                log_msg = f'{_("Changed referent")} {new_referent.__str__()}'

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Unical referent edited successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': f'{company.referente_unical}'
                   }
    return render(request,
                  'company_unical_referent_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'choosen_person': referent_data[1] if referent_data else None,
                   'url': reverse('ricerca:teacherslist')})



@login_required
@can_manage_companies
@can_edit_company
def company_unical_referent_data_delete(request, code, data_id=None,
                  my_offices=None, company=None, departments=None):
    company = get_object_or_404(SpinoffStartupDatiBase,
                                   pk=code)

    company.matricola_referente_unical = None
    company.save()

    log_action(user=request.user,
               obj=company,
               flag=CHANGE,
               msg=f'{_("Deleted unical referent data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Unical referent data removed successfully"))
    return redirect('ricerca_crud:crud_company_edit',
                    code=code)



@login_required
@can_manage_companies
@can_edit_company
def company_unical_department_data_new(request, code,
                              my_offices=None, company=None, departments=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': _('New department')}
    form = SpinoffStartupDipartimentoForm()
    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():
            department_code = form.cleaned_data['choosen_department']
            department = get_object_or_404(DidatticaDipartimento, dip_id=department_code)
            SpinoffStartupDipartimento.objects.create(
                                                id_spinoff_startup_dati_base = company,
                                                id_didattica_dipartimento = department,
                                                    nome_origine_dipartimento=department.dip_des_it)

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=f'{_("Added department")} {department.dip_des_it}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department added successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'company_unical_department_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'url': reverse('ricerca:departmentslist')})



@login_required
@can_manage_companies
@can_edit_company
def company_unical_department_data_edit(request, code, department_id,
                               my_offices=None, company=None, departments=None):

    department_company = get_object_or_404(SpinoffStartupDipartimento,
                                       pk=department_id)

    department = department_company.id_didattica_dipartimento

    department_data = (department.dip_id, f'{department.dip_des_it}')
    form = SpinoffStartupDipartimentoForm(instance=department_company,
                                            initial={'choosen_department': department_data[0]})

    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():

            department_code = form.cleaned_data['choosen_department']
            new_department = get_object_or_404(DidatticaDipartimento, dip_id=department_code)
            department_company.user_mod = request.user
            department_company.id_didattica_dipartimento = new_department
            department_company.nome_origine_dipartimento = f'{new_department.dip_des_it}'
            department_company.save()


            log_msg = f'{_("Changed department")} {department.__str__()}' \
                      if department == new_department \
                      else f'{department} {_("substituted with")} {new_department.__str__()}'

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department edited successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': f'{department.dip_des_it}'}


    return render(request,
                  'company_unical_department_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'department_id': department_id,
                   'choosen_department': department_data[1],
                   'url': reverse('ricerca:departmentslist')})



@login_required
@can_manage_companies
@can_edit_company
def company_unical_department_data_delete(request, code, department_id,
                                 my_offices=None, company=None, departments=None):
    department_company = get_object_or_404(SpinoffStartupDipartimento,
                                       id_spinoff_startup_dati_base=company,
                                       pk=department_id)

    if SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base=company).count() == 1:
        raise Exception(_("Permission denied. Only one department remains"))

    log_action(user=request.user,
               obj=company,
               flag=CHANGE,
               msg=f'{_("Deleted department")} {department_company.id_didattica_dipartimento}')

    department_company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Department removed successfully"))
    return redirect('ricerca_crud:crud_company_edit', code=code)




@login_required
@can_manage_companies
@can_edit_company
def company_delete(request, code,
                         my_offices=None, company=None, departments=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))
    logo = company.nome_file_logo.path

    company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Company removed successfully"))
    try:
        os.remove(logo)
    except Exception:  # pragma: no cover
        logger.warning(f'File {logo} not found')

    return redirect('ricerca_crud:crud_companies')


@login_required
@can_manage_projects
def projects(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Projects')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:projects')}
    return render(request, 'projects.html', context)


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
            director_code = decrypt(director_form.cleaned_data['choosen_person'])
            director = get_object_or_404(Personale, matricola=director_code)

            structure_code = structure_form.cleaned_data['choosen_structure']
            structure = get_object_or_404(UnitaOrganizzativa, uo=structure_code)


            # check if user can manage teacher structure
            if not request.user.is_superuser:

                query_filter = Q(office__organizational_structure__unique_code=director.cd_uo_aff_org_id)

                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(query_filter,
                                                                                        employee=request.user,
                                                                                        office__name=OFFICE_PROJECTS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True
                                                                                        )
                if not structure_afforg:
                    raise Exception(_("Add director belonging to your structure"))

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
                director = ProgettoResponsabileScientifico.objects.values('nome_origine')

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
                  'project_new.html',
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
                   reverse('ricerca_crud:crud_project_edit', kwargs={'code': code }): project.titolo,
                   reverse('ricerca_crud:crud_project_director_data_edit', kwargs={'code': code, 'director_id': director_id}): _('Project director data')
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
            new_structure = get_object_or_404(UnitaOrganizzativa, uo=structure_code)
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
                  'project_structure_data_edit.html',
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
        director_data = (encrypt(director.matricola), f'{director.cognome} {director.nome}')
        form = ProgettoResponsabileScientificoWithoutFieldsForm(initial={'choosen_person': director_data[0]})
    else:
        form = ProgettoResponsabileScientificoWithoutFieldsForm()

    if request.POST:
        form = ProgettoResponsabileScientificoWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            director_code = decrypt(form.cleaned_data['choosen_person'])
            new_director = get_object_or_404(Personale, matricola=director_code)
            director_project.matricola = new_director
            director_project.nome_origine = f'{new_director.cognome} {new_director.nome}'
            director_project.save()

            if director and director == new_director:
                log_msg = f'{_("Changed director")} {director.__str__()}'
            elif director and director!=new_director:
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
                  'project_director_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'director_id': director_id,
                   'choosen_person': director_data[1] if director_data  else None,
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
                    director = get_object_or_404(Personale, matricola=director_code)
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
                      'project_director.html',
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


    researcher_project = get_object_or_404(ProgettoRicercatore,
                                    pk=researcher_id, id_progetto=code)

    researcher = researcher_project.matricola
    researcher_data = ()

    if researcher:
        researcher_data = (encrypt(researcher.matricola), f'{researcher.cognome} {researcher.nome}')
        form = ProgettoRicercatoreWithoutFieldsForm(initial={'choosen_person': researcher_data[0]})
    else:
        form = ProgettoRicercatoreWithoutFieldsForm()

    if request.POST:
        form = ProgettoRicercatoreWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            researcher_code = decrypt(form.cleaned_data['choosen_person'])
            new_researcher = get_object_or_404(Personale, matricola=researcher_code)
            researcher_project.matricola = new_researcher
            researcher_project.nome_origine = f'{new_researcher.cognome} {new_researcher.nome}'
            researcher_project.save()

            if researcher and researcher == new_researcher:
                log_msg = f'{_("Changed inventor")} {researcher.__str__()}'
            elif researcher and researcher!=new_researcher:
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
                  'project_researcher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'project': project,
                   'researcher_id': researcher_id,
                   'choosen_person': researcher_data[1] if researcher_data  else None,
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
                    researcher = get_object_or_404(Personale, matricola=researcher_code)
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
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    project.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Project removed successfully"))

    return redirect('ricerca_crud:crud_projects')



@login_required
@can_manage_teachers
def teachers(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Teachers and PTA')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:teacherslist')}
    return render(request, 'teachers.html', context)



@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_detail(request, code,
                  my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_teachers'): _('Teachers'),
                   '#': teacher}

    other_data = DocentePtaAltriDati.objects.filter(matricola=teacher.matricola)
    board = DocentePtaBacheca.objects.filter(matricola=teacher.matricola)
    materials = DocenteMaterialeDidattico.objects.filter(matricola=teacher.matricola)

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(teacher).pk,
                                   object_id=teacher.pk)

    return render(request,
                  'teacher_detail.html',
                  {'breadcrumbs': breadcrumbs,
                   'logs': logs,
                   'other_data': other_data,
                   'board': board,
                   'materials': materials,
                   'teacher': teacher,
                   'code': code})



@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_edit(request, code, data_id,
                  my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    other_data = get_object_or_404(DocentePtaAltriDati,
                                   pk=data_id, matricola=decrypt(code))
    form = DocentePtaAltriDatiForm(instance=other_data)

    if request.POST:
        form = DocentePtaAltriDatiForm(instance=other_data, data=request.POST, files=request.FILES)
        if form.is_valid():
            current_foto = other_data.path_foto
            current_cv_ita = other_data.path_cv_ita
            current_cv_en = other_data.path_cv_en
            other_data.user_mod = request.user
            other_data.path_foto = form.cleaned_data['path_foto']
            other_data.path_cv_ita = form.cleaned_data['path_cv_ita']
            other_data.path_cv_en = form.cleaned_data['path_cv_en']
            other_data.breve_bio = form.cleaned_data['breve_bio']
            other_data.breve_bio_en = form.cleaned_data['breve_bio_en']
            other_data.orario_ricevimento = form.cleaned_data['orario_ricevimento']
            other_data.orario_ricevimento_en = form.cleaned_data['orario_ricevimento_en']
            other_data.orcid = form.cleaned_data['orcid']
            other_data.save()


            if other_data.path_foto and current_foto:
                try:
                    os.remove(current_foto.path)

                except Exception:  # pragma: no cover
                    logger.warning(f'File {current_foto} not found')

            if other_data.path_cv_ita and current_cv_ita:
                try:
                    os.remove(current_cv_ita.path)

                except Exception:  # pragma: no cover
                    logger.warning(f'File {current_cv_ita} not found')

            if other_data.path_cv_en and current_cv_en:
                try:
                    os.remove(current_cv_en.path)

                except Exception:  # pragma: no cover
                    logger.warning(f'File {current_cv_en} not found')

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=teacher,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Other data edited successfully"))

            return redirect('ricerca_crud:crud_teacher_edit',
                            code=code)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {
        reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
        reverse('ricerca_crud:crud_teachers'): _('Teachers'),
        reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
        reverse('ricerca_crud:crud_teacher_other_data_edit', kwargs={'code': code,'data_id': data_id}): _("Other data")
    }

    return render(request,
                  'teacher_other_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher,
                   'other_data': other_data})



@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_new(request, code, my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_teachers'): _('Teachers'),
                    reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
                    reverse('ricerca_crud:crud_teacher_other_data_new', kwargs={'code': code}): _(
                       "Other data"),
                   '#': _('New')}

    form = DocentePtaAltriDatiForm()


    if request.POST:
        form = DocentePtaAltriDatiForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            other_data = DocentePtaAltriDati.objects.create(
            path_foto = form.cleaned_data['path_foto'] if form.cleaned_data.get('path_foto') else None,
            matricola = teacher,
            path_cv_ita = form.cleaned_data['path_cv_ita'] if form.cleaned_data.get('path_cv_ita') else None,
            path_cv_en = form.cleaned_data['path_cv_en'] if form.cleaned_data.get('path_cv_en') else None,
            breve_bio = form.cleaned_data['breve_bio'],
            breve_bio_en = form.cleaned_data['breve_bio_en'],
            orario_ricevimento = form.cleaned_data['orario_ricevimento'],
            orario_ricevimento_en = form.cleaned_data['orario_ricevimento_en'],
            orcid = form.cleaned_data['orcid'],
            )

            log_action(user=request.user,
                       obj=teacher,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher other data set created successfully"))
            return redirect("ricerca_crud:crud_teacher_edit",code=code,)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
    return render(request,
                  'teacher_other_data_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher})


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_delete(request, code, data_id, my_offices=None, teacher=None, materials=None,
                                  other_data=None, board=None):
    other_data = get_object_or_404(DocentePtaAltriDati,
                                  pk=data_id, matricola=teacher.matricola)

    # if DocentePtaAltriDati.objects.filter(matricola=teacher.matricola).count() == 1:
    #     raise Exception(_("Permission denied. Only one data set remains"))

    log_action(user=request.user,
               obj=teacher,
               flag=CHANGE,
               msg=f'{_("Deleted other data")}')

    other_data.delete()


    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teachers other data removed successfully"))
    return redirect('ricerca_crud:crud_teacher_edit', code=code)



@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_edit(request, code, data_id,
                  my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    board = get_object_or_404(DocentePtaBacheca,
                                   pk=data_id, matricola=decrypt(code))

    form = DocentePtaBachecaForm(instance=board)

    if request.POST:
        form = DocentePtaBachecaForm(instance=board, data=request.POST)
        if form.is_valid():
            board.user_mod = request.user
            board.titolo = form.cleaned_data['titolo']
            board.titolo_en = form.cleaned_data['titolo_en']
            board.tipo_testo = form.cleaned_data['tipo_testo']
            board.tipo_testo_en = form.cleaned_data['tipo_testo_en']
            board.testo = form.cleaned_data['testo']
            board.testo_en = form.cleaned_data['testo_en']
            board.url_testo = form.cleaned_data['url_testo']
            board.url_testo_en = form.cleaned_data['url_testo_en']
            board.ordine = form.cleaned_data['ordine']
            board.attivo = form.cleaned_data['attivo']
            board.dt_pubblicazione = form.cleaned_data['dt_pubblicazione']
            board.dt_inizio_validita = form.cleaned_data['dt_inizio_validita']
            board.dt_fine_validita = form.cleaned_data['dt_fine_validita']
            board.save()


            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=teacher,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Board data edited successfully"))

            return redirect('ricerca_crud:crud_teacher_edit',
                            code=code)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {
        reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
        reverse('ricerca_crud:crud_teachers'): _('Teachers'),
        reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
        reverse('ricerca_crud:crud_teacher_board_data_edit', kwargs={'code': code,'data_id': data_id}): _("Board data")
    }

    return render(request,
                  'teacher_board_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher,
                   'board': board})


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_new(request, code, my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_teachers'): _('Teachers'),
                    reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
                    reverse('ricerca_crud:crud_teacher_board_data_new', kwargs={'code': code}): _(
                       "Board data"),
                   '#': _('New')}

    form = DocentePtaBachecaForm()


    if request.POST:
        form = DocentePtaBachecaForm(data=request.POST)

        if form.is_valid():
            board = DocentePtaBacheca.objects.create(
                    titolo = form.cleaned_data['titolo'],
                    titolo_en = form.cleaned_data['titolo_en'],
                    matricola = teacher,
                    tipo_testo = form.cleaned_data['tipo_testo'],
                    tipo_testo_en = form.cleaned_data['tipo_testo_en'],
                    testo = form.cleaned_data['testo'],
                    testo_en = form.cleaned_data['testo_en'],
                    url_testo = form.cleaned_data['url_testo'],
                    url_testo_en = form.cleaned_data['url_testo_en'],
                    ordine = form.cleaned_data['ordine'],
                    attivo = form.cleaned_data['attivo'],
                    dt_pubblicazione = form.cleaned_data['dt_pubblicazione'],
                    dt_inizio_validita = form.cleaned_data['dt_inizio_validita'],
                    dt_fine_validita = form.cleaned_data['dt_fine_validita'],
                )


            log_action(user=request.user,
                       obj=teacher,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher board data set created successfully"))
            return redirect("ricerca_crud:crud_teacher_edit", code=code,)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
    return render(request,
                  'teacher_board_data_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher
                   })


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_delete(request, code, data_id, my_offices=None, teacher=None, materials=None,
                                  other_data=None, board=None):
    board = get_object_or_404(DocentePtaBacheca,
                                  pk=data_id, matricola=teacher.matricola)

    board.delete()

    log_action(user=request.user,
               obj=teacher,
               flag=CHANGE,
               msg=f'{_("Deleted board data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teachers board data removed successfully"))
    return redirect('ricerca_crud:crud_teacher_edit', code=code)


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_edit(request, code, data_id,
                  my_offices=None, teacher=None, materials=None, other_data=None, board=None):
    materials = get_object_or_404(DocenteMaterialeDidattico,
                                   pk=data_id, matricola=decrypt(code))

    form = DocenteMaterialeDidatticoForm(instance=materials)

    if request.POST:
        form = DocenteMaterialeDidatticoForm(instance=materials, data=request.POST)
        if form.is_valid():
            materials.user_mod = request.user
            materials.titolo = form.cleaned_data['titolo']
            materials.titolo_en = form.cleaned_data['titolo_en']
            materials.testo = form.cleaned_data['testo']
            materials.testo_en = form.cleaned_data['testo_en']
            materials.url_testo = form.cleaned_data['url_testo']
            materials.url_testo_en = form.cleaned_data['url_testo_en']
            materials.ordine = form.cleaned_data['ordine']
            materials.attivo = form.cleaned_data['attivo']
            materials.url_testo_en = form.cleaned_data['url_testo_en']
            materials.dt_pubblicazione = form.cleaned_data['dt_pubblicazione']
            materials.dt_inizio_validita = form.cleaned_data['dt_inizio_validita']
            materials.dt_fine_validita = form.cleaned_data['dt_fine_validita']
            materials.save()


            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=teacher,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teaching material data edited successfully"))

            return redirect('ricerca_crud:crud_teacher_edit',
                            code=code)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {
        reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
        reverse('ricerca_crud:crud_teachers'): _('Teachers'),
        reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
        reverse('ricerca_crud:crud_teacher_materials_data_edit', kwargs={'code': code,'data_id': data_id}): _("Teaching material data")
    }

    return render(request,
                  'teacher_materials_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher,
                   'materials': materials})


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_new(request, code, my_offices=None, teacher=None, materials=None, other_data=None, board=None ):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_teachers'): _('Teachers'),
                   reverse('ricerca_crud:crud_teacher_edit', kwargs={'code': code}): teacher,
                   reverse('ricerca_crud:crud_teacher_board_data_new', kwargs={'code': code}): _(
                       "Teaching material data"),
                   '#': _('New')}

    form = DocenteMaterialeDidatticoForm()

    if request.POST:
        form = DocenteMaterialeDidatticoForm(data=request.POST)

        if form.is_valid():
            teaching_materials = DocenteMaterialeDidattico.objects.create(
                titolo=form.cleaned_data['titolo'],
                titolo_en=form.cleaned_data['titolo_en'],
                matricola=teacher,
                testo=form.cleaned_data['testo'],
                testo_en=form.cleaned_data['testo_en'],
                url_testo=form.cleaned_data['url_testo'],
                url_testo_en=form.cleaned_data['url_testo_en'],
                ordine=form.cleaned_data['ordine'],
                attivo=form.cleaned_data['attivo'],
                dt_pubblicazione=form.cleaned_data['dt_pubblicazione'],
                dt_inizio_validita=form.cleaned_data['dt_inizio_validita'],
                dt_fine_validita=form.cleaned_data['dt_fine_validita'],
            )

            log_action(user=request.user,
                       obj=teacher,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher materials data set created successfully"))
            return redirect("ricerca_crud:crud_teacher_edit", code=code,)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
    return render(request,
                  'teacher_materials_data_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'teacher': teacher
                   })


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_delete(request, code, data_id, my_offices=None, teacher=None, materials=None, other_data=None, board=None ):

    materials = get_object_or_404(DocenteMaterialeDidattico,
                                    pk=data_id, matricola=teacher.matricola)

    materials.delete()

    log_action(user=request.user,
               obj=teacher,
               flag=CHANGE,
               msg=f'{_("Deleted teacher materials data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teachers materials data removed successfully"))
    return redirect('ricerca_crud:crud_teacher_edit', code=code)
