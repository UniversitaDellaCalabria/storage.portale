import datetime
import logging
import os

from .. utils.utils import log_action
from .. utils.utils import custom_message
from .. utils.forms import ChoosenPersonForm

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt


from . decorators import *
from . decorators import _is_user_scientific_director
from . forms import *
from . settings import *

logger = logging.getLogger(__name__)

def __get_user_roles(request, laboratory, my_offices, is_validator):
    roles = {
        "superuser": False,
        "operator": False,
        "validator": False
    }
    if request.user.is_superuser:
        roles["superuser"] = True
        return roles
    if my_offices.exists() or _is_user_scientific_director(request, laboratory):
        roles["operator"] = True
    if is_validator:
        roles["validator"] = True
    return roles


@login_required
@can_manage_laboratories
def laboratories(request, laboratory=None, my_offices=None, is_validator=False):
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
@can_view_laboratories
def laboratory_info_sede_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
    if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))
    if request.POST:
        laboratoriodatibaseinfosedestruttureform = LaboratorioDatiBaseInfoSedeStruttureForm(data=request.POST, instance=laboratory)
        if laboratoriodatibaseinfosedestruttureform.is_valid():
            lab_instance = laboratoriodatibaseinfosedestruttureform.save(commit=False)
            lab_instance.user_mod_id = request.user
            lab_instance.dt_mod=datetime.datetime.now()
            lab_instance.visibile=False
            lab_instance.save(update_fields=['sede_note_descrittive', 'sede_dimensione', 'strumentazione_descrizione', 'visibile', 'user_mod_id', 'dt_mod'])

            if laboratoriodatibaseinfosedestruttureform.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(laboratoriodatibaseinfosedestruttureform,
                                                                        laboratoriodatibaseinfosedestruttureform.changed_data)
                log_action(user=request.user,
                            obj=laboratory,
                            flag=CHANGE,
                            msg=[{'changed': {"fields": changed_field_labels}}])

                messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Laboratory edited successfully"))

        else:  # pragma: no cover
            for k, v in laboratoriodatibaseinfosedestruttureform.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{laboratoriodatibaseinfosedestruttureform.fields[k].label}</b>: {v}")

            request.session["lab_infosedestrutture_form_data"] = laboratoriodatibaseinfosedestruttureform.data

    return redirect(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}) + "#facilities_equipment")



