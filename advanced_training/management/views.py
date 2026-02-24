import datetime
import logging

from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from advanced_training.management.decorators import (
    can_manage_advanced_training,
    can_view_advanced_training,
    can_manage_consiglio_interno,
    can_change_master_status,
    check_temporal_window,
)
from advanced_training.management.forms import (
    ChoosenPersonForm,
    ConsiglioInternoEsternoForm,
    ConsiglioScientificoEsternoFormSet,
    IncaricoDidatticoFormSet,
    MasterDatiBaseForm,
    PartnerFormSet,
    PianoDidatticoFormSet,
)
from advanced_training.models import (
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneFinestraTemporale,
    AltaFormazioneStatus,
    AltaFormazioneStatusStorico,
)
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING,
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
)
from addressbook.models import Personale
from generics.utils import custom_message, decrypt, encrypt, log_action
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
        .order_by("-data_status", "-dt_mod", "-id")
        .first()
    )
    if entry:
        cod = entry.id_alta_formazione_status.status_cod
        return {
            "cod": cod,
            "description": entry.id_alta_formazione_status.status_desc,
            "badge_class": _get_status_badge_class(cod),
        }
    return {"cod": "3", "description": "Approvato", "badge_class": "success"}


def is_temporal_window_active():
    today = datetime.date.today()
    return AltaFormazioneFinestraTemporale.objects.filter(
        data_inizio__lte=today, data_fine__gte=today
    ).exists()


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
def advancedtraining_masters(request):
    offices_qs = OrganizationalStructureOfficeEmployee.objects.filter(
        employee=request.user,
        office__is_active=True,
        office__organizational_structure__is_active=True,
        office__name__in=[OFFICE_ADVANCED_TRAINING, OFFICE_ADVANCED_TRAINING_VALIDATOR],
    )
    can_create = request.user.is_superuser or offices_qs.exists()
    is_validator = offices_qs.filter(
        office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR
    ).exists()

    return render(
        request,
        "advanced-training.html",
        {
            "breadcrumbs": {
                reverse("generics:dashboard"): _("Dashboard"),
                "#": _("Advanced Training"),
            },
            "url": reverse("advanced-training:apiv2:advanced-training-list"),
            "can_create": can_create,
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
    has_active_window = is_temporal_window_active()

    can_validate_actions = user_is_validator and current_status_cod == "1"
    can_send_validation = (
        not user_is_validator
        and current_status_cod in ("0", "2", None)
        and has_active_window
        and user_has_same_department
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
        if tab_name in TAB_FORMSET_MAP:
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
            "has_active_window": is_temporal_window_active(),
        },
    )


@login_required
def advancedtraining_info_delete(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    if get_current_status(master)["cod"] != "0":
        messages.error(request, _("Puoi eliminare solo master in stato Bozza"))
        return redirect("advanced-training:management:advanced-training-detail", pk=pk)

    if request.method == "POST":
        master.delete()
        messages.success(request, _("Master eliminato con successo"))
        return redirect("advanced-training:management:advanced-training")

    messages.error(request, _("Richiesta non valida"))
    return redirect("advanced-training:management:advanced-training-detail", pk=pk)


@login_required
@check_temporal_window(required=False)
@can_change_master_status
def advancedtraining_status_change(
    request, pk, status_cod, dati_base=None, has_active_window=None
):
    if request.method != "POST":
        return custom_message(request, _("Metodo non consentito"))

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

        AltaFormazioneStatusStorico.objects.create(
            motivazione=motivazione,
            data_status=timezone.now().date(),
            dt_mod=timezone.now(),
            user_mod_id=request.user.pk,
            id_alta_formazione_dati_base=dati_base,
            id_alta_formazione_status=status,
        )

        try:
            log_action(
                user=request.user,
                obj=dati_base,
                flag=CHANGE,
                msg=_("Changed advanced training status to")
                + f" '{status.status_desc}'",
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

    old.pk = None
    old.titolo_it = new_title
    old.dt_mod = timezone.now()
    old.user_mod_id = request.user.id
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
        member_id = decrypt(form.cleaned_data["choosen_person"])
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
    external_form = ConsiglioInternoEsternoForm()

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ConsiglioInternoEsternoForm(data=request.POST)
        form = internal_form if "choosen_person" in request.POST else external_form

        if form.is_valid():
            member = AltaFormazioneConsiglioScientificoInterno()
            member.alta_formazione_dati_base = master
            _apply_consiglio_member(member, form)
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

        for k, v in form.errors.items():
            messages.error(request, f"<b>{form.fields[k].label}</b>: {v}")

    return render(
        request,
        "consiglio_interno_form.html",
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
            "external_form": external_form,
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
        "consiglio_interno_form.html",
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
