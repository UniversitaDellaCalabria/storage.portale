import datetime
import logging

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from addressbook.utils import get_personale_matricola
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings

from advanced_training.management.decorators import (
    can_manage_advanced_training,
    can_view_advanced_training,
    can_manage_consiglio_interno,
    can_change_master_status,
    # ~ check_temporal_window,
)
from advanced_training.management.forms import (
    ChoosenPersonForm,
    ConsiglioInternoEsternoForm,
    ConsiglioScientificoEsternoForm,
    ConsiglioScientificoEsternoFormSet,
    DirettoreScientificoEsternoForm,
    IncaricoDidatticoForm,
    IncaricoDidatticoFormSet,
    MasterDatiBaseForm,
    PartnerForm,
    PartnerFormSet,
    PianoDidatticoForm,
    PianoDidatticoFormSet,
    ProponenteEsternoForm,
    MasterTirocinioForm,
    MasterProvaFinaleForm,
)
from advanced_training.models import (
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneFinestraTemporale,
    AltaFormazioneIncaricoDidattico,
    AltaFormazionePartner,
    AltaFormazionePianoDidattico,
    AltaFormazioneStatus,
    AltaFormazioneStatusStorico,
)
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING,
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
)
from structures.models import DidatticaDipartimento
from addressbook.models import Personale
from generics.utils import custom_message, encrypt, log_action, download_file
from locks.concurrency import get_lock_from_cache
from locks.exceptions import LockCannotBeAcquiredException
from organizational_area.models import OrganizationalStructureOfficeEmployee

logger = logging.getLogger(__name__)

FORMSET_CLASSES = (
    IncaricoDidatticoFormSet,
    PianoDidatticoFormSet,
    PartnerFormSet,
    ConsiglioScientificoEsternoFormSet,
    ConsiglioInternoEsternoForm,
)

TAB_FORMSET_MAP = {
    "Incarichi Didattici": (IncaricoDidatticoFormSet, "tabs/incarichi_didattici.html"),
    "Piano Didattico": (PianoDidatticoFormSet, "tabs/piano_didattico.html"),
    "Partner": (PartnerFormSet, "tabs/partner.html"),
    "Consiglio Scientifico Esterno": (
        ConsiglioScientificoEsternoFormSet,
        "tabs/consiglio_esterno.html",
    ),
    "Tirocinio": (MasterTirocinioForm, "tabs/tirocinio.html"),
    "Prova Finale": (MasterProvaFinaleForm, "tabs/prova_finale.html"),
}

OPTIONAL_MOTIVATION_STATUSES = {"1", "3"}


def _get_status_badge_class(status_cod):
    return {
        "0": "secondary",
        "1": "warning",
        "2": "info",
        "3": "success",
        "4": "danger",
    }.get(status_cod, "secondary")


def get_current_status(master):
    entry = (
        AltaFormazioneStatusStorico.objects.filter(id_alta_formazione_dati_base=master)
        .select_related("id_alta_formazione_status", "utente_cambio_stato")
        .order_by("-data_status", "-dt_mod", "-id")
        .first()
    )
    if entry:
        cod = entry.id_alta_formazione_status.status_cod
        utente = entry.utente_cambio_stato
        return {
            "cod": cod,
            "description": entry.id_alta_formazione_status.status_desc,
            "badge_class": _get_status_badge_class(cod),
            "motivazione": entry.motivazione or "",
            "data_status": entry.data_status,
            "utente": f"{utente.get_full_name() or utente.username}" if utente else "",
            "dipartimento_utente": entry.dipartimento_utente or "",
            "dipartimento_master": entry.dipartimento_master or "",
        }
    return {
        "cod": "3",
        "description": "Approvato",
        "badge_class": "success",
        "motivazione": "",
        "data_status": None,
        "utente": "",
        "dipartimento_utente": "",
        "dipartimento_master": "",
    }


def _get_user_office_info(user):
    """Return a dict with office membership details for the given user."""
    all_offices = OrganizationalStructureOfficeEmployee.objects.filter(
        employee=user,
        office__is_active=True,
        office__organizational_structure__is_active=True,
    )
    names = list(all_offices.values_list("office__name", flat=True))
    master_offices = all_offices.filter(office__name=OFFICE_ADVANCED_TRAINING)
    is_validator = OFFICE_ADVANCED_TRAINING_VALIDATOR in names
    return {
        "all_offices": all_offices,
        "names": names,
        "master_offices": master_offices,
        "is_validator": is_validator,
    }


def _save_formset(form, user):
    objs = form.save(commit=False)
    for obj in objs:
        obj.dt_mod = timezone.now()
        obj.user_mod_id = user.id
        obj.save()
    form.save_m2m()
    for deleted in form.deleted_objects:
        deleted.delete()


@login_required
@can_manage_advanced_training
def advancedtraining_masters(request, advanced_training=None, my_offices=None, is_validator=False):
    return render(
        request,
        "advanced-training.html",
        {
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                "#": _("Advanced Training"),
            },
            "url": reverse("advanced-training:apiv2:advanced-training-list"),
            "is_validator": is_validator,
        },
    )


