import logging
import datetime

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from ricerca_app.models import *

from . decorators import *
from . forms import *
from . utils import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites_pages(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS pages')}
    context = { 'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites_pages.html', context)

#Topics
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_topics_edit(request, code, cds_website=None, my_offices=None):
    """
    modifica dei dati dei topic del sito web del corso di studio
    """

    topics = SitoWebCdsTopic.objects.all()

    objects_list = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_website.cds_id)

    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects\
        .select_related("id_sito_web_cds_oggetti_portale", "id_sito_web_cds_topic", "id_didattica_cds_articoli_regolamento")\
        .filter(Q(id_sito_web_cds_oggetti_portale__cds_id=cds_website.cds_id) | Q(id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds_id=cds_website.cds_id))

    topics_per_page_response = get_topics_per_page()
    topics_per_page_response_status_code = topics_per_page_response["status_code"]
    topics_per_page = topics_per_page_response["content"]
    if topics_per_page_response_status_code != 200:
         messages.add_message(  request,
                                messages.WARNING,
                                _("Unable to determine which topics are shown on the Portal nor the page they're appearing on"))

    '''
    pages = {
        "page_name": {
            topic_id: {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg
            },
        },
    }
    '''
    pages = {}
    for key in topics_per_page.keys():
        pages[key.capitalize()] = {}
    pages["Topic non mostrati"] = {}
    
    for topic in topics:
        t_id = topic.id
        cds_topic_ogg_art_current = cds_topic_ogg_art.filter(id_sito_web_cds_topic=t_id).order_by("ordine")
        topic_objs = cds_topic_ogg_art_current.filter(id_sito_web_cds_oggetti_portale__isnull=False)
        topic_areg = cds_topic_ogg_art_current.filter(id_didattica_cds_articoli_regolamento__isnull=False)

        is_shown_topic = False
        for k,v in topics_per_page.items():
            if t_id in v:
                pages[k.capitalize()][str(t_id)] = {
                    "topic" : topic,
                    "objects" : topic_objs,
                    "regarts" : topic_areg
                }
                is_shown_topic = True
                break

        if not is_shown_topic:
            pages["Topic non mostrati"][str(t_id)] = {
                    "topic" : topic,
                    "objects" : topic_objs,
                    "regarts" : topic_areg
                }
            
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   '#': (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                  }

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    popover_title_content = {
        "portal_objects": {
            "title": _("Shared Portal objects"),
            "content": _("This section allows to insert, remove and edit Publications/WebPath (Active Pages) under a certain topic.") + "<br /><br />" +
                       "<b>" + _("In order for a web Publication/WebPath to be iserted here, you must first import it from the \"Shared objects\" section.") + "</b>"
        }
    }

    return render(request, 'cds_website_pages_topics.html',
                  {
                    'cds_website' : cds_website,
                    'pages': pages,
                    'topics_list': topics,
                    'objects_list': objects_list,
                    'breadcrumbs': breadcrumbs,
                    'popover_title_content': popover_title_content,
                    'logs' : logs,
                   })

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_objects_edit(request, code, cds_website=None, my_offices=None):
    
    objects_list = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_website.cds_id)

    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                          (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                        '#': _("Shared objects") }
    
    return render(request, 'cds_websites_pages_shared_objects.html',
                  {
                  'cds_website' : cds_website,
                  'objects_list': objects_list,
                  'breadcrumbs': breadcrumbs,
                  })    

#Common
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_item_delete(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    if not request.user.is_superuser and (is_protected_by_etl(regart.id_user_mod.pk) 
                                          or regart.id_didattica_cds_articoli_regolamento is not None):
        return custom_message(request, _("Permission denied"))

    regart.delete()

    log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Removed Item"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Item removed successfully"))

    return redirect('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', code=code)



