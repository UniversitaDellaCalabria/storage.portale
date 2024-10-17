import datetime
import logging
import re
import unicodedata

from cds.models import DidatticaRegolamento
from cds_websites.models import (
    SitoWebCdsOggettiPortale,
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTipoDato,
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliReg,
    SitoWebCdsTopicArticoliRegAltriDati,
)
from cds_websites.settings import (
    OFFICE_CDS_WEBSITES_STRUCTURES,
    UNICMS_CORSI_LM_URL,
    UNICMS_CORSI_LT_LMCU_URL,
)
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message, log_action

from .decorators import (
    can_edit_cds_website,
    can_edit_cds_website_structure,
    can_manage_cds_website,
)
from .forms import (
    SitoWebCdsArticoliRegolamentoItemForm,
    SitoWebCdsExternalOggettiPortaleForm,
    SitoWebCdsOggettiItemForm,
    SitoWebCdsSubArticoliRegolamentoForm,
    SitoWebCdsTopicArticoliRegAltriDatiForm,
)
from .utils import get_topics_per_page

logger = logging.getLogger(__name__)


def _can_user_edit_structure(offices_structures):
    for structure in offices_structures:
        if structure.office.name == OFFICE_CDS_WEBSITES_STRUCTURES:
            return True
    return False


@login_required
@can_manage_cds_website
def cds_websites(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("CdS pages")}
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("cds:apiv1:cds-list"),
    }
    return render(request, "cds_websites.html", context)


# Topics
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_topics(request, cds_id, cds=None, my_offices=None):
    """
    modifica dei dati dei topic del sito web del corso di studio
    """

    cds_website_url = (
        UNICMS_CORSI_LM_URL
        if (cds.tipo_corso_cod == "LM")
        else UNICMS_CORSI_LT_LMCU_URL
    )

    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    cds_website_page_name = re.sub(r"[^ \w]", "", cds.nome_cds_it)
    cds_website_page_name = re.sub(r"\s+", "-", cds_website_page_name)
    cds_website_page_name = cds_website_page_name.lower()
    cds_website_url += "/" + cds_website_page_name + "/cds"

    topics = SitoWebCdsTopic.objects.all()

    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects.select_related(
        "sito_web_cds_oggetti_portale",
        "sito_web_cds_topic",
        "didattica_cds_articoli_regolamento",
    ).filter(
        Q(sito_web_cds_oggetti_portale__cds_id=cds_id)
        | Q(
            didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds_id=cds_id
        )
    )

    topics_per_page_response = get_topics_per_page()
    topics_per_page_response_status_code = topics_per_page_response["status_code"]
    topics_per_page = topics_per_page_response["content"]
    if topics_per_page_response_status_code != 200:
        messages.add_message(
            request,
            messages.WARNING,
            _(
                "Unable to determine which topics are shown on the Portal nor the page they're appearing on"
            ),
        )

    """
    pages = {
        "page_name": {
            topic_id: {
                "topic": topic,
                "objects": topic_objs,
                "regarts": topic_areg
            },
        },
    }
    """
    pages = {}
    for key in topics_per_page.keys():
        pages[
            unicodedata.normalize("NFKD", key)
            .encode("ascii", "ignore")
            .decode()
            .capitalize()
        ] = {}
    pages["Altro"] = {}

    for topic in topics:
        t_id = topic.id
        cds_topic_ogg_art_current = cds_topic_ogg_art.filter(
            sito_web_cds_topic=topic
        ).order_by("ordine")
        topic_objs = cds_topic_ogg_art_current.filter(
            sito_web_cds_oggetti_portale__isnull=False
        )
        topic_areg = cds_topic_ogg_art_current.filter(
            didattica_cds_articoli_regolamento__isnull=False
        )

        is_shown_topic = False
        for k, v in topics_per_page.items():
            if t_id in v:
                pages[
                    unicodedata.normalize("NFKD", k)
                    .encode("ascii", "ignore")
                    .decode()
                    .capitalize()
                ][str(t_id)] = {
                    "topic": topic,
                    "objects": topic_objs,
                    "regarts": topic_areg,
                }
                is_shown_topic = True
                break

        if not is_shown_topic:
            pages["Altro"][str(t_id)] = {
                "topic": topic,
                "objects": topic_objs,
                "regarts": topic_areg,
            }

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        "#": (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
    }

    external_objects_logs = LogEntry.objects.filter(
        content_type=ContentType.objects.get_for_model(SitoWebCdsOggettiPortale),
        object_id__in=SitoWebCdsOggettiPortale.objects.filter(cds=cds).values_list(
            "id", flat=True
        ),
    )

    regart_logs = LogEntry.objects.filter(
        content_type=ContentType.objects.get_for_model(SitoWebCdsTopicArticoliReg),
        object_id__in=SitoWebCdsTopicArticoliReg.objects.filter(
            Q(sito_web_cds_oggetti_portale__cds=cds)
            | Q(
                didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds=cds
            )
        ).values_list("id", flat=True),
    )

    sub_art_logs = LogEntry.objects.filter(
        content_type=ContentType.objects.get_for_model(
            SitoWebCdsSubArticoliRegolamento
        ),
        object_id__in=SitoWebCdsSubArticoliRegolamento.objects.filter(
            sito_web_cds_topic_articoli_reg__in=SitoWebCdsTopicArticoliReg.objects.filter(
                didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds=cds
            ).values_list("id", flat=True)
        ).values_list("id", flat=True),
    )

    # Combine and order logs
    logs = regart_logs.union(sub_art_logs, external_objects_logs).order_by(
        "-action_time"
    )

    popover_title_content = {
        "portal_objects": {
            "title": _("Shared Portal objects"),
            "content": _(
                "This section allows to insert, remove and edit Publications/WebPath (Active Pages) under a certain topic."
            )
            + "<br /><br />"
            + "<b>"
            + _(
                'In order for a web Publication/WebPath to be iserted here, you must first import it from the "Shared objects" section.'
            )
            + "</b>",
        }
    }

    return render(
        request,
        "cds_websites_topics.html",
        {
            "cds": cds,
            "pages": pages,
            "topics_list": topics,
            "breadcrumbs": breadcrumbs,
            "popover_title_content": popover_title_content,
            "cds_website_url": cds_website_url,
            "user_can_edit": user_can_edit,
            "logs": logs,
        },
    )