@login_required
@can_manage_advanced_training
@can_view_advanced_training
def advancedtraining_info_edit(
    request, pk, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    current_status = get_current_status(master)
    current_status_cod = current_status["cod"]

    office_info = _get_user_office_info(request.user)
    user_is_validator = office_info["is_validator"]
    master_offices = office_info["master_offices"]

    department_code = (
        master.dipartimento_riferimento.dip_cod
        if master.dipartimento_riferimento
        else None
    )
    user_has_same_department = master_offices.filter(
        office__organizational_structure__unique_code=department_code
    ).exists()

    can_edit = master._check_edit_permission(office_info["names"])
    is_readonly = not can_edit or str(current_status_cod) in ["1", "3", "4"]

    can_validate_actions = user_is_validator and current_status_cod == "1"
    has_active_window = master.has_active_window()

    can_send_validation = (
        not user_is_validator
        and (
            (current_status_cod in ("0", None) and has_active_window)
            or
            current_status_cod == "2"
        )
        and (user_has_same_department or not master.dipartimento_riferimento)
    )

    allowed_department_codes = None
    if not user_is_validator and master_offices.exists():
        allowed_department_codes = list(
            set(
                master_offices.values_list(
                    "office__organizational_structure__unique_code", flat=True
                )
            )
        )

    dati_generali_form = MasterDatiBaseForm(
        instance=master,
        **(
            {"allowed_department_codes": allowed_department_codes}
            if allowed_department_codes is not None
            else {}
        ),
    )
    last_viewed_tab = request.GET.get("tab", "Dati generali")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        "#": _("Edit Master"),
    }

    logs_master = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(master).pk,
        object_id=master.pk,
    )

    def _render(extra=None):
        ctx = {
            "master": master,
            "dati_generali_form": dati_generali_form,
            "last_viewed_tab": last_viewed_tab,
            "breadcrumbs": breadcrumbs,
            "current_status_description": current_status["description"],
            "status_badge_class": current_status["badge_class"],
            "available_statuses": AltaFormazioneStatus.objects.all(),
            "current_status_cod": current_status_cod,
            "is_readonly": is_readonly,
            "is_validator": user_is_validator,
            "can_send_validation": can_send_validation,
            "can_validate_actions": can_validate_actions,
            "has_active_window": has_active_window,
            "user_has_same_department": user_has_same_department,
            "current_status_motivazione": current_status.get("motivazione", ""),
            "current_status_date": current_status.get("data_status"),
            "logs_master": logs_master,
            "current_status_utente": current_status.get("utente", ""),
            "current_status_dipartimento_utente": current_status.get(
                "dipartimento_utente", ""
            ),
            "current_status_dipartimento_master": current_status.get(
                "dipartimento_master", ""
            ),
        }
        if extra:
            ctx.update(extra)
        return render(request, "advanced-training-info.html", ctx)

    if request.method != "POST":
        return _render()

    if is_readonly:
        messages.error(
            request,
            _(
                "Impossibile modificare: il master è in sola lettura per lo stato corrente."
            ),
        )
        return redirect(
            reverse(
                "advanced-training:management:advanced-training-detail",
                args=[master.id],
            )
        )

    form_name = request.POST.get("tab_form_dict_key")
    last_viewed_tab = form_name
    form = None

    if form_name == "Dati generali":
        kwargs = {"data": request.POST, "files": request.FILES, "instance": master}
        if allowed_department_codes is not None:
            kwargs["allowed_department_codes"] = allowed_department_codes
        form = MasterDatiBaseForm(**kwargs)

        if form.is_valid():
            new_dept = form.cleaned_data.get("dipartimento_riferimento")
            if new_dept and not user_is_validator:
                if (
                    allowed_department_codes
                    and new_dept.dip_cod not in allowed_department_codes
                ):
                    messages.error(
                        request,
                        _(
                            "Non puoi assegnare il master a un dipartimento diverso dal tuo"
                        ),
                    )
                    dati_generali_form = form
                    return _render()

    elif form_name in TAB_FORMSET_MAP:
        FormClass, _template = TAB_FORMSET_MAP[form_name]
        form = FormClass(request.POST, instance=master)
    elif form_name == "Consiglio Scientifico Interno":
        form = ConsiglioInternoEsternoForm(request.POST, instance=master)

    if form and form.is_valid():
        if isinstance(form, FORMSET_CLASSES):
            _save_formset(form, request.user)
        else:
            if hasattr(form, '_ore_warning'):
                messages.warning(request, form._ore_warning)
            
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

        messages.success(
            request, f"({form_name}) - Dati master aggiornati con successo"
        )
        return redirect(
            f"{reverse('advanced-training:management:advanced-training-detail', args=[master.id])}?tab={form_name}"
        )

    if form:
        if form_name == "Dati generali":
            dati_generali_form = form
        if isinstance(form, FORMSET_CLASSES):
            for subform in form.forms:
                for field, errors in subform.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return _render()


