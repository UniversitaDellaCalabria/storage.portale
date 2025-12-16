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
from django.contrib.admin.models import CHANGE, ADDITION, DELETION

from generics.utils import custom_message, decrypt, encrypt, log_action
from locks.concurrency import get_lock_from_cache
from locks.exceptions import LockCannotBeAcquiredException
from django.contrib.contenttypes.models import ContentType

from advanced_training.models import (
    AltaFormazioneConsiglioScientificoInterno,
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
    ConsiglioInternoEsternoForm,
    ChoosenPersonForm,
)
from advanced_training.api.v2.views import AdvancedTrainingMastersViewSet
from advanced_training.management.decorators import check_temporal_window
from addressbook.models import Personale

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

    dati_generali_form = MasterDatiBaseForm(instance=master)

    last_viewed_tab = request.GET.get("tab", "Dati generali")

    if request.method == "POST":
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
            form = ConsiglioInternoEsternoForm(request.POST, instance=master)

        last_viewed_tab = form_name

        if form and form.is_valid():
            if isinstance(
                form,
                (
                    IncaricoDidatticoFormSet,
                    PianoDidatticoFormSet,
                    PartnerFormSet,
                    ConsiglioScientificoEsternoFormSet,
                    ConsiglioInternoEsternoForm,
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
                        ConsiglioInternoEsternoForm,
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

    form = None
    template = None
    context = {
        "tab_name": tab_name,
        "is_readonly": is_readonly,
        "master": master,
    }

    try:
        if tab_name == "Incarichi Didattici":
            form = IncaricoDidatticoFormSet(instance=master)
            template = "tabs/incarichi_didattici.html"
            context["form"] = form

        elif tab_name == "Piano Didattico":
            form = PianoDidatticoFormSet(instance=master)
            template = "tabs/piano_didattico.html"
            context["form"] = form

        elif tab_name == "Partner":
            form = PartnerFormSet(instance=master)
            template = "tabs/partner.html"
            context["form"] = form

        elif tab_name == "Consiglio Scientifico Esterno":
            form = ConsiglioScientificoEsternoFormSet(instance=master)
            template = "tabs/consiglio_esterno.html"
            context["form"] = form

        elif tab_name == "Consiglio Scientifico Interno":
            # NUOVO: Carica i membri invece del formset
            consiglio_members = (
                AltaFormazioneConsiglioScientificoInterno.objects.filter(
                    alta_formazione_dati_base=master
                )
                .select_related("matricola_cons")
                .order_by("nome_origine_cons")
            )

            template = "tabs/consiglio_interno.html"
            context["consiglio_members"] = consiglio_members

        html = render(request, template, context).content.decode("utf-8")

        return JsonResponse({"html": html, "success": True})

    except Exception as e:
        return JsonResponse(
            {"error": f"Errore nel caricamento: {str(e)}", "tab_name": tab_name},
            status=500,
        )


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
@check_temporal_window()
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


@login_required
def consiglio_interno_new(request, master_id):
    """
    Creazione nuovo membro del consiglio scientifico interno
    """
    master = get_object_or_404(AltaFormazioneDatiBase, pk=master_id)

    # Inizializza i form
    internal_form = ChoosenPersonForm(required=True)
    external_form = ConsiglioInternoEsternoForm()

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ConsiglioInternoEsternoForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            consiglio_member = AltaFormazioneConsiglioScientificoInterno()
            consiglio_member.alta_formazione_dati_base = master

            if form.cleaned_data.get("choosen_person"):
                # Personale interno
                member_id = decrypt(form.cleaned_data["choosen_person"])
                member = get_object_or_404(Personale, matricola=member_id)
                consiglio_member.matricola_cons = member
                consiglio_member.nome_origine_cons = f"{member.cognome} {member.nome}"
            else:
                # Personale esterno
                consiglio_member.matricola_cons = None
                consiglio_member.nome_origine_cons = form.cleaned_data[
                    "nome_origine_cons"
                ]

            consiglio_member.user_ins_id = request.user.id
            consiglio_member.dt_mod = timezone.now()
            consiglio_member.save()

            log_action(
                user=request.user,
                obj=master,
                flag=ADDITION,
                msg=f"Aggiunto membro consiglio interno: {consiglio_member.nome_origine_cons}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Council member added successfully")
            )
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
            )
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        reverse(
            "advanced-training:management:advanced-training-detail",
            kwargs={"pk": master_id},
        ): master.titolo_it,
        "#": _("New Council Member"),
    }

    return render(
        request,
        "consiglio_interno_form.html",  # Nome template modificato
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": "",  # Vuoto per nuovo inserimento
            "external_form": external_form,
            "internal_form": internal_form,
            "master": master,
            "url": reverse("teachers:apiv1:teachers-list"),
            "is_edit": False,
        },
    )


@login_required
def consiglio_interno_edit(request, master_id, consiglio_id):
    """
    Modifica membro del consiglio scientifico interno
    """
    master = get_object_or_404(AltaFormazioneDatiBase, pk=master_id)
    consiglio_member = get_object_or_404(
        AltaFormazioneConsiglioScientificoInterno.objects.select_related(
            "matricola_cons"
        ),
        pk=consiglio_id,
        alta_formazione_dati_base=master,
    )

    old_label = consiglio_member.nome_origine_cons
    member = consiglio_member.matricola_cons
    initial = {}
    member_data = ""

    if member:
        member_data = f"{member.cognome} {member.nome}"
        initial = {"choosen_person": encrypt(member.matricola)}

    external_form = ConsiglioInternoEsternoForm(instance=consiglio_member)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ConsiglioInternoEsternoForm(
            instance=consiglio_member, data=request.POST
        )

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                # Personale interno
                member_id = decrypt(form.cleaned_data["choosen_person"])
                member = get_object_or_404(Personale, matricola=member_id)
                consiglio_member.matricola_cons = member
                consiglio_member.nome_origine_cons = f"{member.cognome} {member.nome}"
            else:
                # Personale esterno
                consiglio_member.matricola_cons = None
                consiglio_member.nome_origine_cons = form.cleaned_data[
                    "nome_origine_cons"
                ]

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

            messages.add_message(
                request, messages.SUCCESS, _("Council member data edited successfully")
            )
            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
            )
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        reverse(
            "advanced-training:management:advanced-training-detail",
            kwargs={"pk": master_id},
        ): master.titolo_it,
        "#": f"{_('Edit Council Member')} {consiglio_member.nome_origine_cons}",
    }

    return render(
        request,
        "consiglio_interno_form.html",  # Nome template modificato
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": member_data,  # Dati del membro selezionato
            "external_form": external_form,
            "internal_form": internal_form,
            "master": master,
            "url": reverse("teachers:apiv1:teachers-list"),
            "is_edit": True,
        },
    )


@login_required
def consiglio_interno_delete(request, master_id, consiglio_id):
    """
    Eliminazione membro del consiglio scientifico interno
    """
    master = get_object_or_404(AltaFormazioneDatiBase, pk=master_id)
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

    messages.add_message(
        request, messages.SUCCESS, _("Council member removed successfully")
    )

    return redirect(
        f"{reverse('advanced-training:management:advanced-training-detail', args=[master_id])}?tab=Consiglio Scientifico Interno"
    )
