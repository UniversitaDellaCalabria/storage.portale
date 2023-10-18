import logging
import os

from datetime import datetime

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. utils.forms import ChoosenPersonForm

from . decorators import *
from . forms import *
from . settings import *

logger = logging.getLogger(__name__)

def __get_user_roles(user, my_offices, validator_user):
    roles = {
        "superuser": False,
        "operator": False,
        "validator": False
    }
    if user.is_superuser:
        roles["superuser"] = True
        return roles
    if my_offices.exists():
        roles["operator"] = True
    if validator_user:
        roles["validator"] = True
    return roles


@login_required
@can_manage_laboratories
def laboratories(request, laboratory=None, my_offices=None, validator_user=False):
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
@can_edit_laboratories
def laboratory(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    if not laboratory.visibile:
        messages.add_message(request, messages.WARNING, _("Laboratory NOT active"))

    #LaboratorioDatiBase
    form = LaboratorioDatiBaseForm(instance=laboratory)
    #LaboratorioTipologiaRischio
    selected_risks_ids = LaboratorioTipologiaRischio.objects.filter(id_laboratorio_dati=code).values_list("id_tipologia_rischio", flat=True)
    selected_risks_ids = tuple(map(str, selected_risks_ids))
    risk_type_form = LaboratorioTipologiaRischioForm(initial={"tipologie_rischio" : selected_risks_ids})
    #LaboratorioAltriDipartimenti
    extra_departments = LaboratorioAltriDipartimenti.objects.filter(id_laboratorio_dati=code)
    #LaboratorioAttrezzature
    equipment = LaboratorioAttrezzature.objects.filter(id_laboratorio_dati=code)
    #LaboratorioDatiErc1
    researches_erc1 = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code).values("id", "id_ricerca_erc1", "id_ricerca_erc1__descrizione")
    #LaboratorioUbicazione
    locations = LaboratorioUbicazione.objects.filter(id_laboratorio_dati=code)
    #LaboratorioPersonaleRicerca
    researchers = LaboratorioPersonaleRicerca.objects.filter(id_laboratorio_dati=code)
    #LaboratorioPersonaleTecnico
    technicians = LaboratorioPersonaleTecnico.objects.filter(id_laboratorio_dati=code).values("id", "cognomenome_origine")
    #LaboratorioAttivita
    activities = LaboratorioAttivita.objects.filter(id_laboratorio_dati=code).values("id", "id_tipologia_attivita__descrizione")
    #LaboratorioServiziErogati
    provided_services = LaboratorioServiziErogati.objects.filter(id_laboratorio_dati=code).values("id", "descrizione")
    #LaboratorioServiziOfferti
    offered_services = LaboratorioServiziOfferti.objects.filter(id_laboratorio_dati=code).values("id", "nome_servizio")

    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioDatiBaseForm(instance=laboratory, data=request.POST, files=request.FILES)
                
        if form.is_valid():
            form.save(commit=False)
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()    

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

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
                   'logs': logs,
                   'form': form,
                   'risk_type_form': risk_type_form,
                   'laboratory': laboratory,
                   'extra_departments': extra_departments,
                   'laboratory_equipment': equipment,
                   'researches_erc1': researches_erc1,
                   'locations': locations,
                   'researchers': researchers,
                   'technicians': technicians,
                   'activities': activities,
                   'provided_services': provided_services,
                   'offered_services': offered_services,
                   'user_roles' : __get_user_roles(request.user, my_offices, validator_user)
                   })     
        