# Shared Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_shared_objects(request, cds_id, cds=None, my_offices=None):
    objects_list = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_id)

    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        "#": _("Shared objects"),
    }

    return render(
        request,
        "cds_websites_shared_objects.html",
        {
            "cds": cds,
            "objects_list": objects_list,
            "breadcrumbs": breadcrumbs,
            "user_can_edit": user_can_edit,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_shared_object_edit(
    request, cds_id, data_id, cds=None, my_offices=None
):
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    object_form = SitoWebCdsExternalOggettiPortaleForm(
        data=request.POST if request.POST else None, user=request.user, instance=_object
    )
    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    if request.POST:
        if not user_can_edit:
            return custom_message(request, _("Permission denied"))

        if object_form.is_valid() and object_form.changed_data:
            _object = object_form.save(commit=False)
            _object.user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.save()

            log_action(
                user=request.user,
                obj=_object,
                flag=CHANGE,
                msg=_("Edited Shared Object") + f" - {_object.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-shared-objects",
                cds_id=cds_id,
            )

        else:  # pragma: no cover
            for k, v in object_form.errors.items():
                if k == "__all__":
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"<b>{object_form.fields[k].label}</b>: {v}",
                    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-shared-objects",
            kwargs={"cds_id": cds_id},
        ): _("Shared objects"),
        "#": _("Edit Object"),
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "form": object_form,
            "user_can_edit": user_can_edit,
            "item_label": _("Object"),
            "show_submit_warning": 1,
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
@can_edit_cds_website_structure
def cds_websites_shared_object_new(request, cds_id, cds=None, my_offices=None):
    object_form = SitoWebCdsExternalOggettiPortaleForm(
        data=request.POST if request.POST else None
    )

    if request.POST:
        if object_form.is_valid():
            _object = object_form.save(commit=False)
            _object.cds = cds
            _object.user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.aa_regdid_id = max(
                DidatticaRegolamento.objects.filter(cds_id=cds_id).values_list(
                    "aa_reg_did", flat=True
                )
            )
            _object.save()

            log_action(
                user=request.user,
                obj=_object,
                flag=CHANGE,
                msg=_("Added Shared Object") + f" - {_object.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object added successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-shared-objects",
                cds_id=cds_id,
            )

        else:  # pragma: no cover
            for k, v in object_form.errors.items():
                if k == "__all__":
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"<b>{object_form.fields[k].label}</b>: {v}",
                    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-shared-objects",
            kwargs={"cds_id": cds_id},
        ): _("Shared objects"),
        "#": _("New Object"),
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "form": object_form,
            "item_label": _("Object"),
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
@can_edit_cds_website_structure
def cds_websites_shared_object_delete(
    request, cds_id, data_id, cds=None, my_offices=None
):
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    _object.delete()

    messages.add_message(request, messages.SUCCESS, _("Object removed successfully"))

    return redirect(
        "cds-websites:management:cds-websites-shared-objects",
        cds_id=cds_id,
    )