@login_required
@require_http_methods(["GET"])
def advancedtraining_load_tab(request, pk, tab_name):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)
    current_status = get_current_status(master)
    is_readonly = str(current_status["cod"]) in ["1", "3", "4"]

    context = {"tab_name": tab_name, "is_readonly": is_readonly, "master": master}

    try:
        if tab_name == "Piano Didattico":
            FormClass, template = TAB_FORMSET_MAP[tab_name]
            context["form"] = FormClass(instance=master)

            ore_moduli = (
                master.altaformazionepianodidattico_set.aggregate(tot=Sum("num_ore"))["tot"] or 0
            )
            cfu_moduli = (
                master.altaformazionepianodidattico_set.aggregate(tot_cfu=Sum("cfu"))["tot_cfu"] or 0
            )
            ore_tirocinio = master.ore_stage_tirocinio or 0
            cfu_tirocinio = master.cfu_stage or 0
            cfu_prova_finale = master.cfu_prova_finale or 0

            context["ore_piano_totale"]    = ore_moduli + ore_tirocinio
            context["ore_piano_moduli"]    = ore_moduli
            context["ore_piano_tirocinio"] = ore_tirocinio
            context["cfu_piano_totale"]    = cfu_moduli + cfu_tirocinio + cfu_prova_finale
            context["cfu_piano_moduli"]    = cfu_moduli
            context["cfu_piano_tirocinio"] = cfu_tirocinio
            context["cfu_piano_prova_finale"] = cfu_prova_finale
        elif tab_name in TAB_FORMSET_MAP:
            FormClass, template = TAB_FORMSET_MAP[tab_name]
            context["form"] = FormClass(instance=master)
        elif tab_name in ["Tirocinio", "Prova Finale"]:
            FormClass, template = TAB_FORMSET_MAP[tab_name]
            context["form"] = FormClass(instance=master)
        elif tab_name == "Consiglio Scientifico Interno":
            template = "tabs/consiglio_interno.html"
            context["consiglio_members"] = (
                AltaFormazioneConsiglioScientificoInterno.objects.filter(
                    alta_formazione_dati_base=master
                )
                .select_related("matricola_cons")
                .order_by("nome_origine_cons")
            )
        else:
            return JsonResponse(
                {"error": "Tab non trovato", "tab_name": tab_name}, status=404
            )

        html = render(request, template, context).content.decode("utf-8")
        return JsonResponse({"html": html, "success": True})

    except Exception as e:
        return JsonResponse(
            {"error": f"Errore nel caricamento: {str(e)}", "tab_name": tab_name},
            status=500,
        )


@login_required
def advancedtraining_info_create(request):
    if not request.user.is_superuser:
        has_office = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
            office__name__in=[
                OFFICE_ADVANCED_TRAINING,
                OFFICE_ADVANCED_TRAINING_VALIDATOR,
            ],
        ).exists()
        if not has_office:
            return custom_message(
                request,
                _(
                    "Permission denied - You need to be part of a master office to create"
                ),
            )

    office_info = _get_user_office_info(request.user)
    user_is_validator = office_info["is_validator"]
    master_offices = office_info["master_offices"]

    allowed_department_codes = None
    if not user_is_validator:
        allowed_department_codes = (
            list(
                master_offices.values_list(
                    "office__organizational_structure__unique_code", flat=True
                )
            )
            or None
        )

    def _form_kwargs(extra=None):
        kwargs = {"instance": AltaFormazioneDatiBase()}
        if allowed_department_codes:
            kwargs["allowed_department_codes"] = allowed_department_codes
        if extra:
            kwargs.update(extra)
        return kwargs

    if request.method == "POST":
        form = MasterDatiBaseForm(
            **_form_kwargs({"data": request.POST, "files": request.FILES})
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=obj,
                flag=ADDITION,
                msg=_("Nuovo master creato"),
            )

            draft_status = AltaFormazioneStatus.objects.get(status_cod="0")
            AltaFormazioneStatusStorico.objects.create(
                motivazione="Nuovo master creato",
                data_status=timezone.now().date(),
                dt_mod=timezone.now(),
                user_mod_id=request.user.id,
                id_alta_formazione_dati_base=obj,
                id_alta_formazione_status=draft_status,
            )
            messages.success(request, "Nuovo master creato con successo")
            return redirect(
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    args=[obj.id],
                )
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    else:
        form = MasterDatiBaseForm(**_form_kwargs())

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": AltaFormazioneDatiBase(),
            "dati_generali_form": form,
            "last_viewed_tab": "Dati generali",
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                "#": _("New Master"),
            },
            "current_status_description": "Bozza",
            "status_badge_class": "secondary",
            "available_statuses": [],
            "current_status_cod": None,
            "is_readonly": False,
            "is_validator": user_is_validator,
            "can_send_validation": False,
            "can_validate_actions": False,
            # ~ "has_active_window": has_active_window(),
        },
    )


