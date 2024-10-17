import datetime
import logging

from cds.models import DidatticaCdsLingua
from cds_brochure.models import (
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider,
)
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import log_action

from .decorators import can_manage_cds_website
from .forms import (
    CdsBrochureDatiCorsoForm,
    CdsBrochureInPilloleForm,
    CdsBrochureIntroAmmForm,
    CdsBrochureProfiloCorsoForm,
    CdsBrochureExStudentiForm,
    CdsBrochureLinkForm,
    CdsBrochureSliderForm,
)

logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_brochure(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("CdS in brief")}
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("cds-brochure:apiv1:cds-brochures-list"),
    }
    return render(request, "cds_brochures.html", context)


@login_required
@can_manage_cds_website
def cds_website_brochure(request, code, cds_website=None, my_offices=None):
    """
    Menu di un sito web dei corsi di studio
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        "#": cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
    }

    return render(
        request,
        "cds_brochure.html",
        {
            "breadcrumbs": breadcrumbs,
            "cds_website": cds_website,
        },
    )


# Dati Base
@login_required
@can_manage_cds_website
def cds_brochure_info_edit(request, code, cds_website=None, my_offices=None):
    tab_form_dict = {
        "Dati corso": CdsBrochureDatiCorsoForm(instance=cds_website),
        "In pillole": CdsBrochureInPilloleForm(instance=cds_website),
        "Profilo corso": CdsBrochureProfiloCorsoForm(instance=cds_website),
        "Intro amm": CdsBrochureIntroAmmForm(instance=cds_website),
    }
    last_viewed_tab = None

    languages = (
        DidatticaCdsLingua.objects.filter(cdsord=cds_website.cds)
        .values("lingua_des_it", "lingua_des_eng")
        .distinct()
    )

    if request.POST:
        form = None
        dati_base = None
        form_name = request.POST.get("tab_form_dict_key")
        try:
            match form_name:
                case "Dati corso":
                    form = CdsBrochureDatiCorsoForm(
                        data=request.POST, instance=cds_website
                    )
                case "In pillole":
                    form = CdsBrochureInPilloleForm(
                        data=request.POST, instance=cds_website
                    )
                case "Profilo corso":
                    form = CdsBrochureProfiloCorsoForm(
                        data=request.POST, instance=cds_website
                    )
                case "Intro amm":
                    form = CdsBrochureIntroAmmForm(
                        data=request.POST, instance=cds_website
                    )

            last_viewed_tab = form_name

            if not form.is_valid():
                raise Exception(_("Form validation failed"))

            dati_base = form.save(commit=False)

            dati_base.dt_mod = datetime.datetime.now()
            dati_base.user_mod = request.user
            dati_base.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited website info") + f" ({form_name})",
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                f"({form_name}) - " + _("Website info edited successfully"),
            )

            return redirect(
                "cds-brochure:management:cds-brochure-info-edit",
                code=code,
            )

        except Exception:
            tab_form_dict[form_name] = form

            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        "#": _("Info"),
    }

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(cds_website).pk,
        object_id=cds_website.pk,
    )

    return render(
        request,
        "cds_brochure_info_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "languages": languages,
            "logs": logs,
            "forms": tab_form_dict,
            "last_viewed_tab": last_viewed_tab,
            "item_label": _("Info"),
        },
    )


# Sliders
@login_required
@can_manage_cds_website
def cds_brochure_sliders(request, code, cds_website=None, my_offices=None):
    sliders = CdsBrochureSlider.objects.filter(cds_brochure=code).order_by(
        "ordine"
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        "#": _("Sliders"),
    }

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(cds_website).pk,
        object_id=cds_website.pk,
    )

    return render(
        request,
        "cds_brochure_sliders.html",
        {
            "cds_website": cds_website,
            "sliders": sliders,
            "breadcrumbs": breadcrumbs,
            "logs": logs,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_sliders_new(request, code, cds_website=None, my_offices=None):
    slider_form = CdsBrochureSliderForm(data=request.POST if request.POST else None)

    if request.POST:
        if slider_form.is_valid():
            slider = slider_form.save(commit=False)
            slider.dt_mod = datetime.datetime.now()
            slider.user_mod = request.user
            slider.cds_brochure = cds_website
            slider.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Added Scrollable Text"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Scrollable Text added successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-sliders",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{slider_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _("CdS"),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-sliders",
            kwargs={"code": code},
        ): _("Sliders"),
        "#": _("New"),
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                slider_form,
            ],
            "item_label": _("Scrollable Text"),
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_sliders_edit(
    request, code, data_id, cds_website=None, my_offices=None
):
    slider = get_object_or_404(CdsBrochureSlider, pk=data_id)
    slider_form = CdsBrochureSliderForm(
        data=request.POST if request.POST else None, instance=slider
    )

    if request.POST:
        if slider_form.is_valid():
            slider = slider_form.save(commit=False)
            slider.dt_mod = datetime.datetime.now()
            slider.user_mod = request.user
            slider.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited Scrollable Text"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Scrollable Text edited successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-sliders",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{slider_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-sliders",
            kwargs={"code": code},
        ): _("Sliders"),
        "#": _("Edit"),
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                slider_form,
            ],
            "item_label": _("Scrollable Text"),
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_sliders_delete(
    request, code, data_id, cds_website=None, my_offices=None
):
    slider = get_object_or_404(CdsBrochureSlider, pk=data_id)
    slider.delete()

    log_action(
        user=request.user,
        obj=cds_website,
        flag=CHANGE,
        msg=_("Deleted Scrollable Text"),
    )

    messages.add_message(
        request, messages.SUCCESS, _("Scrollable Text deleted successfully")
    )

    return redirect(
        "cds-brochure:management:cds-brochure-sliders", code=code
    )


# Ex Students
@login_required
@can_manage_cds_website
def cds_brochure_exstudents(request, code, cds_website=None, my_offices=None):
    exstudents = CdsBrochureExStudenti.objects.filter(
        cds_brochure=code
    ).order_by("ordine")

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        "#": _("Ex Students"),
    }

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(cds_website).pk,
        object_id=cds_website.pk,
    )

    return render(
        request,
        "cds_brochure_exstudents.html",
        {
            "cds_website": cds_website,
            "exstudents": exstudents,
            "breadcrumbs": breadcrumbs,
            "logs": logs,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_exstudents_new(
    request, code, cds_website=None, my_offices=None
):
    exstudent_form = CdsBrochureExStudentiForm(
        data=request.POST if request.POST else None,
        files=request.FILES if request.FILES else None,
    )

    if request.POST:
        if exstudent_form.is_valid():
            exstudent = exstudent_form.save(commit=False)
            exstudent.cds_brochure = cds_website
            exstudent.dt_mod = datetime.datetime.now()
            exstudent.user_mod = request.user
            exstudent.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Added Ex Student"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Ex Student added successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-exstudents",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{exstudent_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:crud_cds_website", kwargs={"code": code}
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-exstudents",
            kwargs={"code": code},
        ): _("Ex Students"),
        "#": _("New"),
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                exstudent_form,
            ],
            "item_label": _("Ex Student"),
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_exstudents_edit(
    request, code, data_id, cds_website=None, my_offices=None
):
    exstudent = get_object_or_404(CdsBrochureExStudenti, pk=data_id)
    exstudent_form = CdsBrochureExStudentiForm(
        data=request.POST if request.POST else None,
        files=request.FILES if request.FILES else None,
        instance=exstudent,
    )

    if request.POST:
        if exstudent_form.is_valid():
            exstudent = exstudent_form.save(commit=False)
            exstudent.dt_mod = datetime.datetime.now()
            exstudent.user_mod = request.user
            exstudent.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited Ex Student"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Ex Student edited successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-exstudents",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{exstudent_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-exstudents",
            kwargs={"code": code},
        ): _("Ex Students"),
        "#": exstudent.nome,
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                exstudent_form,
            ],
            "item_label": _("Ex Student"),
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_exstudents_delete(
    request, code, data_id, cds_website=None, my_offices=None
):
    exstudent = get_object_or_404(CdsBrochureExStudenti, pk=data_id)
    exstudent.delete()

    log_action(
        user=request.user, obj=cds_website, flag=CHANGE, msg=_("Deleted Ex Student")
    )

    messages.add_message(
        request, messages.SUCCESS, _("Ex Student deleted successfully")
    )

    return redirect(
        "cds-brochure:management:cds-brochure-exstudents", code=code
    )


# Links
@login_required
@can_manage_cds_website
def cds_brochure_links(request, code, cds_website=None, my_offices=None):
    links = CdsBrochureLink.objects.filter(cds_brochure=code).order_by(
        "ordine"
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        "#": _("Links"),
    }

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(cds_website).pk,
        object_id=cds_website.pk,
    )

    return render(
        request,
        "cds_brochure_links.html",
        {
            "cds_website": cds_website,
            "links": links,
            "breadcrumbs": breadcrumbs,
            "logs": logs,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_links_new(request, code, cds_website=None, my_offices=None):
    link_form = CdsBrochureLinkForm(data=request.POST if request.POST else None)

    if request.POST:
        if link_form.is_valid():
            link = link_form.save(commit=False)
            link.cds_brochure = cds_website
            link.dt_mod = datetime.datetime.now()
            link.user_mod = request.user
            link.save()

            log_action(
                user=request.user, obj=cds_website, flag=CHANGE, msg=_("Added Link")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Link added successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-links",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{link_form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-links",
            kwargs={"code": code},
        ): _("Links"),
        "#": _("New"),
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                link_form,
            ],
            "item_label": _("Link"),
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_links_edit(
    request, code, data_id, cds_website=None, my_offices=None
):
    link = get_object_or_404(CdsBrochureLink, pk=data_id)
    link_form = CdsBrochureLinkForm(
        data=request.POST if request.POST else None, instance=link
    )

    if request.POST:
        if link_form.is_valid():
            link = link_form.save(commit=False)
            link.dt_mod = datetime.datetime.now()
            link.user_mod = request.user
            link.save()

            log_action(
                user=request.user, obj=cds_website, flag=CHANGE, msg=_("Edited Link")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Link edited successfully")
            )

            return redirect(
                "cds-brochure:management:cds-brochure-links",
                code=code,
            )

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{link_form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-brochure:management:cds-brochure"): _(
            "CdS in brief"
        ),
        reverse(
            "cds-brochure:management:cds-website-brochure",
            kwargs={"code": code},
        ): cds_website.cds.nome_cds_it
        if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
        else cds_website.cds.nome_cds_eng,
        reverse(
            "cds-brochure:management:cds-brochure-links",
            kwargs={"code": code},
        ): _("Links"),
        "#": link.descrizione_link_it,
    }

    return render(
        request,
        "cds_brochure_unique_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "forms": [
                link_form,
            ],
            "item_label": _("Link"),
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
def cds_brochure_links_delete(
    request, code, data_id, cds_website=None, my_offices=None
):
    link = get_object_or_404(CdsBrochureLink, pk=data_id)
    link.delete()

    log_action(user=request.user, obj=cds_website, flag=CHANGE, msg=_("Deleted Link"))

    messages.add_message(request, messages.SUCCESS, _("Link deleted successfully"))

    return redirect(
        "cds-brochure:management:cds-brochure-links", code=code
    )
