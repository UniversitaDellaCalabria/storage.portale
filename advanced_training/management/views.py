from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from advanced_training.models import AltaFormazioneDatiBase
from advanced_training.management.forms import (
    MasterDatiBaseForm,
    IncaricoDidatticoFormSet,
    PianoDidatticoFormSet,
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
def advancedtraining_info_edit(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        "#": _("Edit Master"),
    }

    tab_form_dict = {
        "Dati generali": MasterDatiBaseForm(instance=master),
        "Incarichi Didattici": IncaricoDidatticoFormSet(instance=master),
        "Piano Didattico": PianoDidatticoFormSet(instance=master),
    }

    last_viewed_tab = request.GET.get("tab")

    if request.method == "POST":
        form_name = request.POST.get("tab_form_dict_key")
        form = None

        match form_name:
            case "Dati generali":
                form = MasterDatiBaseForm(request.POST, instance=master)
            case "Incarichi Didattici":
                form = IncaricoDidatticoFormSet(request.POST, instance=master)
            case "Piano Didattico":
                form = PianoDidatticoFormSet(request.POST, instance=master)

        last_viewed_tab = form_name

        if form and form.is_valid():
            if isinstance(form, (IncaricoDidatticoFormSet, PianoDidatticoFormSet)):
                objs = form.save(commit=False)
                for obj in objs:
                    obj.dt_mod = timezone.now()
                    obj.save()
                form.save_m2m()
            else:
                obj = form.save(commit=False)
                obj.dt_mod = timezone.now()
                obj.save()

            messages.success(
                request, f"({form_name}) - Dati master aggiornati con successo"
            )

            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master.id])}?tab={form_name}"
            )
        else:
            if form:
                tab_form_dict[form_name] = form
                if isinstance(form, (IncaricoDidatticoFormSet, PianoDidatticoFormSet)):
                    for subform_errors in form.errors:
                        for field, errors in subform_errors.items():
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
            "forms": tab_form_dict,
            "last_viewed_tab": last_viewed_tab,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
def advancedtraining_info_create(request):
    master = AltaFormazioneDatiBase()

    tab_form_dict = {
        "Dati generali": MasterDatiBaseForm(instance=master),
        "Incarichi Didattici": IncaricoDidatticoFormSet(instance=master),
        "Piano Didattico": PianoDidatticoFormSet(instance=master),
    }

    if request.method == "POST":
        form = MasterDatiBaseForm(request.POST, instance=master)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.save()
            messages.success(request, "Nuovo master creato con successo")
            return redirect(
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    args=[obj.id],
                )
            )
        else:
            tab_form_dict["Dati generali"] = form

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": master,
            "forms": tab_form_dict,
            "last_viewed_tab": "Dati generali",
        },
    )
