import logging
import os

from .. utils.utils import log_action

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. utils.forms import ChoosenPersonForm

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_companies
def companies(request, company=None):
    """
    lista delle imprese
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Companies')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:companies')}
    return render(request, 'companies.html', context)


@login_required
@can_manage_companies
def company(request, code, company=None):
    """
    dettaglio impresa
    """
    form = SpinoffStartupDatiBaseForm(instance=company)

    referent_data = get_object_or_404(SpinoffStartupDatiBase,
                                      pk=code)
    departments = SpinoffStartupDipartimento.objects.filter(
        id_spinoff_startup_dati_base=company)

    if request.POST:
        form = SpinoffStartupDatiBaseForm(instance=company,
                                          data=request.POST,
                                          files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            company.user_mod = request.user
            company.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            if changed_field_labels:
                log_action(user=request.user,
                           obj=company,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company edited successfully"))

            return redirect('crud_companies:crud_company_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(company).pk,
                                   object_id=company.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_companies:crud_companies'): _('Companies'),
                   '#': company.nome_azienda}

    return render(request,
                  'company.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'company': company,
                   'departments': departments,
                   'referent_data': referent_data})


@login_required
@can_manage_companies
def company_new(request, company=None):
    """
    aggiungi nuova impresa
    """
    # due form, uno per i dati del brevetto
    # e uno per l'inventore iniziale
    form = SpinoffStartupDatiBaseForm()
    department_form = SpinoffStartupDipartimentoForm()
    referent_form = ChoosenPersonForm(required=True)

    # se la validazione dovesse fallire ritroveremmo
    # comunque l'inventore scelto senza doverlo cercare
    # nuovamente dall'elenco

    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                       dip_id=request.POST['choosen_department'])

    referent = None
    if request.POST.get('choosen_person', ''):
        referent = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = SpinoffStartupDatiBaseForm(
            data=request.POST, files=request.FILES)
        department_form = SpinoffStartupDipartimentoForm(data=request.POST)

        referent_form = ChoosenPersonForm(data=request.POST, required=True)

        if form.is_valid() and department_form.is_valid() and referent_form.is_valid():
            company = form.save(commit=False)

            company.referente_unical = f'{referent.cognome} {referent.nome}'
            company.matricola_referente_unical = referent
            company.save()

            # se viene scelto un dipartimento
            # questo viene associato all'impresa
            if department:
                SpinoffStartupDipartimento.objects.create(id_spinoff_startup_dati_base=company,
                                                          nome_origine_dipartimento=f'{department.dip_des_it}',
                                                          id_didattica_dipartimento=department)

            log_action(user=request.user,
                       obj=company,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company created successfully"))
            return redirect("crud_companies:crud_companies")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")
            for k, v in referent_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{referent_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_companies:crud_companies'): _('Companies'),
                   '#': _('New')}
    return render(request,
                  'company_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_department': f'{department.dip_des_it}' if department else '',
                   'choosen_person': f'{referent.cognome} {referent.nome}' if referent else '',
                   'form': form,
                   'departments_api': reverse('ricerca:departmentslist'),
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'department_form': department_form,
                   'referent_form': referent_form,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_companies
def company_unical_referent_edit(request, code, data_id, company=None):
    """
    dettaglio referente Unical dell'impresa
    """
    company_referent = get_object_or_404(SpinoffStartupDatiBase.objects.select_related('matricola_referente_unical'),
                                         pk=data_id)
    old_label = company_referent.referente_unical
    referent = company_referent.matricola_referente_unical
    initial = {}
    referent_data = ''
    if referent:
        referent_data = f'{referent.cognome} {referent.nome}'
        initial = {'choosen_person': encrypt(referent.matricola)}

    form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST, required=True)

        if form.is_valid():
            referent_code = decrypt(form.cleaned_data['choosen_person'])
            referent = get_object_or_404(
                Personale, matricola=referent_code)
            company_referent.matricola_referente_unical = referent
            company_referent.referente_unical = f'{referent.cognome} {referent.nome}'
            company_referent.save()

            if old_label != company_referent.referente_unical:
                log_action(user=request.user,
                           obj=company,
                           flag=CHANGE,
                           msg=f'Sostituito referente {old_label} con {company_referent.referente_unical}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company referent edited successfully"))

            return redirect('crud_companies:crud_company_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_companies:crud_companies'): _('Companies'),
                   reverse('crud_companies:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   reverse('crud_companies:crud_company_unical_referent_edit', kwargs={'code': code, 'data_id': data_id}): _('Unical Referent')
                   }

    return render(request,
                  'company_unical_referent.html',
                  {'breadcrumbs': breadcrumbs,
                   'company': company,
                   'choosen_person': referent_data,
                   'form': form,
                   'url': reverse('ricerca:teacherslist')})


# @login_required
# @can_manage_companies
# def company_unical_referent_data_delete(request, code, data_id=None,
    # company=None):
    # """
    # elimina referente unical
    # """
    # company = get_object_or_404(SpinoffStartupDatiBase,
    # pk=code)

    # company.matricola_referente_unical = None
    # company.save()

    # log_action(user=request.user,
    # obj=company,
    # flag=CHANGE,
    # msg=f'{_("Deleted unical referent")}')

    # messages.add_message(request,
    # messages.SUCCESS,
    # _("Unical referent removed successfully"))
    # return redirect('crud_companies:crud_company_unical_referent_edit',
    # code=code,
    # data_id=data_id)


