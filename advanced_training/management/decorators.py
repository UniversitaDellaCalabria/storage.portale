from functools import wraps
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee
from advanced_training.settings import OFFICE_ADVANCED_TRAINING_VALIDATOR
from advanced_training.models import AltaFormazioneFinestraTemporale
import datetime


def can_manage_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può gestire i master.
    Aggiunge al contesto:
    - my_offices: uffici validatori dell'utente
    - is_validator: True se l'utente è validatore
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        # Se è superuser, passa direttamente
        if request.user.is_superuser:
            kwargs["is_validator"] = True
            kwargs["my_offices"] = OrganizationalStructureOfficeEmployee.objects.none()
            return func_to_decorate(*args, **kwargs)

        # Recupera gli uffici dell'utente
        offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        # Filtra solo gli uffici validatori
        my_offices = offices.filter(office__name=OFFICE_ADVANCED_TRAINING_VALIDATOR)

        # Verifica se è validatore
        is_validator = my_offices.exists()

        # Aggiungi al contesto
        kwargs["my_offices"] = my_offices
        kwargs["is_validator"] = is_validator

        # Se non ha permessi, nega l'accesso
        if not is_validator:
            return custom_message(request, _("Permission denied"))

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_view_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può visualizzare un master specifico.
    Richiede che can_manage_advanced_training sia già stato applicato.
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        # Verifica accesso tramite il metodo del model
        advanced_training = kwargs.get("advanced_training")
        if advanced_training:
            user_permissions = advanced_training.get_user_permissions_and_offices(
                request.user
            )
            if not user_permissions["permissions"]["access"]:
                return custom_message(request, _("Permission denied"))

        return func_to_decorate(*args, **kwargs)

    return wrapper


def can_edit_advanced_training(func_to_decorate):
    """
    Decoratore che verifica se l'utente può modificare un master.
    Considera anche lo stato del master.
    """

    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.is_superuser:
            return func_to_decorate(*args, **kwargs)

        advanced_training = kwargs.get("advanced_training")
        if not advanced_training:
            return custom_message(request, _("Advanced training not found"))

        # Verifica permessi di modifica
        user_permissions = advanced_training.get_user_permissions_and_offices(
            request.user
        )
        if not user_permissions["permissions"]["edit"]:
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
