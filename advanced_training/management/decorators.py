from django.utils.translation import gettext_lazy as _
import datetime
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from advanced_training.models import (
    AltaFormazioneFinestraTemporale,
    AltaFormazioneStatusStorico,
    AltaFormazioneDatiBase,
)


def check_temporal_window():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            pk = kwargs.get("pk")
            new_status = kwargs.get("status_cod")

            # Non è un cambio stato
            if not pk or not new_status:
                return view_func(request, *args, **kwargs)

            if new_status != "1":
                return view_func(request, *args, **kwargs)

            master = AltaFormazioneDatiBase.objects.filter(pk=pk).first()
            if not master:
                return view_func(request, *args, **kwargs)

            # Stato corrente
            last_status = (
                AltaFormazioneStatusStorico.objects.filter(
                    id_alta_formazione_dati_base=master
                )
                .order_by("-data_status", "-dt_mod", "-id")
                .first()
            )

            old_status = (
                last_status.id_alta_formazione_status.status_cod
                if last_status
                else None
            )

            # Se NON è Bozza -> Validazione, lascia passare
            if old_status != "0":
                return view_func(request, *args, **kwargs)

            # Controllo finestra temporale
            today = datetime.date.today()
            active_window = AltaFormazioneFinestraTemporale.objects.filter(
                data_inizio__lte=today, data_fine__gte=today
            ).exists()

            if not active_window:
                messages.error(
                    request,
                    _(
                        "Non è presente una finestra temporale attiva. "
                        "La mandata in validazione non è consentita."
                    ),
                )
                return redirect(
                    "advanced-training:management:advanced-training-detail", pk=pk
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator