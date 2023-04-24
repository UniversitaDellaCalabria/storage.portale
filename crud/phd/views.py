import datetime
import logging

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry, ADDITION
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from ricerca_app import *
from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. utils.forms import ChoosenPersonForm
from .. utils.utils import log_action

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_phd
def phd_list(request, my_offices=None):
    """
    lista phd
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('PhD activities')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:phd-activities-list')}
    return render(request, 'phd_list.html', context)


@login_required
@can_manage_phd
def phd_new(request, my_offices=None):
    """
    nuova attività di dottorato
    """
    form = DidatticaDottoratoAttivitaFormativaForm()

    teacher_form = DidatticaDottoratoAttivitaFormativaDocenteForm()

    query_filter = Q()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))


    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaForm(data=request.POST)
        teacher_form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)

        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_person'])

            if teacher:
                teacher = get_object_or_404(Personale,
                                            matricola=teacher_code)


            # check if user can manage teacher structure
            if not request.user.is_superuser:

                query_filter = Q(office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)

                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(query_filter,
                                                                                        employee=request.user,
                                                                                        office__name=OFFICE_PHD,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True)
                if not structure_afforg:
                    raise Exception(
                        _("Add a teacher belonging to your structure"))

            phd.user_mod_id = request.user
            phd.dt_mod = datetime.datetime.now()
            phd = form.save()

            new_teacher = DidatticaDottoratoAttivitaFormativaDocente.objects.create(id_didattica_dottorato_attivita_formativa=phd,
                                                                                    cognome_nome_origine=teacher_form.cleaned_data['cognome_nome_origine'],
                                                                                    matricola=teacher)

            if teacher and not teacher_form.cleaned_data['cognome_nome_origine']:
                new_teacher.cognome_nome_origine=f'{teacher.nome} {teacher.cognome}'
                new_teacher.save()

            log_action(user=request.user,
                       obj=phd,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("PhD activity created successfully"))
            return redirect("crud_phd:crud_phd_list")

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                   '#': _('New')}

    return render(request,
                  'phd_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.nome} {teacher.cognome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})


@login_required
@can_manage_phd
@can_edit_phd
def phd(request, code, my_offices=None, phd=None,
        teachers=None, other_teachers=None):
    """
    dettaglio dottorato
    """
    form = DidatticaDottoratoAttivitaFormativaForm(instance=phd)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaForm(instance=phd,
                                                       data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            phd.user_mod_id = request.user
            phd.dt_mod = datetime.datetime.now()
            phd.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("PhD activity edited successfully"))

            return redirect('crud_phd:crud_phd_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(phd).pk,
                                   object_id=phd.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                   '#': phd.nome_af}

    return render(request,
                  'phd.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'phd': phd,
                   'teachers': teachers,
                   'other_teachers': other_teachers})

@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_data(request, code, teacher_id, phd=None,
                          teachers=None, other_teachers=None, my_offices=None):
    """
    docente principale dottorato
    """
    teacher_data = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                     pk=teacher_id,
                                     id_didattica_dottorato_attivita_formativa=phd)

    form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=teacher_data)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=teacher_data,
                                                              data=request.POST)
        if form.is_valid():
            teacher_data.user_mod = request.user
            teacher_data.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            if not form.cleaned_data['cognome_nome_origine'] and teacher_data.matricola:
                teacher_data.cognome_nome_origine = f'{teacher_data.matricola.nome} {teacher_data.matricola.cognome}'

            teacher_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('crud_phd:crud_phd_main_teacher_data',
                            code=code,
                            teacher_id=teacher_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                   reverse('crud_phd:crud_phd_edit', kwargs={'code': code }): phd.nome_af,
                   '#': _('PhD activity teacher data')
                   }

    return render(request,
                  'phd_main_teacher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'phd': phd,
                   'teacher_data': teacher_data})


@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_data_edit(request, code, teacher_id, teachers=None,
                               other_teachers=None,
                               my_offices=None, phd=None):
    """
    modifica link docente principale
    """

    teacher_phd = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                    pk=teacher_id,
                                    id_didattica_dottorato_attivita_formativa=phd)

    teacher = teacher_phd.matricola
    # mettere nel model il binding tra la tabella DidatticaDottoratoAttivitaFormativaDocente e Personale
    teacher_data = ''
    initial = {}

    if teacher:
        teacher_data = f'{teacher.nome} {teacher.cognome}'
        initial={'choosen_person':  encrypt(teacher.matricola)}

    form = ChoosenPersonForm(initial=initial)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale,
                                            matricola=teacher_code)
            teacher_phd.matricola = new_teacher
            if not teacher_phd.cognome_nome_origine:
                teacher_phd.cognome_nome_origine = f'{new_teacher.cognome} {new_teacher.nome}'
            teacher_phd.user_mod_id = request.user
            teacher_phd.dt_mod = datetime.datetime.now()
            teacher_phd.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed teacher")} {teacher}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher}'
            else:
                log_msg = f'{_("Changed teacher")} {new_teacher}'

            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('crud_phd:crud_phd_edit', code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activity'),
                   reverse('crud_phd:crud_phd_edit', kwargs={'code': code}): phd.nome_af,
                   '#': _('Teacher')}

    return render(request,
                  'phd_main_teacher_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'phd': phd,
                   'teacher_id': teacher_id,
                   'choosen_person': teacher_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_new(request, code, my_offices=None,
                         phd=None, teachers=None,
                         other_teachers=None):
        """
        nuovo docente principale
        """
        form = DidatticaDottoratoAttivitaFormativaDocenteForm()
        if request.POST:
            form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)
            if form.is_valid():

                d = DidatticaDottoratoAttivitaFormativaDocente.objects.create(
                    id_didattica_dottorato_attivita_formativa=phd,
                    cognome_nome_origine=form.cleaned_data['cognome_nome_origine']
                )

                d.user_mod_id = request.user
                d.dt_mod = datetime.datetime.now()

                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                if teacher_code:
                    teacher = get_object_or_404(Personale, matricola=teacher_code)
                    d.matricola = teacher

                    if not form.cleaned_data['cognome_nome_origine']:
                        d.cognome_nome_origine =  f'{teacher.nome} {teacher.cognome}'
                    d.save()

                log_action(user=request.user,
                           obj=phd,
                           flag=CHANGE,
                           msg=f'{_("Added teacher")} {d}')

                messages.add_message(request,
                                     messages.SUCCESS,
                                     _("Teacher added successfully"))
                return redirect('crud_phd:crud_phd_edit',
                                code=code)
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                       reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                       reverse('crud_phd:crud_phd_edit', kwargs={'code': code}): phd.nome_af,
                       '#': _('New teacher')}

        return render(request,
                      'phd_main_teacher.html',
                      {'breadcrumbs': breadcrumbs,
                       'form': form,
                       'phd': phd,
                       'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_delete(request, code, teacher_id,
                            my_offices=None, phd=None,
                            teachers=None, other_teachers=None):
    """
    rimuovi un docente principale
    """
    phd_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                    pk=teacher_id,
                                    id_didattica_dottorato_attivita_formativa=phd)

    main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(id_didattica_dottorato_attivita_formativa=code)
    other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(id_didattica_dottorato_attivita_formativa=code)

    if main_teachers.count() == 1 and not other_teachers:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=phd,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {phd_teacher.cognome_nome_origine}')

    phd_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('crud_phd:crud_phd_edit', code=code)


@login_required
@can_manage_phd
@can_edit_phd
def phd_other_teacher_data(request, code, teacher_id, teachers=None,
                           other_teachers=None, my_offices=None,
                           phd=None):
    """
    modifica dati altro docente
    """
    other_teacher_data = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                           pk=teacher_id,
                                           id_didattica_dottorato_attivita_formativa=phd)

    form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=other_teacher_data)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=other_teacher_data,
                                                                   data=request.POST)
        if form.is_valid():
            other_teacher_data.user_mod = request.user
            other_teacher_data.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            if not form.cleaned_data['cognome_nome_origine'] and other_teacher_data.matricola:
                other_teacher_data.cognome_nome_origine = f'{other_teacher_data.matricola.nome} {other_teacher_data.matricola.cognome}'

            other_teacher_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('crud_phd:crud_phd_other_teacher_data',
                            code=code,
                            teacher_id=teacher_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                   reverse('crud_phd:crud_phd_edit', kwargs={'code': code}): phd.nome_af,
                   '#': _('PhD activity teacher data')
                   }

    return render(request,
                  'phd_other_teacher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'phd': phd,
                   'other_teacher_data': other_teacher_data})


@login_required
@can_manage_phd
@can_edit_phd
def phd_other_teacher_data_edit(request, code, teacher_id, teachers,
                                other_teachers=None, my_offices=None,
                                phd=None):
    """
    modifica link altro docente
    """

    other_teacher_phd = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                          pk=teacher_id,
                                          id_didattica_dottorato_attivita_formativa=phd)

    teacher = other_teacher_phd.matricola
    teacher_data = ''
    initial = {}

    if teacher:
        teacher_data = f'{teacher.nome} {teacher.cognome}'
        initial={'choosen_person':  encrypt(teacher.matricola)}

    form = ChoosenPersonForm(initial=initial)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale,
                                            matricola=teacher_code)
            other_teacher_phd.matricola = new_teacher
            if not other_teacher_phd.cognome_nome_origine:
                other_teacher_phd.cognome_nome_origine = f'{new_teacher.cognome} {new_teacher.nome}'
            other_teacher_phd.user_mod_id = request.user
            other_teacher_phd.dt_mod = datetime.datetime.now()
            other_teacher_phd.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed teacher")} {teacher}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher}'
            else:
                log_msg = f'{_("Changed teacher")} {new_teacher}'

            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('crud_phd:crud_phd_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                   reverse('crud_phd:crud_phd_edit', kwargs={'code': code}): phd.nome_af,
                   '#': _('Teacher')}

    return render(request,
                  'phd_other_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'phd': phd,
                   'teacher_id': teacher_id,
                   'choosen_person': other_teacher_data[1] if other_teacher_data  else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_other_teacher_new(request, code, my_offices=None,
                          phd=None, teachers=None,
                          other_teachers=None):
        """
        nuovo altro docente
        """
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm()
        if request.POST:
            form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(data=request.POST)
            if form.is_valid():

                p = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(
                    id_didattica_dottorato_attivita_formativa=phd,
                    cognome_nome_origine=form.cleaned_data['cognome_nome_origine']
                )

                p.user_mod_id = request.user
                p.dt_mod = datetime.datetime.now()

                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                if teacher_code:
                    teacher = get_object_or_404(Personale, matricola=teacher_code)
                    p.matricola = teacher
                    if not form.cleaned_data['cognome_nome_origine']:
                        p.cognome_nome_origine =  f'{teacher.nome} {teacher.cognome}'
                    p.save()

                log_action(user=request.user,
                           obj=phd,
                           flag=CHANGE,
                           msg=f'{_("Added teacher")} {p}')

                messages.add_message(request,
                                     messages.SUCCESS,
                                     _("Teacher added successfully"))
                return redirect('crud_phd:crud_phd_edit',
                                code=code)
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                       reverse('crud_phd:crud_phd_list'): _('PhD activities'),
                       reverse('crud_phd:crud_phd_edit', kwargs={'code': code}): phd.nome_af,
                       '#': _('New teacher')}

        return render(request,
                      'phd_other_teacher.html',
                      {'breadcrumbs': breadcrumbs,
                       'form': form,
                       'phd': phd,
                       'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_other_teacher_delete(request, code, teacher_id,
                             my_offices=None, phd=None,
                             teachers=None, other_teachers=None):
    phd_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                    pk=teacher_id,
                                    id_didattica_dottorato_attivita_formativa=phd)

    main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(id_didattica_dottorato_attivita_formativa=code)
    other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(id_didattica_dottorato_attivita_formativa=code)

    if other_teachers.count() == 1 and not main_teachers:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=phd,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {phd_teacher.cognome_nome_origine}')

    phd_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('crud_phd:crud_phd_edit', code=code)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_phd
# @can_edit_phd
def phd_delete(request, code, my_offices=None, phd=None,
               teachers=None, other_teachers=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
        # raise Exception(_('Permission denied'))

    phd.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("PhD activity removed successfully"))

    return redirect('crud_phd:crud_phd_list')
