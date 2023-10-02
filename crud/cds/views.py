import datetime
import logging
import os

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

from .. utils.forms import ChoosenPersonForm

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds
def cds(request, my_offices=None):
    """
    lista dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist')}
    return render(request, 'cds.html', context)


@login_required
@can_manage_cds
# @can_edit_cds
def cds_detail(request, regdid_id, my_offices=None, regdid=None):
    """
    dettaglio corso di studio
    """

    # altri dati corso di studio
    other_data = DidatticaCdsAltriDati.objects.filter(
        regdid_id=regdid_id).first()

    # dati uffici corso di studio
    regdid = DidatticaRegolamento.objects\
                                 .filter(pk=regdid_id)\
                                 .select_related('cds')\
                                 .first()
    office_data = DidatticaCdsAltriDatiUfficio.objects.filter(
        cds_id=regdid.cds.pk)

    # dati gruppi cds
    gruppi_cds_data = DidatticaCdsGruppi.objects.filter(
        id_didattica_cds=regdid.cds.pk)

    # dati gruppi dipartimento
    gruppi_dip_data = DidatticaDipartimentoGruppi.objects.filter(
        id_didattica_dipartimento=regdid.cds.dip.pk)

    # dizionario chiave-valore
    gruppi_cds = {}
    for gruppo in gruppi_cds_data:
        gruppi_cds_componenti = DidatticaCdsGruppiComponenti.objects.filter(
            id_didattica_cds_gruppi=gruppo)
        gruppi_cds[gruppo.pk] = gruppi_cds_componenti

    gruppi_dip = {}
    for gruppo in gruppi_dip_data:
        gruppi_dip_componenti = DidatticaDipartimentoGruppiComponenti.objects.filter(
            id_didattica_dipartimento_gruppi=gruppo)
        gruppi_dip[gruppo.pk] = gruppi_dip_componenti

    # logs
    logs_regdid = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(regdid).pk,
                                          object_id=regdid.pk)

    logs_cds = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(regdid.cds).pk,
                                       object_id=regdid.cds.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   '#': regdid.cds.nome_cds_it}

    return render(request,
                  'cds_detail.html',
                  {'breadcrumbs': breadcrumbs,
                   'logs_regdid': logs_regdid,
                   'logs_cds': logs_cds,
                   'other_data': other_data,
                   'office_data': office_data,
                   'regdid': regdid,
                   'gruppi_cds_data': gruppi_cds_data,
                   'gruppi_dip_data': gruppi_dip_data,
                   'gruppi_cds': gruppi_cds,
                   'gruppi_dip': gruppi_dip})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):
    """
    modifica altri dati corso di studio
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)
    form = DidatticaCdsAltriDatiForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsAltriDatiForm(instance=other_data,
                                         data=request.POST,
                                         files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            other_data.user_mod = request.user
            if not form.cleaned_data['nome_origine_coordinatore'] and other_data.matricola_coordinatore:
                other_data.nome_origine_coordinatore = f'{other_data.matricola_coordinatore.nome} {other_data.matricola_coordinatore.cognome}'
            if not form.cleaned_data['nome_origine_vice_coordinatore'] and other_data.matricola_vice_coordinatore:
                other_data.nome_origine_vice_coordinatore = f'{other_data.matricola_vice_coordinatore.nome} {other_data.matricola_vice_coordinatore.cognome}'

            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
                log_action(user=request.user,
                           obj=regdid,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Other data edited successfully"))

            return redirect('crud_cds:crud_cds_other_data_edit',
                            regdid_id=regdid_id,
                            data_id=data_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {
        reverse('crud_utils:crud_dashboard'): _('Dashboard'),
        reverse('crud_cds:crud_cds'): _('CdS'),
        reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
        reverse('crud_cds:crud_cds_other_data_edit', kwargs={'regdid_id': regdid_id, 'data_id': data_id}): _("Other data")
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
    """
    modifica coordinatore corso di studio
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati.objects.select_related('matricola_coordinatore'),
                                   pk=data_id, regdid_id=regdid_id)

    teacher = other_data.matricola_coordinatore
    teacher_data = ''
    initial = {}

    if teacher:
        teacher_data = f'{teacher.nome} {teacher.cognome}'
        initial = {'choosen_person': encrypt(teacher.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_coordinatore = new_teacher

            if not other_data.nome_origine_coordinatore:
                other_data.nome_origine_coordinatore = f'{new_teacher.nome} {new_teacher.cognome}'

            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = ''
            elif teacher and teacher != new_teacher:
                log_msg = f'Sostituito link coordinatore {teacher} con {new_teacher}'
            else:
                log_msg = f'Aggiunto link coordinatore a {new_teacher}'

            if log_msg:
                log_action(user=request.user,
                           obj=regdid,
                           flag=CHANGE,
                           msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('crud_cds:crud_cds_other_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('crud_cds:crud_cds_other_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id': data_id}): _('Other data'),
                   '#': _('Coordinator')}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id': data_id,
                   'choosen_person': teacher_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator(request, regdid_id, data_id,
                                      my_offices=None, regdid=None):
    """
    modifica vice coordinatore corso di studio
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati.objects.select_related('matricola_vice_coordinatore'),
                                   pk=data_id,
                                   regdid_id=regdid_id)

    teacher = other_data.matricola_vice_coordinatore
    teacher_data = ''
    initial = {}

    if teacher:
        teacher_data = f'{teacher.nome} {teacher.cognome}'
        initial = {'choosen_person': encrypt(teacher.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_vice_coordinatore = new_teacher

            if not other_data.nome_origine_vice_coordinatore:
                other_data.nome_origine_vice_coordinatore = f'{new_teacher.nome} {new_teacher.cognome}'

            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = ''
            elif teacher and teacher != new_teacher:
                log_msg = f'Sostituito link vice-coordinatore {teacher} con {new_teacher}'
            else:
                log_msg = f'Aggiunto link vice-coordinatore a {new_teacher}'

            if log_msg:
                log_action(user=request.user,
                           obj=regdid,
                           flag=CHANGE,
                           msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Deputy Coordinator edited successfully"))
            return redirect('crud_cds:crud_cds_other_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('crud_cds:crud_cds_other_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id': data_id}): _('Other data'),
                   '#': _('Deputy coordinator')}

    return render(request,
                  'cds_other_data_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id': data_id,
                   'choosen_person': teacher_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    elimina altri dati
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)

    other_data.delete()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg='Set di dati eliminato')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data removed successfully"))
    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_new(request, regdid_id, my_offices=None, regdid=None):
    """
    nuovi altri dati per il corso di studio
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id)

    if other_data:
        raise Exception(_('Other data set already existent for this cds'))

    DidatticaCdsAltriDati.objects.create(regdid_id=regdid)

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg='Creato nuovo set di dati')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Other data created successfully"))
    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator_delete(request, regdid_id, data_id,
                                      my_offices=None, regdid=None):
    """
    elimina coordinatore
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)

    other_data.matricola_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg='Rimosso link a coordinatore')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Coordinator data removed successfully"))
    return redirect('crud_cds:crud_cds_other_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator_delete(request, regdid_id, data_id,
                                             my_offices=None, regdid=None):
    """
    elimina vice coordinatore
    """
    other_data = get_object_or_404(DidatticaCdsAltriDati,
                                   pk=data_id,
                                   regdid_id=regdid_id)

    other_data.matricola_vice_coordinatore = None
    other_data.save()

    log_action(user=request.user,
               obj=regdid,
               flag=CHANGE,
               msg='Rimosso link a vice-coordinatore')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Deputy coordinator data removed successfully"))
    return redirect('crud_cds:crud_cds_other_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    elimina dati ufficio per il corso di studio
    """
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio,
                                    pk=data_id, cds=regdid.cds)

    office_data.delete()

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg='Rimosso set dati ufficio')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data removed successfully"))
    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):
    """
    modifica dati ufficio per il corso di studio
    """
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio.objects.select_related('matricola_riferimento'),
                                    pk=data_id,
                                    cds=regdid.cds)

    form = DidatticaCdsAltriDatiUfficioForm(instance=office_data)

    if request.POST:
        form = DidatticaCdsAltriDatiUfficioForm(instance=office_data,
                                                data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            office_data.user_mod = request.user

            # se è valorizzato il link a una Persona
            # e non viene definita un'etichetta per il responsabile
            # questa viene impostata automaticamente
            # con i dati dell'oggetto linkato
            if not form.cleaned_data['nome_origine_riferimento'] and office_data.matricola_riferimento:
                persona = office_data.matricola_riferimento
                office_data.nome_origine_riferimento = f'{persona.nome} {persona.cognome}'

            office_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)

                log_action(user=request.user,
                           obj=regdid.cds,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Office data edited successfully"))

            return redirect('crud_cds:crud_cds_office_data_edit',
                            regdid_id=regdid_id,
                            data_id=data_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
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
    """
    aggiungi dati ufficio al corso di studio
    """
    new = DidatticaCdsAltriDatiUfficio.objects.create(cds=regdid.cds,
                                                      ordine=10)

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg='Aggiunto nuovo set dati ufficio')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Office data created successfully"))

    return redirect('crud_cds:crud_cds_office_data_edit',
                    regdid_id=regdid_id,
                    data_id=new.pk)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    modifica il responsabile dell'ufficio
    """
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio.objects.select_related('matricola_riferimento'),
                                    pk=data_id, cds=regdid.cds)

    person = office_data.matricola_riferimento
    person_data = ''
    initial = {}
    if person:
        person_data = f'{person.nome} {person.cognome}'
        initial = {'choosen_person': encrypt(person.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            person_code = decrypt(form.cleaned_data['choosen_person'])
            new_person = get_object_or_404(Personale, matricola=person_code)
            office_data.matricola_riferimento = new_person
            if not office_data.nome_origine_riferimento:
                office_data.nome_origine_riferimento = f'{new_person.nome} {new_person.cognome}'
            office_data.save()

            if person and person == new_person:
                log_msg = ''
            elif person and person != new_person:
                log_msg = f'Sostituito link responsabile {person} con {new_person}'
            else:
                log_msg = f'Aggiunto link responsabile a {new_person}'

            log_action(user=request.user,
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Coordinator edited successfully"))
            return redirect('crud_cds:crud_cds_office_data_edit',
                            regdid_id=regdid_id, data_id=data_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('crud_cds:crud_cds_office_data_edit',
                           kwargs={'regdid_id': regdid_id, 'data_id': data_id}): _('Office data'),
                   '#': _('Responsible')}

    return render(request,
                  'cds_office_data_responsible.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid,
                   'data_id': data_id,
                   'choosen_person': person_data,
                   'url': reverse('ricerca:addressbooklist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    elimina responsabile ufficio
    """
    office_data = get_object_or_404(DidatticaCdsAltriDatiUfficio.objects.select_related('matricola_riferimento'),
                                    pk=data_id, cds=regdid.cds)
    office_data.matricola_riferimento = None
    office_data.save()

    log_action(user=request.user,
               obj=regdid.cds,
               flag=ADDITION,
               msg=_("New organization added successfully"))

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Responsible data removed successfully"))
    return redirect('crud_cds:crud_cds_office_data_edit',
                    regdid_id=regdid_id,
                    data_id=data_id)


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_teaching_system
def cds_doc_teaching_system(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi/modifica ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid).first()
    form = DidatticaCdsOrdinamentoForm(instance=other_data)

    if request.POST:

        form = DidatticaCdsOrdinamentoForm(instance=other_data,
                                           files=request.FILES)
        if form.is_valid():
            other_data = form.save(commit=False)
            other_data.regdid_id = regdid
            other_data.user_mod = request.user
            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                           form.changed_data)

                log_action(user=request.user,
                           obj=regdid,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teaching system file edited successfully"))

            return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   '#': _('Teaching system')
                   }

    return render(request,
                  'cds_teaching_system.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid})


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_teaching_system
def cds_doc_teaching_system_delete(request, regdid_id, my_offices=None, regdid=None):
    """
    elimina ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid).first()
    if other_data:
        try:
            path = other_data.ordinamento_didattico.path
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
        other_data.user_mod = request.user
        other_data.ordinamento_didattico = None
        other_data.save(update_fields=['ordinamento_didattico', 'user_mod'])

        log_action(user=request.user,
                   obj=regdid,
                   flag=CHANGE,
                   msg=_("Teaching system file removed"))

        messages.add_message(request,
                             messages.SUCCESS,
                             _("Teaching system file removed successfully"))

    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_manifesto_regulation(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi/modifica ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid).first()
    form = DidatticaCdsManifestoRegolamentoForm(instance=other_data)

    if request.POST:

        form = DidatticaCdsManifestoRegolamentoForm(instance=other_data,
                                                    files=request.FILES)
        if form.is_valid():
            other_data = form.save(commit=False)
            other_data.user_mod = request.user
            other_data.regdid_id = regdid
            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                           form.changed_data)

                log_action(user=request.user,
                           obj=regdid,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Documents edited successfully"))

            return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   '#': _('Teaching system')
                   }

    return render(request,
                  'cds_manifesto_regulation.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'regdid': regdid})


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_study_manifesto_delete(request, regdid_id, my_offices=None, regdid=None):
    """
    elimina manifesto studi
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid).first()
    if other_data:
        try:
            path = other_data.manifesto_studi.path
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
        other_data.user_mod = request.user
        other_data.manifesto_studi = None
        other_data.save(update_fields=['manifesto_studi', 'user_mod'])

        log_action(user=request.user,
                   obj=regdid,
                   flag=CHANGE,
                   msg=_("Study manifesto file removed"))

        messages.add_message(request,
                             messages.SUCCESS,
                             _("Study manifesto file removed successfully"))

    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_didactic_regulation_delete(request, regdid_id, my_offices=None, regdid=None):
    """
    elimina regolamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid).first()
    if other_data:
        try:
            path = other_data.regolamento_didattico.path
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
        other_data.user_mod = request.user
        other_data.regolamento_didattico = None
        other_data.save(update_fields=['regolamento_didattico','user_mod'])

        log_action(user=request.user,
                   obj=regdid,
                   flag=CHANGE,
                   msg=_("Didactic regulation file removed"))

        messages.add_message(request,
                             messages.SUCCESS,
                             _("Didactic regulation file removed successfully"))

    return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_organizations_new(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi organizzazione cds
    """
    form = DidatticaCdsGruppoForm()

    if request.POST:
        form = DidatticaCdsGruppoForm(data=request.POST)
        if form.is_valid():
            cds_organization = form.save(commit=False)
            cds_organization.id_didattica_cds = regdid.cds
            cds_organization.id_user_mod = request.user
            cds_organization.dt_mod = datetime.datetime.now()
            cds_organization.save()

            log_action(user=request.user,
                       obj=regdid.cds,
                       flag=ADDITION,
                       msg=_("Nuova organizzazione creata con successo"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("CdS Organization successfully"))

            return redirect('crud_cds:crud_cds_detail', regdid_id=regdid_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'cds_organization.html',
                  {'form': form,})


@login_required
@can_manage_cds
@can_edit_cds
def cds_organizations_edit(request, regdid_id, group_id, my_offices=None, regdid=None):
    """
    modifica organizzazione cds
    """
    cds_organization = get_object_or_404(DidatticaCdsGruppi,
                                         pk=group_id,
                                         id_didattica_cds=regdid.cds)
    form = DidatticaCdsGruppoForm(instance=cds_organization)

    if request.POST:
        form = DidatticaCdsGruppoForm(instance=cds_organization,
                                      data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            cds_organization.id_didattica_cds = regdid.cds
            cds_organization.id_user_mod = request.user
            cds_organization.dt_mod = datetime.datetime.now()
            cds_organization.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)

            log_action(user=request.user,
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("CdS Organization successfully edited"))

            return redirect('crud_cds:crud_cds_organizations_edit',
                            regdid_id=regdid_id,
                            group_id=group_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'cds_organization.html',
                  {'form': form,
                   'cds_organization': cds_organization,
                   'regdid': regdid})


@login_required
@can_manage_cds
@can_edit_cds
def cds_organizations_components_new(request, regdid_id, group_id,
                                     my_offices=None, regdid=None):
    """
    aggiungi nuovo componente al gruppo
    """
    cds_organization = get_object_or_404(DidatticaCdsGruppi,
                                         pk=group_id,
                                         id_didattica_cds=regdid.cds)

    external_form = DidatticaCdsGruppoComponenteForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaCdsGruppoComponenteForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                # matricola
                component_code = decrypt(form.cleaned_data['choosen_person'])
                matricola = get_object_or_404(
                    Personale, matricola=component_code)
                cognome = f'{component.cognome} {component.nome}'
            else:
                matricola = None
                cognome = form.cleaned_data['cognome']

            c = DidatticaCdsGruppiComponenti.objects.create(
                id_didattica_cds_gruppi=cds_organization,
                matricola=matricola,
                cognome=cognome,
                nome="",
                funzione_it=form.cleaned_data.get('funzione_it'),
                funzione_en=form.cleaned_data.get('funzione_en'),
                ordine=form.cleaned_data.get('ordine'),
                visibile=form.cleaned_data.get('visibile'),
                dt_mod=datetime.datetime.now(),
                id_user_mod=request.user
            )

            log_action(user=request.user,
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo componente {c} al gruppo {cds_organization.pk}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Component added successfully"))
            return redirect('crud_cds:crud_cds_organizations_edit',
                            regdid_id=regdid_id,
                            group_id=group_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('crud_cds:crud_cds_organizations_edit', kwargs={'regdid_id': regdid_id, 'group_id': group_id}): cds_organization.descr_breve_it,
                   '#': _('New component')}

    return render(request,
                  'cds_organization_component.html',
                  {'breadcrumbs': breadcrumbs,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'cds_organization': cds_organization,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_organizations_components_edit(request, regdid_id, group_id, component_id,
                                     my_offices=None, regdid=None):
    """
    aggiungi nuovo componente al gruppo
    """
    cds_organization = get_object_or_404(DidatticaCdsGruppi,
                                         pk=group_id,
                                         id_didattica_cds=regdid.cds)

    component = get_object_or_404(DidatticaCdsGruppiComponenti,
                                  pk=component_id,
                                  id_didattica_cds_gruppi=cds_organization)

    component_data = ''
    initial = {}

    if component.matricola:
        component_data = f'{component.matricola.cognome} {component.matricola.nome}'
        initial = {'choosen_person': encrypt(component.matricola.matricola)}

    external_form = DidatticaCdsGruppoComponenteForm(instance=component)
    internal_form = ChoosenPersonForm(initial=initial, instance=component, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(instance=component, data=request.POST, required=True)
        external_form = DidatticaCdsGruppoComponenteForm(instance=component, data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                # matricola
                component_code = decrypt(form.cleaned_data['choosen_person'])
                matricola = get_object_or_404(Personale,
                                              matricola=component_code)
                component.matricola = matricola
                component.cognome = f'{matricola.cognome} {matricola.nome}'
            else:
                component.matricola = None
                component.cognome = form.cleaned_data['cognome']

            form.save(commit=False)
            component.dt_mod=datetime.datetime.now()
            component.id_user_mod=request.user

            component.save()

            log_action(user=request.user,
                       obj=regdid.cds,
                       flag=CHANGE,
                       msg=f'Modificato componente {component} al gruppo {cds_organization.pk}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Component edited successfully"))
            return redirect('crud_cds:crud_cds_organizations_edit',
                            regdid_id=regdid_id,
                            group_id=group_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds:crud_cds'): _('CdS'),
                   reverse('crud_cds:crud_cds_detail', kwargs={'regdid_id': regdid_id}): regdid.cds.nome_cds_it,
                   reverse('crud_cds:crud_cds_organizations_edit', kwargs={'regdid_id': regdid_id, 'group_id': group_id}): cds_organization.descr_breve_it,
                   '#': _('Edit component')}

    return render(request,
                  'cds_organization_component.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': component_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'cds_organization': cds_organization,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_cds
@can_edit_cds
def cds_organizations_components_delete(request, regdid_id, group_id, component_id,
                                     my_offices=None, regdid=None):
    """
    elimina componente di un gruppo
    """

    cds_organization = get_object_or_404(DidatticaCdsGruppi,
                                         pk=group_id,
                                         id_didattica_cds=regdid.cds)

    component = get_object_or_404(DidatticaCdsGruppiComponenti,
                                  pk=component_id,
                                  id_didattica_cds_gruppi=cds_organization)

    component.delete()

    log_action(user=request.user,
               obj=regdid.cds,
               flag=CHANGE,
               msg=f'Eliminato componente {component} dal gruppo {cds_organization.pk}')


    messages.add_message(request,
                        messages.SUCCESS,
                        _("Component deleted successfully"))
    
    return render(request,
                'cds_organization.html',
                {'cds_organization': cds_organization,
                'regdid': regdid})