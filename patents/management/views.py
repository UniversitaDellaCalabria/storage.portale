import logging

from addressbook.models import Personale
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.forms import ChoosenPersonForm
from generics.utils import decrypt, encrypt, log_action
from patents.models import BrevettoDatiBase, BrevettoInventori

from .decorators import can_manage_patents
from .forms import BrevettoDatiBaseForm, BrevettoInventoriForm

logger = logging.getLogger(__name__)


@login_required
@can_manage_patents
def patents(request, patent=None):
    """
    lista dei brevetti
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("Patents")}
    context = {"breadcrumbs": breadcrumbs, "url": reverse("patents:apiv1:patents")}
    return render(request, "patents.html", context)


@login_required
@can_manage_patents
def patent_new(request, patent=None):
    """
    nuovo brevetto
    """
    form = BrevettoDatiBaseForm()

    if request.POST:
        form = BrevettoDatiBaseForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            patent = form.save()
            log_action(
                user=request.user, obj=patent, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request, messages.SUCCESS, _("Patent created successfully")
            )
            return redirect("patents:management:patents")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("patents:management:patents"): _("Patents"),
        "#": _("New"),
    }

    return render(
        request, "patent_new.html", {"breadcrumbs": breadcrumbs, "form": form}
    )


@login_required
@can_manage_patents
def patent(request, patent_id, patent=None):
    """
    modifica brevetto
    """
    form = BrevettoDatiBaseForm(instance=patent)
    inventors = BrevettoInventori.objects.filter(brevetto=patent)

    if request.POST:
        form = BrevettoDatiBaseForm(
            instance=patent, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            form.save(commit=False)
            patent.user_mod = request.user
            patent.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )
                log_action(
                    user=request.user,
                    obj=patent,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Patent edited successfully")
            )

            return redirect("patents:management:patent-edit", patent_id=patent_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(patent).pk,
        object_id=patent.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("patents:management:patents"): _("Patents"),
        "#": patent.titolo,
    }

    return render(
        request,
        "patent.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "logs": logs,
            "patent": patent,
            "inventors": inventors,
        },
    )


@login_required
@can_manage_patents
def patent_inventor_new(request, patent_id, patent=None):
    """
    nuovo inventore
    """
    external_form = BrevettoInventoriForm()
    internal_form = ChoosenPersonForm(required=True)
    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = BrevettoInventoriForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                inventor_patent_id = decrypt(form.cleaned_data["choosen_person"])
                inventor = get_object_or_404(Personale, matricola=inventor_patent_id)
                cognomenome_origine = f"{inventor.cognome} {inventor.nome}"
            else:
                inventor = None
                cognomenome_origine = form.cleaned_data["cognomenome_origine"]

            b = BrevettoInventori.objects.create(
                brevetto=patent,
                matricola_inventore=inventor,
                cognomenome_origine=cognomenome_origine,
            )

            log_action(
                user=request.user,
                obj=patent,
                flag=CHANGE,
                msg=f"Aggiunto nuovo inventore {b}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Inventor added successfully")
            )
            return redirect("patents:management:patent-edit", patent_id=patent_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("patents:management:patents"): _("Patents"),
        reverse("patents:management:patent-edit", kwargs={"patent_id": patent_id}): patent.titolo,
        "#": _("New inventor"),
    }

    return render(
        request,
        "patent_inventor.html",
        {
            "breadcrumbs": breadcrumbs,
            "external_form": external_form,
            "internal_form": internal_form,
            "patent": patent,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_patents
def patent_inventor_edit(request, patent_id, inventor_id, patent=None):
    """
    dettaglio dati inventore
    """
    patent_inventor = get_object_or_404(
        BrevettoInventori.objects.select_related("matricola_inventore"),
        pk=inventor_id,
        brevetto=patent_id,
    )
    old_label = patent_inventor.cognomenome_origine
    inventor = patent_inventor.matricola_inventore
    initial = {}
    inventor_data = ""
    if inventor:
        inventor_data = f"{inventor.cognome} {inventor.nome}"
        initial = {"choosen_person": encrypt(inventor.matricola)}

    external_form = BrevettoInventoriForm(instance=patent_inventor)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = BrevettoInventoriForm(
            instance=patent_inventor, data=request.POST
        )

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                inventor_patent_id = decrypt(form.cleaned_data["choosen_person"])
                inventor = get_object_or_404(Personale, matricola=inventor_patent_id)
                patent_inventor.matricola_inventore = inventor
                patent_inventor.cognomenome_origine = (
                    f"{inventor.cognome} {inventor.nome}"
                )
            else:
                patent_inventor.matricola_inventore = None
                patent_inventor.cognomenome_origine = form.cleaned_data[
                    "cognomenome_origine"
                ]

            patent_inventor.save()

            if old_label != patent_inventor.cognomenome_origine:
                log_action(
                    user=request.user,
                    obj=patent,
                    flag=CHANGE,
                    msg=f"Sostituito inventore {old_label} con {patent_inventor}",
                )

            messages.add_message(
                request, messages.SUCCESS, _("Patent inventor edited successfully")
            )

            return redirect("patents:management:patent-edit", patent_id=patent_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("patents:management:patents"): _("Patents"),
        reverse("patents:management:patent-edit", kwargs={"patent_id": patent_id}): patent.titolo,
        reverse(
            "patents:management:patent-inventor-edit",
            kwargs={"patent_id": patent_id, "inventor_id": inventor_id},
        ): _("Patent inventor data"),
    }

    return render(
        request,
        "patent_inventor.html",
        {
            "breadcrumbs": breadcrumbs,
            "patent": patent,
            "choosen_person": inventor_data,
            "external_form": external_form,
            "internal_form": internal_form,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_patents
def patent_inventor_delete(request, patent_id, inventor_id, patent=None):
    """
    elimina inventore
    """
    inventor = get_object_or_404(BrevettoInventori, pk=inventor_id, brevetto=patent_id)

    # if BrevettoInventori.objects.filter(brevetto=patent_id).count() == 1:
    # return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(
        user=request.user, obj=patent, flag=CHANGE, msg=f"Rimosso inventore {inventor}"
    )

    inventor.delete()
    messages.add_message(request, messages.SUCCESS, _("Inventor removed successfully"))
    return redirect("patents:management:patent-edit", patent_id=patent_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_patents
def patent_delete(request, patent_id, patent=None):
    """
    rimuovi brevetto
    """
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    #     raise Exception(_('Permission denied'))

    patent = get_object_or_404(BrevettoDatiBase, pk=patent_id)
    patent.delete()
    messages.add_message(request, messages.SUCCESS, _("Patent removed successfully"))

    return redirect("patents:management:patents")
