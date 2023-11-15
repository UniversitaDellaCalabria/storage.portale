import logging

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils.timezone import *


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *
from . settings import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS Websites')}
    context = { 'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites.html', context)



@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_topics_edit(request, code, cds_website=None, my_offices=None):
    """
    modifica dei dati dei topic del sito web del corso di studio
    """

    topics = SitoWebCdsTopic.objects.all()
    
    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects\
        .select_related("id_sito_web_cds_oggetti_portale", "id_sito_web_cds_topic")\
        .filter(Q(id_sito_web_cds_oggetti_portale__cds_id=cds_website.cds_id) | Q(id_sito_web_cds_articoli_regolamento__cds_id=cds_website.cds_id))
    
    topic_enroll = {}
    topic_study = {}
    topic_opportunities = {}
    topic_organization = {}
    topic_notshown = {}
        
    for topic in topics:
        t_id = topic.id
        cds_topic_ogg_art_current = cds_topic_ogg_art.filter(id_sito_web_cds_topic=t_id).order_by("ordine")
        topic_objs = cds_topic_ogg_art_current.filter(id_sito_web_cds_oggetti_portale__isnull=False)
        topic_areg = cds_topic_ogg_art_current.filter(id_sito_web_cds_articoli_regolamento__isnull=False)
        if t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['iscriversi']:
            topic_enroll[t_id] = {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg 
            }
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['studiare']:
            topic_study[t_id] = {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg 
            }
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['opportunità']:
            topic_opportunities[t_id] = {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg 
            }
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['organizzazione']:
            topic_organization[t_id] = {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg 
            }
        else:
            topic_notshown[t_id] = {
                "topic" : topic,
                "objects" : topic_objs,
                "regarts" : topic_areg 
            }

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   '#': cds_website.cds.nome_cds_it }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    return render(request, 'cds_website.html',
                  { 
                    'cds_website' : cds_website,
                    'topic_enroll': topic_enroll,
                    'topic_study': topic_study,
                    'topic_opportunities': topic_opportunities,
                    'topic_organization': topic_organization,
                    'topic_notshown': topic_notshown,
                    'topics_list': topics,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                   })


#Common
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_item_delete(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    if regart.id_sito_web_cds_articoli_regolamento is not None:
        regart.delete()
    elif regart.id_sito_web_cds_oggetti_portale is not None:
        regart.id_sito_web_cds_oggetti_portale.delete()
        
    return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)


