from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from advanced_training.models import AltaFormazioneDatiBase
from advanced_training.management.forms import (
    MasterDatiGeneraliForm,
    MasterIscrizioniForm,
    MasterContenutiForm,
    MasterStageForm,
    MasterAltroForm,
    MasterIncaricoDidatticoFormSet,
)
from django.contrib import messages
from django.utils import timezone


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
def master_info_edit(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    tab_form_dict = {
        "Dati generali": MasterDatiGeneraliForm(instance=master),
        "Iscrizioni": MasterIscrizioniForm(instance=master),
        "Contenuti": MasterContenutiForm(instance=master),
        "Stage e Project Work": MasterStageForm(instance=master),
        "Altro": MasterAltroForm(instance=master),
        "Incarichi Didattici": MasterIncaricoDidatticoFormSet(instance=master),
    }

    last_viewed_tab = None

    if request.POST:
        form_name = request.POST.get("tab_form_dict_key")
        form = None

        match form_name:
            case "Dati generali":
                form = MasterDatiGeneraliForm(request.POST, instance=master)
            case "Iscrizioni":
                form = MasterIscrizioniForm(request.POST, instance=master)
            case "Contenuti":
                form = MasterContenutiForm(request.POST, instance=master)
            case "Stage e Project Work":
                form = MasterStageForm(request.POST, instance=master)
            case "Altro":
                form = MasterAltroForm(request.POST, instance=master)
            case "Incarichi Didattici":
                form = MasterIncaricoDidatticoFormSet(request.POST, instance=master)

        last_viewed_tab = form_name

        if form.is_valid():
            objs = form.save(commit=False)
            for obj in objs:
                obj.dt_mod = timezone.now()
                obj.save()
            form.save_m2m()

            messages.success(
                request, f"({form_name}) - Dati master aggiornati con successo"
            )
            return redirect("advanced-training:management:master-info-edit", pk=master.id)
        else:
            tab_form_dict[form_name] = form
            for k, v in form.errors.items():
                messages.error(request, f"<b>{k}</b>: {v}")

    return render(
        request,
        "advanced-training-info.html",
        {"master": master, "forms": tab_form_dict, "last_viewed_tab": last_viewed_tab},
    )

