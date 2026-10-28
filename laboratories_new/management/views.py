import datetime
import logging

from addressbook.models import Personale
from addressbook.utils import get_personale_matricola
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.forms import ChoosenPersonForm
from generics.utils import custom_message, log_action
from laboratories.models import (
    LaboratorioAttivita,
    LaboratorioDatiErc1,
    LaboratorioServiziErogati,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
    LaboratorioAffiliati,
    LaboratorioDatiErc1,
    LaboratorioDipartimenti,
    LaboratorioResponsabile,
    LaboratorioRuolo,
    LaboratorioServizi,
)
from laboratories.settings import (
    OFFICE_LABORATORIES,
    OFFICE_LABORATORY_VALIDATORS,
    TO_VALIDATORS_EMAIL_MESSAGE,
    TO_VALIDATORS_EMAIL_SUBJECT,
)
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.models import RicercaErc1
from structures.models import DidatticaDipartimento

from .decorators import (
    can_edit_laboratories,
    can_manage_laboratories,
    can_view_laboratories,
    check_if_superuser,
)
from .forms import (
    LaboratorioAltriDipartimentiForm,
    LaboratorioAttivitaForm,
    LaboratorioDatiBaseForm,
    LaboratorioDatiBaseSafetyManagerForm,
    LaboratorioDatiBaseScientificDirectorChoosenPersonForm,
    LaboratorioDatiBaseScientificDirectorForm,
    LaboratorioDatiErc1Form,
    LaboratorioPersonaleForm,
    LaboratorioPersonaleTecnicoForm,
    LaboratorioServiziErogatiForm,
    LaboratorioServiziErogatiResponsabileForm,
    LaboratorioServiziOffertiForm,
    LaboratorioUbicazioneForm,
    LaboratorioAltriDipartimentiForm,
    LaboratorioDatiBaseForm,
    LaboratorioDatiBaseSafetyManagerForm,
    LaboratorioDatiBaseScientificDirectorChoosenPersonForm,
    LaboratorioDatiBaseScientificDirectorForm,
    LaboratorioDatiErc1Form,
    LaboratorioPersonaleForm,
    LaboratorioPersonaleTecnicoForm,
    LaboratorioServiziForm,
)
from .utils import _get_user_roles, _is_user_scientific_director

logger = logging.getLogger(__name__)

ROLE_SCIENTIFIC_DIRECTOR = ("Responsabile scientifico", "Scientific director")
ROLE_SAFETY_MANAGER = ("Preposto alla sicurezza", "Safety manager")
ROLE_RESEARCH_STAFF = ("Personale di ricerca", "Research staff")


@login_required
@can_manage_laboratories
def laboratories(request, laboratory=None, my_offices=None, is_validator=False):
    """
    lista dei laboratori
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Laboratories"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("laboratories:apiv1:laboratories-list"),
    }
    return render(request, "laboratories.html", context)


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    if not laboratory.visibile and not request.POST:
        messages.add_message(request, messages.WARNING, _("Laboratory NOT visible"))

    user_lab_offices = OrganizationalStructureOfficeEmployee.objects.filter(
        employee=request.user,
        office__is_active=True,
        office__organizational_structure__is_active=True,
        office__name=OFFICE_LABORATORIES,
    )

    allowed_related_departments_codes = (
        []
        if (not user_lab_offices.exists())
        else user_lab_offices.values_list(
            "office_id__organizational_structure_id__unique_code", flat=True
        )
    )

    lab_departments = LaboratorioDipartimenti.objects.filter(
        laboratorio_dati_base=laboratory
    ).select_related("didattica_dipartimento")

    initial = {
        "choosen_department_id": list(
            lab_departments.values_list("didattica_dipartimento_id", flat=True)
        )
    }

    form = LaboratorioDatiBaseForm(
        initial=initial,
        allowed_department_codes=allowed_related_departments_codes,
        instance=laboratory,
    )

    # LaboratorioDatiErc1
    researches_erc1 = LaboratorioDatiErc1.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).values("id", "ricerca_erc1", "ricerca_erc1__descrizione")
    # LaboratorioUbicazione
    locations = LaboratorioUbicazione.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).select_related("anagrafica_ubicazione")
    # LaboratorioServizi
    services = LaboratorioServizi.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).select_related("laboratorio_anagrafica_servizi", "traiettoria_s3")
    # LaboratorioResponsabile
    managers = LaboratorioResponsabile.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).select_related("matricola_personale", "laboratorio_ruolo")
    # LaboratorioAffiliati
    affiliates = LaboratorioAffiliati.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).select_related("matricola_personale", "laboratorio_ruolo")

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioDatiBaseForm(
            data=request.POST,
            files=request.FILES,
            allowed_department_codes=allowed_related_departments_codes,
            instance=laboratory,
        )

        if form.is_valid():
            with transaction.atomic():
                laboratory = form.save(commit=False)
                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.save()

                _sync_laboratory_departments(request, form, laboratory)

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )
                log_action(
                    user=request.user,
                    obj=laboratory,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Laboratory edited successfully")
            )

            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(laboratory).pk,
        object_id=laboratory.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratory"),
        "#": laboratory.nome_laboratorio,
    }

    return render(
        request,
        "laboratory.html",
        {
            "breadcrumbs": breadcrumbs,
            "logs": logs,
            "form": form,
            "laboratory": laboratory,
            "departments": lab_departments,
            "researches_erc1": researches_erc1,
            "locations": locations,
            "services": services,
            "managers": managers,
            "affiliates": affiliates,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


def _sync_laboratory_departments(request, form, laboratory):
    """
    Allinea LaboratorioDipartimenti ai dipartimenti scelti nel form.
    Rimuove solo quelli deselezionati che l'operatore poteva effettivamente
    vedere/scegliere (così non tocca dipartimenti fuori dal suo perimetro).
    """
    selected_ids = {int(i) for i in form.cleaned_data["choosen_department_id"]}
    selectable_ids = {
        int(value) for value, _label in form.fields["choosen_department_id"].choices
    }

    current = LaboratorioDipartimenti.objects.filter(laboratorio_dati_base=laboratory)

    # Rimozione dei deselezionati (solo nel perimetro dell'operatore)
    current.filter(didattica_dipartimento_id__in=selectable_ids - selected_ids).delete()

    existing_ids = set(current.values_list("didattica_dipartimento_id", flat=True))
    has_main = current.filter(principale=True).exists()

    new_departments = DidatticaDipartimento.objects.filter(
        pk__in=selected_ids - existing_ids
    )
    for department in new_departments:
        LaboratorioDipartimenti.objects.create(
            laboratorio_dati_base=laboratory,
            didattica_dipartimento=department,
            descr_dip_lab=department.dip_des_it,
            principale=not has_main,
            dt_mod=datetime.date.today(),
            id_user_mod=request.user,
        )
        has_main = True


@login_required
@can_manage_laboratories
def laboratory_new(request, laboratory=None, my_offices=None, is_validator=False):
    if not (request.user.is_superuser or my_offices.exists()):
        return custom_message(request, _("Permission denied"))

    allowed_related_departments_codes = (
        []
        if (not my_offices or not my_offices.exists())
        else my_offices.values_list(
            "office_id__organizational_structure_id__unique_code", flat=True
        )
    )

    form = LaboratorioDatiBaseForm(
        allowed_department_codes=allowed_related_departments_codes
    )

    scientific_director_internal_form = (
        LaboratorioDatiBaseScientificDirectorChoosenPersonForm(required=True)
    )
    scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    if request.POST:
        form = LaboratorioDatiBaseForm(
            data=request.POST,
            files=request.FILES,
            allowed_department_codes=allowed_related_departments_codes,
        )

        if request.POST.get("choosen_scientific_director"):
            scientific_director_form = (
                LaboratorioDatiBaseScientificDirectorChoosenPersonForm(
                    data=request.POST, required=True
                )
            )
        else:
            scientific_director_form = LaboratorioDatiBaseScientificDirectorForm(
                data=request.POST
            )

        if form.is_valid() and scientific_director_form.is_valid():
            today = datetime.date.today()

            with transaction.atomic():
                laboratory = form.save(commit=False)
                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

                # Dipartimenti: il primo scelto è quello principale
                department_ids = [
                    int(i) for i in form.cleaned_data["choosen_department_id"]
                ]
                departments = {
                    d.pk: d
                    for d in DidatticaDipartimento.objects.filter(pk__in=department_ids)
                }
                for index, department_id in enumerate(department_ids):
                    department = departments.get(department_id)
                    if department is None:
                        continue
                    LaboratorioDipartimenti.objects.create(
                        laboratorio_dati_base=laboratory,
                        didattica_dipartimento=department,
                        descr_dip_lab=department.dip_des_it,
                        principale=(index == 0),
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                # Ruoli (responsabile scientifico e preposto sicurezza)
                roles = []
                for descr_it, descr_en in (
                    ROLE_SCIENTIFIC_DIRECTOR,
                    ROLE_SAFETY_MANAGER,
                ):
                    role = LaboratorioRuolo.objects.filter(
                        descr_ruolo_it=descr_it
                    ).first()
                    if role is None:
                        role = LaboratorioRuolo.objects.create(
                            descr_ruolo_it=descr_it,
                            descr_ruolo_en=descr_en,
                            dt_mod=today,
                            id_user_mod=request.user,
                        )
                    roles.append(role)

                # Persona: interna -> LaboratorioResponsabile, esterna -> LaboratorioAffiliati
                chosen_code = scientific_director_form.cleaned_data.get(
                    "choosen_scientific_director"
                )
                if chosen_code:
                    person = get_object_or_404(Personale, id_ab=chosen_code)
                    for role in roles:
                        LaboratorioResponsabile.objects.create(
                            laboratorio_dati_base=laboratory,
                            matricola_personale=person,
                            laboratorio_ruolo=role,
                            data_inizio=today,
                            dt_mod=today,
                            id_user_mod=request.user,
                        )
                else:
                    full_name = scientific_director_form.cleaned_data[
                        "responsabile_scientifico"
                    ]
                    for role in roles:
                        LaboratorioAffiliati.objects.create(
                            laboratorio_dati_base=laboratory,
                            nome_cognome=full_name,
                            laboratorio_ruolo=role,
                            data_inizio=today,
                            dt_mod=today,
                            id_user_mod=request.user,
                        )

            log_action(
                user=request.user, obj=laboratory, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _(
                    "Laboratory anagraphic created successfully, please fill in the other fields"
                ),
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory.pk
            )
        else:  # pragma: no cover
            for f in (form, scientific_director_form):
                for k, v in f.errors.items():
                    field = f.fields.get(k)
                    label = field.label if field else _("Error")
                    messages.add_message(
                        request, messages.ERROR, f"<b>{label}</b>: {v}"
                    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        "#": _("New"),
    }
    return render(
        request,
        "laboratory_new.html",
        {
            "breadcrumbs": breadcrumbs,
            "url": reverse("teachers:apiv1:teachers-list"),
            "form": form,
            "departments_api": reverse("structures:apiv1:departments-list"),
            "teachers_api": reverse("teachers:apiv1:teachers-list"),
            "scientific_director_label": "choosen_scientific_director",
            "scientific_director_internal_form": scientific_director_internal_form,
            "scientific_director_external_form": scientific_director_external_form,
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_scientific_director_edit(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    today = datetime.date.today()

    # Ruolo "responsabile scientifico"
    role = LaboratorioRuolo.objects.filter(
        descr_ruolo_it=ROLE_SCIENTIFIC_DIRECTOR[0]
    ).first()

    # Record attualmente in corso (senza data_fine o con data_fine futura)
    still_valid = Q(data_fine__isnull=True) | Q(data_fine__gte=today)

    current_internal = None
    current_external = None
    if role:
        current_internal = (
            LaboratorioResponsabile.objects.filter(
                still_valid, laboratorio_dati_base=laboratory, laboratorio_ruolo=role
            )
            .select_related("matricola_personale")
            .order_by("-data_inizio", "-id")
            .first()
        )
        current_external = (
            LaboratorioAffiliati.objects.filter(
                still_valid, laboratorio_dati_base=laboratory, laboratorio_ruolo=role
            )
            .order_by("-data_inizio", "-id")
            .first()
        )

    old_label = None
    initial = {}
    if current_internal and current_internal.matricola_personale:
        scientific_director = current_internal.matricola_personale
        old_label = f"{scientific_director.cognome} {scientific_director.nome}"
        initial = {"choosen_person": scientific_director.id_ab}
    elif current_external:
        old_label = current_external.nome_cognome
        initial = {"responsabile_scientifico": old_label}

    external_form = LaboratorioDatiBaseScientificDirectorForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseScientificDirectorForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            with transaction.atomic():
                if role is None:
                    role = LaboratorioRuolo.objects.create(
                        descr_ruolo_it=ROLE_SCIENTIFIC_DIRECTOR[0],
                        descr_ruolo_en=ROLE_SCIENTIFIC_DIRECTOR[1],
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                # Chiudo i responsabili scientifici in corso
                LaboratorioResponsabile.objects.filter(
                    still_valid,
                    laboratorio_dati_base=laboratory,
                    laboratorio_ruolo=role,
                ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)
                LaboratorioAffiliati.objects.filter(
                    still_valid,
                    laboratorio_dati_base=laboratory,
                    laboratorio_ruolo=role,
                ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)

                # Creo il nuovo responsabile scientifico
                if form.cleaned_data.get("choosen_person"):
                    scientific_director = get_object_or_404(
                        Personale,
                        matricola=get_personale_matricola(
                            form.cleaned_data["choosen_person"]
                        ),
                    )
                    new_label = (
                        f"{scientific_director.cognome} {scientific_director.nome}"
                    )
                    LaboratorioResponsabile.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=scientific_director,
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )
                else:
                    new_label = form.cleaned_data["responsabile_scientifico"]
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        nome_cognome=new_label,
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            if old_label != new_label:
                log_action(
                    user=request.user,
                    obj=laboratory,
                    flag=CHANGE,
                    msg=f"Sostituito responsabile scientifico {old_label} con {new_label}",
                )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Laboratory scientific director edited successfully"),
            )

            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-scientific-director-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Scientific Director"),
    }

    return render(
        request,
        "laboratory_choose_person.html",
        {
            "breadcrumbs": breadcrumbs,
            "laboratory": laboratory,
            "choosen_person": old_label,
            "external_form": external_form,
            "internal_form": internal_form,
            "item_label": _("Scientific Director"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("teachers:apiv1:teachers-list"),
            "including": "blocks/crud_teacherslist.html",
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_safety_manager_edit(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    today = datetime.date.today()

    # Ruolo "preposto alla sicurezza"
    role = LaboratorioRuolo.objects.filter(
        descr_ruolo_it=ROLE_SAFETY_MANAGER[0]
    ).first()

    # Record attualmente in corso (senza data_fine o con data_fine futura)
    still_valid = Q(data_fine__isnull=True) | Q(data_fine__gte=today)

    current_internal = None
    current_external = None
    if role:
        current_internal = (
            LaboratorioResponsabile.objects.filter(
                still_valid, laboratorio_dati_base=laboratory, laboratorio_ruolo=role
            )
            .select_related("matricola_personale")
            .order_by("-data_inizio", "-id")
            .first()
        )
        current_external = (
            LaboratorioAffiliati.objects.filter(
                still_valid, laboratorio_dati_base=laboratory, laboratorio_ruolo=role
            )
            .order_by("-data_inizio", "-id")
            .first()
        )

    old_label = None
    choosen_person = None
    initial = {}
    if current_internal and current_internal.matricola_personale:
        safety_manager = current_internal.matricola_personale
        old_label = f"{safety_manager.cognome} {safety_manager.nome}"
        choosen_person = old_label
        initial = {"choosen_person": safety_manager.id_ab}
    elif current_external:
        old_label = current_external.nome_cognome
        initial = {"preposto_sicurezza": old_label}

    external_form = LaboratorioDatiBaseSafetyManagerForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseSafetyManagerForm(data=request.POST)

        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            with transaction.atomic():
                if role is None:
                    role = LaboratorioRuolo.objects.create(
                        descr_ruolo_it=ROLE_SAFETY_MANAGER[0],
                        descr_ruolo_en=ROLE_SAFETY_MANAGER[1],
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                # Chiudo i preposti in corso
                LaboratorioResponsabile.objects.filter(
                    still_valid,
                    laboratorio_dati_base=laboratory,
                    laboratorio_ruolo=role,
                ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)
                LaboratorioAffiliati.objects.filter(
                    still_valid,
                    laboratorio_dati_base=laboratory,
                    laboratorio_ruolo=role,
                ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)

                # Creo il nuovo preposto
                if form.cleaned_data.get("choosen_person"):
                    safety_manager = get_object_or_404(
                        Personale,
                        matricola=get_personale_matricola(
                            form.cleaned_data["choosen_person"]
                        ),
                    )
                    new_label = f"{safety_manager.cognome} {safety_manager.nome}"
                    LaboratorioResponsabile.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=safety_manager,
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )
                else:
                    new_label = form.cleaned_data["preposto_sicurezza"]
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        nome_cognome=new_label,
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            if old_label != new_label:
                log_action(
                    user=request.user,
                    obj=laboratory,
                    flag=CHANGE,
                    msg=f"Sostituito preposto sicurezza {old_label} con {new_label}",
                )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Laboratory safety manager edited successfully"),
            )

            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

            external_form = LaboratorioDatiBaseSafetyManagerForm(initial=initial)
            internal_form = ChoosenPersonForm(initial=initial, required=True)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-safety-manager-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Safety Manager"),
    }

    return render(
        request,
        "laboratory_choose_person.html",
        {
            "breadcrumbs": breadcrumbs,
            "laboratory": laboratory,
            "choosen_person": choosen_person,
            "external_form": external_form,
            "internal_form": internal_form,
            "item_label": _("Safety Manager"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_safety_manager_delete(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    today = datetime.date.today()
    still_valid = Q(data_fine__isnull=True) | Q(data_fine__gte=today)

    role = LaboratorioRuolo.objects.filter(
        descr_ruolo_it=ROLE_SAFETY_MANAGER[0]
    ).first()

    closed = 0
    if role:
        with transaction.atomic():
            # Chiudo i preposti in corso (interni ed esterni)
            closed += LaboratorioResponsabile.objects.filter(
                still_valid,
                laboratorio_dati_base=laboratory,
                laboratorio_ruolo=role,
            ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)
            closed += LaboratorioAffiliati.objects.filter(
                still_valid,
                laboratorio_dati_base=laboratory,
                laboratorio_ruolo=role,
            ).update(data_fine=today, dt_mod=today, id_user_mod=request.user)

            if closed:
                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

    if closed:
        log_action(
            user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Deleted safety manager"),
        )
        messages.add_message(
            request, messages.SUCCESS, _("Safety manager removed successfully")
        )
    else:
        messages.add_message(
            request, messages.WARNING, _("No safety manager to remove")
        )

    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@check_if_superuser
@can_manage_laboratories
def laboratory_delete(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    laboratory.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Laboratory removed successfully")
    )

    return redirect("laboratories:management:laboratories")


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_extra_departments_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    department_form = LaboratorioAltriDipartimentiForm()
    if request.POST:
        department_form = LaboratorioAltriDipartimentiForm(data=request.POST)
        if department_form.is_valid() and department_form.cleaned_data.get(
            "choosen_department"
        ):
            today = datetime.date.today()
            department = get_object_or_404(
                DidatticaDipartimento,
                pk=department_form.cleaned_data["choosen_department"],
            )

            # Il dipartimento non deve essere già associato (principale o extra)
            already_associated = LaboratorioDipartimenti.objects.filter(
                Q(data_fine__isnull=True) | Q(data_fine__gte=today),
                laboratorio_dati_base=laboratory,
                didattica_dipartimento=department,
            ).exists()

            if already_associated:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(
                        "Extra departments must be different from the departments already associated with the Laboratory"
                    ),
                )
            else:
                with transaction.atomic():
                    LaboratorioDipartimenti.objects.create(
                        laboratorio_dati_base=laboratory,
                        didattica_dipartimento=department,
                        descr_dip_lab=department.dip_des_it,
                        principale=False,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                    laboratory.user_mod = request.user
                    laboratory.dt_mod = datetime.datetime.now()
                    laboratory.visibile = False
                    laboratory.save()

                log_action(
                    user=request.user,
                    obj=laboratory,
                    flag=ADDITION,
                    msg=_("Added extra department"),
                )

                messages.add_message(
                    request, messages.SUCCESS, _("Extra department added successfully")
                )
                return redirect(
                    "laboratories:management:laboratory-edit",
                    laboratory_id=laboratory_id,
                )

        else:  # pragma: no cover
            for k, v in department_form.errors.items():
                field = department_form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-extra-departments-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Extra Department"),
    }
    department_data = None
    return render(
        request,
        "laboratory_department.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": department_form,
            "laboratory": laboratory,
            "choosen_department": department_data,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("structures:apiv1:departments-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_extra_departments_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    # Solo dipartimenti extra di questo laboratorio (non il principale)
    extra_department_lab = get_object_or_404(
        LaboratorioDipartimenti,
        pk=data_id,
        laboratorio_dati_base=laboratory,
        principale=False,
    )

    with transaction.atomic():
        extra_department_lab.delete()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    log_action(
        user=request.user,
        obj=laboratory,
        flag=CHANGE,
        msg=_("Deleted extra department"),
    )

    messages.add_message(
        request, messages.SUCCESS, _("Extra department removed successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_researches_erc1_edit(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    # Previously selected researches
    researches_erc1_old = LaboratorioDatiErc1.objects.filter(
        laboratorio_dati_base=laboratory_id
    )

    # Ids to initialize form's checkboxes
    researches_erc1 = researches_erc1_old.values(
        "id",
        "ricerca_erc1",
        "ricerca_erc1__descrizione",
        "ricerca_erc1__ricerca_erc0_cod",
    )
    erc0 = (
        researches_erc1.first()["ricerca_erc1__ricerca_erc0_cod"]
        if researches_erc1.exists()
        else None
    )
    researches_erc1_ids = researches_erc1.values_list("ricerca_erc1", flat=True)
    fields = ["id_ricerche_erc1_ls", "id_ricerche_erc1_pe", "id_ricerche_erc1_sh"]
    researches_erc1_ids = tuple(map(str, researches_erc1_ids))
    initial = {}
    if erc0 is not None:
        for field in fields:
            if erc0.lower() in field:
                initial[field] = researches_erc1_ids
                initial["erc0_selector"] = erc0
                break

    research_erc1_form = LaboratorioDatiErc1Form(initial=initial)

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        research_erc1_form = LaboratorioDatiErc1Form(data=request.POST)
        if research_erc1_form.is_valid():
            erc0_selector = request.POST.get("erc0_selector")
            selected_erc1_res_ids = research_erc1_form.cleaned_data.get(
                f"id_ricerche_erc1_{erc0_selector.lower()}", []
            )

            LaboratorioDatiErc1.objects.filter(
                laboratorio_dati_base=laboratory_id
            ).exclude(ricerca_erc1__in=selected_erc1_res_ids).delete()

            current_erc1_res_ids = LaboratorioDatiErc1.objects.filter(
                laboratorio_dati_base=laboratory_id
            ).values_list("ricerca_erc1", flat=True)
            current_erc1_res_ids = map(str, current_erc1_res_ids)

            current_erc1_res = list(
                set(selected_erc1_res_ids) - set(current_erc1_res_ids)
            )
            erc1_researches = RicercaErc1.objects.filter(id__in=current_erc1_res)

            for research in erc1_researches:
                LaboratorioDatiErc1.objects.create(
                    laboratorio_dati_base=laboratory, ricerca_erc1=research
                )

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Edited ERC classification"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("ERC classification edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-researches-erc1-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): _("ERC classification"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (research_erc1_form,),
            "laboratory": laboratory,
            "erc_form": 1,
            "item_label": _("ERC classification"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


# Can be viewed by validators but not modified
@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_locations_edit(
    request,
    data_id,
    laboratory_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    location = get_object_or_404(
        LaboratorioUbicazione, pk=data_id, laboratorio_dati_base=laboratory
    )
    location_form = LaboratorioUbicazioneForm(instance=location)

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        location_form = LaboratorioUbicazioneForm(instance=location, data=request.POST)
        if location_form.is_valid():
            with transaction.atomic():
                location = location_form.save(commit=False)
                location.dt_mod = datetime.date.today()
                location.id_user_mod = request.user
                location.save()

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Edited laboratory location"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Location edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in location_form.errors.items():
                field = location_form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-locations-edit",
            kwargs={"laboratory_id": laboratory_id, "data_id": data_id},
        ): _("Location"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (location_form,),
            "item_label": _("Location"),
            "laboratory": laboratory,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_locations_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    location_form = LaboratorioUbicazioneForm()
    if request.POST:
        location_form = LaboratorioUbicazioneForm(data=request.POST)
        if location_form.is_valid():
            with transaction.atomic():
                location = location_form.save(commit=False)
                location.laboratorio_dati_base = laboratory
                location.dt_mod = datetime.date.today()
                location.id_user_mod = request.user
                location.save()

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Added laboratory location"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Location added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in location_form.errors.items():
                field = location_form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-locations-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Locations"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (location_form,),
            "laboratory": laboratory,
            "item_label": _("Location"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_locations_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    location = get_object_or_404(
        LaboratorioUbicazione, pk=data_id, laboratorio_dati_base=laboratory
    )

    with transaction.atomic():
        location.delete()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted location")
    )

    messages.add_message(request, messages.SUCCESS, _("Location removed successfully"))
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_research_staff_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    researcher = None
    internal_form = ChoosenPersonForm(required=True)
    external_form = LaboratorioPersonaleForm()

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioPersonaleForm(data=request.POST)
        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            today = datetime.date.today()

            with transaction.atomic():
                role = LaboratorioRuolo.objects.filter(
                    descr_ruolo_it=ROLE_RESEARCH_STAFF[0]
                ).first()
                if role is None:
                    role = LaboratorioRuolo.objects.create(
                        descr_ruolo_it=ROLE_RESEARCH_STAFF[0],
                        descr_ruolo_en=ROLE_RESEARCH_STAFF[1],
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                if form.cleaned_data.get("choosen_person"):
                    researcher = get_object_or_404(
                        Personale,
                        matricola=get_personale_matricola(
                            form.cleaned_data["choosen_person"]
                        ),
                    )
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=researcher,
                        nome_cognome=f"{researcher.cognome} {researcher.nome}",
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )
                else:
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=None,
                        nome_cognome=form.cleaned_data["laboratory_staff"],
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Added laboratory researcher"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Researcher added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-research-staff-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Research Staff"),
    }
    return render(
        request,
        "laboratory_choose_person.html",
        {
            "breadcrumbs": breadcrumbs,
            "laboratory": laboratory,
            "choosen_person": researcher,
            "internal_form": internal_form,
            "external_form": external_form,
            "item_label": _("Research Staff Member"),
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_research_staff_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    researcher = get_object_or_404(
        LaboratorioAffiliati,
        pk=data_id,
        laboratorio_dati_base=laboratory,
        laboratorio_ruolo__descr_ruolo_it=ROLE_RESEARCH_STAFF[0],
    )

    with transaction.atomic():
        researcher.delete()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted researcher")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Researcher removed successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_technical_staff_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
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
            today = datetime.date.today()
            role_descr = technician_form.cleaned_data["ruolo"]

            with transaction.atomic():
                # Il ruolo è testo libero nel form: lo cerco o lo creo in anagrafica
                role = LaboratorioRuolo.objects.filter(
                    descr_ruolo_it=role_descr
                ).first()
                if role is None:
                    role = LaboratorioRuolo.objects.create(
                        descr_ruolo_it=role_descr,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                if person_form.cleaned_data.get("choosen_person"):
                    technician = get_object_or_404(
                        Personale,
                        matricola=get_personale_matricola(
                            person_form.cleaned_data["choosen_person"]
                        ),
                    )
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=technician,
                        nome_cognome=f"{technician.cognome} {technician.nome}",
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )
                else:
                    LaboratorioAffiliati.objects.create(
                        laboratorio_dati_base=laboratory,
                        matricola_personale=None,
                        nome_cognome=person_form.cleaned_data["laboratory_staff"],
                        laboratorio_ruolo=role,
                        data_inizio=today,
                        dt_mod=today,
                        id_user_mod=request.user,
                    )

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Added laboratory technician"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("technician added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for f in (person_form, technician_form):
                for k, v in f.errors.items():
                    field = f.fields.get(k)
                    label = field.label if field else _("Error")
                    messages.add_message(
                        request, messages.ERROR, f"<b>{label}</b>: {v}"
                    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-technical-staff-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Technical Staff"),
    }
    return render(
        request,
        "laboratory_technician.html",
        {
            "breadcrumbs": breadcrumbs,
            "laboratory": laboratory,
            "choosen_person": technician,
            "internal_form": internal_form,
            "external_form": external_form,
            "form": technician_form,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_technical_staff_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    technician = get_object_or_404(
        LaboratorioAffiliati, pk=data_id, laboratorio_dati_base=laboratory
    )

    with transaction.atomic():
        technician.delete()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted technician")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Technician removed successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_services_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    form = LaboratorioServiziForm()
    if request.POST:
        form = LaboratorioServiziForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                service = form.save(commit=False)
                service.laboratorio_dati_base = laboratory
                service.dt_mod = datetime.date.today()
                service.id_user_mod = request.user
                service.save()

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Added service"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Service added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-services-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Service"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (form,),
            "item_label": _("Service"),
            "laboratory": laboratory,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_services_edit(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    service = get_object_or_404(
        LaboratorioServizi, pk=data_id, laboratorio_dati_base=laboratory
    )
    form = LaboratorioServiziForm(instance=service)

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioServiziForm(data=request.POST, instance=service)

        if form.is_valid():
            with transaction.atomic():
                service = form.save(commit=False)
                service.dt_mod = datetime.date.today()
                service.id_user_mod = request.user
                service.save()

                laboratory.user_mod = request.user
                laboratory.dt_mod = datetime.datetime.now()
                laboratory.visibile = False
                laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Edited service"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Service edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                field = form.fields.get(k)
                label = field.label if field else _("Error")
                messages.add_message(request, messages.ERROR, f"<b>{label}</b>: {v}")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-services-edit",
            kwargs={"laboratory_id": laboratory_id, "data_id": data_id},
        ): _("Service"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (form,),
            "laboratory": laboratory,
            "item_label": _("Service"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_services_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    service = get_object_or_404(
        LaboratorioServizi, pk=data_id, laboratorio_dati_base=laboratory
    )

    with transaction.atomic():
        service.delete()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    log_action(user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted service"))

    messages.add_message(request, messages.SUCCESS, _("Service removed successfully"))
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_activities_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    activity_types_already_specified = LaboratorioAttivita.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).values_list("tipologia_attivita", flat=True)

    if activity_types_already_specified and len(activity_types_already_specified) >= 3:
        messages.add_message(request, messages.ERROR, _("Activities list is full"))
        return redirect(
            "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
        )

    activity_form = LaboratorioAttivitaForm(
        activity_types_already_specified=activity_types_already_specified
    )

    if request.POST:
        activity_form = LaboratorioAttivitaForm(
            activity_types_already_specified=activity_types_already_specified,
            data=request.POST,
        )
        if activity_form.is_valid():
            activity_type = get_object_or_404(
                LaboratorioTipologiaAttivita,
                pk=activity_form.cleaned_data["tipologia_attivita"],
            )
            activity = activity_form.save(commit=False)
            activity.laboratorio_dati_base = laboratory
            activity.tipologia_attivita = activity_type
            activity.save()

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user, obj=laboratory, flag=CHANGE, msg=_("Added activity")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Activities added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in activity_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{activity_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-activities-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Activities"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (activity_form,),
            "laboratory": laboratory,
            "item_label": _("Activity"),
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_activities_edit(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    selected_activity_id = activity.tipologia_attivita.id
    selected_activity_type = get_object_or_404(
        LaboratorioTipologiaAttivita, pk=selected_activity_id
    )

    activity_types_already_specified = (
        LaboratorioAttivita.objects.filter(laboratorio_dati_base=laboratory_id)
        .exclude(tipologia_attivita=selected_activity_type)
        .values_list("tipologia_attivita", flat=True)
    )

    activity_form = LaboratorioAttivitaForm(
        activity_types_already_specified=activity_types_already_specified,
        instance=activity,
        initial={"tipologia_attivita": selected_activity_id},
    )

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        activity_form = LaboratorioAttivitaForm(
            activity_types_already_specified=activity_types_already_specified,
            instance=activity,
            data=request.POST,
        )
        if activity_form.is_valid():
            activity_type = get_object_or_404(
                LaboratorioTipologiaAttivita,
                pk=activity_form.cleaned_data["tipologia_attivita"],
            )
            activity = activity_form.save(commit=False)
            activity.tipologia_attivita = activity_type
            activity.save()

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user, obj=laboratory, flag=CHANGE, msg=_("Edited activity")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Activity edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in activity_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{activity_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-activities-edit",
            kwargs={"laboratory_id": laboratory_id, "data_id": data_id},
        ): _("Activity"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (activity_form,),
            "laboratory": laboratory,
            "item_label": _("Activity"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_activities_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    activity = get_object_or_404(LaboratorioAttivita, pk=data_id)
    activity.delete()

    laboratory.user_mod = request.user
    laboratory.dt_mod = datetime.datetime.now()
    laboratory.visibile = False
    laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted activity")
    )

    messages.add_message(request, messages.SUCCESS, _("Activity removed successfully"))
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_provided_services_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
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
            provided_service.laboratorio_dati_base = laboratory

            if person_form.cleaned_data.get("choosen_person"):
                manager_code = get_personale_matricola(
                    person_form.cleaned_data["choosen_person"]
                )
                manager = get_object_or_404(Personale, matricola=manager_code)
                provided_service.matricola_responsabile = manager_code
                provided_service.responsabile_origine = (
                    f"{manager.cognome} {manager.nome}"
                )
            else:
                provided_service.matricola_responsabile = None
                provided_service.responsabile_origine = person_form.cleaned_data[
                    "laboratory_manager"
                ]

            provided_service.save()

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Added provided service"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Provided service added successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in person_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{person_form.fields[k].label}</b>: {v}",
                )
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-provided-services-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Provided Service"),
    }
    return render(
        request,
        "laboratory_provided_service.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "laboratory": laboratory,
            "choosen_person": manager,
            "internal_form": internal_form,
            "external_form": external_form,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_provided_services_edit(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    manager = None
    cpf_initial = {}
    lpf_initial = {}
    manager_origine = None
    if provided_service.matricola_responsabile:
        manager = get_object_or_404(
            Personale, matricola=provided_service.matricola_responsabile
        )
        cpf_initial["choosen_person"] = provided_service.matricola_responsabile.id_ab
        manager_origine = f"{manager.cognome} {manager.nome}"
    else:
        lpf_initial["laboratory_manager"] = provided_service.responsabile_origine

    internal_form = ChoosenPersonForm(initial=cpf_initial, required=False)
    external_form = LaboratorioServiziErogatiResponsabileForm(initial=lpf_initial)
    form = LaboratorioServiziErogatiForm(instance=provided_service)

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioServiziErogatiForm(
            data=request.POST, instance=provided_service
        )

        if "choosen_person" in request.POST and request.POST["choosen_person"]:
            person_form = ChoosenPersonForm(
                initial=cpf_initial, data=request.POST, required=False
            )
        else:
            person_form = LaboratorioServiziErogatiResponsabileForm(
                initial=lpf_initial, data=request.POST
            )

        if person_form.is_valid() and form.is_valid():
            provided_service = form.save(commit=False)

            if person_form.cleaned_data.get("choosen_person"):
                manager_code = get_personale_matricola(
                    person_form.cleaned_data["choosen_person"]
                )
                manager = get_object_or_404(Personale, matricola=manager_code)
                provided_service.matricola_responsabile = manager_code
                provided_service.responsabile_origine = (
                    f"{manager.cognome} {manager.nome}"
                )
            elif person_form.cleaned_data.get("laboratory_manager"):
                provided_service.matricola_responsabile = None
                provided_service.responsabile_origine = person_form.cleaned_data[
                    "laboratory_manager"
                ]

            provided_service.save()

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Edited provided service"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Provided service edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

        else:  # pragma: no cover
            for k, v in person_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{person_form.fields[k].label}</b>: {v}",
                )
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

            internal_form = ChoosenPersonForm(initial=cpf_initial, required=False)
            external_form = LaboratorioServiziErogatiResponsabileForm(
                initial=lpf_initial
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-provided-services-edit",
            kwargs={"laboratory_id": laboratory_id, "data_id": data_id},
        ): _("Provided Service"),
    }
    return render(
        request,
        "laboratory_provided_service.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "laboratory": laboratory,
            "choosen_person": manager_origine,
            "internal_form": internal_form,
            "external_form": external_form,
            "provided_service": provided_service,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_provided_services_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    provided_service = get_object_or_404(LaboratorioServiziErogati, pk=data_id)
    provided_service.delete()

    laboratory.user_mod = request.user
    laboratory.dt_mod = datetime.datetime.now()
    laboratory.visibile = False
    laboratory.save()

    log_action(
        user=request.user,
        obj=laboratory,
        flag=CHANGE,
        msg=_("Deleted provided service"),
    )

    messages.add_message(
        request, messages.SUCCESS, _("Provided service removed successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_offered_services_new(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    form = LaboratorioServiziOffertiForm()
    if request.POST:
        form = LaboratorioServiziOffertiForm(data=request.POST)
        offered_service = form.save(commit=False)
        offered_service.laboratorio_dati_base = laboratory
        offered_service.save()

        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

        log_action(
            user=request.user,
            obj=laboratory,
            flag=CHANGE,
            msg=_("Added offered service"),
        )

        messages.add_message(
            request, messages.SUCCESS, _("Offered service added successfully")
        )
        return redirect(
            "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
        )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-offered-services-new",
            kwargs={"laboratory_id": laboratory_id},
        ): _("Offered Service"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (form,),
            "item_label": _("Offered Service"),
            "laboratory": laboratory,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_offered_services_edit(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    form = LaboratorioServiziOffertiForm(instance=offered_service)

    if request.POST:
        if not (
            request.user.is_superuser
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        form = LaboratorioServiziOffertiForm(
            data=request.POST, instance=offered_service
        )

        if form.is_valid():
            offered_service = form.save()

            laboratory.user_mod = request.user
            laboratory.dt_mod = datetime.datetime.now()
            laboratory.visibile = False
            laboratory.save()

            log_action(
                user=request.user,
                obj=laboratory,
                flag=CHANGE,
                msg=_("Edited offered service"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Offered service edited successfully")
            )
            return redirect(
                "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("laboratories:management:laboratories"): _("Laboratories"),
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory_id},
        ): laboratory.nome_laboratorio,
        reverse(
            "laboratories:management:laboratory-offered-services-edit",
            kwargs={"laboratory_id": laboratory_id, "data_id": data_id},
        ): _("Offered Service"),
    }
    return render(
        request,
        "laboratory_unique_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "forms": (form,),
            "laboratory": laboratory,
            "offered_service": offered_service,
            "item_label": _("Offered Service"),
            "edit": 1,
            "user_roles": _get_user_roles(
                request, laboratory, my_offices, is_validator
            ),
        },
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_offered_services_delete(
    request,
    laboratory_id,
    data_id,
    laboratory=None,
    my_offices=None,
    is_validator=False,
):
    offered_service = get_object_or_404(LaboratorioServiziOfferti, pk=data_id)
    offered_service.delete()

    laboratory.user_mod = request.user
    laboratory.dt_mod = datetime.datetime.now()
    laboratory.visibile = False
    laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Deleted offered service")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Offered service removed successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
@can_edit_laboratories
def laboratory_request_approval(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    if laboratory.visibile:
        return custom_message(request, _("Laboratory is already visible"))

    # LaboratorioDipartimenti
    if not LaboratorioDipartimenti.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).exists():
        messages.add_message(
            request,
            messages.ERROR,
            _("Laboratory must have at least one Department"),
        )
        return redirect(
            "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
        )

    # LaboratorioDatiErc1
    if not LaboratorioDatiErc1.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).exists():
        messages.add_message(
            request,
            messages.ERROR,
            _("Laboratory must have at least one ERC 1 Research"),
        )
        return redirect(
            "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
        )

    # LaboratorioUbicazione
    if not LaboratorioUbicazione.objects.filter(
        laboratorio_dati_base=laboratory_id
    ).exists():
        messages.add_message(
            request, messages.ERROR, _("Laboratory must have at least one Location")
        )
        return redirect(
            "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
        )

    validators = OrganizationalStructureOfficeEmployee.objects.filter(
        office__is_active=True,
        office__name=OFFICE_LABORATORY_VALIDATORS,
        office__organizational_structure__is_active=True,
    ).values_list("employee_id__email", flat=True)

    validators = list(set(validators))
    lab_url = request.build_absolute_uri(
        reverse(
            "laboratories:management:laboratory-edit",
            kwargs={"laboratory_id": laboratory.id},
        )
    )

    send_mail(
        TO_VALIDATORS_EMAIL_SUBJECT,
        f"{TO_VALIDATORS_EMAIL_MESSAGE} {laboratory.nome_laboratorio} {lab_url}",
        settings.DEFAULT_FROM_EMAIL,
        validators,
        fail_silently=True,
    )

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Requested approval")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Request for approval sent successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )


@login_required
@can_manage_laboratories
@can_view_laboratories
def laboratory_approve(
    request, laboratory_id, laboratory=None, my_offices=None, is_validator=False
):
    if not (request.user.is_superuser or is_validator):
        return custom_message(request, _("Permission denied"))
    if laboratory.visibile:
        return custom_message(request, _("Laboratory is already visible"))

    laboratory.visibile = True
    laboratory.save()

    log_action(
        user=request.user, obj=laboratory, flag=CHANGE, msg=_("Approved Laboratory")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Laboratory approved successfully")
    )
    return redirect(
        "laboratories:management:laboratory-edit", laboratory_id=laboratory_id
    )