@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_scope_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
    if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))
    if request.POST:
        laboratoriodatibaseambitoform = LaboratorioDatiBaseAmbitoForm(data=request.POST, instance=laboratory)
        if laboratoriodatibaseambitoform.is_valid():
            lab_instance = laboratoriodatibaseambitoform.save(commit=False)
            lab_instance.user_mod_id = request.user
            lab_instance.dt_mod=datetime.datetime.now()
            lab_instance.visibile=False
            lab_instance.save(update_fields=['ambito', 'visibile', 'user_mod_id', 'dt_mod'])

            if laboratoriodatibaseambitoform.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(laboratoriodatibaseambitoform,
                                                                        laboratoriodatibaseambitoform.changed_data)
                log_action(user=request.user,
                            obj=laboratory,
                            flag=CHANGE,
                            msg=[{'changed': {"fields": changed_field_labels}}])

                messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Laboratory edited successfully"))

        else:  # pragma: no cover
            for k, v in laboratoriodatibaseambitoform.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{laboratoriodatibaseambitoform.fields[k].label}</b>: {v}")

            request.session["lab_ambito_form_data"] = laboratoriodatibaseambitoform.data

    return redirect(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}) + "#scope")


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_equipment_value_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
    if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))
    if request.POST:
        laboratoriodatibasestrumentazionevaloreform = LaboratorioDatiBaseStrumentazioneValoreForm(data=request.POST, instance=laboratory)
        if laboratoriodatibasestrumentazionevaloreform.is_valid():
            lab_instance = laboratoriodatibasestrumentazionevaloreform.save(commit=False)
            lab_instance.user_mod_id = request.user
            lab_instance.dt_mod=datetime.datetime.now()
            lab_instance.visibile=False
            lab_instance.save(update_fields=['strumentazione_valore', 'visibile', 'user_mod_id', 'dt_mod'])

            if laboratoriodatibasestrumentazionevaloreform.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(laboratoriodatibasestrumentazionevaloreform,
                                                                        laboratoriodatibasestrumentazionevaloreform.changed_data)
                log_action(user=request.user,
                            obj=laboratory,
                            flag=CHANGE,
                            msg=[{'changed': {"fields": changed_field_labels}}])

                messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Laboratory edited successfully"))

        else:  # pragma: no cover
            for k, v in laboratoriodatibasestrumentazionevaloreform.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{laboratoriodatibasestrumentazionevaloreform.fields[k].label}</b>: {v}")

            request.session["lab_strumentazionevalore_form_data"] = laboratoriodatibasestrumentazionevaloreform.data

    return redirect(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}) + "#equipment_value")


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_interdepartmental_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
    if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))
    if request.POST:
        laboratoriodatibaseinterdipartimentaleform = LaboratorioDatiBaseInterdipartimentaleForm(data=request.POST, instance=laboratory)
        if laboratoriodatibaseinterdipartimentaleform.is_valid():

            if request.POST.get("laboratorio_interdipartimentale") == "NO":
                LaboratorioAltriDipartimenti.objects.filter(id_laboratorio_dati=code).delete()

            lab_instance = laboratoriodatibaseinterdipartimentaleform.save(commit=False)
            lab_instance.user_mod_id = request.user
            lab_instance.dt_mod=datetime.datetime.now()
            lab_instance.visibile=False
            lab_instance.save(update_fields=['laboratorio_interdipartimentale', 'visibile', 'user_mod_id', 'dt_mod'])

            if laboratoriodatibaseinterdipartimentaleform.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(laboratoriodatibaseinterdipartimentaleform,
                                                                        laboratoriodatibaseinterdipartimentaleform.changed_data)
                log_action(user=request.user,
                            obj=laboratory,
                            flag=CHANGE,
                            msg=[{'changed': {"fields": changed_field_labels}}])

                messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Laboratory edited successfully"))

        else:  # pragma: no cover
            for k, v in laboratoriodatibaseinterdipartimentaleform.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{laboratoriodatibaseinterdipartimentaleform.fields[k].label}</b>: {v}")

            request.session["lab_interdipartimentale_form_data"] = laboratoriodatibaseinterdipartimentaleform.data

    return redirect(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}) + "#extra_department")



@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory(request, code, laboratory=None, my_offices=None, is_validator=False):

    if not laboratory.visibile and not request.POST:
        messages.add_message(request, messages.WARNING, _("Laboratory NOT visible"))

    lab_infosedestrutture_form_data = request.session.pop('lab_infosedestrutture_form_data', None)
    lab_ambito_form_data = request.session.pop('lab_ambito_form_data', None)
    lab_strumentazionevalore_form_data = request.session.pop('lab_strumentazionevalore_form_data', None)
    lab_interdipartimentale_form_data = request.session.pop('lab_interdipartimentale_form_data', None)

    #LaboratorioDatiBase
    user_lab_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                    office__is_active=True,
                                                                    office__organizational_structure__is_active=True,
                                                                    office__name=OFFICE_LABORATORIES)

    allowed_related_departments_codes = [] if (not user_lab_offices.exists()) else user_lab_offices.values_list("office_id__organizational_structure_id__unique_code", flat=True)
    initial = {"choosen_department_id": laboratory.id_dipartimento_riferimento.dip_id}
    form = LaboratorioDatiBaseForm(initial=initial, allowed_department_codes=allowed_related_departments_codes, instance=laboratory)
    laboratoriodatibaseinfosedestruttureform = LaboratorioDatiBaseInfoSedeStruttureForm(instance=laboratory, data=lab_infosedestrutture_form_data)
    laboratoriodatibaseambitoform = LaboratorioDatiBaseAmbitoForm(instance=laboratory, data=lab_ambito_form_data)
    laboratoriodatibasestrumentazionevaloreform = LaboratorioDatiBaseStrumentazioneValoreForm(instance=laboratory, data=lab_strumentazionevalore_form_data)
    laboratoriodatibaseinterdipartimentaleform = LaboratorioDatiBaseInterdipartimentaleForm(instance=laboratory, data=lab_interdipartimentale_form_data)
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


    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioDatiBaseForm(data=request.POST, files=request.FILES, allowed_department_codes=allowed_related_departments_codes, instance=laboratory)

        if form.is_valid():
            laboratory = form.save(commit=False)
            related_department_id = form.cleaned_data.get('choosen_department_id')[0]
            related_department = get_object_or_404(DidatticaDipartimento, pk=related_department_id)
            laboratory.id_dipartimento_riferimento = related_department
            laboratory.dipartimento_riferimento = related_department.dip_des_it
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
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
                   'laboratoriodatibaseinfosedestruttureform': laboratoriodatibaseinfosedestruttureform,
                   'laboratoriodatibaseambitoform': laboratoriodatibaseambitoform,
                   'laboratoriodatibasestrumentazionevaloreform': laboratoriodatibasestrumentazionevaloreform,
                   'laboratoriodatibaseinterdipartimentaleform': laboratoriodatibaseinterdipartimentaleform,
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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator)
                   })


