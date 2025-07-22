from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from advanced_training.models import AltaFormazioneDatiBase


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
def advancedtraining_detail(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _("Advanced Training"),
        "#": master.titolo_it
    }

    context = {
        "breadcrumbs": breadcrumbs,
        "master": master,
    }

    return render(request, "advanced-training-detail.html", context)