@login_required
def advancedtraining_info_delete(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    if get_current_status(master)["cod"] != "0":
        messages.error(request, _("Puoi eliminare solo master in stato Bozza"))
        return redirect("advanced-training:management:advanced-training-detail", pk=pk)

    if request.method == "POST":
        master_title = master.titolo_it
        master.delete()
        log_action(
            user=request.user,
            obj=master,
            flag=DELETION,
            msg=_("Eliminato master") + f": {master_title}",
        )
        messages.success(request, _("Master eliminato con successo"))
        return redirect("advanced-training:management:advanced-training")

    messages.error(request, _("Richiesta non valida"))
    return redirect("advanced-training:management:advanced-training-detail", pk=pk)


def _check_ore_piano_didattico(master):
    """
    Restituisce (ok, totale) dove ok=False se il totale è sotto 1500.
    """
    from django.db.models import Sum

    ore_moduli = (
        master.altaformazionepianodidattico_set.aggregate(tot=Sum("num_ore"))["tot"]
        or 0
    )
    ore_tirocinio = master.ore_stage_tirocinio or 0
    totale = ore_moduli + ore_tirocinio
    return totale == 1500, totale
    
def _check_cfu_piano_didattico(master):
    """
    Restituisce (ok, totale) dove ok=False se il totale è sotto 60.
    """
    from django.db.models import Sum

    cfu_moduli = (
        master.altaformazionepianodidattico_set.aggregate(tot=Sum("cfu"))["tot"]
        or 0
    )
    return cfu_moduli == 60, cfu_moduli

@login_required
# ~ @check_temporal_window(required=False)
@can_change_master_status
def advancedtraining_status_change(
    request, pk, status_cod, dati_base=None): #, has_active_window=None

    if request.method != "POST":
        return custom_message(request, _("Metodo non consentito"))
        
    if status_cod == "1":
        if not dati_base.has_active_window():
            messages.error(
                request,
                "Anno accademico non valido: l'anno di erogazione del master non è coerente con la finestra temporale attiva."
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )
            
        ore_ok, ore_totali = _check_ore_piano_didattico(dati_base)
        cfu_ok, cfu_totali = _check_cfu_piano_didattico(dati_base)
        # ~ if not ore_ok:
            # ~ messages.error(
                # ~ request,
                # ~ f"Impossibile inviare in validazione: il totale ore del piano didattico "
                # ~ f"+ tirocinio è {ore_totali} su 1500 richieste. "
                # ~ f"Completa il piano didattico prima di procedere."
            # ~ )
            # ~ return redirect(
                # ~ "advanced-training:management:advanced-training-detail", pk=pk
            # ~ )
        # ~ if not cfu_ok:
            # ~ messages.error(
                # ~ request,
                # ~ f"Impossibile inviare in validazione: il totale CFU del piano didattico "
                # ~ f"è {cfu_totali} su 60 richiesti. "
                # ~ f"Completa il piano didattico prima di procedere."
            # ~ )
            # ~ return redirect(
                # ~ "advanced-training:management:advanced-training-detail", pk=pk
            # ~ )
    

    try:
        content_type_id = ContentType.objects.get_for_model(dati_base).pk
        lock = get_lock_from_cache(content_type_id, dati_base.pk)
        if lock[0] and lock[0] != request.user.pk:
            raise LockCannotBeAcquiredException(lock)

        current = dati_base.get_current_status()
        old_status_cod = getattr(
            getattr(current, "id_alta_formazione_status", None), "status_cod", None
        )

        status = get_object_or_404(AltaFormazioneStatus, status_cod=status_cod)

        if old_status_cod == status_cod:
            messages.error(
                request, _("Advanced training is already") + f" '{status.status_desc}'"
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        motivazione = request.POST.get("motivazione", "").strip()
        if not motivazione and status_cod not in OPTIONAL_MOTIVATION_STATUSES:
            messages.error(
                request, _("Motivazione richiesta per questo cambiamento di stato.")
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        # ── Recupera il dipartimento dell'ufficio dell'utente ──
        user_office = (
            OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
                office__name__in=[
                    OFFICE_ADVANCED_TRAINING,
                    OFFICE_ADVANCED_TRAINING_VALIDATOR,
                ],
            )
            .select_related("office__organizational_structure")
            .first()
        )

        dipartimento_utente = (
            user_office.office.organizational_structure.unique_code
            if user_office
            else None
        )

        # ── Dipartimento del master al momento del cambio ──
        dipartimento_master = (
            dati_base.dipartimento_riferimento.dip_cod
            if dati_base.dipartimento_riferimento
            else None
        )

        AltaFormazioneStatusStorico.objects.create(
            motivazione=motivazione,
            data_status=timezone.now().date(),
            dt_mod=timezone.now(),
            user_mod_id=request.user.pk,
            id_alta_formazione_dati_base=dati_base,
            id_alta_formazione_status=status,
            utente_cambio_stato=request.user,
            dipartimento_utente=dipartimento_utente,
            dipartimento_master=dipartimento_master,
        )
        recipients = []
        if status_cod == "1":
            recipients = OrganizationalStructureOfficeEmployee.objects.filter(
                office__is_active=True,
                office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR,
                office__organizational_structure__is_active=True,
            ).values_list("employee__email", flat=True)
        else:
            recipients = OrganizationalStructureOfficeEmployee.objects.filter(
                office__is_active=True,
                office__name=OFFICE_ADVANCED_TRAINING,
                office__organizational_structure__unique_code=dipartimento_master,
                office__organizational_structure__is_active=True,
            ).values_list("employee__email", flat=True)

        recipients = list(set(recipients))

        master_url = request.build_absolute_uri(
            reverse(
                "advanced-training:management:advanced-training-detail",
                kwargs={"pk": dati_base.pk},
            )
        )

        send_mail(
            "Cambio stato Master",
            f"Il master '{dati_base.titolo_it}' è stato portato allo stato '{status.status_desc}'. {master_url}",
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=True,
        )

        try:
            log_action(
                user=request.user,
                obj=dati_base,
                flag=CHANGE,
                msg=_("Changed advanced training status to")
                + f" '{status.status_desc}'"
                + (
                    f" [dip. utente: {dipartimento_utente}]"
                    if dipartimento_utente
                    else ""
                ),
            )
        except Exception:
            logger.exception("log_action failed")

        messages.success(request, _("Advanced training status updated successfully"))

    except AltaFormazioneStatus.DoesNotExist:
        messages.error(request, _("Status not found"))
    except Exception as exc:
        logger.exception("Error changing advanced training status")
        messages.error(request, str(exc))

    return redirect("advanced-training:management:advanced-training-detail", pk=pk)


@login_required
@transaction.atomic
def advancedtraining_duplicate(request, pk):
    if not request.user.is_superuser:
        has_office = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
            office__name__in=[
                OFFICE_ADVANCED_TRAINING,
                # OFFICE_ADVANCED_TRAINING_VALIDATOR,
            ],
        )
        if not has_office.exists():
            return custom_message(
                request,
                _(
                    "Permission denied - You need to be part of a master office to duplicate"
                ),
            )

    old = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    relations = {
        "alta_formazione_dati_base": [
            list(old.altaformazioneconsiglioscientificoesterno_set.all()),
            list(old.altaformazioneconsiglioscientificointerno_set.all()),
            list(old.altaformazioneattivitaformative_set.all()),
            list(old.altaformazioneincaricodidattico_set.all()),
            list(old.altaformazionemodalitaselezione_set.all()),
            list(old.altaformazionepartner_set.all()),
            list(old.altaformazionepianodidattico_set.all()),
        ]
    }

    base_title = old.titolo_it
    new_title = f"{base_title} (copia)"
    counter = 1
    while AltaFormazioneDatiBase.objects.filter(titolo_it=new_title).exists():
        counter += 1
        new_title = f"{base_title} (copia {counter})"

    dip_cod = has_office.first().office.organizational_structure.unique_code

    old.pk = None
    old.titolo_it = new_title
    old.dt_mod = timezone.now()
    old.user_mod_id = request.user.id
    old.dipartimento_riferimento = DidatticaDipartimento.objects.filter(
        dip_cod=dip_cod
    ).first()

    old.save()
    new = old

    for fk_name, querysets in relations.items():
        for qs in querysets:
            for obj in qs:
                obj.pk = None
                setattr(obj, fk_name, new)
                obj.dt_mod = timezone.now()
                obj.user_mod_id = request.user.id
                obj.save()

    draft_status = AltaFormazioneStatus.objects.get(status_cod="0")
    AltaFormazioneStatusStorico.objects.create(
        motivazione="Master duplicato",
        data_status=timezone.now().date(),
        dt_mod=timezone.now(),
        user_mod_id=request.user.id,
        id_alta_formazione_dati_base=new,
        id_alta_formazione_status=draft_status,
    )

    messages.success(request, f"Master duplicato con successo come '{new_title}'")
    return redirect(
        reverse("advanced-training:management:advanced-training-detail", args=[new.id])
    )


def _apply_consiglio_member(consiglio_member, form):
    if form.cleaned_data.get("choosen_person"):
        member_id = get_personale_matricola(form.cleaned_data["choosen_person"])
        member = get_object_or_404(Personale, matricola=member_id)
        consiglio_member.matricola_cons = member
        consiglio_member.nome_origine_cons = f"{member.cognome} {member.nome}"
    else:
        consiglio_member.matricola_cons = None
        consiglio_member.nome_origine_cons = form.cleaned_data["nome_origine_cons"]


@login_required
@can_manage_consiglio_interno
def consiglio_interno_new(request, master_id, master=None):
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)

        if internal_form.is_valid():
            member = AltaFormazioneConsiglioScientificoInterno()
            member.alta_formazione_dati_base = master
            _apply_consiglio_member(member, internal_form)
            member.user_ins_id = request.user.id
            member.dt_mod = timezone.now()
            member.save()

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto membro consiglio interno: {member.nome_origine_cons}",
            )
            messages.success(request, _("Council member added successfully"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
            )

        for k, v in internal_form.errors.items():
            messages.error(request, f"<b>{internal_form.fields[k].label}</b>: {v}")

    return render(
        request,
        "forms/consiglio_interno_form.html",
        {
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": master_id},
                ): master.titolo_it,
                "#": _("New Council Member"),
            },
            "choosen_person": "",
            "internal_form": internal_form,
            "master": master,
            "url": reverse("teachers:apiv1:teachers-list"),
            "is_edit": False,
        },
    )


