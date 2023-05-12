import logging

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS Websites')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites.html', context)


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_website(request, code,
            my_offices=None, cds_website=None, ex_students=None, sliders=None, links=None):
    """
    modifica dati del sito web del corso di studio
    """
    form = SitoWebCdsDatiBaseForm(instance=cds_website)
    print('casa')
    cds_data = get_object_or_404(SitoWebCdsDatiBase, pk=code)
    print('casa')

    if request.POST:
        form = SitoWebCdsDatiBaseForm(instance=cds_website, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            cds_website.user_mod = request.user
            cds_website.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=cds_website,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Cds website edited successfully"))

            return redirect('crud_cds_websites:crud_cds_website_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cdswebsites'): _('Cds websites'),
                   '#': cds_website.nome_corso_it}

    return render(request,
                  'cds_website.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'cds_website': cds_website,
                   'cds_data': cds_data,
                   'ex_students': ex_students,
                   'sliders': sliders,
                   'links': links})


@login_required
@can_manage_cds_website
@can_edit_cds_website
def phd_ex_student_data(request, code, student_id, cds_website=None,
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

    form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST, required=True)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale,
                                            matricola=teacher_code)
            teacher_phd.matricola = new_teacher
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
        return custom_message(request, _("Operation not permitted. At least one teacher must be present"))

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

    form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST, required=True)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale,
                                            matricola=teacher_code)
            other_teacher_phd.matricola = new_teacher
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
                   'choosen_person': teacher_data[1] if teacher_data  else None,
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
        return custom_message(request, _("Operation not permitted. At least one teacher must be present"))

    log_action(user=request.user,
               obj=phd,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {phd_teacher.cognome_nome_origine}')

    phd_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('crud_phd:crud_phd_edit', code=code)