# Common
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_items_order_edit(request, cds_id, topic_id, cds=None, my_offices=None):
    user_can_edit = request.user.is_superuser
    if not user_can_edit:
        return custom_message(request, _("Permission denied"))

    topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)

    items_list = (
        SitoWebCdsTopicArticoliReg.objects.select_related(
            "sito_web_cds_oggetti_portale",
            "sito_web_cds_topic",
            "didattica_cds_articoli_regolamento",
        )
        .filter(
            Q(sito_web_cds_topic=topic)
            & (
                Q(sito_web_cds_oggetti_portale__cds_id=cds_id)
                | Q(
                    didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds_id=cds_id
                )
            )
        )
        .order_by("ordine")
        .all()
    )

    if request.POST:
        item_order = request.POST.getlist("item_order")
        for index, item_id in enumerate(item_order):
            item = items_list.get(id=item_id)
            item.ordine = (index * 10) + 10
            item.dt_mod = datetime.datetime.now()
            item.save(update_fields=["ordine", "dt_mod"])

            log_action(
                user=request.user,
                obj=item,
                flag=CHANGE,
                msg=_("Updated item order") + f" - {item.titolo_it} - {item.ordine}",
            )

        messages.add_message(
            request, messages.SUCCESS, _("Items order updated successfully")
        )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        "#": f"{topic.descr_topic_it} - " + _("order"),
    }

    return render(
        request,
        "cds_website_pages_items_order.html",
        {
            "cds": cds,
            "user_can_edit": user_can_edit,
            "items_list": items_list,
            "breadcrumbs": breadcrumbs,
        },
    )


# Articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_article_edit(
    request, cds_id, topic_id, data_id, cds=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    art_reg_form = SitoWebCdsArticoliRegolamentoItemForm(
        data=request.POST if request.POST else None, user=request.user, instance=regart
    )
    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    if request.POST:
        if not user_can_edit:
            return custom_message(request, _("Permission denied"))

        if art_reg_form.is_valid():
            art_reg = art_reg_form.save(commit=False)
            art_reg.dt_mod = datetime.datetime.now()
            # art_reg.user_mod=request.user
            art_reg.save()

            log_action(
                user=request.user,
                obj=art_reg,
                flag=CHANGE,
                msg=_("Edited Regulation Article") + f" - {regart.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Regulation Article edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                cds_id=cds_id,
            )

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{art_reg_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        "#": regart.titolo_it,
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "forms": [
                art_reg_form,
            ],
            "regart": regart,
            "item_label": _("Regulation Article"),
            "topic_id": topic_id,
            "user_can_edit": user_can_edit,
            "edit": 1,
        },
    )