@login_required
@can_manage_consiglio_interno
def consiglio_interno_edit(request, master_id, consiglio_id, master=None):
    consiglio_member = get_object_or_404(
        AltaFormazioneConsiglioScientificoInterno.objects.select_related(
            "matricola_cons"
        ),
        pk=consiglio_id,
        alta_formazione_dati_base=master,
    )

    old_label = consiglio_member.nome_origine_cons
    staff = consiglio_member.matricola_cons
    member_data = f"{staff.cognome} {staff.nome}" if staff else ""
    initial = {"choosen_person": encrypt(staff.matricola)} if staff else {}

    internal_form = ChoosenPersonForm(initial=initial, required=True)
    external_form = ConsiglioInternoEsternoForm(instance=consiglio_member)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ConsiglioInternoEsternoForm(
            instance=consiglio_member, data=request.POST
        )
        form = internal_form if "choosen_person" in request.POST else external_form

        if form.is_valid():
            _apply_consiglio_member(consiglio_member, form)
            consiglio_member.user_mod_id = request.user.id
            consiglio_member.dt_mod = timezone.now()
            consiglio_member.save()

            if old_label != consiglio_member.nome_origine_cons:
                log_action(
                    user=request.user,
                    obj=master,
                    flag=CHANGE,
                    msg=f"Modificato membro consiglio interno: {old_label} → {consiglio_member.nome_origine_cons}",
                )

            messages.success(request, _("Council member data edited successfully"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
            )

        for k, v in form.errors.items():
            messages.error(request, f"<b>{form.fields[k].label}</b>: {v}")

    return render(
        request,
        "forms/consiglio_interno_form.html",
        {
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": master_id},
                ): master.titolo_it,
                "#": f"{_('Edit Council Member')} {consiglio_member.nome_origine_cons}",
            },
            "choosen_person": member_data,
            "external_form": external_form,
            "internal_form": internal_form,
            "master": master,
            "url": reverse("teachers:apiv1:teachers-list"),
            "is_edit": True,
        },
    )