@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_regart_item_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):

    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extras = SitoWebCdsTopicArticoliRegAltriDati.objects.filter(id_sito_web_cds_topic_articoli_reg=data_id)
    art_reg_form = SitoWebCdsArticoliRegolamentoItemForm(data=request.POST if request.POST else None, instance=regart, cds_id=cds_website.cds_id)

    if request.POST:

        if not request.user.is_superuser and is_protected_by_etl(regart.id_user_mod.pk):
            return custom_message(request, _("Permission denied"))

        if art_reg_form.is_valid():

            art_reg = art_reg_form.save(commit=False)
            art_reg.dt_mod = datetime.datetime.now()
            art_reg.id_user_mod=request.user
            art_reg.save()

            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Regulation Article"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulation Article edited successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")


    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   '#': regart.titolo_it }

    popover_title_content = {
        'extras': {
            'title': _("Regulation Articles' Extras"),
            'content': _("This section allows to manage Extra elements (usually links) which are appended beneath the article.")
        }
    }

    return render(request, 'cds_websites_pages_regulation_articles_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form,],
                    'regart': regart,
                    'regart_extras': regart_extras,
                    'item_label': _('Regulation Article'),
                    'popover_title_content': popover_title_content,
                    'topic_id': topic_id,
                    'edit': 1,
                  })

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_regart_extra_new(request, code, topic_id, data_id, cds_website=None, my_offices=None):

    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(data=request.POST if request.POST else None)

    if request.POST:
        if regart_extra_form.is_valid():

            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.id_sito_web_cds_topic_articoli_reg = regart
            regart_extra.id_sito_web_cds_tipo_dato = get_object_or_404(SitoWebCdsTipoDato, pk=regart_extra_form.data.get("id_sito_web_cds_tipo_dato", None))
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.id_user_mod=request.user
            regart_extra.save()

            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Regulation Article Extra"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulation Article Extra added successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_regart_item_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': _("New Extra") }

    return render(request, 'cds_websites_pages_unique_form.html',
                  {
                    'cds_website': cds_website,
                    'topic_id': topic_id,
                    'forms': [regart_extra_form,],
                    'item_label': _('Regulation Article Extra'),
                    'breadcrumbs': breadcrumbs,
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_regart_extra_edit(request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None):

    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)

    if not request.user.is_superuser and is_protected_by_etl(regart_extra.id_user_mod.pk):
        return custom_message(request, _("Permission denied"))

    initial = {
        'id_sito_web_cds_tipo_dato' : regart_extra.id_sito_web_cds_tipo_dato_id
    }
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(data=request.POST if request.POST else None, instance=regart_extra, initial=initial)

    if request.POST:
        if regart_extra_form.is_valid():

            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.id_sito_web_cds_tipo_dato = get_object_or_404(SitoWebCdsTipoDato, pk=regart_extra_form.data.get("id_sito_web_cds_tipo_dato", None))
            regart_extra.dt_mod = datetime.datetime.now()
            regart_extra.id_user_mod=request.user
            regart_extra.save()

            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Regulation Article Extra"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulation Article Extra edited successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")


    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_regart_item_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': regart_extra.testo_it if (request.LANGUAGE_CODE == 'it' or not regart_extra.testo_en) else regart_extra.testo_en }

    return render(request, 'cds_websites_pages_unique_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id': topic_id,
                    'forms': [regart_extra_form,],
                    'item_label': _('Regulation Article Extra'),
                    'edit': 1,
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_regart_extra_delete(request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None):

    extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)

    if not request.user.is_superuser and is_protected_by_etl(extra.id_user_mod.pk):
        return custom_message(request, _("Permission denied"))

    extra.delete()

    log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Deleted Regulation Article Extra"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Regulation Article Extra deleted successfully"))

    return redirect('crud_cds_websites_pages:crud_cds_websites_pages_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)



#Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_object_edit(request, code, data_id, cds_website=None, my_offices=None):

    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    if not request.user.is_superuser and is_protected_by_etl(_object.id_user_mod.pk):
        return custom_message(request, _("Permission denied"))

    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None, instance=_object)

    if request.POST:
        if object_form.is_valid():

            _object = object_form.save(commit=False)
            _object.id_user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.save()

            log_action(user=request.user,
                        obj=cds_website,
                        flag=CHANGE,
                        msg=_("Edited object"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Object edited successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_objects_edit', code=code)

        else:  # pragma: no cover
            for k, v in object_form.errors.items():
                if k == '__all__':
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_objects_edit', kwargs={'code': code}): _("Shared objects"),
                   '#': _("Edit Object") }

    return render(request, 'cds_website_pages_shared_object_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [object_form,],
                    'item_label': _('Object'),
                    'edit': 1,
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_object_new(request, code, cds_website=None, my_offices=None):

    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None)

    if request.POST:
        if  object_form.is_valid():

            _object = object_form.save(commit=False)
            _object.cds = cds_website.cds
            _object.id_user_mod = request.user
            _object.dt_mod = datetime.datetime.now()
            _object.aa_regdid_id = max(DidatticaRegolamento.objects.filter(cds_id=cds_website.cds_id).values_list('aa_reg_did', flat=True))
            _object.save()

            log_action(user=request.user,
                        obj=cds_website,
                        flag=CHANGE,
                        msg=_("Added object"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Object added successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_objects_edit', code=code)

        else:  # pragma: no cover
            for k, v in object_form.errors.items():
                if k == '__all__':
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_objects_edit', kwargs={'code': code}): _("Shared objects"),
                   '#': _("New Object") }

    return render(request, 'cds_website_pages_shared_object_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [object_form,],
                    'item_label': _('Object'),
                  })

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_object_delete(request, code, data_id, cds_website=None, my_offices=None):

    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)

    if not request.user.is_superuser and is_protected_by_etl(_object.id_user_mod.pk):
        return custom_message(request, _("Permission denied"))

    _object.delete()

    log_action(user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Removed object"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Object removed successfully"))

    return redirect('crud_cds_websites_pages:crud_cds_websites_pages_objects_edit', code=code)


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_object_item_add(request, code, topic_id, cds_website=None, my_offices=None):

    obj_item_form = SitoWebCdsOggettiItemForm(data=request.POST if request.POST else None, cds_id=cds_website.cds_id)

    if request.POST:
        if obj_item_form.is_valid():

            obj_item = obj_item_form.save(commit=False)
            obj_item.id_sito_web_cds_topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)
            obj_item.id_sito_web_cds_oggetti_portale = get_object_or_404(SitoWebCdsOggettiPortale, pk=obj_item_form.data.get("id_sito_web_cds_oggetti_portale", None))
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.id_user_mod=request.user
            obj_item.save()

            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Portal Object"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Portal Object added successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in obj_item_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{obj_item_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   '#': _("Add Portal Object") }

    return render(request, 'cds_websites_pages_unique_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id' : topic_id,
                    'forms': [obj_item_form,],
                    'item_label': _('Portal Object'),
                  })

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_pages_object_item_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):

    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)

    if not request.user.is_superuser and is_protected_by_etl(regart.id_user_mod.pk):
        return custom_message(request, _("Permission denied"))

    initial = {
        "id_sito_web_cds_oggetti_portale": regart.id_sito_web_cds_oggetti_portale.id,
    }
    obj_item_form = SitoWebCdsOggettiItemForm(data=request.POST if request.POST else None, instance=regart, cds_id=cds_website.cds_id, initial=initial)

    if request.POST:
        if obj_item_form.is_valid():

            obj_item = obj_item_form.save(commit=False)
            obj_item.dt_mod = datetime.datetime.now()
            obj_item.id_user_mod=request.user
            obj_item.save()

            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Item Article"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Item edited successfully"))

            return redirect('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in obj_item_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{obj_item_form.fields[k].label}</b>: {v}")


    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages'): _('CdS pages'),
                   reverse('crud_cds_websites_pages:crud_cds_websites_pages_topics_edit', kwargs={'code': code}):
                       (cds_website.cds.nome_cds_it if (request.LANGUAGE_CODE == 'it' or not cds_website.cds.nome_cds_eng) else cds_website.cds.nome_cds_eng) + ' (' + _("Topics") + ')',
                   '#': regart.titolo_it }


    return render(request, 'cds_websites_pages_unique_form.html',
                  {
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [obj_item_form,],
                    'regart': regart,
                    'item_label': _('Item'),
                    'topic_id': topic_id,
                    'edit': 1,
                  })