@login_required
@can_manage_laboratories
def laboratory_new(request, laboratory=None, my_offices=None, validator_user=False):
    #new
    form = LaboratorioDatiBaseForm()
    department_form = LaboratorioDatiBaseDipartimentoForm()

    # unical_referent_internal_form = LaboratorioDatiBaseUnicalReferentChoosenPersonForm(required=True)
    # unical_referent_external_form = LaboratorioDatiBaseUnicalReferentForm()

    scientific_director_internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(required=True)
    scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                       dip_id=request.POST['choosen_department'])

    unical_referent = None
    scientific_director = None

    # if request.POST.get(UNICAL_REFERENT_ID, ''):
    #     unical_referent = get_object_or_404(Personale, matricola=(decrypt(request.POST[UNICAL_REFERENT_ID])))

    if request.POST.get("choosen_scientific_director", ''):
        scientific_director = get_object_or_404(Personale, matricola=(decrypt(request.POST["choosen_scientific_director"])))
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioDatiBaseForm(data=request.POST, files=request.FILES)
        department_form = LaboratorioDatiBaseDipartimentoForm(data=request.POST)
        
        # if UNICAL_REFERENT_ID in request.POST and request.POST[UNICAL_REFERENT_ID]:
        #     unical_referent_form = LaboratorioDatiBaseUnicalReferentChoosenPersonForm(data=request.POST, required=True) 
        # else:
        #     unical_referent_form = LaboratorioDatiBaseUnicalReferentForm(data=request.POST)

        if "choosen_scientific_director" in request.POST and request.POST["choosen_scientific_director"]:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(data=request.POST, required=True) 
        else:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorForm(data=request.POST)
                    
        if form.is_valid() and department_form.is_valid() and scientific_director_form.is_valid(): #and unical_referent_form.is_valid()
            laboratory = form.save(commit=False)

            #unical referent
            # if unical_referent_form.cleaned_data.get(UNICAL_REFERENT_ID):
            #     unical_referent_code = decrypt(unical_referent_form.cleaned_data[UNICAL_REFERENT_ID])
            #     unical_referent = get_object_or_404(Personale, matricola=unical_referent_code)
            #     laboratory.matricola_referente_compilazione = unical_referent
            #     laboratory.referente_compilazione = f'{unical_referent.cognome} {unical_referent.nome}'
            #     laboratory.email_compilazione = unical_referent.email
            # else:
            #     laboratory.matricola_referente_compilazione = None
            #     laboratory.referente_compilazione = unical_referent_form.cleaned_data['referente_compilazione']
            #     laboratory.email_compilazione = unical_referent_form.cleaned_data['email_compilazione']
            #scientific director
            if scientific_director_form.cleaned_data.get("choosen_scientific_director"):
                scientific_director_code = decrypt(scientific_director_form.cleaned_data["choosen_scientific_director"])
                scientific_director = get_object_or_404(Personale, matricola=scientific_director_code)
                laboratory.matricola_responsabile_scientifico = scientific_director
                laboratory.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
            else:
                laboratory.matricola_responsabile_scientifico = None
                laboratory.responsabile_scientifico = scientific_director_form.cleaned_data['responsabile_scientifico']
            
            #department
            laboratory.dipartimento_riferimento = department.dip_des_it
            laboratory.id_dipartimento_riferimento = department


            laboratory.dt_sottomissione = datetime.now()
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
            log_action(user=request.user,
                       obj=laboratory,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request, messages.SUCCESS, _("Laboratory anagraphic created successfully, please fill in the other fields"))
            return redirect("crud_laboratories:crud_laboratory_edit", code=laboratory.pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")
            # for k, v in unical_referent_form.errors.items():
            #     messages.add_message(request, messages.ERROR,
            #                          f"<b>{unical_referent_form.fields[k].label}</b>: {v}")
            for k, v in scientific_director_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{scientific_director_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   '#': _('New')}
    return render(request,
                    'laboratory_new.html',
                    {'breadcrumbs': breadcrumbs,
                    'url': reverse('ricerca:teacherslist'),
                    'form': form,
                    'departments_api': reverse('ricerca:departmentslist'),
                    'teachers_api': reverse('ricerca:teacherslist'),
                    'department_form': department_form,
                    # 'unical_referent_label' : UNICAL_REFERENT_ID,
                    # 'unical_referent_internal_form': unical_referent_internal_form,
                    # 'unical_referent_external_form': unical_referent_external_form,
                    'scientific_director_label' : "choosen_scientific_director",
                    'scientific_director_internal_form': scientific_director_internal_form,
                    'scientific_director_external_form': scientific_director_external_form,
                    })

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_unical_department_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    department = laboratory.id_dipartimento_riferimento
    old_label = department.dip_des_it
    
    form = LaboratorioDatiBaseDipartimentoForm(initial={'choosen_department': department.dip_id})

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioDatiBaseDipartimentoForm(data=request.POST)
        if form.is_valid():

            department_id = form.cleaned_data['choosen_department']
            department = get_object_or_404(DidatticaDipartimento, dip_id=department_id)
            laboratory.id_dipartimento_riferimento = department
            laboratory.dipartimento_riferimento = f'{department.dip_des_it}'
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

            if old_label != department.dip_des_it:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito dipartimento {old_label} con {department.dip_des_it}')


            messages.add_message(request, messages.SUCCESS, _("Department edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)
        
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
                   'url': reverse('ricerca:departmentslist'),
                   'form': form,
                   'laboratory': laboratory,
                   'choosen_department': old_label,
                   })

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_unical_referent_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    unical_referent = None
    unical_referent_ecode = None
    old_label = None
    initial = {}
    if laboratory.matricola_referente_compilazione:
        unical_referent = laboratory.matricola_referente_compilazione
        old_label = f'{unical_referent.cognome} {unical_referent.nome}'
        unical_referent_ecode = encrypt(unical_referent.matricola)
        initial = {'choosen_person': unical_referent_ecode}
    
    else:
        old_label = laboratory.referente_compilazione
        initial = {'referente_compilazione': old_label}

    external_form = LaboratorioDatiBaseUnicalReferentForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseUnicalReferentForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            
            if form.cleaned_data.get('choosen_person'):
                unical_referent = get_object_or_404(Personale, matricola=decrypt(form.cleaned_data['choosen_person']))
                laboratory.matricola_referente_compilazione = unical_referent
                laboratory.referente_compilazione = f'{unical_referent.cognome} {unical_referent.nome}'
                laboratory.email_compilazione = unical_referent.email
            else:
                laboratory.matricola_referente_compilazione = None
                laboratory.referente_compilazione = form.cleaned_data['referente_compilazione']
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

            if old_label != laboratory.referente_compilazione:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito referente unical {old_label} con {laboratory.referente_compilazione}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory unical referent edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_unical_referent_edit', kwargs={'code': code}): _('Unical Referent')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': old_label,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Unical Referent"),
                   'edit': 1,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_scientific_director_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    scientific_director = None
    scientific_director_ecode = None
    old_label = None
    initial = {}
    if laboratory.matricola_responsabile_scientifico:
        scientific_director = laboratory.matricola_responsabile_scientifico
        old_label = f'{scientific_director.cognome} {scientific_director.nome}'
        scientific_director_ecode = encrypt(scientific_director.matricola)
        initial = {'choosen_person': scientific_director_ecode}
    
    else:
        old_label = laboratory.responsabile_scientifico
        initial = {'responsabile_scientifico': old_label}

    external_form = LaboratorioDatiBaseScientificDirectorForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseScientificDirectorForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            
            if form.cleaned_data.get('choosen_person'):
                scientific_director = get_object_or_404(Personale, matricola=decrypt(form.cleaned_data['choosen_person']))
                laboratory.matricola_responsabile_scientifico = scientific_director
                laboratory.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
            else:
                laboratory.matricola_responsabile_scientifico = None
                laboratory.responsabile_scientifico = form.cleaned_data['responsabile_scientifico']
                
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

            if old_label != laboratory.responsabile_scientifico:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito responsabile scientifico {old_label} con {laboratory.responsabile_scientifico}')

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
                   reverse('crud_laboratories:crud_laboratory_scientific_director_edit', kwargs={'code': code }): _('Scientific Director')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': old_label,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Scientific Director"),
                   'edit': 1,
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_safety_manager_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    safety_manager = None
    safety_manager_ecode = None
    old_label = None
    initial = {}
    if laboratory.matricola_preposto_sicurezza:
        safety_manager = laboratory.matricola_preposto_sicurezza
        old_label = f'{safety_manager.cognome} {safety_manager.nome}'
        safety_manager_ecode = encrypt(safety_manager.matricola)
        initial = {'choosen_person': safety_manager_ecode}
    
    else:
        old_label = laboratory.preposto_sicurezza
        initial = {'preposto_sicurezza': old_label}

    external_form = LaboratorioDatiBaseSafetyManagerForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseSafetyManagerForm(data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            
            if form.cleaned_data.get('choosen_person'):
                safety_manager = get_object_or_404(Personale, matricola=decrypt(form.cleaned_data['choosen_person']))
                laboratory.matricola_preposto_sicurezza = safety_manager
                laboratory.preposto_sicurezza = f'{safety_manager.cognome} {safety_manager.nome}'
                laboratory.email_compilazione = safety_manager.email
            else:
                laboratory.matricola_preposto_sicurezza = None
                laboratory.preposto_sicurezza = form.cleaned_data['preposto_sicurezza']
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

            if old_label != laboratory.referente_compilazione:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito preposto sicurezza {old_label} con {laboratory.preposto_sicurezza}')

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
                   reverse('crud_laboratories:crud_laboratory_safety_manager_edit', kwargs={'code': code}): _('Safety Manager')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': old_label,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Safety Manager"),
                   'edit': 1,
                   'url': reverse('ricerca:teacherslist')})
    
