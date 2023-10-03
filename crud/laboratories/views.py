import logging
import os

from .. utils.utils import log_action

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

from .. utils.forms import ChoosenPersonForm

from . decorators import *
from . forms import *
from . settings import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_laboratories
def laboratories(request, laboratory=None):
    """
    lista dei laboratori
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Laboratories')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:laboratorieslist')}
    return render(request, 'laboratories.html', context)


@login_required
@can_manage_laboratories
def laboratory(request, code, laboratory=None):
    """
    dettaglio laboratorio
    """
    #LaboratorioDatiBase
    form = LaboratorioDatiBaseForm(instance=laboratory)
    referent_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)
    scientific_director_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)
    safety_manager_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)
    department_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)
    #LaboratorioAltriDipartimenti
    extra_departments = LaboratorioAltriDipartimenti.objects.filter(
            id_laboratorio_dati=code).all()
    #LaboratorioAttrezzature
    equipment = LaboratorioAttrezzature.objects.filter(id_laboratorio_dati=code).all()
    #LaboratorioTipologiaRischio
    risk_type = LaboratorioTipologiaRischio.objects.filter(
            id_laboratorio_dati=code).all()
    risk_type_form = LaboratorioTipologiaRischioForm(instance=risk_type[0])
    
    #LaboratorioDatiErc1
    researches_erc1 = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code).values("id",
                                                                                          "id_ricerca_erc1",
                                                                                          "id_ricerca_erc1__descrizione")
    #LaboratorioUbicazione
    locations = LaboratorioUbicazione.objects.filter(id_laboratorio_dati=code).all()
    #LaboratorioPersonaleRicerca
    researchers = LaboratorioPersonaleRicerca.objects.filter(id_laboratorio_dati=code).all()
    #LaboratorioPersonaleTecnico
    technicians = LaboratorioPersonaleTecnico.objects.filter(id_laboratorio_dati=code).values("id", "cognomenome_origine")
    #LaboratorioAttivita
    activities = LaboratorioAttivita.objects.filter(id_laboratorio_dati=code).values("id", "id_tipologia_attivita__descrizione")
    #LaboratorioServiziErogati
    provided_services = LaboratorioServiziErogati.objects.filter(id_laboratorio_dati=code).values("id", "descrizione")
    #LaboratorioServiziOfferti
    offered_services = LaboratorioServiziOfferti.objects.filter(id_laboratorio_dati=code).values("id", "nome_servizio")

    
    if request.POST:
        form = LaboratorioDatiBaseForm(instance=laboratory,
                                          data=request.POST,
                                          files=request.FILES)
        risk_type_form = LaboratorioTipologiaRischioForm(instance=risk_type[0],
                                                            data=request.POST)
        if form.is_valid() and risk_type_form.is_valid():
            form.save(commit=False)
            laboratory.user_mod = request.user
            laboratory.save()

            risk_type_form.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            if risk_type_form.changed_data:
                changed_risk_type_form_field_labels = _get_changed_field_labels_from_form(risk_type_form,
                                                                       risk_type_form.changed_data)
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_risk_type_form_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(laboratory).pk,
                                   object_id=laboratory.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratory'),
                   '#': laboratory.nome_laboratorio}

    return render(request,
                  'laboratory.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'laboratory': laboratory,
                   'referent_data': referent_data,
                   'department_data': department_data,
                   'scientific_director_data': scientific_director_data,
                   'safety_manager_data' : safety_manager_data,
                   'extra_departments': extra_departments,
                   'laboratory_equipment': equipment,
                   'risk_type_form': risk_type_form,
                   'researches_erc1': researches_erc1,
                   'locations': locations,
                   'researchers': researchers,
                   'technicians': technicians,
                   'activities': activities,
                   'provided_services': provided_services,
                   'offered_services': offered_services,
                   })


@login_required
@can_manage_laboratories
def laboratory_new(request, laboratory=None):
    """
    aggiungi nuovo laboratorio
    """

    #new
    form = LaboratorioDatiBaseForm()
    department_form = LaboratorioDatiBaseDipartimentoForm()
    risk_type_form = LaboratorioTipologiaRischioForm()

    unical_referent_internal_form = LaboratorioDatiBaseUnicalReferentChoosenPersonForm(required=True)
    unical_referent_external_form = LaboratorioDatiBaseUnicalReferentForm()

    scientific_director_internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(required=True)
    scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                       dip_id=request.POST['choosen_department'])

    unical_referent = None
    scientific_director = None


    if request.POST.get(UNICAL_REFERENT_ID, ''):
        unical_referent = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST[UNICAL_REFERENT_ID])))

    if request.POST.get(SCIENTIFIC_DIRECTOR_ID, ''):
        scientific_director = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST[SCIENTIFIC_DIRECTOR_ID])))

    if request.POST:
        form = LaboratorioDatiBaseForm(
            data=request.POST, files=request.FILES)
        department_form = LaboratorioDatiBaseDipartimentoForm(data=request.POST)
        
        if UNICAL_REFERENT_ID in request.POST and request.POST[UNICAL_REFERENT_ID]:
            unical_referent_form = LaboratorioDatiBaseUnicalReferentChoosenPersonForm(data=request.POST, required=True) 
        else:
            unical_referent_form = LaboratorioDatiBaseUnicalReferentForm(data=request.POST)

        if SCIENTIFIC_DIRECTOR_ID in request.POST and request.POST[SCIENTIFIC_DIRECTOR_ID]:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(data=request.POST, required=True) 
        else:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorForm(data=request.POST)

        risk_type_form = LaboratorioTipologiaRischioForm(data=request.POST)
        
        if form.is_valid() and unical_referent_form.is_valid() and department_form.is_valid() and scientific_director_form.is_valid() and risk_type_form.is_valid():
            laboratory = form.save(commit=False)

            #unical referent
            if unical_referent_form.cleaned_data.get(UNICAL_REFERENT_ID):
                unical_referent_code = decrypt(unical_referent_form.cleaned_data[UNICAL_REFERENT_ID])
                unical_referent = get_object_or_404(
                    Personale, matricola=unical_referent_code)
                laboratory.matricola_referente_compilazione = unical_referent
                laboratory.referente_compilazione = f'{unical_referent.cognome} {unical_referent.nome}'
                laboratory.email_compilazione = unical_referent.email
            else:
                laboratory.matricola_referente_compilazione = None
                laboratory.referente_compilazione = unical_referent_form.cleaned_data['referente_compilazione']
                laboratory.email_compilazione = unical_referent_form.cleaned_data['email_compilazione']
            #scientific director
            if scientific_director_form.cleaned_data.get(SCIENTIFIC_DIRECTOR_ID):
                scientific_director_code = decrypt(scientific_director_form.cleaned_data[SCIENTIFIC_DIRECTOR_ID])
                scientific_director = get_object_or_404(
                    Personale, matricola=scientific_director_code)
                laboratory.matricola_responsabile_scientifico = scientific_director
                laboratory.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
            else:
                laboratory.matricola_responsabile_scientifico = None
                laboratory.responsabile_scientifico = scientific_director_form.cleaned_data['responsabile_scientifico']
            
            # se viene scelto un dipartimento
            # questo viene associato al laboratorio
            laboratory.dipartimento_riferimento = department.dip_des_it
            laboratory.id_dipartimento_riferimento = department

            # tipologia rischio
            laboratory.save()
            laboratory_risk_type = risk_type_form.save(commit=False)
            laboratory_risk_type.id_laboratorio_dati = laboratory
            laboratory_risk_type.save()

            log_action(user=request.user,
                       obj=laboratory,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory created successfully"))
            return redirect("crud_laboratories:crud_laboratories")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")
            for k, v in unical_referent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{unical_referent_form.fields[k].label}</b>: {v}")
            for k, v in scientific_director_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{scientific_director_form.fields[k].label}</b>: {v}")
            for k, v in risk_type_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{risk_type_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   '#': _('New')}
    return render(request,
                    'laboratory_new.html',
                    {'breadcrumbs': breadcrumbs,
                    'form': form,
                    'departments_api': reverse('ricerca:departmentslist'),
                    'teachers_api': reverse('ricerca:teacherslist'),
                    'department_form': department_form,
                    'url': reverse('ricerca:teacherslist'),
                    'unical_referent_label' : UNICAL_REFERENT_ID,
                    'scientific_director_label' : SCIENTIFIC_DIRECTOR_ID,
                    'choosen_department': f'{department.dip_des_it}' if department else '',
                    'choosen_unical_referent': f'{unical_referent.cognome} {unical_referent.nome}' if unical_referent else '',
                    'choosen_scientific_director' : f'{scientific_director.cognome} {scientific_director.nome}' if scientific_director else '',
                    'unical_referent_internal_form': unical_referent_internal_form,
                    'unical_referent_external_form': unical_referent_external_form,
                    'scientific_director_internal_form': scientific_director_internal_form,
                    'scientific_director_external_form': scientific_director_external_form,
                    'risk_type_form': risk_type_form,
                    })

@login_required
@can_manage_laboratories
def laboratory_unical_department_data_edit(request, code, department_id,
                                        laboratory=None):
    """
    modifica dipartimento
    """
    department_laboratory = get_object_or_404(LaboratorioDatiBase.objects.select_related('id_dipartimento_riferimento'),
                                           pk=department_id)
    department = department_laboratory.id_dipartimento_riferimento
    if department:
        old_label = department.dip_des_it
    else:
        old_label = ''
    department_data = ''
    initial = {}
    if department:
        department_data = department.dip_des_it
        initial = {'choosen_department': department.dip_id}

    form = LaboratorioDatiBaseDipartimentoForm(initial=initial)

    if request.POST:
        form = LaboratorioDatiBaseDipartimentoForm(data=request.POST)
        if form.is_valid():

            department_code = form.cleaned_data['choosen_department']
            new_department = get_object_or_404(DidatticaDipartimento,
                                               dip_id=department_code)
            department_laboratory.user_mod = request.user
            department_laboratory.id_dipartimento_riferimento = new_department
            department_laboratory.dipartimento_riferimento = f'{new_department.dip_des_it}'
            department_laboratory.save()

            if old_label == '':
                log_action(user=request.user,
                           obj=laboratory,
                           flag=ADDITION,
                           msg=f'Aggiunto dipartimento {new_department}')

            if old_label != new_department:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito dipartimento {old_label} con {new_department}')


            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   '#': f'{laboratory.dipartimento_riferimento}'}

    return render(request,
                  'laboratory_department.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'laboratory': laboratory,
                   'department_id': department_id,
                   'choosen_department': department_data,
                   'url': reverse('ricerca:departmentslist')})

@login_required
@can_manage_laboratories
def laboratory_unical_referent_edit(request, code, data_id, laboratory=None):
    """
    dettaglio referente Unical del laboratorio
    """
    laboratory_referent = get_object_or_404(LaboratorioDatiBase.objects.select_related('matricola_referente_compilazione'),
                                         pk=data_id)
    old_label = laboratory_referent.referente_compilazione
    referent = laboratory_referent.matricola_referente_compilazione
    initial = {}
    referent_data = ''
    if referent:
        referent_data = f'{referent.cognome} {referent.nome}'
        initial = {'choosen_person': encrypt(referent.matricola)}

    external_form = LaboratorioDatiBaseUnicalReferentForm(
        instance=laboratory_referent)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:

        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseUnicalReferentForm(instance=laboratory_referent,
                                                            data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                referent_code = decrypt(form.cleaned_data['choosen_person'])
                referent = get_object_or_404(
                    Personale, matricola=referent_code)
                laboratory_referent.matricola_referente_compilazione = referent
                laboratory_referent.referente_compilazione = f'{referent.cognome} {referent.nome}'
                laboratory_referent.email_compilazione = referent.email
            else:
                laboratory_referent.matricola_referente_compilazione = None
                laboratory_referent.referente_compilazione = form.cleaned_data['referente_compilazione']
                laboratory_referent.email_compilazione = form.cleaned_data['email_compilazione']


            laboratory_referent.save()

            if old_label != laboratory_referent.referente_compilazione:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito referente {old_label} con {laboratory_referent.referente_compilazione}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory referent edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_unical_referent_edit', kwargs={'code': code, 'data_id': data_id}): _('Unical Referent')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': referent_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Unical Referent"),
                   'edit': 1,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_laboratories
def laboratory_scientific_director_edit(request, code, data_id, laboratory=None):
    """
    dettaglio responsabile scientifico del laboratorio
    """
    laboratory_scientific_director = get_object_or_404(LaboratorioDatiBase.objects.select_related('matricola_responsabile_scientifico'),
                                         pk=data_id)
    old_label = laboratory_scientific_director.responsabile_scientifico
    scientific_director = laboratory_scientific_director.matricola_responsabile_scientifico
    initial = {}
    scientific_director_data = ''
    if scientific_director:
        scientific_director_data = f'{scientific_director.cognome} {scientific_director.nome}'
        initial = {'choosen_person': encrypt(scientific_director.matricola)}

    external_form = LaboratorioDatiBaseScientificDirectorForm(
        instance=laboratory_scientific_director)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:

        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseScientificDirectorForm(instance=laboratory_scientific_director,
                                                            data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                scientific_director_code = decrypt(form.cleaned_data['choosen_person'])
                scientific_director = get_object_or_404(
                    Personale, matricola=scientific_director_code)
                laboratory_scientific_director.matricola_responsabile_scientifico = scientific_director
                laboratory_scientific_director.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
            else:
                laboratory_scientific_director.matricola_responsabile_scientifico = None
                laboratory_scientific_director.responsabile_scientifico = form.cleaned_data['responsabile_scientifico']

            laboratory_scientific_director.save()

            if old_label != laboratory_scientific_director.responsabile_scientifico:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito responsabile scientifico {old_label} con {laboratory_scientific_director.responsabile_scientifico}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory scientific director edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_scientific_director_edit', kwargs={'code': code, 'data_id': data_id}): _('Scientific Director')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': scientific_director_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Scientific Director"),
                   'edit': 1,
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
def laboratory_safety_manager_edit(request, code, data_id, laboratory=None):
    """
    dettaglio responsabile scientifico del laboratorio
    """
    laboratory_safety_manager = get_object_or_404(LaboratorioDatiBase.objects.select_related('matricola_preposto_sicurezza'), pk=data_id)
    old_label = laboratory_safety_manager.preposto_sicurezza
    safety_manager = laboratory_safety_manager.matricola_preposto_sicurezza
    initial = {}
    safety_manager_data = ''
    if safety_manager:
        safety_manager_data = f'{safety_manager.cognome} {safety_manager.nome}'
        initial = {'choosen_person': encrypt(safety_manager.matricola)}

    form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:

        form = ChoosenPersonForm(data=request.POST, required=True)

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                safety_manager_code = decrypt(form.cleaned_data['choosen_person'])
                safety_manager = get_object_or_404(
                    Personale, matricola=safety_manager_code)
                laboratory_safety_manager.matricola_preposto_sicurezza = safety_manager
                laboratory_safety_manager.preposto_sicurezza = f'{safety_manager.cognome} {safety_manager.nome}'
            else:
                laboratory_safety_manager.matricola_preposto_sicurezza = None
                laboratory_safety_manager.preposto_sicurezza = form.cleaned_data['preposto_sicurezza']

            laboratory_safety_manager.save()

            if old_label != laboratory_safety_manager.preposto_sicurezza:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito preposto sicurezza {old_label} con {laboratory_safety_manager.preposto_sicurezza}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory safety manager edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_safety_manager_edit', kwargs={'code': code, 'data_id': data_id}): _('Safety Manager')
                   }

    return render(request,
                  'laboratory_safety_manager.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': safety_manager_data,
                   'form': form,
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
def laboratory_safety_manager_delete(request, code, data_id, laboratory=None):
    """
    elimina preposto sicurezza
    """
    laboratory = get_object_or_404(LaboratorioDatiBase,
    pk=code)

    laboratory.matricola_preposto_sicurezza = None
    laboratory.preposto_sicurezza = None
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted safety manager")}')

    messages.add_message(request, messages.SUCCESS, _("Safety manager removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@can_manage_laboratories
def laboratory_delete(request, code, laboratory=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    laboratory = get_object_or_404(LaboratorioDatiBase, pk=code)
    laboratory.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Laboratory removed successfully"))

    return redirect('crud_laboratories:crud_laboratories')


@login_required
@can_manage_laboratories
def laboratory_extra_departments_new(request, code, laboratory=None):
    department_form = LaboratorioAltriDipartimentiForm()
    if request.POST:
        department_form = LaboratorioAltriDipartimentiForm(data=request.POST)
        if department_form.is_valid() and department_form.cleaned_data.get('choosen_department'):
            
            laboratory = get_object_or_404(LaboratorioDatiBase, pk=code)
            department = get_object_or_404(DidatticaDipartimento, pk=department_form.cleaned_data['choosen_department'])

            if department.dip_id == laboratory.id_dipartimento_riferimento_id:
                messages.add_message(request, messages.ERROR, _("Extra departments must be different from Laboratory's department"))
            else:
                LaboratorioAltriDipartimenti.objects.create(
                    id_laboratorio_dati=laboratory,
                    id_dip=department,
                    descr_dip_lab=department.dip_nome_breve
                )

                log_action(user=request.user,
                obj=laboratory,
                flag=ADDITION,
                msg=f'{_("Added extra department")}')

                messages.add_message(request, messages.SUCCESS, _("Extra department added successfully"))
                return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_extra_departments_new', kwargs={'code': code}): _('Extra Department')
                   }
    department_data = None
    return render(request,
                  'laboratory_department.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': department_form,
                   'laboratory': laboratory,
                   'choosen_department': department_data,
                   'url': reverse('ricerca:departmentslist')})



@login_required
@can_manage_laboratories
def laboratory_extra_departments_delete(request, code, data_id, laboratory=None):
    """
    elimina un dipartimento extra
    """
    extra_department_lab = get_object_or_404(LaboratorioAltriDipartimenti, pk=data_id)

    extra_department_lab.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted extra department")}')

    messages.add_message(request, messages.SUCCESS, _("Extra department removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_equipment_new(request, code, laboratory=None):
    equipment_form = LaboratorioAttrezzatureForm()
    laboratory = get_object_or_404(LaboratorioDatiBase, pk=code)
    if request.POST:
        equipment_form = LaboratorioAttrezzatureForm(data=request.POST)
        if equipment_form.is_valid():

            laboratory_equipment = equipment_form.save(commit=False)         
            laboratory_equipment.id_laboratorio_dati = laboratory
            laboratory_equipment.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added piece of equipment")}')

            messages.add_message(request, messages.SUCCESS, _("Piece of equipment added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in equipment_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{equipment_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_equipment_new', kwargs={'code': code}): _('Equipment')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': equipment_form,
                   'laboratory': laboratory,
                   'item_label': _("Equipment piece"),
                })


@login_required
@can_manage_laboratories
def laboratory_equipment_edit(request, code, data_id, laboratory=None):
    
    laboratory = get_object_or_404(LaboratorioDatiBase, pk=code)
    laboratory_equipment = get_object_or_404(LaboratorioAttrezzature, pk=data_id)
    equipment_form = LaboratorioAttrezzatureForm(instance=laboratory_equipment)

    if request.POST:
        equipment_form = LaboratorioAttrezzatureForm(instance=laboratory_equipment, data=request.POST)
        if equipment_form.is_valid():
            equipment_form.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited piece of equipment")}')

            messages.add_message(request, messages.SUCCESS, _("Piece of equipment edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in equipment_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{equipment_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_equipment_edit', kwargs={'code': code, 'data_id': data_id}): _('Equipment')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': equipment_form,
                   'laboratory': laboratory,
                   'item_label': _("Equipment Piece"),
                   'edit': 1,
                })


@login_required
@can_manage_laboratories
def laboratory_equipment_delete(request, code, data_id, laboratory=None):
    
    equipment_piece = get_object_or_404(LaboratorioAttrezzature, pk=data_id)

    equipment_piece.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted piece of equipment")}')

    messages.add_message(request, messages.SUCCESS, _("Piece of equipment removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_researches_erc1_edit(request, code, laboratory=None):
    
    #Previously selected researches (needed for request.post logic)
    researches_erc1_old = LaboratorioDatiErc1.objects\
                        .filter(id_laboratorio_dati=code)
    
    #Values passed to the template               
    researches_erc1 = researches_erc1_old.values("id","id_ricerca_erc1","id_ricerca_erc1__descrizione")
    
    #Ids to initialize form's checkboxes (needed for request.post logic)
    researches_erc1_ids = researches_erc1.values_list('id_ricerca_erc1', flat=True)
    researches_erc1_ids = tuple(map(str, researches_erc1_ids))
                        
    research_erc1_form = LaboratorioDatiErc1Form(initial={'id_ricerche_erc1': researches_erc1_ids})
    
    if request.POST:
        research_erc1_form = LaboratorioDatiErc1Form(data=request.POST)
        if research_erc1_form.is_valid():
            researches_erc1_selected = research_erc1_form.cleaned_data.get('id_ricerche_erc1', [])
            
            researches_to_delete = []
            for res in researches_erc1_ids:
                if res not in researches_erc1_selected:
                    researches_to_delete.append(res)
            
            if len(researches_to_delete) > 0:
                researches_erc1_old.filter(id_ricerca_erc1__in=researches_to_delete).delete()
                           
            for res in researches_erc1_selected:
                if res not in researches_erc1_ids:
                    LaboratorioDatiErc1.objects.create(
                        id_laboratorio_dati=laboratory,
                        id_ricerca_erc1=get_object_or_404(RicercaErc1, pk=res)
                    )
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited researches ERC1")}')

            messages.add_message(request, messages.SUCCESS, _("Researches ERC1 edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_researches_erc1_edit', kwargs={'code': code}): _('Researches ERC1')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': research_erc1_form,
                   'laboratory': laboratory,
                   'item_label': _("ERC 1 Researches"),
                   'edit': 1,
                })
    
    
@login_required
@can_manage_laboratories
def laboratory_locations_edit(request, data_id, code, laboratory=None):
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)
    location_form = LaboratorioUbicazioneForm(instance=location)
    
    if request.POST:
        location_form = LaboratorioUbicazioneForm(instance=location, data=request.POST)
        if location_form.is_valid():
           
            location_form.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited laboratory location")}')

            messages.add_message(request, messages.SUCCESS, _("Location edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_locations_edit', kwargs={'code': code, 'data_id': data_id}): _('Location')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': location_form,
                   'item_label': _("location"),
                   'laboratory': laboratory,
                })
    

@login_required
@can_manage_laboratories
def laboratory_locations_new(request, code, laboratory=None):
    location_form = LaboratorioUbicazioneForm()
    if request.POST:
        location_form = LaboratorioUbicazioneForm(data=request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)         
            location.id_laboratorio_dati = laboratory
            location.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added laboratory location")}')

            messages.add_message(request, messages.SUCCESS, _("Location added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in location_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{location_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_locations_new', kwargs={'code': code}): _('Locations')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': location_form,
                   'laboratory': laboratory,
                   'item_label': _("location"),
                   'edit': 1,
                })

@login_required
@can_manage_laboratories
def laboratory_locations_delete(request, code, data_id, laboratory=None):
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)

    location.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted location")}')

    messages.add_message(request, messages.SUCCESS, _("Location removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_research_staff_new(request, code, laboratory=None):
    researcher = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()
    
    if request.POST:
        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            form = ChoosenPersonForm(data=request.POST, required=True)
        else:
            form = LaboratorioPersonaleForm(data=request.POST)
            
        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                researcher_code = decrypt(form.cleaned_data['choosen_person'])
                researcher = get_object_or_404(Personale, matricola=researcher_code)
                LaboratorioPersonaleRicerca.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_ricerca=researcher,
                    cognomenome_origine=f'{researcher.cognome} {researcher.nome}')
            else:
                LaboratorioPersonaleRicerca.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_ricerca=None,
                    cognomenome_origine=form.cleaned_data['laboratory_staff'])

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added laboratory researcher")}')

            messages.add_message(request, messages.SUCCESS, _("Researcher added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_research_staff_new', kwargs={'code': code}): _('Research Staff')
                   }
    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': researcher,
                   'internal_form': internal_form,
                   'external_form': external_form,
                   'item_label': _("Researcher"),
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
def laboratory_research_staff_delete(request, code, data_id, laboratory=None):
    researcher = get_object_or_404(LaboratorioPersonaleRicerca, pk=data_id)
    researcher.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted researcher")}')

    messages.add_message(request, messages.SUCCESS, _("Researcher removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_technical_staff_new(request, code, laboratory=None):
    technician = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()
    technician_form = LaboratorioPersonaleTecnicoForm()
    
    if request.POST:
        technician_form = LaboratorioPersonaleTecnicoForm(request.POST)
        
        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            person_form = ChoosenPersonForm(data=request.POST, required=True)
        else:
            person_form = LaboratorioPersonaleForm(data=request.POST)
            
        if person_form.is_valid() and technician_form.is_valid():

            if person_form.cleaned_data.get('choosen_person'):
                technician_code = decrypt(person_form.cleaned_data['choosen_person'])
                technician = get_object_or_404(Personale, matricola=technician_code)
                LaboratorioPersonaleTecnico.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_tecnico=technician,
                    cognomenome_origine=f'{technician.cognome} {technician.nome}',
                    ruolo=technician_form.cleaned_data.get('ruolo'),
                    field_impegno=technician_form.cleaned_data.get('field_impegno'))
            else:
                LaboratorioPersonaleTecnico.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_tecnico=None,
                    cognomenome_origine=form.cleaned_data['laboratory_staff'],
                    ruolo=technician_form.cleaned_data.get('ruolo'),
                    field_impegno=technician_form.cleaned_data.get('field_impegno'))

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added laboratory technician")}')

            messages.add_message(request, messages.SUCCESS, _("technician added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in person_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{person_form.fields[k].label}</b>: {v}")
            for k, v in technician_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{technician_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_technical_staff_new', kwargs={'code': code}): _('Technical Staff')
                   }
    return render(request,
                  'laboratory_technician.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': technician,
                   'internal_form': internal_form,
                   'external_form': external_form,
                   'form': technician_form,
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
def laboratory_technical_staff_delete(request, code, data_id, laboratory=None):
    technician = get_object_or_404(LaboratorioPersonaleTecnico, pk=data_id)
    technician.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted technician")}')

    messages.add_message(request, messages.SUCCESS, _("Technician removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)

@login_required
@can_manage_laboratories
def laboratory_activities_new(request, code, laboratory=None):
    
    activity_types_already_specified = LaboratorioAttivita\
        .objects\
        .filter(id_laboratorio_dati=code)\
        .values_list("id_tipologia_attivita", flat=True)
        
    if activity_types_already_specified and len(activity_types_already_specified) >= 3:
        messages.add_message(request, messages.ERROR, _("Activities list is full"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified)
    
    if request.POST:
        form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, data=request.POST)
        if form.is_valid():
            activity_type=get_object_or_404(LaboratorioTipologiaAttivita, pk=form.cleaned_data["tipologia_attivita"])
            activity = form.save(commit=False)
            activity.id_laboratorio_dati=laboratory
            activity.id_tipologia_attivita=activity_type
            activity.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added activity")}')

            messages.add_message(request, messages.SUCCESS, _("Activities added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_activities_new', kwargs={'code': code}): _('Activities')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'laboratory': laboratory,
                   'item_label': _("activity"),
                })
    

@login_required
@can_manage_laboratories
def laboratory_activities_edit(request, code, data_id, laboratory=None):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    selected_activity_id = activity.id_tipologia_attivita.id
    selected_activity_type = get_object_or_404(LaboratorioTipologiaAttivita, pk=selected_activity_id)
    
    activity_types_already_specified = LaboratorioAttivita\
        .objects\
        .filter(id_laboratorio_dati=code)\
        .exclude(id_tipologia_attivita=selected_activity_type)\
        .values_list("id_tipologia_attivita", flat=True)
    
    activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, instance=activity, initial={'tipologia_attivita': selected_activity_id})
    
    if request.POST:
        activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, instance=activity, data=request.POST)
        if activity_form.is_valid():
            activity_type = get_object_or_404(LaboratorioTipologiaAttivita, pk=activity_form.cleaned_data["tipologia_attivita"])
            activity = activity_form.save(commit=False)
            activity.id_tipologia_attivita = activity_type
            activity.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited activity")}')

            messages.add_message(request, messages.SUCCESS, _("Activity edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_activities_edit', kwargs={'code': code, "data_id": data_id}): _('Activity')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': activity_form,
                   'laboratory': laboratory,
                   'item_label': _("activity"),
                   'edit': 1,
                })

@login_required
@can_manage_laboratories
def laboratory_activities_delete(request, code, data_id, laboratory=None):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    activity.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted activity")}')

    messages.add_message(request, messages.SUCCESS, _("Activity removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_provided_services_new(request, code, laboratory=None):
    form = LaboratorioServiziErogatiForm()
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioServiziErogatiResponsabileForm()
    manager = None
    if request.POST:
        
        form = LaboratorioServiziErogatiForm(data=request.POST)
        
        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            person_form = ChoosenPersonForm(data=request.POST, required=True)
        else:
            person_form = LaboratorioServiziErogatiResponsabileForm(data=request.POST)
            
        if person_form.is_valid() and form.is_valid():
            
            provided_service = form.save(commit=False)
            provided_service.id_laboratorio_dati = laboratory

            if person_form.cleaned_data.get('choosen_person'):
                manager_code = decrypt(person_form.cleaned_data['choosen_person'])
                manager = get_object_or_404(Personale, matricola=manager_code)
                provided_service.matricola_responsabile = manager_code
                provided_service.responsabile_origine=f'{manager.cognome} {manager.nome}'
            else:
                provided_service.matricola_responsabile = None
                provided_service.responsabile_origine = form.cleaned_data['laboratory_manager']

            provided_service.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Added provided service")}')

            messages.add_message(request, messages.SUCCESS, _("Provided service added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_provided_services_new', kwargs={'code': code}): _('Provided Service')
                   }
    return render(request,
                  'laboratory_provided_service.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'laboratory': laboratory,
                   'choosen_person': manager,
                   'internal_form': internal_form,
                   'external_form': external_form,
                   'url': reverse('ricerca:teacherslist')
                   })
    
    
@login_required
@can_manage_laboratories
def laboratory_provided_services_edit(request, code, data_id, laboratory=None):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    manager = None
    cpf_initial = {}
    lpf_initial = {}
    manager_origine = None
    if(provided_service.matricola_responsabile):
        manager = get_object_or_404(Personale, matricola=provided_service.matricola_responsabile)
        cpf_initial["choosen_person"] = encrypt(provided_service.matricola_responsabile)
        manager_origine = f'{manager.cognome} {manager.nome}'
    else:
        lpf_initial["laboratory_manager"] = provided_service.responsabile_origine
        
    internal_form = ChoosenPersonForm(initial=cpf_initial, required=False)
    external_form = LaboratorioServiziErogatiResponsabileForm(initial=lpf_initial)
    form = LaboratorioServiziErogatiForm(instance=provided_service)

    if request.POST:
        form = LaboratorioServiziErogatiForm(data=request.POST, instance=provided_service)
        
        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            person_form = ChoosenPersonForm(initial=cpf_initial, data=request.POST, required=False)
        else:
            person_form = LaboratorioServiziErogatiResponsabileForm(initial=lpf_initial, data=request.POST)
            
        if person_form.is_valid() and form.is_valid():
            
            provided_service = form.save(commit=False)
            
            if person_form.cleaned_data.get('choosen_person'):
                manager_code = decrypt(person_form.cleaned_data['choosen_person'])
                manager = get_object_or_404(Personale, matricola=manager_code)
                provided_service.matricola_responsabile = manager_code
                provided_service.responsabile_origine=f'{manager.cognome} {manager.nome}'
            elif person_form.cleaned_data.get('laboratory_manager'):
                provided_service.matricola_responsabile = None
                provided_service.responsabile_origine = person_form.cleaned_data['laboratory_manager']

            provided_service.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited provided service")}')

            messages.add_message(request, messages.SUCCESS, _("Provided service edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_provided_services_edit', kwargs={'code': code, 'data_id': data_id}): _('Provided Service')
                   }
    return render(request,
                  'laboratory_provided_service.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'laboratory': laboratory,
                   'choosen_person': manager_origine,
                   'internal_form': internal_form,
                   'external_form': external_form,
                   'provided_service': provided_service,
                   'url': reverse('ricerca:teacherslist')
                   })

@login_required
@can_manage_laboratories
def laboratory_provided_services_delete(request, code, data_id, laboratory=None):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    provided_service.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted provided service")}')

    messages.add_message(request, messages.SUCCESS, _("Provided service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
def laboratory_offered_services_new(request, code, laboratory=None):
    form = LaboratorioServiziOffertiForm()
    if request.POST:
        form = LaboratorioServiziOffertiForm(data=request.POST)
        offered_service = form.save(commit=False)
        offered_service.id_laboratorio_dati = laboratory
        offered_service.save()
        
        log_action(user=request.user,
        obj=laboratory,
        flag=CHANGE,
        msg=f'{_("Added offered service")}')

        messages.add_message(request, messages.SUCCESS, _("Offered service added successfully"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_offered_services_new', kwargs={'code': code}): _('Offered Service')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'item_label': _("offered service"),
                   'laboratory': laboratory,
                   })
    
    
@login_required
@can_manage_laboratories
def laboratory_offered_services_edit(request, code, data_id, laboratory=None):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    form = LaboratorioServiziOffertiForm(instance=offered_service)

    if request.POST:
        form = LaboratorioServiziOffertiForm(data=request.POST, instance=offered_service)
    
        if form.is_valid():
            offered_service = form.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Edited offered service")}')

            messages.add_message(request, messages.SUCCESS, _("Offered service edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
        
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_offered_services_edit', kwargs={'code': code, 'data_id': data_id}): _('Offered Service')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'laboratory': laboratory,
                   'offered_service': offered_service,
                   'item_label': _("offered service"),
                   'edit': True,
                   })

@login_required
@can_manage_laboratories
def laboratory_offered_services_delete(request, code, data_id, laboratory=None):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    offered_service.delete()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted offered service")}')

    messages.add_message(request, messages.SUCCESS, _("Offered service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)