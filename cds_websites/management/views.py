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
    UNICMS_CORSI_LM_URL,
    UNICMS_CORSI_LT_LMCU_URL,
)
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message, log_action

from .decorators import (
    can_edit_cds_website,
    can_manage_cds_website,
    can_edit_cds_website_structure,
)
from .forms import (
    SitoWebCdsArticoliRegolamentoItemForm,
    SitoWebCdsOggettiItemForm,
    SitoWebCdsOggettiPortaleForm,
    SitoWebCdsSubArticoliRegolamentoForm,
    SitoWebCdsTopicArticoliRegAltriDatiForm,
)
from .utils import get_topics_per_page

logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("CdS pages")}
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("cds-brochure:apiv1:cds-websites-list"),
    }
    return render(request, "cds_websites.html", context)


# Topics
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_topics(request, code, cds_website=None, my_offices=None):
    """
    modifica dei dati dei topic del sito web del corso di studio
    """

    cds_website_url = (
        UNICMS_CORSI_LM_URL
        if (cds_website.cds.tipo_corso_cod == "LM")
        else UNICMS_CORSI_LT_LMCU_URL
    )
    cds_website_page_name = re.sub(r"[^ \w]", "", cds_website.cds.nome_cds_it)
    cds_website_page_name = re.sub(r"\s", "-", cds_website_page_name)
    cds_website_page_name = cds_website_page_name.lower()
    cds_website_url += "/" + cds_website_page_name + "/cds"

    topics = SitoWebCdsTopic.objects.all()

    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects.select_related(
        "id_sito_web_cds_oggetti_portale",
        "id_sito_web_cds_topic",
        "id_didattica_cds_articoli_regolamento",
    ).filter(
        Q(id_sito_web_cds_oggetti_portale__cds_id=cds_website.cds_id)
        | Q(
            id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds_id=cds_website.cds_id
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
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg
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
            id_sito_web_cds_topic=t_id
        ).order_by("ordine")
        topic_objs = cds_topic_ogg_art_current.filter(
            id_sito_web_cds_oggetti_portale__isnull=False
        )
        topic_areg = cds_topic_ogg_art_current.filter(
            id_didattica_cds_articoli_regolamento__isnull=False
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
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
    }

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(cds_website).pk,
        object_id=cds_website.pk,
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
            "cds_website": cds_website,
            "pages": pages,
            "topics_list": topics,
            "breadcrumbs": breadcrumbs,
            "popover_title_content": popover_title_content,
            "cds_website_url": cds_website_url,
            "logs": logs,
        },
    )


