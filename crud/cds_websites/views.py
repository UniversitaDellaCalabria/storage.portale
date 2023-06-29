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


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from . decorators import *
from . forms import *


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
def cds_website(request, code,
            my_offices=None, cds_website=None, ex_students=None, sliders=None, links=None):
    """
    modifica dati del sito web del corso di studio
    """
    form = SitoWebCdsDatiBaseForm(instance=cds_website)
    cds_data = get_object_or_404(SitoWebCdsDatiBase, pk=code)

    if request.POST:
        form = SitoWebCdsDatiBaseForm(instance=cds_website, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            cds_website.user_mod = request.user
            cds_website.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=cds_website,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Cds website edited successfully"))

            return redirect('crud_cds_websites:crud_cds_website_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(cds_website).pk,
                                   object_id=cds_website.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cdswebsites'): _('Cds websites'),
                   '#': cds_website.nome_corso_it}

    return render(request,
                  'cds_website.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'cds_website': cds_website,
                   'cds_data': cds_data,
                   'ex_students': ex_students,
                   'sliders': sliders,
                   'links': links})


@login_required
@can_manage_cds_website
@can_edit_cds_website
def cds_websites_ex_students_data_edit(request, code, student_id, cds_website=None, my_offices=None):
    """
    docente principale dottorato
    """
    ex_student = get_object_or_404(SitoWebCdsExStudenti,
                                         pk=student_id,
                                         id_sito_web_cds_dati_base=cds_website)


    if request.POST:
        form = SitoWebCdsExStudentiForm(instance=ex_student, data=request.POST)

        if form.is_valid():
            ex_student.nome = form.cleaned_data['nome']

            ex_student.user_mod = request.user
            ex_student.dt_mod = datetime.datetime.now()
            ex_student.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=cds_website,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Ex student edited successfully"))

            return redirect('crud_cds_websites:crud_cds_website_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_cds_websites:crud_cdswebsites'): _('PhD activities'),
                   reverse('crud_cds_websites:crud_cds_website_edit', kwargs={'code': code}): cds_website.nome_corso_it,
                   '#': _('Cds website ex-student data')
                   }

    return render(request,
                  'phd_main_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': teacher_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'phd': phd,
                   'url': reverse('ricerca:teacherslist')})
