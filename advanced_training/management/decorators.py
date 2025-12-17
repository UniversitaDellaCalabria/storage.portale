from functools import wraps
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
from django.shortcuts import get_object_or_404
import datetime


def can_manage_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può gestire i master.
    Aggiunge al contesto:
    - my_offices: uffici dell'utente relativi ai master (sia validatori che generici)
    - is_validator: True se l'utente è validatore
    - advanced_training: oggetto master (se pk presente)
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        # Recupera il master se presente
        if kwargs.get("pk"):
            master = get_object_or_404(AltaFormazioneDatiBase, pk=kwargs["pk"])
            kwargs["advanced_training"] = master

        # Se è superuser, passa direttamente
        if request.user.is_superuser:
            kwargs["is_validator"] = True
            kwargs["my_offices"] = OrganizationalStructureOfficeEmployee.objects.none()
            return func_to_decorate(*args, **kwargs)

        # Recupera TUTTI gli uffici attivi dell'utente
        offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        # Filtra uffici master (validatori + uffici generici)
        my_offices = offices.filter(
            office__name__in=[
                OFFICE_ADVANCED_TRAINING_VALIDATOR,
                OFFICE_ADVANCED_TRAINING,
            ]
        )

        # Verifica se è validatore
        is_validator = offices.filter(
            office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR
        ).exists()

        # Aggiungi al contesto
        kwargs["my_offices"] = my_offices
        kwargs["is_validator"] = is_validator

        # Se non ha permessi, nega l'accesso
        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_view_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può visualizzare un master specifico.
    Filtra my_offices per dipartimento se non è validatore.
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        advanced_training = kwargs.get("advanced_training")
        my_offices = kwargs.get("my_offices")
        is_validator = kwargs.get("is_validator", False)

        if not advanced_training:
            return custom_message(request, _("Advanced training not found"))

        # I validatori vedono tutto
        if is_validator:
            return func_to_decorate(*args, **kwargs)

        # Gli altri vedono solo i master del loro dipartimento
        department_code = (
            advanced_training.dipartimento_riferimento.dip_cod
            if advanced_training.dipartimento_riferimento
            else None
        )

        my_offices = my_offices.filter(
            office__organizational_structure__unique_code=department_code
        )
        kwargs["my_offices"] = my_offices

        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_edit_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può modificare un master.
    Considera anche lo stato del master e il dipartimento.
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        advanced_training = kwargs.get("advanced_training")
        my_offices = kwargs.get("my_offices")
        is_validator = kwargs.get("is_validator", False)

        if not advanced_training:
            return custom_message(request, _("Advanced training not found"))

        # I validatori non possono editare (solo approvare/rifiutare)
        if is_validator:
            return custom_message(
                request, _("Permission denied - Validators cannot edit")
            )

        # Verifica che l'ufficio sia dello stesso dipartimento
        department_code = (
            advanced_training.dipartimento_riferimento.dip_cod
            if advanced_training.dipartimento_riferimento
            else None
        )

        my_offices = my_offices.filter(
            office__organizational_structure__unique_code=department_code
        )

        if not my_offices.exists():
            return custom_message(request, _("Permission denied - Department mismatch"))

        # Verifica permessi di modifica basati sullo stato
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


def check_temporal_window(required=True):
    """
    Decoratore che verifica se esiste una finestra temporale attiva.

    Args:
        required (bool): Se True, blocca l'accesso se non c'è finestra attiva.
                        Se False, aggiunge solo l'informazione al contesto.
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
    Decoratore che verifica se l'utente è un validatore.
    Utile per azioni riservate solo ai validatori (Approva, Rifiuta, Correggi).
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        # Verifica se è validatore
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
