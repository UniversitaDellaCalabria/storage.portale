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
from . utils import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Study Course Websites')}
    context = { 'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites.html', context)


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_website(request, code, cds_website=None, my_offices=None):
    """
    Menu di un sito web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Study Course Websites'),
                    '#': cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                }
    
    return render(request, 'cds_website.html', {
        'breadcrumbs': breadcrumbs,
        'cds_website': cds_website,
    })
    
#Dati Base
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_base_edit(request, code, cds_website=None, my_offices=None):
    base_form = SitoWebCdsDatiBaseForm(data=request.POST if request.POST else None, instance=cds_website)
    
    if request.POST:
        if base_form.is_valid():
        
            base = base_form.save(commit=False)
            base.dt_mod = now()
            base.id_user_mod=request.user
            base.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edit Base Information"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Base Information edited successfully"))

            return redirect('crud_cds_websites:crud_cds_website_base_edit', code=code)

        else:  # pragma: no cover
            for k, v in base_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{base_form.fields[k].label}</b>: {v}")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Base Info") }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)
    
    return render(request, 'base_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                    'forms': [base_form,],
                    'item_label': _('Item'),
                  })

#Sliders
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sliders(request, code, cds_website=None, my_offices=None):
    
    sliders = SitoWebCdsSlider.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Sliders") }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    return render(request, 'cds_website_sliders.html',
                  { 
                    'cds_website' : cds_website,
                    'sliders': sliders,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                   })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sliders_new(request, code, cds_website=None, my_offices=None):
    slider_form = SitoWebCdsSliderForm(data=request.POST if request.POST else None)        
        
    if request.POST:
        if slider_form.is_valid():
        
            slider = slider_form.save(commit=False)
            slider.dt_mod = now()
            slider.id_user_mod=request.user
            slider.id_sito_web_cds_dati_base = cds_website
            slider.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Slider"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Slider added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_sliders', code=code)

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{slider_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_sliders', kwargs={'code': code}): _("Sliders"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [slider_form,],
                    'item_label': _('Scrollable Text'),
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sliders_edit(request, code, data_id, cds_website=None, my_offices=None):
    slider = get_object_or_404(SitoWebCdsSlider, pk=data_id)
    slider_form = SitoWebCdsSliderForm(data=request.POST if request.POST else None, instance=slider)        
        
    if request.POST:
        if slider_form.is_valid():
        
            slider = slider_form.save(commit=False)
            slider.dt_mod = now()
            slider.id_user_mod=request.user
            slider.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Slider"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Slider edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_sliders', code=code)

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{slider_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_sliders', kwargs={'code': code}): _("Sliders"),
                   '#': _("Edit"), }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [slider_form,],
                    'item_label': _('Scrollable Text'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_sliders_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    slider = get_object_or_404(SitoWebCdsSlider, pk=data_id)
    slider.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Slider"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Slider deleted successfully"))

    return redirect('crud_cds_websites:crud_cds_websites_sliders', code=code)


#Ex Students
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_exstudents(request, code, cds_website=None, my_offices=None):
    
    exstudents = SitoWebCdsExStudenti.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Ex Students") }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    return render(request, 'cds_website_exstudents.html',
                  { 
                    'cds_website' : cds_website,
                    'exstudents': exstudents,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                   })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_exstudents_new(request, code, cds_website=None, my_offices=None):
    exstudent_form = SitoWebCdsExStudentiForm(data=request.POST if request.POST else None,
                                              files=request.FILES if request.FILES else None)
        
    if request.POST:
        if exstudent_form.is_valid():
        
            exstudent = exstudent_form.save(commit=False)
            exstudent.id_sito_web_cds_dati_base = cds_website
            exstudent.dt_mod = now()
            exstudent.id_user_mod=request.user
            exstudent.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Ex Student"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Ex Student added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_exstudents', code=code)

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{exstudent_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_exstudents', kwargs={'code': code}): _("Ex Students"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [exstudent_form,],
                    'item_label': _('Ex Student'),
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_exstudents_edit(request, code, data_id, cds_website=None, my_offices=None):
    exstudent = get_object_or_404(SitoWebCdsExStudenti, pk=data_id)
    exstudent_form = SitoWebCdsExStudentiForm(data=request.POST if request.POST else None,
                                              files=request.FILES if request.FILES else None,
                                              instance=exstudent)        
        
    if request.POST:
        if exstudent_form.is_valid():
        
            exstudent = exstudent_form.save(commit=False)
            exstudent.dt_mod = now()
            exstudent.id_user_mod=request.user
            exstudent.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Ex Student"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Ex Student edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_exstudents', code=code)

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{exstudent_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_exstudents', kwargs={'code': code}): _("Ex Students"),
                   '#': exstudent.nome, }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [exstudent_form,],
                    'item_label': _('Ex Student'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_exstudents_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    exstudent = get_object_or_404(SitoWebCdsExStudenti, pk=data_id)
    exstudent.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Ex Student"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Ex Student deleted successfully"))

    return redirect('crud_cds_websites:crud_cds_websites_exstudents', code=code)


#Links
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_links(request, code, cds_website=None, my_offices=None):
    
    links = SitoWebCdsLink.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Links") }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    return render(request, 'cds_website_links.html',
                  { 
                    'cds_website' : cds_website,
                    'links': links,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                   })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_links_new(request, code, cds_website=None, my_offices=None):
    link_form = SitoWebCdsLinkForm(data=request.POST if request.POST else None)
        
    if request.POST:
        if link_form.is_valid():
        
            link = link_form.save(commit=False)
            link.id_sito_web_cds_dati_base = cds_website
            link.dt_mod = now()
            link.id_user_mod=request.user
            link.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Link"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Link added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_links', code=code)

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{link_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_links', kwargs={'code': code}): _("Links"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [link_form,],
                    'item_label': _('Link'),
                  })
    
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_links_edit(request, code, data_id, cds_website=None, my_offices=None):
    link = get_object_or_404(SitoWebCdsLink, pk=data_id)
    link_form = SitoWebCdsLinkForm(data=request.POST if request.POST else None, instance=link)        
        
    if request.POST:
        if link_form.is_valid():
        
            link = link_form.save(commit=False)
            link.dt_mod = now()
            link.id_user_mod=request.user
            link.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Link"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Link edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_links', code=code)

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{link_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_links', kwargs={'code': code}): _("Links"),
                   '#': link.descrizione_link_it, }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [link_form,],
                    'item_label': _('Link'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_links_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    link = get_object_or_404(SitoWebCdsLink, pk=data_id)
    link.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Link"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Link deleted successfully"))

    return redirect('crud_cds_websites:crud_cds_websites_links', code=code)



#Topics
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_topics_edit(request, code, cds_website=None, my_offices=None):
    """
    modifica dei dati dei topic del sito web del corso di studio
    """

    topics = SitoWebCdsTopic.objects.all()
    
    objects_list = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_website.cds_id)
    
    cds_topic_ogg_art = SitoWebCdsTopicArticoliReg.objects\
        .select_related("id_sito_web_cds_oggetti_portale", "id_sito_web_cds_topic")\
        .filter(Q(id_sito_web_cds_oggetti_portale__cds_id=cds_website.cds_id) | Q(id_sito_web_cds_articoli_regolamento__cds_id=cds_website.cds_id))
    
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
    pages["Non mostrati"] = {}
        
    for topic in topics:
        t_id = topic.id
        cds_topic_ogg_art_current = cds_topic_ogg_art.filter(id_sito_web_cds_topic=t_id).order_by("ordine")
        topic_objs = cds_topic_ogg_art_current.filter(id_sito_web_cds_oggetti_portale__isnull=False)
        topic_areg = cds_topic_ogg_art_current.filter(id_sito_web_cds_articoli_regolamento__isnull=False)
        
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
            pages["Non mostrati"][str(t_id)] = {
                    "topic" : topic,
                    "objects" : topic_objs,
                    "regarts" : topic_areg 
                }

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Topics"),
                   }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    return render(request, 'cds_website_topics.html',
                  { 
                    'cds_website' : cds_website,
                    'pages': pages,
                    'topics_list': topics,
                    'objects_list': objects_list,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                   })


#Common
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_item_delete(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart.delete()
    
    log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Removed Item"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Item removed successfully"))
        
    return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)


#Reg Articles
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_add(request, code, topic_id, cds_website=None, my_offices=None):
                
    art_reg_form = SitoWebCdsArticoliRegolamentoItemForm(data=request.POST if request.POST else None, cds_id=cds_website.cds_id)
    
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

            return redirect('crud_cds_websites:crud_cds_websites_regart_item_edit', code=code, topic_id=topic_id, data_id=art_reg.id)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': _("Add Regulament Article") }
    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id' : topic_id,
                    'forms': [art_reg_form,],
                    'item_label': _('Regulament Article'),
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_regart_item_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    regart_extras = SitoWebCdsTopicArticoliRegAltriDati.objects.filter(id_sito_web_cds_topic_articoli_reg=data_id)
    art_reg_form = SitoWebCdsArticoliRegolamentoItemForm(data=request.POST if request.POST else None, instance=regart, cds_id=cds_website.cds_id)        
        
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
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': regart.titolo_it }

    
    return render(request, 'regulament_articles.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form,],
                    'regart': regart,
                    'regart_extras': regart_extras,
                    'item_label': _('Regulament Article'),
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

            return redirect('crud_cds_websites:crud_cds_websites_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}) : _("Topics"),
                   reverse('crud_cds_websites:crud_cds_websites_regart_item_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': _("New Extra") }
    
    return render(request, 'cds_websites_unique_form.html',
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

            return redirect('crud_cds_websites:crud_cds_websites_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)

        else:  # pragma: no cover
            for k, v in regart_extra_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{regart_extra_form.fields[k].label}</b>: {v}")
    
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en,
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}) : _("Topics"),
                   reverse('crud_cds_websites:crud_cds_websites_regart_item_edit', kwargs={'code': code, 'topic_id' : topic_id, 'data_id' : data_id }) : regart.titolo_it,
                   '#': regart_extra.testo_it if (request.LANGUAGE_CODE == 'it' or not regart_extra.testo_en) else regart_extra.testo_en }
    
    return render(request, 'cds_websites_unique_form.html',
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
    
    return redirect('crud_cds_websites:crud_cds_websites_regart_item_edit', code=code, topic_id=topic_id, data_id=data_id)
    
    
    
#Objects
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_edit(request, code, data_id, cds_website=None, my_offices=None):
        
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)
    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None, instance=_object)
    
    object_preview = get_object_preview(_object.id_oggetto_portale, _object.id_classe_oggetto_portale)
    
    if request.POST:
        if object_form.is_valid():
            
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
            for k, v in object_form.errors.items():
                if k == '__all__':
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")                    
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en,
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': _("Edit Object") }
    
    return render(request, 'object_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'object_preview': object_preview,
                    'forms': [object_form,],
                    'item_label': _('Object'),
                    'edit': 1,
                  })


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_new(request, code, cds_website=None, my_offices=None):
        
    object_form = SitoWebCdsOggettiPortaleForm(data=request.POST if request.POST else None)
    
    if request.POST:
        if  object_form.is_valid():
            
            _object = object_form.save(commit=False)
            _object.cds = cds_website.cds 
            _object.id_user_mod = request.user
            _object.dt_mod = now()
            _object.save()

            log_action(user=request.user,
                        obj=cds_website,
                        flag=CHANGE,
                        msg=_("Added object"))

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Object added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in object_form.errors.items():
                if k == '__all__':
                    messages.add_message(request, messages.ERROR, f"{v}")
                else:
                    messages.add_message(request, messages.ERROR,
                                     f"<b>{object_form.fields[k].label}</b>: {v}")  
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en,
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': _("New Object") }
    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [object_form,],
                    'item_label': _('Object'),
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_delete(request, code, data_id, cds_website=None, my_offices=None):
        
    _object = get_object_or_404(SitoWebCdsOggettiPortale, pk=data_id)
    _object.delete()

    log_action(user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Removed object"))

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Object removed successfully"))

    return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_add(request, code, topic_id, cds_website=None, my_offices=None):
                
    art_reg_form = SitoWebCdsOggettiItemForm(data=request.POST if request.POST else None, cds_id=cds_website.cds_id)
    
    if request.POST:
        if art_reg_form.is_valid():
        
            art_reg = art_reg_form.save(commit=False)
            art_reg.id_sito_web_cds_topic = get_object_or_404(SitoWebCdsTopic, pk=topic_id)
            art_reg.id_sito_web_cds_oggetti_portale = get_object_or_404(SitoWebCdsOggettiPortale, pk=art_reg_form.data.get("id_sito_web_cds_oggetti_portale", None))
            art_reg.dt_mod = now()
            art_reg.id_user_mod=request.user
            art_reg.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Added Portal Object"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Portal Object added successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_regart_item_edit', code=code, topic_id=topic_id, data_id=art_reg.id)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': _("Add Portal Object") }
    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'topic_id' : topic_id,
                    'forms': [art_reg_form,],
                    'item_label': _('Portal Object'),
                  })
    
@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_object_item_edit(request, code, topic_id, data_id, cds_website=None, my_offices=None):
    
    regart = get_object_or_404(SitoWebCdsTopicArticoliReg, pk=data_id)
    initial = {
        "id_sito_web_cds_oggetti_portale": regart.id_sito_web_cds_oggetti_portale.id,
    }
    art_reg_form = SitoWebCdsOggettiItemForm(data=request.POST if request.POST else None, instance=regart, cds_id=cds_website.cds_id, initial=initial)        
        
    if request.POST:
        if art_reg_form.is_valid():
        
            art_reg = art_reg_form.save(commit=False)
            art_reg.dt_mod = now()
            art_reg.id_user_mod=request.user
            art_reg.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited Item Article"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Item edited successfully"))

            return redirect('crud_cds_websites:crud_cds_websites_topics_edit', code=code)

        else:  # pragma: no cover
            for k, v in art_reg_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{art_reg_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cds_websites'): _('Cds websites'),
                   reverse('crud_cds_websites:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites:crud_cds_websites_topics_edit', kwargs={'code': code}): _("Topics"),
                   '#': regart.titolo_it }

    
    return render(request, 'cds_websites_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [art_reg_form,],
                    'regart': regart,
                    'item_label': _('Item'),
                    'topic_id': topic_id,
                    'edit': 1,
                  })