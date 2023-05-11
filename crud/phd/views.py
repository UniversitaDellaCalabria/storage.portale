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

from ricerca_app import *
from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. utils.forms import ChoosenPersonForm
from .. utils.utils import custom_message, log_action

from . decorators import *
from . forms import *
from . utils import is_allowed


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

    external_form = DidatticaDottoratoAttivitaFormativaDocenteForm()
    internal_form = ChoosenPersonForm(required=True)

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:

        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)

        if 'choosen_person' in request.POST:
            teacher_form = internal_form
        else:
            teacher_form = external_form

        form = DidatticaDottoratoAttivitaFormativaForm(data=request.POST)

        if form.is_valid() and teacher_form.is_valid():
            if teacher_form.cleaned_data.get('choosen_person'):
                cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
            else:
                cognome_nome_origine = teacher_form.cleaned_data['cognome_nome_origine']

            # controllo che l'utente abbia il permesso
            # di agire nel dottorato di riferimento
            allow_user = is_allowed(request.user, my_offices, form.cleaned_data['rif_dottorato'])
            if not allow_user:
                return custom_message(request, _("You are not authorized to post activities for this PhD"))

            phd = form.save(commit=False)
            phd.user_mod_id = request.user
            phd.dt_mod = datetime.datetime.now()
            phd.save()

            new_teacher = DidatticaDottoratoAttivitaFormativaDocente.objects.create(id_didattica_dottorato_attivita_formativa=phd,
                                                                                    cognome_nome_origine=cognome_nome_origine,
                                                                                    matricola=teacher)

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
                   'choosen_person': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd(request, code, my_offices=None, phd=None):
    """
    dettaglio dottorato
    """
    teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
            id_didattica_dottorato_attivita_formativa=phd.id)
    other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
            id_didattica_dottorato_attivita_formativa=phd.id)

    form = DidatticaDottoratoAttivitaFormativaForm(instance=phd)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaForm(instance=phd,
                                                       data=request.POST)

        if form.is_valid():

            # controllo che l'utente abbia il permesso
            # di agire nel dottorato di riferimento
            allow_user = is_allowed(request.user, my_offices, form.cleaned_data['rif_dottorato'])
            if not allow_user:
                return custom_message(request, _("You are not authorized to post activities for this PhD"))

            form.save(commit=False)
            phd.user_mod_id = request.user
            phd.dt_mod = datetime.datetime.now()
            phd.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            if changed_field_labels:
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
def phd_main_teacher(request, code, teacher_id, phd=None, my_offices=None):
    """
    docente principale dottorato
    """
    activity_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                         pk=teacher_id,
                                         id_didattica_dottorato_attivita_formativa=phd)

    old_label = activity_teacher.cognome_nome_origine
    teacher = activity_teacher.matricola
    initial = {}
    teacher_data = ''
    if teacher:
        teacher_data = f'{teacher.cognome} {teacher.nome}'
        initial = {'choosen_person': encrypt(teacher.matricola)}

    external_form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=activity_teacher)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=patent_inventor,
                                                                  data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                teacher = get_object_or_404(
                    Personale, matricola=teacher_code)
                activity_teacher.matricola = teacher
                activity_teacher.cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
            else:
                activity_teacher.matricola = None
                activity_teacher.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            activity_teacher.user_mod = request.user
            activity_teacher.dt_mod = datetime.datetime.now()
            activity_teacher.save()

            if old_label != activity_teacher.cognome_nome_origine:
                log_action(user=request.user,
                           obj=phd,
                           flag=CHANGE,
                           msg=f'Sostituito docente principale {old_label} con {activity_teacher}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('crud_phd:crud_phd_main_teacher',
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
                  'phd_main_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': teacher_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'phd': phd,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_new(request, code, my_offices=None, phd=None):
    """
    nuovo docente principale
    """
    external_form = DidatticaDottoratoAttivitaFormativaDocenteForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                teacher = get_object_or_404(
                    Personale, matricola=teacher_code)
                cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
            else:
                teacher = None
                cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            d = DidatticaDottoratoAttivitaFormativaDocente.objects.create(
                id_didattica_dottorato_attivita_formativa=phd,
                cognome_nome_origine=cognome_nome_origine,
                matricola=teacher
            )

            d.user_mod_id = request.user
            d.dt_mod = datetime.datetime.now()
            d.save()

            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo docente principale {d}')

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
                   'phd': phd,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_phd
@can_edit_phd
def phd_main_teacher_delete(request, code, teacher_id, my_offices=None, phd=None):
    """
    rimuovi un docente principale
    """
    phd_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                    pk=teacher_id,
                                    id_didattica_dottorato_attivita_formativa=phd)

    main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
        id_didattica_dottorato_attivita_formativa=code)
    other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
        id_didattica_dottorato_attivita_formativa=code)

    if main_teachers.count() == 1 and not other_teachers:
        return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=phd,
               flag=CHANGE,
               msg=f'Rimosso docente principale {phd_teacher}')

    phd_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('crud_phd:crud_phd_edit', code=code)


@login_required
@can_manage_phd
@can_edit_phd
def phd_other_teacher(request, code, teacher_id, my_offices=None, phd=None):
    """
    modifica dati altro docente
    """
    activity_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                         pk=teacher_id,
                                         id_didattica_dottorato_attivita_formativa=phd)

    old_label = activity_teacher.cognome_nome_origine
    teacher = activity_teacher.matricola
    initial = {}
    teacher_data = ''
    if teacher:
        teacher_data = f'{teacher.cognome} {teacher.nome}'
        initial = {'choosen_person': encrypt(teacher.matricola)}

    external_form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=activity_teacher)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=activity_teacher,
                                         data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                teacher = get_object_or_404(
                    Personale, matricola=teacher_code)
                activity_teacher.matricola = teacher
                activity_teacher.cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
            else:
                activity_teacher.matricola = None
                activity_teacher.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            activity_teacher.user_mod = request.user
            activity_teacher.dt_mod = datetime.datetime.now()
            activity_teacher.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            if changed_field_labels and old_label != activity_teacher.cognome_nome_origine:
                log_action(user=request.user,
                           obj=phd,
                           flag=CHANGE,
                           msg=f'Sostituito docente {old_label} con {activity_teacher}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('crud_phd:crud_phd_other_teacher',
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
                  'phd_other_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': teacher_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'phd': phd,
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
    external_form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                teacher = get_object_or_404(
                    Personale, matricola=teacher_code)
                cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
            else:
                teacher = None
                cognome_nome_origine = form.cleaned_data['cognome_nome_origine']

            d = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(
                id_didattica_dottorato_attivita_formativa=phd,
                cognome_nome_origine=cognome_nome_origine,
                matricola=teacher
            )

            d.user_mod_id = request.user
            d.dt_mod = datetime.datetime.now()
            d.save()

            log_action(user=request.user,
                       obj=phd,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo docente {d}')

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
                   'external_form': external_form,
                   'internal_form': internal_form,
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

    main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
        id_didattica_dottorato_attivita_formativa=code)
    other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
        id_didattica_dottorato_attivita_formativa=code)

    if other_teachers.count() == 1 and not main_teachers:
        return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=phd,
               flag=CHANGE,
               msg=f'Rimosso docente {phd_teacher}')

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
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    phd.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("PhD activity removed successfully"))

    return redirect('crud_phd:crud_phd_list')
