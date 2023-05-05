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

from .. utils.utils import custom_message, log_action

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_researchgroups
def researchgroups(request, my_offices=None):
    """
    lista dei gruppi di ricerca
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Research groups')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:researchgroups')}
    return render(request, 'researchgroups.html', context)


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup(request, code,
                  my_offices=None, rgroup=None, teachers=None):
    """
    dettaglio gruppo di ricerca con form di modifica
    """
    form = RicercaGruppoForm(instance=rgroup)
    if request.POST:
        form = RicercaGruppoForm(instance=rgroup, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            rgroup.user_mod = request.user
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

            return redirect('crud_research_groups:crud_researchgroup_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(rgroup).pk,
                                   object_id=rgroup.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_research_groups:crud_researchgroups'): _('Research groups'),
                   '#': rgroup.nome}

    return render(request,
                  'researchgroup.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'rgroup': rgroup,
                   'teachers': teachers})


@login_required
@user_passes_test(lambda u: u.is_superuser)
# attualmente solo i superuser possono effetture l'operazione
# @can_manage_researchgroups
# @can_edit_researchgroup
def researchgroup_delete(request, code,
                         my_offices=None, rgroup=None, teachers=None):
    """
    elimina gruppo di ricerca
    """
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    rgroup = get_object_or_404(RicercaGruppo, pk=code)
    rgroup.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Research group removed successfully"))
    return redirect('crud_research_groups:crud_researchgroups')


@login_required
@can_manage_researchgroups
def researchgroup_new(request, my_offices=None):
    """
    nuovo gruppo di ricerca
    """
    # utilizziamo due form
    # uno per i dati del gruppo di ricerca e uno per il docente
    form = RicercaGruppoForm()
    teacher_form = RicercaGruppoDocenteForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque il docente scelto senza doverlo cercare
    # nuovamente dall'elenco
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = RicercaGruppoForm(data=request.POST)
        teacher_form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            # se l'utente non è un superuser
            # verifica che il docente inserito
            # afferisca alla sua stessa struttura
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_RESEARCHGROUPS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(
                        _("Add a teacher belonging to your structure"))

            # crea il nuovo gruppo di ricerca
            rgroup = form.save(commit=False)
            rgroup.user_ins = request.user
            rgroup.save()

            # crea il nuovo docente da associare al gruppo
            RicercaDocenteGruppo.objects.create(user_ins=request.user,
                                                ricerca_gruppo=rgroup,
                                                dt_inizio=teacher_form.cleaned_data['dt_inizio'],
                                                dt_fine=teacher_form.cleaned_data['dt_fine'],
                                                personale=teacher)

            log_action(user=request.user,
                       obj=rgroup,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Research group created successfully"))
            return redirect("crud_research_groups:crud_researchgroup_edit",
                            code=rgroup.pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_research_groups:crud_researchgroups'): _('Research groups'),
                   '#': _('New')}

    return render(request,
                  'researchgroup_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.nome} {teacher.cognome}' if teacher else '',
                   'form': form,
                   'url': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_teacher_new(request, code,
                              my_offices=None, rgroup=None, teachers=None):
    """
    nuovo docente per il gruppo di ricerca
    """
    form = RicercaGruppoDocenteForm()
    if request.POST:
        form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            teacher = get_object_or_404(Personale, matricola=teacher_code)
            RicercaDocenteGruppo.objects.create(user_ins=request.user,
                                                ricerca_gruppo=rgroup,
                                                dt_inizio=form.cleaned_data['dt_inizio'],
                                                dt_fine=form.cleaned_data['dt_fine'],
                                                personale=teacher)

            log_action(user=request.user,
                       obj=rgroup,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo docente {teacher}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher added successfully"))
            return redirect('crud_research_groups:crud_researchgroup_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_research_groups:crud_researchgroups'): _('Research groups'),
                   reverse('crud_research_groups:crud_researchgroup_edit', kwargs={'code': code}): rgroup.nome,
                   '#': _('New teacher')}

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
    """
    modifica un docente del gruppo di ricerca
    """
    teacher_rgroup = get_object_or_404(RicercaDocenteGruppo.objects.select_related('personale'),
                                       pk=teacher_rgroup_id)
    teacher = teacher_rgroup.personale
    teacher_code = encrypt(teacher.matricola)
    teacher_data = f'{teacher.nome} {teacher.cognome}'

    form = RicercaGruppoDocenteForm(instance=teacher_rgroup,
                                    initial={'choosen_person': teacher_code})

    if request.POST:
        form = RicercaGruppoDocenteForm(instance=teacher_rgroup,
                                        data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_rgroup.user_mod = request.user
            teacher_rgroup.personale = new_teacher
            teacher_rgroup.save()

            if teacher != new_teacher:
                log_msg = f'Sotituito docente {teacher} con {new_teacher}'
                log_action(user=request.user,
                           obj=rgroup,
                           flag=CHANGE,
                           msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('crud_research_groups:crud_researchgroup_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_research_groups:crud_researchgroups'): _('Research groups'),
                   reverse('crud_research_groups:crud_researchgroup_edit', kwargs={'code': code}): rgroup.nome,
                   '#': teacher_data}

    return render(request,
                  'researchgroup_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'rgroup': rgroup,
                   'teacher_rgroup_id': teacher_rgroup_id,
                   'choosen_person': teacher_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_researchgroups
@can_edit_researchgroup
def researchgroup_teacher_delete(request, code, teacher_rgroup_id,
                                 my_offices=None, rgroup=None, teachers=None):
    """
    elimina un docente dal gruppo di ricerca
    """
    teacher_rgroup = get_object_or_404(RicercaDocenteGruppo.objects.select_related('personale'),
                                       ricerca_gruppo=rgroup,
                                       pk=teacher_rgroup_id)

    # un gruppo di ricerca deve avere almeno un docente
    if RicercaDocenteGruppo.objects.filter(ricerca_gruppo=rgroup).count() == 1:
        return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=rgroup,
               flag=CHANGE,
               msg=f'Rimosso docencte {teacher_rgroup.personale}')

    teacher_rgroup.delete()

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('crud_research_groups:crud_researchgroup_edit', code=code)