@login_required
@can_manage_consiglio_interno
def consiglio_interno_delete(request, master_id, consiglio_id, master=None):
    consiglio_member = get_object_or_404(
        AltaFormazioneConsiglioScientificoInterno,
        pk=consiglio_id,
        alta_formazione_dati_base=master,
    )

    member_name = consiglio_member.nome_origine_cons
    consiglio_member.delete()

    log_action(
        user=request.user,
        obj=master,
        flag=DELETION,
        msg=f"Eliminato membro consiglio interno: {member_name}",
    )
    messages.success(request, _("Council member removed successfully"))

    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
    )


@login_required
def advancedtraining_proponente_edit(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    old_label = None
    initial = {}

    if master.matricola_proponente:
        staff = master.matricola_proponente
        old_label = f"{staff.cognome} {staff.nome}"
        initial = {"choosen_person": encrypt(staff.matricola)}
    else:
        old_label = (
            f"{master.cognome_proponente or ''} {master.nome_proponente or ''}".strip()
        )
        initial = {
            "nome_proponente": master.nome_proponente,
            "cognome_proponente": master.cognome_proponente,
        }

    external_form = ProponenteEsternoForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        if request.POST.get("choosen_person"):
            internal_form = ChoosenPersonForm(data=request.POST, required=True)
            form = internal_form
        else:
            external_form = ProponenteEsternoForm(data=request.POST)
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                member = get_object_or_404(
                    Personale,
                    matricola=get_personale_matricola(
                        form.cleaned_data["choosen_person"]
                    ),
                )
                master.matricola_proponente = member
                master.nome_proponente = member.nome
                master.cognome_proponente = member.cognome
            else:
                master.matricola_proponente = None
                master.nome_proponente = form.cleaned_data["nome_proponente"]
                master.cognome_proponente = form.cleaned_data["cognome_proponente"]

            master.dt_mod = timezone.now()
            master.user_mod_id = request.user.id
            master.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=_("Modificato proponente")
                + f": {master.cognome_proponente} {master.nome_proponente}".strip(),
            )
            messages.success(request, "Proponente salvato con successo.")
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        for k, v in form.errors.items():
            messages.error(request, f"<b>{form.fields[k].label}</b>: {v}")

    return render(
        request,
        "forms/proponente_form.html",
        {
            "master": master,
            "choosen_person": old_label,
            "external_form": external_form,
            "internal_form": internal_form,
            "item_label": _("Proponente"),
            "edit": bool(master.matricola_proponente or master.nome_proponente),
            "url": reverse("teachers:apiv1:teachers-list"),
            "including": "blocks/crud_teacherslist.html",
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Proponente"),
            },
        },
    )