@login_required
@can_manage_laboratories
def laboratory_new(request, laboratory=None, my_offices=None, is_validator=False):

    if not (request.user.is_superuser or my_offices.exists()):
            return custom_message(request, _("Permission denied"))

    allowed_related_departments_codes = [] if (not my_offices or not my_offices.exists()) else my_offices.values_list("office_id__organizational_structure_id__unique_code", flat=True)

    form = LaboratorioDatiBaseForm(allowed_department_codes=allowed_related_departments_codes)

    scientific_director_internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(required=True)
    scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                       dip_id=request.POST['choosen_department'])
    scientific_director = None

    if request.POST.get("choosen_scientific_director", ''):
        scientific_director = get_object_or_404(Personale, matricola=(decrypt(request.POST["choosen_scientific_director"])))

    if request.POST:
        form = LaboratorioDatiBaseForm(data=request.POST, files=request.FILES, allowed_department_codes=allowed_related_departments_codes)

        if "choosen_scientific_director" in request.POST and request.POST["choosen_scientific_director"]:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(data=request.POST, required=True)
        else:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorForm(data=request.POST)

        if form.is_valid() and scientific_director_form.is_valid():
            laboratory = form.save(commit=False)

            #scientific director
            if scientific_director_form.cleaned_data.get("choosen_scientific_director"):
                scientific_director_code = decrypt(scientific_director_form.cleaned_data["choosen_scientific_director"])
                scientific_director = get_object_or_404(Personale, matricola=scientific_director_code)
                laboratory.matricola_responsabile_scientifico = scientific_director
                laboratory.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'

                laboratory.matricola_preposto_sicurezza = scientific_director
                laboratory.preposto_sicurezza = f'{scientific_director.cognome} {scientific_director.nome}'

            else:
                laboratory.matricola_responsabile_scientifico = None
                laboratory.responsabile_scientifico = scientific_director_form.cleaned_data['responsabile_scientifico']

                laboratory.matricola_preposto_sicurezza = None
                laboratory.preposto_sicurezza = scientific_director_form.cleaned_data['responsabile_scientifico']


            #department
            related_department = get_object_or_404(DidatticaDipartimento, pk=form.cleaned_data.get('choosen_department_id')[0])
            laboratory.id_dipartimento_riferimento = related_department
            laboratory.dipartimento_riferimento = related_department.dip_des_it
            laboratory.laboratorio_interdipartimentale = 'NO'

            laboratory.dt_sottomissione = datetime.datetime.now()
            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
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
                    'scientific_director_label' : "choosen_scientific_director",
                    'scientific_director_internal_form': scientific_director_internal_form,
                    'scientific_director_external_form': scientific_director_external_form,
                    })

# @login_required
# @can_manage_laboratories
# @can_view_laboratories
# @can_edit_laboratories
# def laboratory_unical_department_edit(request, code, laboratory=None, my_offices=None, is_validator=False):

#     department = laboratory.id_dipartimento_riferimento
#     old_label = department.dip_des_it