#Reg Articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_new(request, code, topic_id, cds_website=None, my_offices=None):
                
    art_reg_form = SitoWebCdsArticoliRegolamentoForm(data=request.POST if request.POST else None, cds_id=cds_website.cds_id)
    
    if request.POST:
        if art_reg_form.is_valid():
        
            art_reg = art_reg_form.save(commit=False)
            art_reg.id_sito_web_cds_topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)
            art_reg.id_sito_web_cds_articoli_regolamento = get_object_or_404(SitoWebCdsArticoliRegolamento, pk=art_reg_form.data.get("id_sito_web_cds_articoli_regolamento", None))
            art_reg.dt_mod = now()
            art_reg.id_user_mod=request.user
            art_reg.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Regulament Article"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulament Article added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_regart_edit', code=code, topic_id=topic_id, data_id=art_reg.id)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): cds_website.cds.nome_cds_it,
                   '#': _("Add") }
    
    return render(request, 'unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id' : topic_id,
                    'forms': [art_reg_form,],
                    'item_label': _('Item'),
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extras = SitoWebCdsTopicArticoliRegAltriDati.objects.filter(id_sito_web_cds_topic_articoli_reg=data_id)
    art_reg_form = SitoWebCdsArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=regart)        
        
    if request.POST:
        if art_reg_form.is_valid():
        
            art_reg = art_reg_form.save(commit=False)
            art_reg.dt_mod = now()
            art_reg.id_user_mod=request.user
            art_reg.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Regulament Article"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulament Article edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}):cds_website.cds.nome_cds_it,
                   '#': regart.titolo_it }
    
    return render(request, 'regulament_articles.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form,],
                    'regart': regart,
                    'regart_extras': regart_extras,
                    'item_label': _('Item'),
                    'topic_id': topic_id,
                    'edit': 1,
                  })

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_extra_new(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(data=request.POST if request.POST else None)
    
    if request.POST:
        if regart_extra_form.is_valid():
        
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.id_sito_web_cds_topic_articoli_reg = regart
            regart_extra.id_sito_web_cds_tipo_dato = get_object_or_404(SitoWebCdsTipoDato, pk=regart_extra_form.data.get("id_sito_web_cds_tipo_dato", None))
            regart_extra.dt_mod = now()
            regart_extra.id_user_mod=request.user
            regart_extra.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Regulament Article Extra"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulament Article Extra added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_regart_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}) : cds_website.cds.nome_cds_it,
                   reverse('crud_cds_websites:crud_cds_websites_regart_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': _("New Extra") }
    
    return render(request, 'unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'topic_id': topic_id,
                    'forms': [regart_extra_form,],
                    'item_label': _('Regulament Article Extra'),
                    'breadcrumbs': breadcrumbs,
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_extra_edit(request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None):
    
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)
    initial = {
        'id_sito_web_cds_tipo_dato' : regart_extra.id_sito_web_cds_tipo_dato_id
    }
    regart_extra_form = SitoWebCdsTopicArticoliRegAltriDatiForm(data=request.POST if request.POST else None, instance=regart_extra, initial=initial)
    
    if request.POST:
        if regart_extra_form.is_valid():
        
            regart_extra = regart_extra_form.save(commit=False)
            regart_extra.id_sito_web_cds_tipo_dato = get_object_or_404(SitoWebCdsTipoDato, pk=regart_extra_form.data.get("id_sito_web_cds_tipo_dato", None))
            regart_extra.dt_mod = now()
            regart_extra.id_user_mod=request.user
            regart_extra.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Regulament Article Extra"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Regulament Article Extra edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_regart_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")
    
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}) : cds_website.cds.nome_cds_it,
                   reverse('crud_cds_websites:crud_cds_websites_regart_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': _("Extra Edit") }
    
    return render(request, 'unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id': topic_id,
                    'forms': [regart_extra_form,],
                    'item_label': _('Regulament Article Extra'),
                    'edit': 1,
                  })
    

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_extra_delete(request, code, topic_id, data_id, extra_id, cds_website=None, my_offices=None):
    
    extra = get_object_or_404(SitoWebCdsTopicArticoliRegAltriDati, pk=extra_id)
    extra.delete()
    
    log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Deleted Regulament Article Extra"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Regulament Article Extra deleted successfully"))
    
    return redirect('crud_cds_websites:crud_cds_websites_regart_edit', code=code, topic_id=topic_id, data_id=data_id)
    
    
    
#Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    
    tregart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    
    art_reg_form = SitoWebCdsTopicArticoliItemForm(data=request.POST if request.POST else None, instance=tregart)

    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None, instance=tregart.id_sito_web_cds_oggetti_portale)
    
    if request.POST:
        if art_reg_form.is_valid() and object_form.is_valid():
            
            art_reg = art_reg_form.save(commit=False)
            art_reg.id_user_mod = request.user
            art_reg.dt_mod = now()
            art_reg.save()
            
            _object = object_form.save(commit=False)
            _object.id_user_mod = request.user
            _object.dt_mod = now()
            _object.save()

            log_action(user=request.user,
                        obj=cds_website,
                        flag=CHANGE,
                        msg=_("Edited object"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Object edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{art_reg_form.fields[k].label}</b>: {v}")
            for k, v in object_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): cds_website.cds.nome_cds_it,
                   '#': tregart.titolo_it }
    
    return render(request, 'unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form, object_form,],
                    'item_label': _('Item'),
                    'edit': 1,
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_new(request, code, topic_id, cds_website=None, my_offices=None):
        
    art_reg_form = SitoWebCdsTopicArticoliItemForm(data=request.POST if request.POST else None)

    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None)
    
    if request.POST:
        if art_reg_form.is_valid() and object_form.is_valid():
            
            _object = object_form.save(commit=False)
            _object.id_sito_web_cds_topic = topic_id
            _object.cds = cds_website.cds 
            _object.id_user_mod = request.user
            _object.dt_mod = now()
            _object.save()
            
            art_reg = art_reg_form.save(commit=False)
            art_reg.id_sito_web_cds_oggetti_portale = _object
            art_reg.id_sito_web_cds_topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)
            art_reg.id_user_mod = request.user
            art_reg.dt_mod = now()
            art_reg.save()

            log_action(user=request.user,
                        obj=cds_website,
                        flag=CHANGE,
                        msg=_("Added object"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Object added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{art_reg_form.fields[k].label}</b>: {v}")
            for k, v in object_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en,
                   '#': _("New Object") }
    
    return render(request, 'unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form, object_form,],
                    'item_label': _('Item'),
                    'edit': 1,
                  })
    

    