@login_required
@can_manage_companies
def company_unical_department_data_new(request, code,
                                       company=None):
    """
    nuovo dipartimento per l'impresa
    """
    form = SpinoffStartupDipartimentoForm()
    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():
            department_code = form.cleaned_data['choosen_department']
            department = get_object_or_404(DidatticaDipartimento,
                                           dip_id=department_code)
            SpinoffStartupDipartimento.objects.create(
                id_spinoff_startup_dati_base=company,
                id_didattica_dipartimento=department,
                nome_origine_dipartimento=department.dip_des_it)

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo dipartimento {department.dip_des_it}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department added successfully"))
            return redirect('crud_companies:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_companies:crud_companies'): _('Companies'),
                   reverse('crud_companies:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': _('New department')}

    return render(request,
                  'company_department.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'url': reverse('ricerca:departmentslist')})


@login_required
@can_manage_companies
def company_unical_department_data_edit(request, code, department_id,
                                        company=None):
    """
    modifica dipartimento
    """
    department_company = get_object_or_404(SpinoffStartupDipartimento.objects.select_related('id_didattica_dipartimento'),
                                           pk=department_id,
                                           id_spinoff_startup_dati_base=company)
    department = department_company.id_didattica_dipartimento
    old_label = department.dip_des_it
    department_data = ''
    initial = {}
    if department:
        department_data = department.dip_des_it
        initial = {'choosen_department': department.dip_id}

    form = SpinoffStartupDipartimentoForm(initial=initial)

    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():

            department_code = form.cleaned_data['choosen_department']
            new_department = get_object_or_404(DidatticaDipartimento,
                                               dip_id=department_code)
            department_company.user_mod = request.user
            department_company.id_didattica_dipartimento = new_department
            department_company.nome_origine_dipartimento = f'{new_department.dip_des_it}'
            department_company.save()

            if old_label != new_department:
                log_action(user=request.user,
                           obj=company,
                           flag=CHANGE,
                           msg=f'Sostituito dipartimento {old_label} con {new_department}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department edited successfully"))
            return redirect('crud_companies:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_companies:crud_companies'): _('Companies'),
                   reverse('crud_companies:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': f'{department.dip_des_it}'}

    return render(request,
                  'company_department.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'department_id': department_id,
                   'choosen_department': department_data,
                   'url': reverse('ricerca:departmentslist')})


@login_required
@can_manage_companies
def company_unical_department_data_delete(request, code, department_id,
                                          company=None):
    """
    elimina dipartimento
    """
    department_company = get_object_or_404(SpinoffStartupDipartimento.objects.select_related('id_didattica_dipartimento'),
                                           id_spinoff_startup_dati_base=company,
                                           pk=department_id)

    # if SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base=company).count() == 1:
    # raise Exception(_("Permission denied. Only one department remains"))

    log_action(user=request.user,
               obj=company,
               flag=CHANGE,
               msg=f'Rimosso dipartimento {department_company.id_didattica_dipartimento}')

    department_company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Department removed successfully"))
    return redirect('crud_companies:crud_company_edit', code=code)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_companies
def company_delete(request, code, company=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    company = get_object_or_404(SpinoffStartupDatiBase, pk=code)
    logo = company.nome_file_logo

    if logo and logo.path:
        try:
            os.remove(logo.path)
        except:  # pragma: no cover
            logger.warning(f'File {logo.path} not found')

    company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Company removed successfully"))

    return redirect('crud_companies:crud_companies')