@login_required
def advancedtraining_direttore_edit(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    old_label = None
    initial = {}

    if master.matricola_direttore_scientifico:
        staff = master.matricola_direttore_scientifico
        old_label = f"{staff.cognome} {staff.nome}"
        initial = {"choosen_person": encrypt(staff.matricola)}
    else:
        old_label = master.nome_origine_direttore_scientifico or ""
        initial = {
            "nome_origine_direttore_scientifico": master.nome_origine_direttore_scientifico,
        }

    external_form = DirettoreScientificoEsternoForm(initial=initial)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        if request.POST.get("choosen_person"):
            internal_form = ChoosenPersonForm(data=request.POST, required=True)
            form = internal_form
        else:
            external_form = DirettoreScientificoEsternoForm(data=request.POST)
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                member = get_object_or_404(
                    Personale,
                    matricola=get_personale_matricola(
                        form.cleaned_data["choosen_person"]
                    ),
                )
                master.matricola_direttore_scientifico = member
                master.nome_origine_direttore_scientifico = (
                    f"{member.cognome} {member.nome}"
                )
            else:
                master.matricola_direttore_scientifico = None
                master.nome_origine_direttore_scientifico = form.cleaned_data[
                    "nome_origine_direttore_scientifico"
                ]

            master.dt_mod = timezone.now()
            master.user_mod_id = request.user.id
            master.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=_("Modificato direttore scientifico")
                + f": {master.nome_origine_direttore_scientifico}",
            )
            messages.success(request, _("Direttore scientifico salvato con successo."))
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        for k, v in form.errors.items():
            messages.error(request, f"<b>{form.fields[k].label}</b>: {v}")

    return render(
        request,
        "forms/proponente_form.html",
        {
            "master": master,
            "choosen_person": old_label,
            "external_form": external_form,
            "internal_form": internal_form,
            "item_label": _("Direttore Scientifico"),
            "edit": bool(
                master.matricola_direttore_scientifico
                or master.nome_origine_direttore_scientifico
            ),
            "url": reverse("teachers:apiv1:teachers-list"),
            "including": "blocks/crud_teacherslist.html",
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Direttore Scientifico"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def incarico_didattico_new(
    request, pk, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    form = IncaricoDidatticoForm()

    if request.method == "POST":
        form = IncaricoDidatticoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.alta_formazione_dati_base = master
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto incarico didattico: {obj.modulo}",
            )
            messages.success(request, _("Incarico didattico aggiunto con successo"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Incarichi Didattici"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/incarico_didattico_form.html",
        {
            "master": master,
            "form": form,
            "is_edit": False,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Nuovo Incarico Didattico"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def incarico_didattico_edit(
    request,
    pk,
    incarico_id,
    advanced_training=None,
    my_offices=None,
    is_validator=False,
):
    master = advanced_training
    incarico = get_object_or_404(
        AltaFormazioneIncaricoDidattico,
        pk=incarico_id,
        alta_formazione_dati_base=master,
    )
    form = IncaricoDidatticoForm(instance=incarico)

    if request.method == "POST":
        form = IncaricoDidatticoForm(data=request.POST, files=request.FILES, instance=incarico)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=f"Modificato incarico didattico: {obj.modulo}",
            )
            messages.success(request, _("Incarico didattico modificato con successo"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Incarichi Didattici"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/incarico_didattico_form.html",
        {
            "master": master,
            "form": form,
            "incarico": incarico,
            "is_edit": True,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Modifica Incarico Didattico"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def incarico_didattico_delete(
    request,
    pk,
    incarico_id,
    advanced_training=None,
    my_offices=None,
    is_validator=False,
):
    master = advanced_training
    incarico = get_object_or_404(
        AltaFormazioneIncaricoDidattico,
        pk=incarico_id,
        alta_formazione_dati_base=master,
    )

    modulo_label = incarico.modulo or f"#{incarico.pk}"
    incarico.delete()

    log_action(
        user=request.user,
        obj=master,
        flag=DELETION,
        msg=f"Eliminato incarico didattico: {modulo_label}",
    )
    messages.success(request, _("Incarico didattico eliminato con successo"))
    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Incarichi Didattici"
    )


@login_required
@can_manage_advanced_training
def piano_didattico_new(
    request, pk, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    form = PianoDidatticoForm(master=master)

    if request.method == "POST":
        form = PianoDidatticoForm(data=request.POST, master=master)
        if form.is_valid():
            obj = form.save(commit=False)
            if hasattr(form, "_ore_warning"):
                messages.warning(request, form._ore_warning)
            obj.alta_formazione_dati_base = master
            # obj = form.save(commit=False)
            # obj.alta_formazione_dati_base = master
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()
            master.numero_moduli = master.altaformazionepianodidattico_set.count()
            master.save(update_fields=["numero_moduli"])

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto modulo piano didattico: {obj.modulo}",
            )
            messages.success(request, _("Modulo piano didattico aggiunto con successo"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Piano Didattico"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/piano_didattico_form.html",
        {
            "master": master,
            "form": form,
            "is_edit": False,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Nuovo Modulo Piano Didattico"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def piano_didattico_edit(
    request,
    pk,
    modulo_id,
    advanced_training=None,
    my_offices=None,
    is_validator=False,
):
    master = advanced_training
    modulo = get_object_or_404(
        AltaFormazionePianoDidattico,
        pk=modulo_id,
        alta_formazione_dati_base=master,
    )
    form = PianoDidatticoForm(instance=modulo, master=master)

    if request.method == "POST":
        form = PianoDidatticoForm(data=request.POST, instance=modulo, master=master)
        if form.is_valid():
            if hasattr(form, "_ore_warning"):
                messages.warning(request, form._ore_warning)
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=f"Modificato modulo piano didattico: {obj.modulo}",
            )
            messages.success(
                request, _("Modulo piano didattico modificato con successo")
            )
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Piano Didattico"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/piano_didattico_form.html",
        {
            "master": master,
            "form": form,
            "modulo": modulo,
            "is_edit": True,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Modifica Modulo Piano Didattico"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def piano_didattico_delete(
    request,
    pk,
    modulo_id,
    advanced_training=None,
    my_offices=None,
    is_validator=False,
):
    master = advanced_training
    modulo = get_object_or_404(
        AltaFormazionePianoDidattico,
        pk=modulo_id,
        alta_formazione_dati_base=master,
    )

    modulo_label = modulo.modulo or f"#{modulo.pk}"
    modulo.delete()
    master.numero_moduli = master.altaformazionepianodidattico_set.count()
    master.save(update_fields=["numero_moduli"])

    log_action(
        user=request.user,
        obj=master,
        flag=DELETION,
        msg=f"Eliminato modulo piano didattico: {modulo_label}",
    )
    messages.success(request, _("Modulo piano didattico eliminato con successo"))
    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Piano Didattico"
    )


@login_required
@can_manage_advanced_training
def partner_new(
    request, pk, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    form = PartnerForm()

    if request.method == "POST":
        form = PartnerForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.alta_formazione_dati_base = master
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto partner: {obj.denominazione}",
            )
            messages.success(request, _("Partner aggiunto con successo"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Partner"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/partner_form.html",
        {
            "master": master,
            "form": form,
            "is_edit": False,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Nuovo Partner"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def partner_edit(
    request, pk, partner_id, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    partner = get_object_or_404(
        AltaFormazionePartner,
        pk=partner_id,
        alta_formazione_dati_base=master,
    )
    form = PartnerForm(instance=partner)

    if request.method == "POST":
        form = PartnerForm(data=request.POST, instance=partner)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=f"Modificato partner: {obj.denominazione}",
            )
            messages.success(request, _("Partner modificato con successo"))
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Partner"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/partner_form.html",
        {
            "master": master,
            "form": form,
            "partner": partner,
            "is_edit": True,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Modifica Partner"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def partner_delete(
    request, pk, partner_id, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    partner = get_object_or_404(
        AltaFormazionePartner,
        pk=partner_id,
        alta_formazione_dati_base=master,
    )

    denominazione_label = partner.denominazione or f"#{partner.pk}"
    partner.delete()

    log_action(
        user=request.user,
        obj=master,
        flag=DELETION,
        msg=f"Eliminato partner: {denominazione_label}",
    )
    messages.success(request, _("Partner eliminato con successo"))
    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Partner"
    )


@login_required
@can_manage_advanced_training
def consiglio_esterno_new(
    request, pk, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    form = ConsiglioScientificoEsternoForm()

    if request.method == "POST":
        form = ConsiglioScientificoEsternoForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.alta_formazione_dati_base = master
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto membro consiglio esterno: {obj.nome_cons}",
            )
            messages.success(
                request, _("Membro consiglio esterno aggiunto con successo")
            )
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Consiglio Scientifico Esterno"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/consiglio_esterno_form.html",
        {
            "master": master,
            "form": form,
            "is_edit": False,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Nuovo Membro Consiglio Esterno"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def consiglio_esterno_edit(
    request, pk, cons_id, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    membro = get_object_or_404(
        AltaFormazioneConsiglioScientificoEsterno,
        pk=cons_id,
        alta_formazione_dati_base=master,
    )
    form = ConsiglioScientificoEsternoForm(instance=membro)

    if request.method == "POST":
        form = ConsiglioScientificoEsternoForm(data=request.POST, instance=membro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            log_action(
                user=request.user,
                obj=master,
                flag=CHANGE,
                msg=f"Modificato membro consiglio esterno: {obj.nome_cons}",
            )
            messages.success(
                request, _("Membro consiglio esterno modificato con successo")
            )
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Consiglio Scientifico Esterno"
            )

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"<b>{form.fields[field].label}</b>: {error}")

    return render(
        request,
        "forms/consiglio_esterno_form.html",
        {
            "master": master,
            "form": form,
            "membro": membro,
            "is_edit": True,
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                reverse("advanced-training:management:advanced-training"): _(
                    "Advanced Training"
                ),
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    kwargs={"pk": pk},
                ): master.titolo_it,
                "#": _("Modifica Membro Consiglio Esterno"),
            },
        },
    )


@login_required
@can_manage_advanced_training
def consiglio_esterno_delete(
    request, pk, cons_id, advanced_training=None, my_offices=None, is_validator=False
):
    master = advanced_training
    membro = get_object_or_404(
        AltaFormazioneConsiglioScientificoEsterno,
        pk=cons_id,
        alta_formazione_dati_base=master,
    )

    nome_label = membro.nome_cons or f"#{membro.pk}"
    membro.delete()

    log_action(
        user=request.user,
        obj=master,
        flag=DELETION,
        msg=f"Eliminato membro consiglio esterno: {nome_label}",
    )
    messages.success(request, _("Membro consiglio esterno eliminato con successo"))
    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[pk])}?tab=Consiglio Scientifico Esterno"
    )

