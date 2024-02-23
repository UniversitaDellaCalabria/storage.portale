import logging

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *

from ricerca_app.models import *
from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_cds_website
def cds_websites_brochure(request, my_offices=None):
    """
    lista dei siti web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('CdS in brief')}
    context = { 'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdswebsitelist')}
    return render(request, 'cds_websites_brochure.html', context)


@login_required
@can_manage_cds_website
def cds_website_brochure(request, code, cds_website=None, my_offices=None):
    """
    Menu di un sito web dei corsi di studio
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                    '#': cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                }
    
    return render(request, 'cds_website_brochure.html', {
        'breadcrumbs': breadcrumbs,
        'cds_website': cds_website,
    })
    
#Dati Base
@login_required
@can_manage_cds_website
def cds_websites_brochure_info_edit(request, code, cds_website=None, my_offices=None):

    tab_form_dict = {
        'Dati corso': SitoWebCdsDatiBaseDatiCorsoForm(instance=cds_website, initial={ 'languages': cds_website.lingua_it}),
        'In pillole': SitoWebCdsDatiBaseInPilloleForm(instance=cds_website),
        'Profilo corso': SitoWebCdsDatiBaseProfiloCorsoForm(instance=cds_website),
        'Intro amm': SitoWebCdsDatiBaseIntroAmmForm(instance=cds_website),
    }
    last_viewed_tab = None
    
    if request.POST:
        form = None
        dati_base = None
        form_name = request.POST.get('tab_form_dict_key')
        try:
            match form_name:
                case 'Dati corso':
                    form = SitoWebCdsDatiBaseDatiCorsoForm(data=request.POST, instance=cds_website, initial={'languages': cds_website.lingua_it})
                case 'In pillole':
                    form = SitoWebCdsDatiBaseInPilloleForm(data=request.POST, instance=cds_website)                
                case 'Profilo corso':
                    form = SitoWebCdsDatiBaseProfiloCorsoForm(data=request.POST, instance=cds_website)
                case 'Intro amm':
                    form = SitoWebCdsDatiBaseIntroAmmForm(data=request.POST, instance=cds_website)
            
            last_viewed_tab = form_name
            
            if not form.is_valid():
                raise Exception(_("Form validation failed"))        
            
            dati_base = form.save(commit=False)            
            
            if form_name == 'Dati corso':
                selected_languages = form.data['languages']
                languages = {
                    'italiano': {
                        'it': 'italiano',
                        'en': 'italian'
                    },
                    'inglese': {
                        'it': 'inglese',
                        'en': 'italiano'
                    },
                    'italiano, inglese': {
                        'it': 'italiano, inglese',
                        'en': 'italian, english'
                    }
                }
                dati_base.lingua_it = languages[selected_languages]['it']
                dati_base.lingua_en = languages[selected_languages]['en']
                                        
            dati_base.dt_mod = now()
            dati_base.id_user_mod=request.user
            dati_base.save()
        
            log_action(user=request.user,
                            obj=cds_website,
                            flag=CHANGE,
                            msg=_("Edited website info") + f" ({form_name})")

            messages.add_message(request,
                                    messages.SUCCESS,
                                    f"({form_name}) - " + _("Website info edited successfully"))

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_info_edit', code=code)    
                
        except:
            
            tab_form_dict[form_name] = form
            
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{form.fields[k].label}</b>: {v}")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   '#': _("Info") }
    
    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)
    
    return render(request, 'cds_website_info_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'logs' : logs,
                    'forms': tab_form_dict,
                    'last_viewed_tab': last_viewed_tab,
                    'item_label': _('Info'),
                  })

