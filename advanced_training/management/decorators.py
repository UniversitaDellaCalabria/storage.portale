from addressbook.models import Personale
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from laboratories.models import LaboratorioDatiBase
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from organizational_area.models import OrganizationalStructureOfficeEmployee
from .utils import _is_user_scientific_director

import datetime
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from advanced_training.models import AltaFormazioneFinestraTemporale



def can_manage_laboratories(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        is_scientific_director = False

        if original_kwargs.get("laboratory_id"):
            laboratory = get_object_or_404(
                LaboratorioDatiBase, pk=original_kwargs["laboratory_id"]
            )
            original_kwargs["laboratory"] = laboratory

            is_scientific_director = _is_user_scientific_director(request, laboratory)

        else:
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(
                    cod_fis=request.user.taxpayer_id
                ).first()
                is_scientific_director = (
                    user_profile is not None
                    and LaboratorioDatiBase.objects.filter(
                        matricola_responsabile_scientifico=user_profile
                    ).exists()
                )

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        my_offices = offices.filter(office__name=OFFICE_LABORATORIES)
        is_validator = offices.filter(
            office__name=OFFICE_LABORATORY_VALIDATORS
        ).exists()

        original_kwargs["my_offices"] = my_offices
        original_kwargs["is_validator"] = is_validator

        if not (my_offices.exists() or is_validator or is_scientific_director):
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func

def check_temporal_window(allowed_statuses=None):
    """
    Decoratore che verifica se esiste una finestra temporale attiva.
    
    Args:
        allowed_statuses: lista di status_cod che sono sempre permessi 
                         indipendentemente dalla finestra temporale
                         (es. ['3', '4'] per approvazione/rigetto)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            today = datetime.date.today()
            
            # Verifica se esiste una finestra temporale attiva
            active_window = AltaFormazioneFinestraTemporale.objects.filter(
                data_inizio__lte=today,
                data_fine__gte=today
            ).exists()
            
            # Se è una richiesta di cambio stato
            if 'status_cod' in kwargs:
                status_cod = kwargs['status_cod']
                
                # Stati sempre permessi (approvazione/rigetto)
                if allowed_statuses and status_cod in allowed_statuses:
                    return view_func(request, *args, **kwargs)
                
                # Stati che richiedono finestra temporale attiva (invio in revisione/correzione)
                # status_cod '1' = Richiesta validazione, '2' = Da correggere
                if status_cod in ['1', '2'] and not active_window:
                    messages.error(
                        request,
                        _("Non è possibile inviare il master in revisione: "
                          "nessuna finestra temporale attiva.")
                    )
                    pk = kwargs.get('pk')
                    if pk:
                        return redirect(
                            'advanced-training:management:advanced-training-detail',
                            pk=pk
                        )
                    return redirect('advanced-training:management:advanced-training')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
