from django.utils.translation import gettext_lazy as _
import datetime
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from advanced_training.models import AltaFormazioneFinestraTemporale

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
