import logging
from datetime import datetime

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
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites.html', context)



@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_edit(request, code, cds=None, my_offices=None):
    """
    modifica dati del sito web del corso di studio
    """

    topics = SitoWebCdsTopic.objects.all()
    
    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects\
        .select_related("id_sito_web_cds_oggetti_portale", "id_sito_web_cds_topic")\
        .filter(Q(id_sito_web_cds_oggetti_portale__cds_id=cds) | Q(id_sito_web_cds_articoli_regolamento__cds_id=cds))
    
    topic_enroll = {}
    topic_study = {}
    topic_opportunities = {}
    topic_organization = {}
    topic_notshown = {}
    
    for topic in topics:
        t_id = topic.id
        cds_topic_ogg_art_current = cds_topic_ogg_art.filter(id_sito_web_cds_topic=t_id).order_by("ordine")
        if t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['iscriversi']:
            topic_enroll[t_id] = cds_topic_ogg_art_current
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['studiare']:
            topic_study[t_id] = cds_topic_ogg_art_current
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['opportunità']:
            topic_opportunities[t_id] = cds_topic_ogg_art_current
        elif t_id in CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS['organizzazione']:
            topic_organization[t_id] = cds_topic_ogg_art_current
        else:
            topic_notshown[t_id] = cds_topic_ogg_art_current
    
    if request.POST:
        pass

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   '#': cds.nome_cds_it }

    return render(request, 'cds_website.html',
                  { 
                    'cds': cds,
                    'topic_enroll': topic_enroll,
                    'topic_study': topic_study,
                    'topic_opportunities': topic_opportunities,
                    'topic_organization': topic_organization,
                    'topic_notshown': topic_notshown,
                    'topics_list': topics,
                    'breadcrumbs': breadcrumbs,
                   })

#Common
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_tregart_edit(request, code, tregart_id, cds=None, my_offices=None):
    
    tregart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=tregart_id)
    print("Editing", tregart.titolo_it)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': tregart.titolo_it }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                    'item_label': _('Regulament Article Settings'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_tregart_delete(request, code, tregart_id, cds=None, my_offices=None):
    
    print("Deleting %d", data_id)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _("New Object") }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                  })

#Reg Articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_tregart_extra_new(request, code, tregart_id, cds=None, my_offices=None):
    
    cds_topic_ogg_art = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=tregart_id)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _("New Extra for Regulament Article") + f" {cds_topic_ogg_art.titolo_it}"  }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                    'item_label': _('Regulament Article Extras'),
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_tregart_extra_edit(request, code, tregart_id, data_id, cds=None, my_offices=None):
    
    print("Editing %", data_id)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _("New Object") }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                    'item_label': _('Regulament Article Attribute'),
                    'edit': 1,
                  })
    

@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_tregart_extra_delete(request, code, tregart_id, data_id, cds=None, my_offices=None):
    
    print("Deleting %d", data_id)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _("New Object") }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                  })    
    
    
    
#Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_objects_new(request, code, cds=None, my_offices=None):
    
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': _("New") }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                    'item_label': _('Object'),
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_objects_edit(request, code, tregart_id, cds=None, my_offices=None):
    
    obj = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_websites_edit', kwargs={'code': code}): cds.nome_cds_it,
                   '#': obj.testo_it }
    
    return render(request, 'unique_form.html',
                  { 
                   'breadcrumbs': breadcrumbs,
                    'cds': cds,
                    'item_label': _('Object'),
                    'edit': 1,
                  })
    