@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_safety_manager_delete(request, code, laboratory=None, my_offices=None, validator_user=False):

    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    laboratory.matricola_preposto_sicurezza = None
    laboratory.preposto_sicurezza = None
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted safety manager")}')

    messages.add_message(request, messages.SUCCESS, _("Safety manager removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@check_if_superuser
@can_manage_laboratories
def laboratory_delete(request, code, laboratory=None, my_offices=None, validator_user=False):
    laboratory.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Laboratory removed successfully"))

    return redirect('crud_laboratories:crud_laboratories')


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_extra_departments_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    department_form = LaboratorioAltriDipartimentiForm()
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        department_form = LaboratorioAltriDipartimentiForm(data=request.POST)
        if department_form.is_valid() and department_form.cleaned_data.get('choosen_department'):
            
            department = get_object_or_404(DidatticaDipartimento, pk=department_form.cleaned_data['choosen_department'])

            if department.dip_id == laboratory.id_dipartimento_riferimento_id:
                messages.add_message(request, messages.ERROR, _("Extra departments must be different from Laboratory's department"))
            else:
                LaboratorioAltriDipartimenti.objects.create(
                    id_laboratorio_dati=laboratory,
                    id_dip=department,
                    descr_dip_lab=department.dip_nome_breve
                )
                
                laboratory.user_mod_id = request.user
                laboratory.dt_mod=datetime.now()
                laboratory.visibile=False
                laboratory.save()

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
@can_edit_laboratories
def laboratory_extra_departments_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    extra_department_lab = get_object_or_404(LaboratorioAltriDipartimenti, pk=data_id)

    extra_department_lab.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted extra department")}')

    messages.add_message(request, messages.SUCCESS, _("Extra department removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_equipment_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    equipment_form = LaboratorioAttrezzatureForm()
    equipment_funds_form = LaboratorioAttrezzatureFondiForm()
    equipment_risks_form = LaboratorioAttrezzatureRischiForm()
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        equipment_form = LaboratorioAttrezzatureForm(data=request.POST)
        equipment_funds_form = LaboratorioAttrezzatureFondiForm(data=request.POST)
        equipment_risks_form = LaboratorioAttrezzatureRischiForm(data=request.POST)
        
        if equipment_form.is_valid() and equipment_funds_form.is_valid() and equipment_risks_form.is_valid():

            laboratory_equipment = equipment_form.save(commit=False)
            laboratory_equipment.id_laboratorio_dati = laboratory
            laboratory_equipment.save()
            
            for fund_id in equipment_funds_form.cleaned_data.get('id_laboratorio_fondo', []):
                LaboratorioAttrezzatureFondi.objects.create(
                    id_laboratorio_attrezzature=laboratory_equipment,
                    id_laboratorio_fondo=get_object_or_404(LaboratorioFondo, pk=fund_id),
                    user_mod_id=request.user,
                    dt_mod=datetime.now()
                )
            
            for risk_id in equipment_risks_form.cleaned_data.get('id_tipologia_rischio', []):
                LaboratorioAttrezzatureRischi.objects.create(
                    id_laboratorio_attrezzature=laboratory_equipment,
                    id_tipologia_rischio=get_object_or_404(TipologiaRischio, pk=risk_id),
                    user_mod_id=request.user,
                    dt_mod=datetime.now()
                )
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

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
            for k, v in equipment_funds_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{equipment_funds_form.fields[k].label}</b>: {v}")
            for k, v in equipment_risks_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{equipment_risks_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_equipment_new', kwargs={'code': code}): _('Equipment')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'forms': (equipment_form, equipment_funds_form, equipment_risks_form,),
                   'laboratory': laboratory,
                   'item_label': _("Equipment piece"),
                })


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_equipment_edit(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    laboratory_equipment = get_object_or_404(LaboratorioAttrezzature, pk=data_id)
    equipment_form = LaboratorioAttrezzatureForm(instance=laboratory_equipment)
    
    selected_funds_ids = LaboratorioAttrezzatureFondi.objects.filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_laboratorio_fondo", flat=True)
    selected_funds_ids = tuple(map(str, selected_funds_ids))
    equipment_funds_form = LaboratorioAttrezzatureFondiForm(initial={"id_laboratorio_fondo" : selected_funds_ids})
    
    selected_risks_ids = LaboratorioAttrezzatureRischi.objects.filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_tipologia_rischio", flat=True)
    selected_risks_ids = tuple(map(str, selected_risks_ids))
    equipment_risks_form = LaboratorioAttrezzatureRischiForm(initial={"id_tipologia_rischio" : selected_risks_ids})

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        equipment_form = LaboratorioAttrezzatureForm(instance=laboratory_equipment, data=request.POST)
        equipment_funds_form = LaboratorioAttrezzatureFondiForm(data=request.POST)
        equipment_risks_form = LaboratorioAttrezzatureRischiForm(data=request.POST)
        
        if equipment_form.is_valid() and equipment_funds_form.is_valid() and equipment_risks_form.is_valid():
            
            laboratory_equipment = equipment_form.save()
            
            #LaboratorioAttrezzatureFondi
            new_selected_funds = equipment_funds_form.cleaned_data.get("id_laboratorio_fondo", [])
            
            LaboratorioAttrezzatureFondi.objects\
                .filter(id_laboratorio_attrezzature=laboratory_equipment.id)\
                .exclude(id_laboratorio_fondo__in=new_selected_funds)\
                .delete()
            
            current_funds = LaboratorioAttrezzatureFondi.objects\
                .filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_laboratorio_fondo", flat=True)
            current_funds = map(str, current_funds)
                
            #for all (new_selected_funds - current_funds) create
            funds_id = list(set(new_selected_funds) - set(current_funds))
            funds = LaboratorioFondo.objects.filter(id__in=funds_id)
                     
            for fund in funds:
                LaboratorioAttrezzatureFondi.objects.create(
                    id_laboratorio_attrezzature=laboratory_equipment,
                    id_laboratorio_fondo=fund,
                    user_mod_id=request.user,
                    dt_mod=datetime.now()
                )
            
            
            #LaboratorioAttrezzatureRischi
            new_selected_risks = equipment_risks_form.cleaned_data.get("id_tipologia_rischio", [])
            
            LaboratorioAttrezzatureRischi.objects\
                .filter(id_laboratorio_attrezzature=laboratory_equipment.id)\
                .exclude(id_tipologia_rischio__in=new_selected_risks)\
                .delete()
            
            current_risks = LaboratorioAttrezzatureRischi.objects\
                .filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_tipologia_rischio", flat=True)
            current_risks = map(str, current_risks)
                
            #for all (new_selected_risks - current_risks) create
            risk_types_id = list(set(new_selected_risks) - set(current_risks))
            risk_types = TipologiaRischio.objects.filter(id__in=risk_types_id)
                     
            for risk_type in risk_types:
                LaboratorioAttrezzatureRischi.objects.create(
                    id_laboratorio_attrezzature=laboratory_equipment,
                    id_tipologia_rischio=risk_type,
                    user_mod_id=request.user,
                    dt_mod=datetime.now()
                )
                
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

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
            for k, v in equipment_funds_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                    f"<b>{equipment_funds_form.fields[k].label}</b>: {v}")
            
            for k, v in equipment_risks_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{equipment_risks_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_equipment_edit', kwargs={'code': code, 'data_id': data_id}): _('Equipment')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'forms': (equipment_form, equipment_funds_form, equipment_risks_form,),
                   'laboratory': laboratory,
                   'item_label': _("Equipment Piece"),
                   'edit': 1,
                })


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_equipment_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    equipment_piece = get_object_or_404(LaboratorioAttrezzature, pk=data_id)

    equipment_piece.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted piece of equipment")}')

    messages.add_message(request, messages.SUCCESS, _("Piece of equipment removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_researches_erc1_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    #Previously selected researches
    researches_erc1_old = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code)
    
    #Ids to initialize form's checkboxes
    researches_erc1 = researches_erc1_old.values("id","id_ricerca_erc1","id_ricerca_erc1__descrizione")
    researches_erc1_ids = researches_erc1.values_list('id_ricerca_erc1', flat=True)
    researches_erc1_ids = tuple(map(str, researches_erc1_ids))
                        
    research_erc1_form = LaboratorioDatiErc1Form(initial={'id_ricerche_erc1': researches_erc1_ids})
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        research_erc1_form = LaboratorioDatiErc1Form(data=request.POST)
        if research_erc1_form.is_valid():
            
            selected_erc1_res_ids = research_erc1_form.cleaned_data.get('id_ricerche_erc1', [])
                        
            LaboratorioDatiErc1.objects\
                .filter(id_laboratorio_dati=code)\
                .exclude(id_ricerca_erc1__in=selected_erc1_res_ids)\
                .delete()
                
            current_erc1_res_ids = LaboratorioDatiErc1.objects\
                .filter(id_laboratorio_dati=code).values_list("id_ricerca_erc1", flat=True)
            current_erc1_res_ids = map(str, current_erc1_res_ids)
                
            current_erc1_res = list(set(selected_erc1_res_ids) - set(current_erc1_res_ids))
            erc1_researches = RicercaErc1.objects.filter(id__in=current_erc1_res)
            
            for research in erc1_researches:
                LaboratorioDatiErc1.objects.create(
                    id_laboratorio_dati=laboratory,
                    id_ricerca_erc1=research
                )
                
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()        
            
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
                   'forms': (research_erc1_form,),
                   'laboratory': laboratory,
                   'item_label': _("ERC 1 Researches"),
                   'edit': 1,
                })
    
    
@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_locations_edit(request, data_id, code, laboratory=None, my_offices=None, validator_user=False):
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)
    location_form = LaboratorioUbicazioneForm(instance=location)
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        location_form = LaboratorioUbicazioneForm(instance=location, data=request.POST)
        if location_form.is_valid():
           
            location_form.save()
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
                   'forms': (location_form,),
                   'item_label': _("location"),
                   'laboratory': laboratory,
                })
    

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_locations_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    location_form = LaboratorioUbicazioneForm()
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        location_form = LaboratorioUbicazioneForm(data=request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)         
            location.id_laboratorio_dati = laboratory
            location.save()
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

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
                   'forms': (location_form,),
                   'laboratory': laboratory,
                   'item_label': _("location"),
                   'edit': 1,
                })

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_locations_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)

    location.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted location")}')

    messages.add_message(request, messages.SUCCESS, _("Location removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_research_staff_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    researcher = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
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

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

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
@can_edit_laboratories
def laboratory_research_staff_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    researcher = get_object_or_404(LaboratorioPersonaleRicerca, pk=data_id)
    researcher.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted researcher")}')

    messages.add_message(request, messages.SUCCESS, _("Researcher removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_technical_staff_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    technician = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()
    technician_form = LaboratorioPersonaleTecnicoForm()
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
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
                    percentuale_impegno=technician_form.cleaned_data.get('percentuale_impegno'))
            else:
                LaboratorioPersonaleTecnico.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_tecnico=None,
                    cognomenome_origine=person_form.cleaned_data.get('laboratory_staff'),
                    ruolo=technician_form.cleaned_data.get('ruolo'),
                    percentuale_impegno=technician_form.cleaned_data.get('percentuale_impegno'))

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()

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
@can_edit_laboratories
def laboratory_technical_staff_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    technician = get_object_or_404(LaboratorioPersonaleTecnico, pk=data_id)
    technician.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted technician")}')

    messages.add_message(request, messages.SUCCESS, _("Technician removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_activities_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    activity_types_already_specified = LaboratorioAttivita\
        .objects\
        .filter(id_laboratorio_dati=code)\
        .values_list("id_tipologia_attivita", flat=True)
        
    if activity_types_already_specified and len(activity_types_already_specified) >= 3:
        messages.add_message(request, messages.ERROR, _("Activities list is full"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)
    
    form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified)
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, data=request.POST)
        if form.is_valid():
            activity_type=get_object_or_404(LaboratorioTipologiaAttivita, pk=form.cleaned_data["tipologia_attivita"])
            activity = form.save(commit=False)
            activity.id_laboratorio_dati=laboratory
            activity.id_tipologia_attivita=activity_type
            activity.save()
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
                   'forms': (form,),
                   'laboratory': laboratory,
                   'item_label': _("activity"),
                })
    

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_activities_edit(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    selected_activity_id = activity.id_tipologia_attivita.id
    selected_activity_type = get_object_or_404(LaboratorioTipologiaAttivita, pk=selected_activity_id)
    
    activity_types_already_specified = LaboratorioAttivita\
        .objects\
        .filter(id_laboratorio_dati=code)\
        .exclude(id_tipologia_attivita=selected_activity_type)\
        .values_list("id_tipologia_attivita", flat=True)
    
    activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, instance=activity, initial={'tipologia_attivita': selected_activity_id})
    
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, instance=activity, data=request.POST)
        if activity_form.is_valid():
            activity_type = get_object_or_404(LaboratorioTipologiaAttivita, pk=activity_form.cleaned_data["tipologia_attivita"])
            activity = activity_form.save(commit=False)
            activity.id_tipologia_attivita = activity_type
            activity.save()
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
                   'forms': (activity_form,),
                   'laboratory': laboratory,
                   'item_label': _("activity"),
                   'edit': 1,
                })

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_activities_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    activity.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted activity")}')

    messages.add_message(request, messages.SUCCESS, _("Activity removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_provided_services_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    form = LaboratorioServiziErogatiForm()
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioServiziErogatiResponsabileForm()
    manager = None
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        
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
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
@can_edit_laboratories
def laboratory_provided_services_edit(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
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

    if request.POST and (request.user.is_superuser or my_offices.exists()):
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
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
@can_edit_laboratories
def laboratory_provided_services_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    provided_service.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted provided service")}')

    messages.add_message(request, messages.SUCCESS, _("Provided service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_offered_services_new(request, code, laboratory=None, my_offices=None, validator_user=False):
    form = LaboratorioServiziOffertiForm()
    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioServiziOffertiForm(data=request.POST)
        offered_service = form.save(commit=False)
        offered_service.id_laboratorio_dati = laboratory
        offered_service.save()
        
        laboratory.user_mod_id = request.user
        laboratory.dt_mod=datetime.now()
        laboratory.visibile=False
        laboratory.save()
        
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
                   'forms': (form,),
                   'item_label': _("offered service"),
                   'laboratory': laboratory,
                   })
    
    
@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_offered_services_edit(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    form = LaboratorioServiziOffertiForm(instance=offered_service)

    if request.POST and (request.user.is_superuser or my_offices.exists()):
        form = LaboratorioServiziOffertiForm(data=request.POST, instance=offered_service)
    
        if form.is_valid():
            offered_service = form.save()
            
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
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
                   'forms': (form,),
                   'laboratory': laboratory,
                   'offered_service': offered_service,
                   'item_label': _("offered service"),
                   'edit': True,
                   })

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_offered_services_delete(request, code, data_id, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    offered_service.delete()
    
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.now()
    laboratory.visibile=False
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Deleted offered service")}')

    messages.add_message(request, messages.SUCCESS, _("Offered service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_risk_types_edit(request, code, laboratory=None, my_offices=None, validator_user=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    if request.POST:
        risk_type_form = LaboratorioTipologiaRischioForm(data=request.POST)
        
        if risk_type_form.is_valid():

            #LaboratorioTipologiaRischio
            new_selected_risks = risk_type_form.cleaned_data.get("tipologie_rischio", [])
            
            LaboratorioTipologiaRischio.objects\
                .filter(id_laboratorio_dati=code)\
                .exclude(id_tipologia_rischio__in=new_selected_risks)\
                .delete()
            
            current_risks = LaboratorioTipologiaRischio.objects\
                .filter(id_laboratorio_dati=code).values_list("id_tipologia_rischio", flat=True)
            current_risks = map(str, current_risks)
                
            #for all (new_selected_risks - current_risks) create
            risk_types_id = list(set(new_selected_risks) - set(current_risks))
            risk_types = TipologiaRischio.objects.filter(id__in=risk_types_id)
            
            for rt in risk_types:
                LaboratorioTipologiaRischio.objects.create(
                    id_laboratorio_dati=laboratory,
                    id_tipologia_rischio=rt
                )
                
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.now()
            laboratory.visibile=False
            laboratory.save()
            
            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=f'{_("Risk types updated")}')
        
            messages.add_message(request, messages.SUCCESS, _("Risk types updated successfully"))
        else:  # pragma: no cover
            for k, v in risk_type_form.errors.items():
                messages.add_message(request, messages.ERROR, f"<b>{risk_type_form.fields[k].label}</b>: {v}")
                
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_request_approval(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    # #LaboratorioTipologiaRischio
    # selected_risks_ids = LaboratorioTipologiaRischio.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioAltriDipartimenti
    # extra_departments = LaboratorioAltriDipartimenti.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioAttrezzature
    # equipment = LaboratorioAttrezzature.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioDatiErc1
    # researches_erc1 = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioUbicazione
    # locations = LaboratorioUbicazione.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioPersonaleRicerca
    # researchers = LaboratorioPersonaleRicerca.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioPersonaleTecnico
    # technicians = LaboratorioPersonaleTecnico.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioAttivita
    # activities = LaboratorioAttivita.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioServiziErogati
    # provided_services = LaboratorioServiziErogati.objects.filter(id_laboratorio_dati=code).exists()
    # #LaboratorioServiziOfferti
    # offered_services = Laboratonot (request.user.is_superuser or my_offices.exists()):rioServiziOfferti.objects.filter(id_laboratorio_dati=code).exists()
    
    
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))
    
    send_mail(
        TO_VALIDATORS_EMAIL_SUBJECT,
        f"{TO_VALIDATORS_EMAIL_MESSAGE} {laboratory.nome_laboratorio}",
        TO_VALIDATORS_EMAIL_FROM,
        [],
        fail_silently=True,
    )
    
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Requested approval")}')
    
    messages.add_message(request, messages.SUCCESS, _("Request for approval sent successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)

@login_required
@can_manage_laboratories
@can_edit_laboratories
def laboratory_approve(request, code, laboratory=None, my_offices=None, validator_user=False):
    
    if not (request.user.is_superuser or user_validator):
        return custom_message(request, _("Permission denied"))
    
    laboratory.visibile = True
    laboratory.save()
    
    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=f'{_("Approved Laboratory")}')
    
    messages.add_message(request, messages.SUCCESS, _("Laboratory approved successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)