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
@can_manage_cds
def cds(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist')}
    return render(request, 'cds/cds.html', context)


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
                  'cds/cds_detail.html',
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
                  'cds/cds_other_data.html',
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
                  'cds/cds_other_data_teacher.html',
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
                  'cds/cds_other_data_teacher.html',
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
                  'cds/cds_office_data.html',
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
                  'cds/cds_office_data_responsible.html',
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
