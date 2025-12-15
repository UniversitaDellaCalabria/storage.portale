import datetime
import logging


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_http_methods

from generics.utils import custom_message, log_action
from django.contrib.admin.models import CHANGE
from locks.concurrency import get_lock_from_cache
from locks.exceptions import LockCannotBeAcquiredException
from django.contrib.contenttypes.models import ContentType

from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneFinestraTemporale,
    AltaFormazioneStatus,
    AltaFormazioneStatusStorico,
)
from advanced_training.management.forms import (
    MasterDatiBaseForm,
    IncaricoDidatticoFormSet,
    PianoDidatticoFormSet,
    PartnerFormSet,
    ConsiglioScientificoEsternoFormSet,
    ConsiglioScientificoInternoFormSet,
)
from advanced_training.api.v2.views import AdvancedTrainingMastersViewSet
from advanced_training.management.decorators import check_temporal_window

logger = logging.getLogger(__name__)


def get_status_badge_class(status_cod):
    """Restituisce la classe CSS del badge in base al codice stato"""
    status_map = {
        "0": "secondary",
        "1": "warning",
        "2": "info",
        "3": "success",
        "4": "danger",
    }
    return status_map.get(status_cod, "secondary")


def get_current_status(master):
    """Ottiene lo stato corrente del master dal database"""
    status_storico = (
        AltaFormazioneStatusStorico.objects.filter(id_alta_formazione_dati_base=master)
        .order_by("-data_status", "-dt_mod", "-id")
        .first()
    )

    if status_storico:
        return {
            "cod": status_storico.id_alta_formazione_status.status_cod,
            "description": status_storico.id_alta_formazione_status.status_desc,
            "badge_class": get_status_badge_class(
                status_storico.id_alta_formazione_status.status_cod
            ),
        }

    return {"cod": None, "description": "Bozza", "badge_class": "secondary"}


def is_temporal_window_active():
    """Verifica se esiste una finestra temporale attiva"""
    today = datetime.date.today()
    return AltaFormazioneFinestraTemporale.objects.filter(
        data_inizio__lte=today, data_fine__gte=today
    ).exists()


def check_user_is_validator(user):
    """Verifica se l'utente ha ruolo di validatore"""
    # TODO: Implementare la logica specifica per il tuo sistema
    # Esempio: return user.groups.filter(name='Validators').exists()
    return user.is_staff or user.is_superuser


@login_required
def advancedtraining_masters(request):
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Advanced Training"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("advanced-training:apiv2:advanced-training-list"),
    }
    return render(request, "advanced-training.html", context)


@login_required
def advancedtraining_info_edit(request, pk):
    """Vista principale - carica solo i dati generali"""
    master = get_object_or_404(AdvancedTrainingMastersViewSet.queryset, pk=pk)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        "#": _("Edit Master"),
    }

    current_status = get_current_status(master)
    current_status_cod = current_status.get("cod")
    is_readonly = str(current_status_cod) in ["1", "3", "4"]
    has_active_window = is_temporal_window_active()
    available_statuses = AltaFormazioneStatus.objects.all()
    user_is_validator = check_user_is_validator(request.user)

    dati_generali_form = MasterDatiBaseForm(instance=master)

    last_viewed_tab = request.GET.get("tab", "Dati generali")

    if request.method == "POST":
        if is_readonly and not user_is_validator:
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
        form = None

        # Carica solo il form richiesto
        if form_name == "Dati generali":
            form = MasterDatiBaseForm(request.POST, request.FILES, instance=master)
        elif form_name == "Incarichi Didattici":
            form = IncaricoDidatticoFormSet(request.POST, instance=master)
        elif form_name == "Piano Didattico":
            form = PianoDidatticoFormSet(request.POST, instance=master)
        elif form_name == "Partner":
            form = PartnerFormSet(request.POST, instance=master)
        elif form_name == "Consiglio Scientifico Esterno":
            form = ConsiglioScientificoEsternoFormSet(request.POST, instance=master)
        elif form_name == "Consiglio Scientifico Interno":
            form = ConsiglioScientificoInternoFormSet(request.POST, instance=master)

        last_viewed_tab = form_name

        if form and form.is_valid():
            if isinstance(
                form,
                (
                    IncaricoDidatticoFormSet,
                    PianoDidatticoFormSet,
                    PartnerFormSet,
                    ConsiglioScientificoEsternoFormSet,
                    ConsiglioScientificoInternoFormSet,
                ),
            ):
                objs = form.save(commit=False)
                for obj in objs:
                    obj.dt_mod = timezone.now()
                    obj.user_mod_id = request.user.id
                    obj.save()
                form.save_m2m()

                for deleted_obj in form.deleted_objects:
                    deleted_obj.delete()
            else:
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
        else:
            if form:
                # Ricarica il form con errori
                dati_generali_form = (
                    form if form_name == "Dati generali" else dati_generali_form
                )

                if isinstance(
                    form,
                    (
                        IncaricoDidatticoFormSet,
                        PianoDidatticoFormSet,
                        PartnerFormSet,
                        ConsiglioScientificoEsternoFormSet,
                        ConsiglioScientificoInternoFormSet,
                    ),
                ):
                    for subform in form.forms:
                        for field, errors in subform.errors.items():
                            for error in errors:
                                messages.error(request, f"{field}: {error}")
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": master,
            "dati_generali_form": dati_generali_form,
            "last_viewed_tab": last_viewed_tab,
            "breadcrumbs": breadcrumbs,
            "current_status_description": current_status["description"],
            "status_badge_class": current_status["badge_class"],
            "available_statuses": available_statuses,
            "current_status_cod": current_status_cod,
            "is_readonly": is_readonly,
            "user_is_validator": user_is_validator,
            "can_send_validation": current_status_cod in ("0", "2", None)
            and has_active_window,
            "has_active_window": has_active_window,
        },
    )