#Sliders
@login_required
@can_manage_cds_website
def cds_websites_brochure_sliders(request, code, cds_website=None, my_offices=None):
    
    sliders = SitoWebCdsSlider.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
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
def cds_websites_brochure_sliders_new(request, code, cds_website=None, my_offices=None):
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
                            msg=_("Added Scrollable Text"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Scrollable Text added successfully"))

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_sliders', code=code)

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{slider_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_sliders', kwargs={'code': code}): _("Sliders"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [slider_form,],
                    'item_label': _('Scrollable Text'),
                  })
    
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_sliders_edit(request, code, data_id, cds_website=None, my_offices=None):
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
                            msg=_("Edited Scrollable Text"))

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Scrollable Text edited successfully"))

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_sliders', code=code)

        else:  # pragma: no cover
            for k, v in slider_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{slider_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_sliders', kwargs={'code': code}): _("Sliders"),
                   '#': _("Edit"), }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [slider_form,],
                    'item_label': _('Scrollable Text'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_sliders_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    slider = get_object_or_404(SitoWebCdsSlider, pk=data_id)
    slider.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Scrollable Text"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Scrollable Text deleted successfully"))

    return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_sliders', code=code)


#Ex Students
@login_required
@can_manage_cds_website
def cds_websites_brochure_exstudents(request, code, cds_website=None, my_offices=None):
    
    exstudents = SitoWebCdsExStudenti.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
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
def cds_websites_brochure_exstudents_new(request, code, cds_website=None, my_offices=None):
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

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_exstudents', code=code)

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{exstudent_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_exstudents', kwargs={'code': code}): _("Ex Students"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [exstudent_form,],
                    'item_label': _('Ex Student'),
                  })
    
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_exstudents_edit(request, code, data_id, cds_website=None, my_offices=None):
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

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_exstudents', code=code)

        else:  # pragma: no cover
            for k, v in exstudent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{exstudent_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_exstudents', kwargs={'code': code}): _("Ex Students"),
                   '#': exstudent.nome, }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [exstudent_form,],
                    'item_label': _('Ex Student'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_exstudents_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    exstudent = get_object_or_404(SitoWebCdsExStudenti, pk=data_id)
    exstudent.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Ex Student"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Ex Student deleted successfully"))

    return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_exstudents', code=code)


#Links
@login_required
@can_manage_cds_website
def cds_websites_brochure_links(request, code, cds_website=None, my_offices=None):
    
    links = SitoWebCdsLink.objects.filter(id_sito_web_cds_dati_base=code).order_by("ordine")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
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
def cds_websites_brochure_links_new(request, code, cds_website=None, my_offices=None):
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

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_links', code=code)

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{link_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_links', kwargs={'code': code}): _("Links"),
                   '#': _("New"), }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [link_form,],
                    'item_label': _('Link'),
                  })
    
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_links_edit(request, code, data_id, cds_website=None, my_offices=None):
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

            return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_links', code=code)

        else:  # pragma: no cover
            for k, v in link_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{link_form.fields[k].label}</b>: {v}")
        
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure'): _('CdS in brief'),
                   reverse('crud_cds_websites_brochure:crud_cds_website_brochure', kwargs={'code': code} ): cds_website.nome_corso_it if (request.LANGUAGE_CODE == 'it' or not cds_website.nome_corso_en) else cds_website.nome_corso_en, 
                   reverse('crud_cds_websites_brochure:crud_cds_websites_brochure_links', kwargs={'code': code}): _("Links"),
                   '#': link.descrizione_link_it, }

    
    return render(request, 'cds_websites_brochure_unique_form.html',
                  { 
                    'cds_website': cds_website,
                    'breadcrumbs': breadcrumbs,
                    'forms': [link_form,],
                    'item_label': _('Link'),
                    'edit': 1,
                  })
    
@login_required
@can_manage_cds_website
def cds_websites_brochure_links_delete(request, code, data_id, cds_website=None, my_offices=None):
    
    link = get_object_or_404(SitoWebCdsLink, pk=data_id)
    link.delete()
        
    log_action( user=request.user,
                obj=cds_website,
                flag=CHANGE,
                msg=_("Deleted Link"))

    messages.add_message(   request,
                            messages.SUCCESS,
                            _("Link deleted successfully"))

    return redirect('crud_cds_websites_brochure:crud_cds_websites_brochure_links', code=code)
