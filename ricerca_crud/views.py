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
def researchgroups(request,
                   my_offices=None):
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
    if request.POST.get('choosen_teacher', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_teacher'])))

    if request.POST:
        form = RicercaGruppoForm(data=request.POST)
        teacher_form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': f'{teacher.cognome} {teacher.nome}' if teacher else '',
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
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
                                    initial={'choosen_teacher': teacher_data[0]})

    if request.POST:
        form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': teacher_data[1],
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
@can_manage_researchlines
def researchline_new_applied(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_applied_researchlines'): _('Applied Research lines'),
                   '#': _('New')}
    form = RicercaLineaApplicataForm()
    teacher_form = RicercaDocenteLineaApplicataForm()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_teacher', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_teacher'])))

    if request.POST:
        form = RicercaLineaApplicataForm(data=request.POST)
        teacher_form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': f'{teacher.cognome} {teacher.nome}' if teacher else '',
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
    if request.POST.get('choosen_teacher', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_teacher'])))

    if request.POST:
        form = RicercaLineaBaseForm(data=request.POST)
        teacher_form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})



@login_required
@can_manage_researchlines
@can_edit_base_researchline
def base_researchline(request, code,
                  my_offices=None, rline=None, teachers=None):
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
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
                                    initial={'choosen_teacher': teacher_data[0]})

    if request.POST:
        form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': teacher_data[1],
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
                                    initial={'choosen_teacher': teacher_data[0]})

    if request.POST:
        form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_teacher'])
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
                   'choosen_teacher': teacher_data[1],
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