@login_required
@require_http_methods(["GET"])
def advancedtraining_load_tab(request, pk, tab_name):
    """API endpoint per caricare lazy i tab"""
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    current_status = get_current_status(master)
    current_status_cod = current_status.get("cod")
    is_readonly = str(current_status_cod) in ["1", "3", "4"]
    user_is_validator = check_user_is_validator(request.user)

    # Determina quale form caricare
    form = None
    if tab_name == "Incarichi Didattici":
        form = IncaricoDidatticoFormSet(instance=master)
        template = "tabs/incarichi_didattici.html"
    elif tab_name == "Piano Didattico":
        form = PianoDidatticoFormSet(instance=master)
        template = "tabs/piano_didattico.html"
    elif tab_name == "Partner":
        form = PartnerFormSet(instance=master)
        template = "tabs/partner.html"
    elif tab_name == "Consiglio Scientifico Esterno":
        form = ConsiglioScientificoEsternoFormSet(instance=master)
        template = "tabs/consiglio_esterno.html"
    elif tab_name == "Consiglio Scientifico Interno":
        form = ConsiglioScientificoInternoFormSet(instance=master)
        template = "tabs/consiglio_interno.html"
    else:
        return JsonResponse({"error": "Tab non valido"}, status=400)

    # Render del template
    html = render(
        request,
        template,
        {
            "form": form,
            "tab_name": tab_name,
            "is_readonly": is_readonly,
            "user_is_validator": user_is_validator,
            "master": master,
        },
    ).content.decode("utf-8")

    return JsonResponse({"html": html})


@login_required
def advancedtraining_info_create(request):
    master = AltaFormazioneDatiBase()

    if request.method == "POST":
        form = MasterDatiBaseForm(request.POST, request.FILES, instance=master)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

            # Crea status iniziale
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
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = MasterDatiBaseForm(instance=master)

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": master,
            "dati_generali_form": form,
            "last_viewed_tab": "Dati generali",
            "current_status_description": "Bozza",
            "status_badge_class": "secondary",
            "available_statuses": [],
            "current_status_cod": None,
            "is_readonly": False,
            "user_is_validator": False,
            "can_send_validation": False,
            "has_active_window": is_temporal_window_active(),
        },
    )


