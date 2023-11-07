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
def cds_website(request, code, cds=None, my_offices=None):
    """
    modifica dati del sito web del corso di studio
    """
    #OGGETTI -> CDS
    #REGOLAMENTO -> CDS
    #ALTRI_DATI -> REG
    #REG : REGOLAMENTO <> TOPIC <> OGGETTI
    
    
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
        topic_objs = [obj for obj in map(lambda toa: (toa, toa.id_sito_web_cds_oggetti_portale), cds_topic_ogg_art_current) if obj[1] is not None]
        topic_areg = [art for art in map(lambda toa: (toa, toa.id_sito_web_cds_articoli_regolamento), cds_topic_ogg_art_current) if art[1] is not None]
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
            

    
    if request.POST:
        pass

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cdswebsites'): _('Cds websites'),
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