#     form = LaboratorioDatiBaseDipartimentoForm(initial={'choosen_department': department.dip_id})

#     if request.POST:
#         form = LaboratorioDatiBaseDipartimentoForm(data=request.POST)
#         if form.is_valid():

#             department_id = form.cleaned_data['choosen_department']
#             department = get_object_or_404(DidatticaDipartimento, dip_id=department_id)
#             laboratory.id_dipartimento_riferimento = department
#             laboratory.dipartimento_riferimento = f'{department.dip_des_it}'
#             laboratory.user_mod_id = request.user
#             laboratory.dt_mod=datetime.datetime.now()
#             laboratory.visibile=False
#             laboratory.save()

#             if old_label != department.dip_des_it:
#                 log_action(user=request.user,
#                            obj=laboratory,
#                            flag=CHANGE,
#                            msg=f'Sostituito dipartimento {old_label} con {department.dip_des_it}')


#             messages.add_message(request, messages.SUCCESS, _("Department edited successfully"))
#             return redirect('crud_laboratories:crud_laboratory_edit', code=code)

#         else:  # pragma: no cover
#             for k, v in form.errors.items():
#                 messages.add_message(request, messages.ERROR,
#                                      f"<b>{form.fields[k].label}</b>: {v}")

#     breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
#                    reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
#                    reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
#                    '#': f'{laboratory.dipartimento_riferimento}'}

