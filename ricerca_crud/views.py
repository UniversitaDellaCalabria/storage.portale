import requests

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructure

from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *


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
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research group edited successfully"))
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'researchgroup.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rgroup,
                   'teachers': teachers})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_delete(request, code,
                         my_offices=None, rgroup=None, teachers=None):
    # ha senso?
    if rgroup.user_ins != request.user:
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
            teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_rgroup.user_mod = request.user
            teacher_rgroup.dt_inizio = form.cleaned_data['dt_inizio']
            teacher_rgroup.dt_fine = form.cleaned_data['dt_fine']
            teacher_rgroup.personale = teacher
            teacher_rgroup.save()
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

    teacher_rgroup.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_researchgroup_edit', code=code)
