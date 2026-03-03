from functools import wraps
import datetime

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
    OFFICE_ADVANCED_TRAINING,
)
from advanced_training.models import (
    AltaFormazioneFinestraTemporale,
    AltaFormazioneDatiBase,
)


def can_manage_advanced_training(func_to_decorate):
    """
    Verifica se l'utente può gestire i master.
    Inietta in kwargs: my_offices, is_validator, advanced_training (se pk presente).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if kwargs.get("pk"):
            kwargs["advanced_training"] = get_object_or_404(
                AltaFormazioneDatiBase, pk=kwargs["pk"]
            )

        if request.user.is_superuser:
            kwargs["is_validator"] = True
            kwargs["my_offices"] = OrganizationalStructureOfficeEmployee.objects.none()
            return func_to_decorate(*args, **kwargs)

        offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        my_offices = offices.filter(
            office__name__in=[
                OFFICE_ADVANCED_TRAINING_VALIDATOR,
                OFFICE_ADVANCED_TRAINING,
            ]
        )
        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))

        kwargs["my_offices"] = my_offices
        kwargs["is_validator"] = offices.filter(
            office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR
        ).exists()
        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_view_advanced_training(func_to_decorate):
    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        advanced_training = kwargs.get("advanced_training")
        if not advanced_training:
            return custom_message(request, _("Advanced training not found"))

        if kwargs.get("is_validator"):
            return func_to_decorate(*args, **kwargs)

        department_code = (
            advanced_training.dipartimento_riferimento.dip_cod
            if advanced_training.dipartimento_riferimento
            else None
        )

        my_offices = kwargs.get("my_offices")
        same_dept_offices = my_offices.filter(
            office__organizational_structure__unique_code=department_code
        )

        if same_dept_offices.exists():
            kwargs["my_offices"] = same_dept_offices
            return func_to_decorate(*args, **kwargs)

        if my_offices.exists():
            from advanced_training.management.views import get_current_status

            current_status = get_current_status(advanced_training)
            if current_status["cod"] == "3":
                kwargs["my_offices"] = my_offices
                return func_to_decorate(*args, **kwargs)
            return custom_message(request, _("Permission denied"))

        return custom_message(request, _("Permission denied"))

    return wrapper


def can_edit_advanced_training(func_to_decorate):
    """
    Verifica se l'utente può modificare un master.
    I validatori non possono editare (solo approvare/rifiutare).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        advanced_training = kwargs.get("advanced_training")
        if not advanced_training:
            return custom_message(request, _("Advanced training not found"))

        if kwargs.get("is_validator"):
            return custom_message(
                request, _("Permission denied - Validators cannot edit")
            )

        department_code = (
            advanced_training.dipartimento_riferimento.dip_cod
            if advanced_training.dipartimento_riferimento
            else None
        )
        my_offices = kwargs.get("my_offices").filter(
            office__organizational_structure__unique_code=department_code
        )
        if not my_offices.exists():
            return custom_message(request, _("Permission denied - Department mismatch"))

        user_offices_names = list(
            OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).values_list("office__name", flat=True)
        )
        if not advanced_training._check_edit_permission(user_offices_names):
            return custom_message(
                request, _("Permission denied - Cannot edit in current status")
            )

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_manage_consiglio_interno(func_to_decorate):
    """
    Verifica che l'utente possa gestire i membri del consiglio scientifico interno.
    Richiede che l'utente abbia un ufficio master nel dipartimento del master,
    e che il master non sia in uno stato non modificabile (1, 3, 4).
    Inietta in kwargs: master (oggetto AltaFormazioneDatiBase).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]
        master = get_object_or_404(AltaFormazioneDatiBase, pk=kwargs["master_id"])
        kwargs["master"] = master

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        # Importa qui per evitare import circolare con views
        from advanced_training.management.views import get_current_status

        current_status_cod = get_current_status(master)["cod"]
        if str(current_status_cod) in ["1", "3", "4"]:
            return custom_message(
                request, _("Permission denied - Master is in read-only status")
            )

        department_code = (
            master.dipartimento_riferimento.dip_cod
            if master.dipartimento_riferimento
            else None
        )
        has_access = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
            office__name=OFFICE_ADVANCED_TRAINING,
            office__organizational_structure__unique_code=department_code,
        ).exists()

        if not has_access:
            return custom_message(
                request,
                _(
                    "Permission denied - Department mismatch or insufficient permissions"
                ),
            )

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_change_master_status(func_to_decorate):
    """
    Verifica i permessi per il cambio di stato di un master.
    - Controlla che l'utente abbia accesso al master.
    - Controlla che possa cambiare a quel specifico stato_cod.
    - Per status_cod "1" (Valida), verifica che l'utente abbia un ufficio
      master nello stesso dipartimento del master.
    Inietta in kwargs: dati_base (oggetto AltaFormazioneDatiBase).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]
        pk = kwargs["pk"]
        status_cod = kwargs["status_cod"]

        dati_base = get_object_or_404(AltaFormazioneDatiBase, pk=pk)
        kwargs["dati_base"] = dati_base

        if not dati_base.get_user_permissions_and_offices(request.user)["permissions"][
            "access"
        ]:
            return custom_message(request, _("Permission denied"))

        if not dati_base.can_user_change_status(request.user, status_cod):
            from django.contrib import messages
            from django.shortcuts import redirect

            messages.error(
                request, _("Non hai i permessi per effettuare questo cambio di stato")
            )
            return redirect(
                "advanced-training:management:advanced-training-detail", pk=pk
            )

        if status_cod == "1" and not request.user.is_superuser:
            department_code = (
                dati_base.dipartimento_riferimento.dip_cod
                if dati_base.dipartimento_riferimento
                else None
            )
            same_dept = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
                office__name=OFFICE_ADVANCED_TRAINING,
                office__organizational_structure__unique_code=department_code,
            ).exists()
            if not same_dept:
                from django.contrib import messages
                from django.shortcuts import redirect

                messages.error(
                    request,
                    _(
                        "Non puoi mandare in validazione un master di un altro dipartimento"
                    ),
                )
                return redirect(
                    "advanced-training:management:advanced-training-detail", pk=pk
                )

        return func_to_decorate(*args, **kwargs)

    return wrapper


def check_temporal_window(required=True):
    """
    Verifica se esiste una finestra temporale attiva.
    Se required=True, blocca l'accesso se non c'è finestra attiva.
    Se required=False, inietta solo has_active_window=True/False in kwargs.
    """

    def decorator(func_to_decorate):
        @wraps(func_to_decorate)
        def wrapper(*args, **kwargs):
            request = args[0]
            today = datetime.date.today()
            has_active_window = AltaFormazioneFinestraTemporale.objects.filter(
                data_inizio__lte=today, data_fine__gte=today
            ).exists()
            kwargs["has_active_window"] = has_active_window

            if required and not has_active_window:
                return custom_message(
                    request,
                    _("No active temporal window. This operation is not available."),
                )
            return func_to_decorate(*args, **kwargs)

        return wrapper

    return decorator


def is_validator_user(func_to_decorate):
    """
    Verifica che l'utente sia un validatore.
    Utile per azioni riservate solo ai validatori (Approva, Rifiuta, Correggi).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        is_validator = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
            office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR,
        ).exists()

        if not is_validator:
            return custom_message(
                request, _("Permission denied - Validator role required")
            )

        return func_to_decorate(*args, **kwargs)

    return wrapper