#     return render(request,
#                   'laboratory_department.html',
#                   {'breadcrumbs': breadcrumbs,
#                    'url': reverse('ricerca:departmentslist'),
#                    'form': form,
#                    'laboratory': laboratory,
#                    'choosen_department': old_label,
#                    'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
#                    })

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_scientific_director_edit(request, code, laboratory=None, my_offices=None, is_validator=False):

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

    if request.POST:
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
            laboratory.dt_mod=datetime.datetime.now()
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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:teacherslist'),
                   'including': 'blocks/crud_teacherslist.html'})

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_safety_manager_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
    safety_manager = None
    safety_manager_ecode = None
    old_label = None
    choosen_person = None
    initial = {}
    if laboratory.matricola_preposto_sicurezza:
        safety_manager = laboratory.matricola_preposto_sicurezza
        old_label = f'{safety_manager.cognome} {safety_manager.nome}'
        choosen_person = old_label
        safety_manager_ecode = encrypt(safety_manager.matricola)
        initial = {'choosen_person': safety_manager_ecode}

    else:
        old_label = laboratory.preposto_sicurezza
        initial = {'preposto_sicurezza': old_label}

    external_form = LaboratorioDatiBaseSafetyManagerForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseSafetyManagerForm(data=request.POST)

        if 'choosen_person' in request.POST and request.POST["choosen_person"]:
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
            laboratory.dt_mod=datetime.datetime.now()
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

            external_form = LaboratorioDatiBaseSafetyManagerForm(initial=initial)
            internal_form = ChoosenPersonForm(initial=initial, required=True)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_safety_manager_edit', kwargs={'code': code}): _('Safety Manager')
                   }

    return render(request,
                  'laboratory_choose_person.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': choosen_person,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'item_label': _("Safety Manager"),
                   'edit': 1,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:addressbooklist')})

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_safety_manager_delete(request, code, laboratory=None, my_offices=None, is_validator=False):
    laboratory.matricola_preposto_sicurezza = None
    laboratory.preposto_sicurezza = None
    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted safety manager"))

    messages.add_message(request, messages.SUCCESS, _("Safety manager removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@check_if_superuser
@can_manage_laboratories
def laboratory_delete(request, code, laboratory=None, my_offices=None, is_validator=False):
    laboratory.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Laboratory removed successfully"))

    return redirect('crud_laboratories:crud_laboratories')


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_extra_departments_new(request, code, laboratory=None, my_offices=None, is_validator=False):
    department_form = LaboratorioAltriDipartimentiForm()
    if request.POST:
        department_form = LaboratorioAltriDipartimentiForm(data=request.POST)
        if department_form.is_valid() and department_form.cleaned_data.get('choosen_department'):

            department = get_object_or_404(DidatticaDipartimento, pk=department_form.cleaned_data['choosen_department'])

            if department.dip_id == laboratory.id_dipartimento_riferimento_id:
                messages.add_message(request, messages.ERROR, _("Extra departments must be different from Laboratory's department"))
            else:
                LaboratorioAltriDipartimenti.objects.create(
                    id_laboratorio_dati=laboratory,
                    id_dip=department,
                    descr_dip_lab=department.dip_des_it
                )

                laboratory.user_mod_id = request.user
                laboratory.dt_mod=datetime.datetime.now()
                laboratory.visibile=False
                laboratory.save()

                log_action(user=request.user,
                obj=laboratory,
                flag=ADDITION,
                msg=_("Added extra department"))

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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:departmentslist')})



@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_extra_departments_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    extra_department_lab = get_object_or_404(LaboratorioAltriDipartimenti, pk=data_id)

    extra_department_lab.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted extra department"))

    messages.add_message(request, messages.SUCCESS, _("Extra department removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_equipment_new(request, code, laboratory=None, my_offices=None, is_validator=False):
    equipment_form = LaboratorioAttrezzatureForm()
    equipment_funds_form = LaboratorioAttrezzatureFondiForm()
    equipment_risks_form = LaboratorioAttrezzatureRischiForm()
    if request.POST:
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
                    dt_mod=datetime.datetime.now()
                )

            for risk_id in equipment_risks_form.cleaned_data.get('id_tipologia_rischio', []):
                LaboratorioAttrezzatureRischi.objects.create(
                    id_laboratorio_attrezzature=laboratory_equipment,
                    id_tipologia_rischio=get_object_or_404(TipologiaRischio, pk=risk_id),
                    user_mod_id=request.user,
                    dt_mod=datetime.datetime.now()
                )

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added piece of equipment"))

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
                   'item_label': _("Equipment Piece"),
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_equipment_edit(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    laboratory_equipment = get_object_or_404(LaboratorioAttrezzature, pk=data_id)
    equipment_form = LaboratorioAttrezzatureForm(instance=laboratory_equipment)

    selected_funds_ids = LaboratorioAttrezzatureFondi.objects.filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_laboratorio_fondo", flat=True)
    selected_funds_ids = tuple(map(str, selected_funds_ids))
    equipment_funds_form = LaboratorioAttrezzatureFondiForm(initial={"id_laboratorio_fondo" : selected_funds_ids})

    selected_risks_ids = LaboratorioAttrezzatureRischi.objects.filter(id_laboratorio_attrezzature=laboratory_equipment.id).values_list("id_tipologia_rischio", flat=True)
    selected_risks_ids = tuple(map(str, selected_risks_ids))
    equipment_risks_form = LaboratorioAttrezzatureRischiForm(initial={"id_tipologia_rischio" : selected_risks_ids})

    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

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
                    dt_mod=datetime.datetime.now()
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
                    dt_mod=datetime.datetime.now()
                )

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited piece of equipment"))

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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_equipment_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    equipment_piece = get_object_or_404(LaboratorioAttrezzature, pk=data_id)

    equipment_piece.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted piece of equipment"))

    messages.add_message(request, messages.SUCCESS, _("Piece of equipment removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_researches_erc1_edit(request, code, laboratory=None, my_offices=None, is_validator=False):

    #Previously selected researches
    researches_erc1_old = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code)

    #Ids to initialize form's checkboxes
    researches_erc1 = researches_erc1_old.values("id","id_ricerca_erc1","id_ricerca_erc1__descrizione", "id_ricerca_erc1__ricerca_erc0_cod")
    erc0 = researches_erc1.first()['id_ricerca_erc1__ricerca_erc0_cod'] if researches_erc1.exists() else None
    researches_erc1_ids = researches_erc1.values_list('id_ricerca_erc1', flat=True)
    fields = ['id_ricerche_erc1_ls', 'id_ricerche_erc1_pe', 'id_ricerche_erc1_sh']
    researches_erc1_ids = tuple(map(str, researches_erc1_ids))
    initial = {}
    if erc0 is not None:
        for field in fields:
            if erc0.lower() in field:
                initial[field] = researches_erc1_ids
                initial['erc0_selector'] = erc0
                break

    research_erc1_form = LaboratorioDatiErc1Form(initial=initial)

    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

        research_erc1_form = LaboratorioDatiErc1Form(data=request.POST)
        if research_erc1_form.is_valid():
            erc0_selector = request.POST.get("erc0_selector")
            selected_erc1_res_ids = research_erc1_form.cleaned_data.get(f'id_ricerche_erc1_{erc0_selector.lower()}', [])

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
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited ERC classification"))

            messages.add_message(request, messages.SUCCESS, _("ERC classification edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_researches_erc1_edit', kwargs={'code': code}): _('ERC classification')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'forms': (research_erc1_form,),
                   'laboratory': laboratory,
                   'erc_form': 1,
                   'item_label': _("ERC classification"),
                   'edit': 1,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })


# Can be viewed by validators but not modified
@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_locations_edit(request, data_id, code, laboratory=None, my_offices=None, is_validator=False):
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)
    location_form = LaboratorioUbicazioneForm(instance=location)

    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

        location_form = LaboratorioUbicazioneForm(instance=location, data=request.POST)
        if location_form.is_valid():

            location_form.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited laboratory location"))

            messages.add_message(request, messages.SUCCESS, _("Location edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in location_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{location_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_locations_edit', kwargs={'code': code, 'data_id': data_id}): _('Location')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'forms': (location_form,),
                   'item_label': _("Location"),
                   'laboratory': laboratory,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_locations_new(request, code, laboratory=None, my_offices=None, is_validator=False):
    location_form = LaboratorioUbicazioneForm()
    if request.POST:
        location_form = LaboratorioUbicazioneForm(data=request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)
            location.id_laboratorio_dati = laboratory
            location.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added laboratory location"))

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
                   'item_label': _("Location"),
                   'edit': 1,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_locations_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    location = get_object_or_404(LaboratorioUbicazione, pk=data_id)

    location.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted location"))

    messages.add_message(request, messages.SUCCESS, _("Location removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_research_staff_new(request, code, laboratory=None, my_offices=None, is_validator=False):
    researcher = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioPersonaleForm(data=request.POST)
        if "choosen_person" in request.POST and request.POST['choosen_person']:
            form = internal_form
        else:
            form = external_form

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
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added laboratory researcher"))

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
                   'item_label': _("Research Staff Member"),
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:addressbooklist')})

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_research_staff_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    researcher = get_object_or_404(LaboratorioPersonaleRicerca, pk=data_id)
    researcher.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted researcher"))

    messages.add_message(request, messages.SUCCESS, _("Researcher removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_technical_staff_new(request, code, laboratory=None, my_offices=None, is_validator=False):
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
                    percentuale_impegno=technician_form.cleaned_data.get('percentuale_impegno'))
            else:
                LaboratorioPersonaleTecnico.objects.create(
                    id_laboratorio_dati=laboratory,
                    matricola_personale_tecnico=None,
                    cognomenome_origine=person_form.cleaned_data.get('laboratory_staff'),
                    ruolo=technician_form.cleaned_data.get('ruolo'),
                    percentuale_impegno=technician_form.cleaned_data.get('percentuale_impegno'))

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added laboratory technician"))

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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:addressbooklist')})

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_technical_staff_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    technician = get_object_or_404(LaboratorioPersonaleTecnico, pk=data_id)
    technician.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted technician"))

    messages.add_message(request, messages.SUCCESS, _("Technician removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_activities_new(request, code, laboratory=None, my_offices=None, is_validator=False):

    activity_types_already_specified = LaboratorioAttivita\
        .objects\
        .filter(id_laboratorio_dati=code)\
        .values_list("id_tipologia_attivita", flat=True)

    if activity_types_already_specified and len(activity_types_already_specified) >= 3:
        messages.add_message(request, messages.ERROR, _("Activities list is full"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified)

    if request.POST:
        activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, data=request.POST)
        if activity_form.is_valid():
            activity_type=get_object_or_404(LaboratorioTipologiaAttivita, pk=activity_form.cleaned_data["tipologia_attivita"])
            activity = activity_form.save(commit=False)
            activity.id_laboratorio_dati=laboratory
            activity.id_tipologia_attivita=activity_type
            activity.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added activity"))

            messages.add_message(request, messages.SUCCESS, _("Activities added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in activity_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{activity_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_activities_new', kwargs={'code': code}): _('Activities')
                   }
    return render(request,
                  'laboratory_unique_form.html',
                  {'breadcrumbs': breadcrumbs,
                   'forms': (activity_form,),
                   'laboratory': laboratory,
                   'item_label': _("Activity"),
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_activities_edit(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
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
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

        activity_form = LaboratorioAttivitaForm(activity_types_already_specified=activity_types_already_specified, instance=activity, data=request.POST)
        if activity_form.is_valid():
            activity_type = get_object_or_404(LaboratorioTipologiaAttivita, pk=activity_form.cleaned_data["tipologia_attivita"])
            activity = activity_form.save(commit=False)
            activity.id_tipologia_attivita = activity_type
            activity.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited activity"))

            messages.add_message(request, messages.SUCCESS, _("Activity edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in activity_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{activity_form.fields[k].label}</b>: {v}")

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
                   'item_label': _("Activity"),
                   'edit': 1,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                })

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_activities_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    activity.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted activity"))

    messages.add_message(request, messages.SUCCESS, _("Activity removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_provided_services_new(request, code, laboratory=None, my_offices=None, is_validator=False):
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
                provided_service.responsabile_origine = person_form.cleaned_data['laboratory_manager']

            provided_service.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added provided service"))

            messages.add_message(request, messages.SUCCESS, _("Provided service added successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in person_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{person_form.fields[k].label}</b>: {v}")
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:addressbooklist')
                   })


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_provided_services_edit(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    manager = None
    cpf_initial = {}
    lpf_initial = {}
    manager_origine = None
    choosen_person = None
    if(provided_service.matricola_responsabile):
        manager = get_object_or_404(Personale, matricola=provided_service.matricola_responsabile)
        cpf_initial["choosen_person"] = encrypt(provided_service.matricola_responsabile)
        manager_origine = f'{manager.cognome} {manager.nome}'
        choosen_person = manager_origine
    else:
        lpf_initial["laboratory_manager"] = provided_service.responsabile_origine

    internal_form = ChoosenPersonForm(initial=cpf_initial, required=False)
    external_form = LaboratorioServiziErogatiResponsabileForm(initial=lpf_initial)
    form = LaboratorioServiziErogatiForm(instance=provided_service)

    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

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
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited provided service"))

            messages.add_message(request, messages.SUCCESS, _("Provided service edited successfully"))
            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in person_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{person_form.fields[k].label}</b>: {v}")
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

            internal_form = ChoosenPersonForm(initial=cpf_initial, required=False)
            external_form = LaboratorioServiziErogatiResponsabileForm(initial=lpf_initial)

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
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   'url': reverse('ricerca:addressbooklist')
                   })

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_provided_services_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    provided_service.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted provided service"))

    messages.add_message(request, messages.SUCCESS, _("Provided service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_offered_services_new(request, code, laboratory=None, my_offices=None, is_validator=False):
    form = LaboratorioServiziOffertiForm()
    if request.POST:
        form = LaboratorioServiziOffertiForm(data=request.POST)
        offered_service = form.save(commit=False)
        offered_service.id_laboratorio_dati = laboratory
        offered_service.save()

        laboratory.user_mod_id = request.user
        laboratory.dt_mod=datetime.datetime.now()
        laboratory.visibile=False
        laboratory.save()

        log_action(user=request.user,
        obj=laboratory,
        flag=CHANGE,
        msg=_("Added offered service"))

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
                   'item_label': _("Offered Service"),
                   'laboratory': laboratory,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   })


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_offered_services_edit(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    form = LaboratorioServiziOffertiForm(instance=offered_service)

    if request.POST:
        if not (request.user.is_superuser or my_offices.exists() or _is_user_scientific_director(request, laboratory)):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioServiziOffertiForm(data=request.POST, instance=offered_service)

        if form.is_valid():
            offered_service = form.save()

            laboratory.user_mod_id = request.user
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Edited offered service"))

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
                   'item_label': _("Offered Service"),
                   'edit': 1,
                   'user_roles' : __get_user_roles(request, laboratory, my_offices, is_validator),
                   })

@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_offered_services_delete(request, code, data_id, laboratory=None, my_offices=None, is_validator=False):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    offered_service.delete()

    laboratory.user_mod_id = request.user
    laboratory.dt_mod=datetime.datetime.now()
    laboratory.visibile=False
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Deleted offered service"))

    messages.add_message(request, messages.SUCCESS, _("Offered service removed successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_risk_types_edit(request, code, laboratory=None, my_offices=None, is_validator=False):
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
            laboratory.dt_mod=datetime.datetime.now()
            laboratory.visibile=False
            laboratory.save()

            log_action(user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Risk types updated"))

            messages.add_message(request, messages.SUCCESS, _("Risk types updated successfully"))
        else:  # pragma: no cover
            for k, v in risk_type_form.errors.items():
                messages.add_message(request, messages.ERROR, f"<b>{risk_type_form.fields[k].label}</b>: {v}")

        return redirect(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}) + "#risks")


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_request_approval(request, code, laboratory=None, my_offices=None, is_validator=False):

    if laboratory.visibile:
        return custom_message(request, _("Laboratory is already visible"))

    #LaboratorioDatiBase
    # if not (laboratory.preposto_sicurezza or laboratory.matricola_preposto_sicurezza):
    #     messages.add_message(request, messages.ERROR, _("Laboratory must have a Safety Manager"))
    #     return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    #LaboratorioAltriDipartimenti
    extra_departments = LaboratorioAltriDipartimenti.objects.filter(id_laboratorio_dati=code).exists()
    if extra_departments and laboratory.laboratorio_interdipartimentale == "NO":
        messages.add_message(request, messages.ERROR, _("Extra Departments specified for NON Interdepartmental Laboratory"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    #LaboratorioDatiErc1
    researches_erc1 = LaboratorioDatiErc1.objects.filter(id_laboratorio_dati=code).exists()
    if not researches_erc1:
        messages.add_message(request, messages.ERROR, _("Laboratory must have at least one ERC 1 Research"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    #LaboratorioUbicazione
    locations = LaboratorioUbicazione.objects.filter(id_laboratorio_dati=code).exists()
    if not locations:
        messages.add_message(request, messages.ERROR, _("Laboratory must have at least one Location"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)

    #LaboratorioAttivita
    activities = LaboratorioAttivita.objects.filter(id_laboratorio_dati=code).exists()
    if not activities:
        messages.add_message(request, messages.ERROR, _("Laboratory must have at least one Activity"))
        return redirect('crud_laboratories:crud_laboratory_edit', code=code)


    validators = OrganizationalStructureOfficeEmployee.objects.filter(office__is_active=True,
                                                                    office__name=OFFICE_LABORATORY_VALIDATORS,
                                                                    office__organizational_structure__is_active=True)\
                                                               .values_list('employee_id__email', flat=True)

    validators = (list(set(validators)))
    lab_url = request.build_absolute_uri(reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': laboratory.id}))

    send_mail(
        TO_VALIDATORS_EMAIL_SUBJECT,
        f"{TO_VALIDATORS_EMAIL_MESSAGE} {laboratory.nome_laboratorio} {lab_url}",
        TO_VALIDATORS_EMAIL_FROM,
        validators,
        fail_silently=True,
    )

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Requested approval"))

    messages.add_message(request, messages.SUCCESS, _("Request for approval sent successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)

@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_approve(request, code, laboratory=None, my_offices=None, is_validator=False):

    if not (request.user.is_superuser or is_validator):
        return custom_message(request, _("Permission denied"))
    if laboratory.visibile:
        return custom_message(request, _("Laboratory is already visible"))

    laboratory.visibile = True
    laboratory.save()

    log_action(user=request.user,
    obj=laboratory,
    flag=CHANGE,
    msg=_("Approved Laboratory"))

    messages.add_message(request, messages.SUCCESS, _("Laboratory approved successfully"))
    return redirect('crud_laboratories:crud_laboratory_edit', code=code)