@login_required
@can_manage_advanced_training
def download_delibera(request, pk, advanced_training=None, my_offices=None, is_validator=False):
    """
    Downloads attachment
    :return: file
    """
    master = get_object_or_404(
        AltaFormazioneDatiBase,
        pk=pk,
    )
    doc = master.path_doc_delibera
    if doc:
        result = download_file(doc.path)
        return result
    raise Http404

    
@login_required
@can_manage_advanced_training
def download_piano_finanziario(request, pk, advanced_training=None, my_offices=None, is_validator=False):
    """
    Downloads attachment
    :return: file
    """
    master = get_object_or_404(
        AltaFormazioneDatiBase,
        pk=pk,
    )
    doc = master.path_piano_finanziario
    if doc:
        result = download_file(doc.path)
        return result
    raise Http404

    
@login_required
@can_manage_advanced_training
def download_cv_incarico(request, pk, pk_incarico, advanced_training=None, my_offices=None, is_validator=False):
    """
    Downloads attachment
    :return: file
    """
    master = get_object_or_404(
        AltaFormazioneDatiBase,
        pk=pk,
    )
    incarico = get_object_or_404(
        AltaFormazioneIncaricoDidattico,
        alta_formazione_dati_base=master,
        pk=pk_incarico
    )
    doc = incarico.path_cv
    if doc:
        result = download_file(doc.path)
        return result
    raise Http404
