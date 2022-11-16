import logging
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

from .. decorators import *
from . .forms import *
from .. utils import log_action


logger = logging.getLogger(__name__)


@login_required
@can_manage_teachers
def teachers(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Teachers and PTA')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:teacherslist')}
    return render(request, 'teachers/teachers.html', context)



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
                  'teachers/teacher_detail.html',
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
                  'teachers/teacher_other_data.html',
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
                  'teachers/teacher_other_data_new.html',
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
                  'teachers/teacher_board_data.html',
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
                  'teachers/teacher_board_data_new.html',
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
                  'teachers/teacher_materials_data.html',
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
                  'teachers/teacher_materials_data_new.html',
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