@login_required
def advancedtraining_info_delete(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    # Verifica stato - può eliminare solo in stato 0 (Bozza)
    current_status = get_current_status(master)
    if current_status.get("cod") not in [None, "0"]:
        messages.error(request, _("Puoi eliminare solo master in stato Bozza"))
        return redirect("advanced-training:management:advanced-training-detail", pk=pk)

    if request.method == "POST":
        master.delete()
        messages.success(request, _("Master eliminato con successo"))
        return redirect("advanced-training:management:advanced-training")

    messages.error(request, _("Richiesta non valida"))
    return redirect("advanced-training:management:advanced-training-detail", pk=pk)


@login_required
@check_temporal_window(allowed_statuses=["0", "2"])
def advancedtraining_status_change(request, pk, status_cod):
    """Gestisce il cambio di stato del master"""
    if request.method != "POST":
        return custom_message(request, _("Metodo non consentito"))

    dati_base = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    # Verifica permessi
    user_permissions_and_offices = dati_base.get_user_permissions_and_offices(
        request.user
    )
    if (
        not user_permissions_and_offices["permissions"]["access"]
        or not user_permissions_and_offices["permissions"]["edit"]
    ):
        return custom_message(request, _("Permission denied"))

    try:
        # Verifica lock
        content_type_id = ContentType.objects.get_for_model(dati_base).pk
        lock = get_lock_from_cache(content_type_id, dati_base.pk)
        if lock[0] and not lock[0] == request.user.pk:
            raise LockCannotBeAcquiredException(lock)

        # Ottieni stato corrente
        dati_base_status = (
            AltaFormazioneStatusStorico.objects.filter(
                id_alta_formazione_dati_base=dati_base
            )
            .order_by("-data_status", "-dt_mod", "-id")
            .first()
        )

        old_status = None
        if dati_base_status:
            old_status = getattr(
                dati_base_status.id_alta_formazione_status, "status_cod", None
            )

        # Ottieni nuovo stato
        status = get_object_or_404(AltaFormazioneStatus, status_cod=status_cod)

        # Verifica se lo stato è già quello attuale
        if old_status == status_cod:
            messages.error(
                request,
                _("Advanced training is already") + f" '{status.status_desc}'",
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        # Ottieni motivazione
        motivazione = request.POST.get("motivazione", "").strip()
        if not motivazione:
            messages.error(
                request,
                _("Motivazione richiesta per questo cambiamento di stato."),
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        # Crea nuovo record nello storico
        AltaFormazioneStatusStorico.objects.create(
            motivazione=motivazione,
            data_status=timezone.now().date(),
            dt_mod=timezone.now(),
            user_mod_id=request.user.pk,
            id_alta_formazione_dati_base=dati_base,
            id_alta_formazione_status=status,
        )

        # Log dell'azione
        try:
            log_action(
                user=request.user,
                obj=dati_base,
                flag=CHANGE,
                msg=_("Changed advanced training status to")
                + f" '{status.status_desc}'",
            )
        except Exception:
            logger.exception("log_action failed or not available")

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
    """Duplica un master con tutte le sue relazioni"""
    old = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    # Fetch delle relazioni (NON includere status_storico)
    consiglio_esterno = list(old.altaformazioneconsiglioscientificoesterno_set.all())
    consiglio_interno = list(old.altaformazioneconsiglioscientificointerno_set.all())
    attivita_formative = list(old.altaformazioneattivitaformative_set.all())
    incarichi_didattici = list(old.altaformazioneincaricodidattico_set.all())
    modalita_selezione = list(old.altaformazionemodalitaselezione_set.all())
    partners = list(old.altaformazionepartner_set.all())
    piano_didattico = list(old.altaformazionepianodidattico_set.all())

    # Duplica il master
    old.pk = None
    old.titolo_it = f"{old.titolo_it} (copia)"
    old.dt_mod = timezone.now()
    old.user_mod_id = request.user.id
    old.save()

    new = old

    # Duplica le relazioni figlie
    def clone_queryset(queryset, fk_name):
        for obj in queryset:
            obj.pk = None
            setattr(obj, fk_name, new)
            obj.dt_mod = timezone.now()
            obj.user_mod_id = request.user.id
            obj.save()

    clone_queryset(consiglio_esterno, "alta_formazione_dati_base")
    clone_queryset(consiglio_interno, "alta_formazione_dati_base")
    clone_queryset(attivita_formative, "alta_formazione_dati_base")
    clone_queryset(incarichi_didattici, "alta_formazione_dati_base")
    clone_queryset(modalita_selezione, "alta_formazione_dati_base")
    clone_queryset(partners, "alta_formazione_dati_base")
    clone_queryset(piano_didattico, "alta_formazione_dati_base")

    # Crea lo status iniziale (Bozza) per il nuovo master
    draft_status = AltaFormazioneStatus.objects.get(status_cod="0")
    AltaFormazioneStatusStorico.objects.create(
        motivazione="Master duplicato",
        data_status=timezone.now().date(),
        dt_mod=timezone.now(),
        user_mod_id=request.user.id,
        id_alta_formazione_dati_base=new,
        id_alta_formazione_status=draft_status,
    )

    messages.success(request, "Master duplicato con successo")
    return redirect(
        reverse("advanced-training:management:advanced-training-detail", args=[new.id])
    )