# Sub articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sub_articles(
    request, cds_id, topic_id, data_id, cds=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    if not regart.didattica_cds_articoli_regolamento:
        return custom_message(request, _("Permission denied"))

    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    sub_articles_list = (
        SitoWebCdsSubArticoliRegolamento.objects.filter(
            sito_web_cds_topic_articoli_reg=regart
        )
        .order_by("ordine")
        .all()
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-article-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        ): regart.titolo_it,
        "#": _("Sub articles"),
    }

    return render(
        request,
        "cds_websites_sub_articles.html",
        {
            "cds": cds,
            "sub_articles_list": sub_articles_list,
            "regart": regart,
            "topic_id": topic_id,
            "user_can_edit": user_can_edit,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sub_article_edit(
    request, cds_id, topic_id, data_id, sub_art_id, cds=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    sub_article = get_object_or_404(SitoWebCdsSubArticoliRegolamento, pk=sub_art_id)
    sitowebcdssubarticoliregolamentoform = SitoWebCdsSubArticoliRegolamentoForm(
        data=request.POST if request.POST else None,
        instance=sub_article,
        user=request.user,
    )
    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    if request.POST:
        if not user_can_edit:
            return custom_message(request, _("Permission denied"))

        if sitowebcdssubarticoliregolamentoform.is_valid():
            art_reg = sitowebcdssubarticoliregolamentoform.save(commit=False)
            art_reg.dt_mod = datetime.datetime.now()
            art_reg.user_mod = request.user
            art_reg.save()

            log_action(
                user=request.user,
                obj=art_reg,
                flag=CHANGE,
                msg=_("Edited sub article") + f" - {sub_article.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Sub article edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                cds_id=cds_id,
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-article-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        ): regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-sub-articles",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        ): _("Sub articles"),
        "#": sub_article.titolo_it,
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "forms": [
                sitowebcdssubarticoliregolamentoform,
            ],
            "regart": regart,
            "item_label": _("Sub article"),
            "topic_id": topic_id,
            "user_can_edit": user_can_edit,
            "edit": 1,
        },
    )


# Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
@can_edit_cds_website_structure
def cds_websites_object_add(request, cds_id, topic_id, cds=None, my_offices=None):
    obj_item_form = SitoWebCdsOggettiItemForm(
        data=request.POST if request.POST else None, cds_id=cds_id
    )

    user_can_edit = True

    if request.POST:
        if obj_item_form.is_valid():
            obj_item = obj_item_form.save(commit=False)
            obj_item.sito_web_cds_topic = get_object_or_404(
                SitoWebCdsTopic, pk=topic_id
            )
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.user_mod = request.user
            obj_item.save()

            log_action(
                user=request.user,
                obj=obj_item,
                flag=CHANGE,
                msg=_("Added Object") + f" - {obj_item.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object added successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                cds_id=cds_id,
            )

        else:  # pragma: no cover
            for k, v in obj_item_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{obj_item_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        "#": _("Add Portal Object"),
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "topic_id": topic_id,
            "form": obj_item_form,
            "user_can_edit": user_can_edit,
            "item_label": _("Portal Object"),
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_edit(
    request, cds_id, topic_id, data_id, cds=None, my_offices=None
):
    user_can_edit = request.user.is_superuser or _can_user_edit_structure(my_offices)

    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    obj_item_form = SitoWebCdsOggettiItemForm(
        data=request.POST if request.POST else None,
        instance=regart,
        user=request.user,
        cds_id=cds_id,
    )

    if request.POST:
        if not user_can_edit:
            return custom_message(request, _("Permission denied"))
        if obj_item_form.is_valid() and obj_item_form.has_changed():
            obj_item = obj_item_form.save(commit=False)
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.user_mod = request.user
            obj_item.save()

            log_action(
                user=request.user,
                obj=obj_item,
                flag=CHANGE,
                msg=_("Edited Object") + f" - {obj_item.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                cds_id=cds_id,
            )

        else:  # pragma: no cover
            for k, v in obj_item_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{obj_item_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        "#": regart.titolo_it,
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "form": obj_item_form,
            "regart": regart,
            "user_can_edit": user_can_edit,
            "item_label": _("Object"),
            "topic_id": topic_id,
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
@can_edit_cds_website_structure
def cds_websites_object_delete(
    request, cds_id, topic_id, data_id, cds=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    if (
        regart.didattica_cds_articoli_regolamento is not None
    ):  # Can't delete articles
        return custom_message(request, _("Permission denied"))

    titolo_it = regart.titolo_it
    regart.delete()

    log_action(
        user=request.user,
        obj=regart,
        flag=CHANGE,
        msg=_("Removed Object") + f" - {titolo_it}",
    )

    messages.add_message(request, messages.SUCCESS, _("Item removed successfully"))

    return redirect("cds-websites:management:cds-websites-topics", cds_id=cds_id)


# Extras
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extras(request, cds_id, topic_id, data_id, cds=None, my_offices=None):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    user_can_edit = True
    extras_list = (
        SitoWebCdsTopicArticoliRegAltriDati.objects.filter(
            sito_web_cds_topic_articoli_reg=regart
        )
        .order_by("ordine")
        .all()
    )

    if request.POST:
        item_order = request.POST.getlist("item_order")
        for index, item_id in enumerate(item_order):
            item = extras_list.get(id=item_id)
            item.ordine = (index * 10) + 10
            item.dt_mod = datetime.datetime.now()
            item.save(update_fields=["ordine", "dt_mod"])

        log_action(
            user=request.user,
            obj=regart,
            flag=CHANGE,
            msg=_("Updated extras order") + f" - {regart.titolo_it}",
        )

        messages.add_message(
            request, messages.SUCCESS, _("Extras order updated successfully")
        )

    breadcrumbs_regart = (
        reverse(
            "cds-websites:management:cds-websites-article-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.didattica_cds_articoli_regolamento is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        breadcrumbs_regart: regart.titolo_it,
        "#": _("Extras"),
    }

    return render(
        request,
        "cds_websites_extras.html",
        {
            "cds": cds,
            "extras_list": extras_list,
            "user_can_edit": user_can_edit,
            "regart": regart,
            "topic_id": topic_id,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extra_new(
    request, cds_id, topic_id, data_id, cds=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(
        data=request.POST if request.POST else None
    )

    user_can_edit = True

    if request.POST:
        if regart_extra_form.is_valid():
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.sito_web_cds_topic_articoli_reg = regart
            regart_extra.sito_web_cds_tipo_dato = get_object_or_404(
                SitoWebCdsTipoDato,
                pk=regart_extra_form.data.get("sito_web_cds_tipo_dato", None),
            )
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.user_mod = request.user
            regart_extra.save()

            log_action(
                user=request.user,
                obj=regart,
                flag=CHANGE,
                msg=_("Added Regulation Article Extra") + f" - {regart.titolo_it}",
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Regulation Article Extra added successfully"),
            )

            return redirect(
                "cds-websites:management:cds-websites-extras",
                cds_id=cds_id,
                topic_id=topic_id,
                data_id=data_id,
            )

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{regart_extra_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs_regart = (
        reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.sito_web_cds_oggetti_portale is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        breadcrumbs_regart: regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-extras",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        ): _("Extras"),
        "#": _("New Extra"),
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds": cds,
            "topic_id": topic_id,
            "user_can_edit": user_can_edit,
            "regart": regart,
            "forms": [
                regart_extra_form,
            ],
            "item_label": _("Regulation Article Extra"),
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extra_edit(
    request, cds_id, topic_id, data_id, extra_id, cds=None, my_offices=None
):
    user_can_edit = True
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)

    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(
        data=request.POST if request.POST else None, instance=regart_extra
    )

    if request.POST:
        if regart_extra_form.is_valid() and regart_extra_form.has_changed():
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.user_mod = request.user
            regart_extra.save()

            log_action(
                user=request.user,
                obj=regart,
                flag=CHANGE,
                msg=_("Edited Regulation Article Extra") - f" - {regart.titolo_it}",
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Regulation Article Extra edited successfully"),
            )

            return redirect(
                "cds-websites:management:cds-websites-extras",
                cds_id=cds_id,
                topic_id=topic_id,
                data_id=data_id,
            )

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{regart_extra_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs_regart = (
        reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.sito_web_cds_oggetti_portale is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"cds_id": cds_id},
        ): (
            cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds.nome_cds_eng)
            else cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        breadcrumbs_regart: regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-extras",
            kwargs={"cds_id": cds_id, "topic_id": topic_id, "data_id": data_id},
        ): _("Extras"),
        "#": regart_extra.testo_it
        if (request.LANGUAGE_CODE == "it" or not regart_extra.testo_en)
        else regart_extra.testo_en,
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds": cds,
            "breadcrumbs": breadcrumbs,
            "topic_id": topic_id,
            "forms": [
                regart_extra_form,
            ],
            "user_can_edit": user_can_edit,
            "item_label": _("Regulation Article Extra"),
            "edit": 1,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extra_delete(
    request, cds_id, topic_id, data_id, extra_id, cds=None, my_offices=None
):
    extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)
    regart = extra.sito_web_cds_topic_articoli_reg

    extra.delete()

    log_action(
        user=request.user,
        obj=regart,
        flag=CHANGE,
        msg=_("Deleted Regulation Article Extra"),
    )

    messages.add_message(
        request, messages.SUCCESS, _("Regulation Article Extra deleted successfully")
    )

    return redirect(
        "cds-websites:management:cds-websites-extras",
        cds_id=cds_id,
        topic_id=topic_id,
        data_id=data_id,
    )