# Shared Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_shared_objects(request, code, cds_website=None, my_offices=None):
    objects_list = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_website.cds_id)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
            "objects_list": objects_list,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_shared_object_edit(
    request, code, data_id, cds_website=None, my_offices=None
):
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    object_form = SitoWebCdsOggettiPortaleForm(
        data=request.POST if request.POST else None, user=request.user, instance=_object
    )
    user_can_edit = request.user.is_superuser

    if request.POST:
        if not request.user.is_superuser:
            return custom_message(request, _("Permission denied"))

        if object_form.is_valid() and object_form.changed_data:
            _object = object_form.save(commit=False)
            _object.id_user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.save()

            log_action(
                user=request.user, obj=cds_website, flag=CHANGE, msg=_("Edited object")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-shared-objects",
                code=code,
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
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-shared-objects",
            kwargs={"code": code},
        ): _("Shared objects"),
        "#": _("Edit Object"),
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds_website": cds_website,
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
def cds_websites_shared_object_new(request, code, cds_website=None, my_offices=None):
    object_form = SitoWebCdsOggettiPortaleForm(
        data=request.POST if request.POST else None
    )

    if request.POST:
        if object_form.is_valid():
            _object = object_form.save(commit=False)
            _object.cds = cds_website.cds
            _object.id_user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.aa_regdid_id = max(
                DidatticaRegolamento.objects.filter(
                    cds_id=cds_website.cds_id
                ).values_list("aa_reg_did", flat=True)
            )
            _object.save()

            log_action(
                user=request.user, obj=cds_website, flag=CHANGE, msg=_("Added object")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object added successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-shared-objects",
                code=code,
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
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-shared-objects",
            kwargs={"code": code},
        ): _("Shared objects"),
        "#": _("New Object"),
    }

    return render(
        request,
        "cds_websites_objects_form.html",
        {
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "form": object_form,
            "item_label": _("Object"),
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_shared_object_delete(
    request, code, data_id, cds_website=None, my_offices=None
):
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    if not request.user.is_superuser:
        return custom_message(request, _("Permission denied"))

    _object.delete()

    log_action(user=request.user, obj=cds_website, flag=CHANGE, msg=_("Removed object"))

    messages.add_message(request, messages.SUCCESS, _("Object removed successfully"))

    return redirect(
        "cds-websites:management:cds-websites-shared-objects",
        code=code,
    )


# Common
@login_required
@user_passes_test(lambda u: u.is_superuser)
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_items_order_edit(
    request, code, topic_id, cds_website=None, my_offices=None
):
    topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)

    items_list = (
        SitoWebCdsTopicArticoliReg.objects.select_related(
            "id_sito_web_cds_oggetti_portale",
            "id_sito_web_cds_topic",
            "id_didattica_cds_articoli_regolamento",
        )
        .filter(
            Q(id_sito_web_cds_topic=topic)
            & (
                Q(id_sito_web_cds_oggetti_portale__cds_id=cds_website.cds_id)
                | Q(
                    id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds_id=cds_website.cds_id
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
            obj=cds_website,
            flag=CHANGE,
            msg=_("Updated items order") + f" - {topic.descr_topic_it}",
        )

        messages.add_message(
            request, messages.SUCCESS, _("Items order updated successfully")
        )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
            "items_list": items_list,
            "breadcrumbs": breadcrumbs,
        },
    )


# Articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_article_edit(
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    art_reg_form = SitoWebCdsArticoliRegolamentoItemForm(
        data=request.POST if request.POST else None, user=request.user, instance=regart
    )
    user_can_edit = request.user.is_superuser

    if request.POST:
        if not request.user.is_superuser:
            return custom_message(request, _("Permission denied"))

        if art_reg_form.is_valid():
            art_reg = art_reg_form.save(commit=False)
            art_reg.dt_mod = datetime.datetime.now()
            # art_reg.id_user_mod=request.user
            art_reg.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited Regulation Article") + f" {regart.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Regulation Article edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                code=code,
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
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
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
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    if not regart.id_didattica_cds_articoli_regolamento:
        return custom_message(request, _("Permission denied"))

    sub_articles_list = (
        SitoWebCdsSubArticoliRegolamento.objects.filter(
            id_sito_web_cds_topic_articoli_reg=regart
        )
        .order_by("ordine")
        .all()
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-article-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        ): regart.titolo_it,
        "#": _("Sub articles"),
    }

    return render(
        request,
        "cds_websites_sub_articles.html",
        {
            "cds_website": cds_website,
            "sub_articles_list": sub_articles_list,
            "regart": regart,
            "topic_id": topic_id,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sub_article_edit(
    request, code, topic_id, data_id, sub_art_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    sub_article = get_object_or_404(SitoWebCdsSubArticoliRegolamento, pk=sub_art_id)
    sitowebcdssubarticoliregolamentoform = SitoWebCdsSubArticoliRegolamentoForm(
        data=request.POST if request.POST else None, instance=sub_article
    )
    user_can_edit = request.user.is_superuser

    if request.POST:
        if not request.user.is_superuser:
            return custom_message(request, _("Permission denied"))

        if sitowebcdssubarticoliregolamentoform.is_valid():
            art_reg = sitowebcdssubarticoliregolamentoform.save(commit=False)
            art_reg.dt_mod = datetime.datetime.now()
            art_reg.id_user_mod = request.user
            art_reg.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited sub article") + f" {sub_article.titolo_it}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Sub article edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                code=code,
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        reverse(
            "cds-websites:management:cds-websites-article-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        ): regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-sub-articles",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        ): _("Sub articles"),
        "#": sub_article.titolo_it,
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds_website": cds_website,
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
def cds_websites_object_add(request, code, topic_id, cds_website=None, my_offices=None):
    obj_item_form = SitoWebCdsOggettiItemForm(
        data=request.POST if request.POST else None, cds_id=cds_website.cds_id
    )

    if request.POST:
        if obj_item_form.is_valid():
            obj_item = obj_item_form.save(commit=False)
            obj_item.id_sito_web_cds_topic = get_object_or_404(
                SitoWebCdsTopic, pk=topic_id
            )
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.id_user_mod = request.user
            obj_item.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Added Portal Object"),
            )

            messages.add_message(
                request, messages.SUCCESS, _("Portal Object added successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                code=code,
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
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
            "breadcrumbs": breadcrumbs,
            "topic_id": topic_id,
            "form": obj_item_form,
            "item_label": _("Portal Object"),
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_edit(
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    obj_item_form = SitoWebCdsOggettiItemForm(
        data=request.POST if request.POST else None,
        instance=regart,
        user=request.user,
        cds_id=cds_website.cds_id,
    )
    user_can_edit = request.user.is_superuser

    if request.POST:
        if not request.user.is_superuser:
            return custom_message(request, _("Permission denied"))
        if obj_item_form.is_valid() and obj_item_form.has_changed():
            obj_item = obj_item_form.save(commit=False)
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.id_user_mod = request.user
            obj_item.save()

            log_action(
                user=request.user, obj=cds_website, flag=CHANGE, msg=_("Edited Object")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Object edited successfully")
            )

            return redirect(
                "cds-websites:management:cds-websites-topics",
                code=code,
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
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
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
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    if (
        request.user.is_superuser
        and regart.id_didattica_cds_articoli_regolamento is None
    ):
        return custom_message(request, _("Permission denied"))

    regart.delete()

    log_action(user=request.user, obj=cds_website, flag=CHANGE, msg=_("Removed Item"))

    messages.add_message(request, messages.SUCCESS, _("Item removed successfully"))

    return redirect("cds-websites:management:cds-websites-topics", code=code)


# Extras
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extras(
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    extras_list = (
        SitoWebCdsTopicArticoliRegAltriDati.objects.filter(
            id_sito_web_cds_topic_articoli_reg=regart
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
            obj=cds_website,
            flag=CHANGE,
            msg=_("Updated extras order") + f" - {regart.titolo_it}",
        )

        messages.add_message(
            request, messages.SUCCESS, _("Extras order updated successfully")
        )

    breadcrumbs_regart = (
        reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.id_sito_web_cds_oggetti_portale is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
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
            "cds_website": cds_website,
            "extras_list": extras_list,
            "regart": regart,
            "topic_id": topic_id,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_extra_new(
    request, code, topic_id, data_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(
        data=request.POST if request.POST else None
    )

    if request.POST:
        if regart_extra_form.is_valid():
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.id_sito_web_cds_topic_articoli_reg = regart
            regart_extra.id_sito_web_cds_tipo_dato = get_object_or_404(
                SitoWebCdsTipoDato,
                pk=regart_extra_form.data.get("id_sito_web_cds_tipo_dato", None),
            )
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.id_user_mod = request.user
            regart_extra.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Added Regulation Article Extra"),
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Regulation Article Extra added successfully"),
            )

            return redirect(
                "cds-websites:management:cds-websites-extras",
                code=code,
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
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.id_sito_web_cds_oggetti_portale is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        breadcrumbs_regart: regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-extras",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        ): _("Extras"),
        "#": _("New Extra"),
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds_website": cds_website,
            "topic_id": topic_id,
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
    request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None
):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)
    user_can_edit = True

    if not request.user.is_superuser:
        return custom_message(request, _("Permission denied"))

    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(
        data=request.POST if request.POST else None, instance=regart_extra
    )

    if request.POST:
        if regart_extra_form.is_valid() and regart_extra_form.has_changed():
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.id_user_mod = request.user
            regart_extra.save()

            log_action(
                user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Edited Regulation Article Extra"),
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Regulation Article Extra edited successfully"),
            )

            return redirect(
                "cds-websites:management:cds-websites-extras",
                code=code,
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
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
        if regart.id_sito_web_cds_oggetti_portale is not None
        else reverse(
            "cds-websites:management:cds-websites-object-edit",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        )
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds-websites:management:cds-websites"): _("CdS pages"),
        reverse(
            "cds-websites:management:cds-websites-topics",
            kwargs={"code": code},
        ): (
            cds_website.cds.nome_cds_it
            if (request.LANGUAGE_CODE == "it" or not cds_website.cds.nome_cds_eng)
            else cds_website.cds.nome_cds_eng
        )
        + " ("
        + _("Topics")
        + ")",
        breadcrumbs_regart: regart.titolo_it,
        reverse(
            "cds-websites:management:cds-websites-extras",
            kwargs={"code": code, "topic_id": topic_id, "data_id": data_id},
        ): _("Extras"),
        "#": regart_extra.testo_it
        if (request.LANGUAGE_CODE == "it" or not regart_extra.testo_en)
        else regart_extra.testo_en,
    }

    return render(
        request,
        "cds_websites_unique_form.html",
        {
            "cds_website": cds_website,
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
    request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None
):
    extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)

    if not request.user.is_superuser:
        return custom_message(request, _("Permission denied"))

    extra.delete()

    log_action(
        user=request.user,
        obj=cds_website,
        flag=CHANGE,
        msg=_("Deleted Regulation Article Extra"),
    )

    messages.add_message(
        request, messages.SUCCESS, _("Regulation Article Extra deleted successfully")
    )

    return redirect(
        "cds-websites:management:cds-websites-extras",
        code=code,
        topic_id=topic_id,
        data_id=data_id,
    )
