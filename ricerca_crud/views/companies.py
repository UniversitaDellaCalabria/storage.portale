import logging
import os

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt

from .. decorators import *
from .. forms import *
from .. utils import log_action


logger = logging.getLogger(__name__)


@login_required
@can_manage_companies
def companies(request, my_offices=None, company=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Companies')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:companies')}
    return render(request, 'companies/companies.html', context)


@login_required
@can_manage_companies
def company_new(request, my_offices=None, company=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   '#': _('New')}
    form = SpinoffStartupDatiBaseForm()
    department_form = SpinoffStartupDipartimentoForm()

    # already choosen before form fails
    department = None
    if request.POST.get('choosen_department', ''):
        department = get_object_or_404(DidatticaDipartimento,
                                       dip_id=request.POST['choosen_department'])

    if request.POST:
        form = SpinoffStartupDatiBaseForm(
            data=request.POST, files=request.FILES)
        department_form = SpinoffStartupDipartimentoForm(data=request.POST)

        if form.is_valid() and department_form.is_valid():
            department_code = department_form.cleaned_data['choosen_department']
            department = get_object_or_404(
                DidatticaDipartimento, dip_id=department_code)

            company = SpinoffStartupDatiBase.objects.create(
                piva=form.cleaned_data['piva'],
                nome_azienda=form.cleaned_data['nome_azienda'],
                descrizione_ita=form.cleaned_data['descrizione_ita'],
                descrizione_eng=form.cleaned_data['descrizione_eng'],
                url_sito_web=form.cleaned_data['url_sito_web'],
                ceo=form.cleaned_data['ceo'],
                id_area_tecnologica=form.cleaned_data['id_area_tecnologica'],
                id_area_innovazione_s3_calabria=form.cleaned_data['id_area_innovazione_s3_calabria'],
                is_startup=form.cleaned_data['is_startup'],
                is_spinoff=form.cleaned_data['is_spinoff'],
                nome_file_logo=form.cleaned_data['nome_file_logo']
            )

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
            return redirect("ricerca_crud:crud_companies")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in department_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{department_form.fields[k].label}</b>: {v}")
    return render(request,
                  'companies/company_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_department': f'{department.dip_des_it}' if department else '',
                   'form': form,
                   'departments_api': reverse('ricerca:departmentslist'),
                   'department_form': department_form})


@login_required
@can_manage_companies
def company(request, code, my_offices=None, company=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   '#': company.nome_azienda}
    form = SpinoffStartupDatiBaseForm(instance=company)

    referent_data = get_object_or_404(SpinoffStartupDatiBase,
                                      pk=code)

    if request.POST:
        form = SpinoffStartupDatiBaseForm(instance=company,
                                          data=request.POST,
                                          files=request.FILES)

        if form.is_valid():
            company.user_mod = request.user
            company.piva = form.cleaned_data['piva']
            company.nome_azienda = form.cleaned_data['nome_azienda']
            company.nome_file_logo = form.cleaned_data['nome_file_logo'] if form.cleaned_data.get(
                'nome_file_logo') else None
            company.descrizione_ita = form.cleaned_data['descrizione_ita']
            company.descrizione_eng = form.cleaned_data['descrizione_eng']
            company.url_sito_web = form.cleaned_data['url_sito_web']
            company.ceo = form.cleaned_data['ceo']
            company.id_area_tecnologica = form.cleaned_data['id_area_tecnologica']
            company.id_area_innovazione_s3_calabria = form.cleaned_data[
                'id_area_innovazione_s3_calabria']
            company.is_startup = form.cleaned_data['is_startup']
            company.is_spinoff = form.cleaned_data['is_spinoff']
            company.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Company edited successfully"))

            return redirect('ricerca_crud:crud_company_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(company).pk,
                                   object_id=company.pk)
    return render(request,
                  'companies/company.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'company': company,
                   'referent_data': referent_data})


@login_required
@can_manage_companies
def company_unical_referent_data(request, code, data_id, company=None, my_offices=None):

    referent_data = get_object_or_404(SpinoffStartupDatiBase,
                                      pk=data_id)

    form = SpinoffStartupDatiBaseReferentForm(instance=referent_data)

    if request.POST:
        form = SpinoffStartupDatiBaseReferentForm(instance=referent_data,
                                                  data=request.POST)
        if form.is_valid():
            referent_data.user_mod = request.user
            referent_data.referente_unical = form.cleaned_data['referente_unical']
            referent_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Office data edited successfully"))

            return redirect('ricerca_crud:crud_company_unical_referent_data',
                            code=code,
                            data_id=data_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   reverse('ricerca_crud:crud_company_unical_referent_data', kwargs={'code': code, 'data_id': data_id}): _('Unical Referent data')
                   }

    return render(request,
                  'companies/company_unical_referent_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'referent_data': referent_data})


@login_required
@can_manage_companies
def company_unical_referent_data_edit(request, code, data_id,
                                      my_offices=None, company=None):
    unical_referent = get_object_or_404(SpinoffStartupDatiBase,
                                        pk=code)

    referent = unical_referent.matricola_referente_unical
    referent_data = ()

    if referent:
        referent_data = (encrypt(referent.matricola),
                         f'{referent.cognome} {referent.nome}')
        form = SpinoffStartupDatiBaseReferentWithoutIDForm(
            initial={'choosen_person': referent_data[0]})
    else:
        form = SpinoffStartupDatiBaseReferentWithoutIDForm()

    if request.POST:
        form = SpinoffStartupDatiBaseReferentWithoutIDForm(data=request.POST)
        if form.is_valid():
            referent_code = decrypt(form.cleaned_data['choosen_person'])
            new_referent = get_object_or_404(
                Personale, matricola=referent_code)
            unical_referent.matricola_referente_unical = new_referent
            unical_referent.save()

            if referent and referent == new_referent:
                log_msg = f'{_("Changed referent")} {referent.__str__()}'
            elif referent and referent != new_referent:
                log_msg = f'{referent} {_("substituted with")} {new_referent.__str__()}'
            else:
                log_msg = f'{_("Changed referent")} {new_referent.__str__()}'

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Unical referent edited successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': f'{company.referente_unical}'
                   }
    return render(request,
                  'companies/company_unical_referent_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'choosen_person': referent_data[1] if referent_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_companies
def company_unical_referent_data_delete(request, code, data_id=None,
                                        my_offices=None, company=None):
    company = get_object_or_404(SpinoffStartupDatiBase,
                                pk=code)

    company.matricola_referente_unical = None
    company.save()

    log_action(user=request.user,
               obj=company,
               flag=CHANGE,
               msg=f'{_("Deleted unical referent data")}')

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Unical referent data removed successfully"))
    return redirect('ricerca_crud:crud_company_edit',
                    code=code)


@login_required
@can_manage_companies
def company_unical_department_data_new(request, code,
                                       my_offices=None, company=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': _('New department')}
    form = SpinoffStartupDipartimentoForm()
    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():
            department_code = form.cleaned_data['choosen_department']
            department = get_object_or_404(
                DidatticaDipartimento, dip_id=department_code)
            SpinoffStartupDipartimento.objects.create(
                id_spinoff_startup_dati_base=company,
                id_didattica_dipartimento=department,
                nome_origine_dipartimento=department.dip_des_it)

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=f'{_("Added department")} {department.dip_des_it}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department added successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'companies/company_unical_department_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'url': reverse('ricerca:departmentslist')})


@login_required
@can_manage_companies
def company_unical_department_data_edit(request, code, department_id,
                                        my_offices=None, company=None):

    department_company = get_object_or_404(SpinoffStartupDipartimento,
                                           pk=department_id)

    department = department_company.id_didattica_dipartimento

    department_data = (department.dip_id, f'{department.dip_des_it}')
    form = SpinoffStartupDipartimentoForm(instance=department_company,
                                          initial={'choosen_department': department_data[0]})

    if request.POST:
        form = SpinoffStartupDipartimentoForm(data=request.POST)
        if form.is_valid():

            department_code = form.cleaned_data['choosen_department']
            new_department = get_object_or_404(
                DidatticaDipartimento, dip_id=department_code)
            department_company.user_mod = request.user
            department_company.id_didattica_dipartimento = new_department
            department_company.nome_origine_dipartimento = f'{new_department.dip_des_it}'
            department_company.save()

            log_msg = f'{_("Changed department")} {department.__str__()}' \
                      if department == new_department \
                      else f'{department} {_("substituted with")} {new_department.__str__()}'

            log_action(user=request.user,
                       obj=company,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Department edited successfully"))
            return redirect('ricerca_crud:crud_company_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_companies'): _('Companies'),
                   reverse('ricerca_crud:crud_company_edit', kwargs={'code': code}): company.nome_azienda,
                   '#': f'{department.dip_des_it}'}

    return render(request,
                  'companies/company_unical_department_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'company': company,
                   'department_id': department_id,
                   'choosen_department': department_data[1],
                   'url': reverse('ricerca:departmentslist')})


@login_required
@can_manage_companies
def company_unical_department_data_delete(request, code, department_id,
                                          my_offices=None, company=None):
    department_company = get_object_or_404(SpinoffStartupDipartimento,
                                           id_spinoff_startup_dati_base=company,
                                           pk=department_id)

    if SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base=company).count() == 1:
        raise Exception(_("Permission denied. Only one department remains"))

    log_action(user=request.user,
               obj=company,
               flag=CHANGE,
               msg=f'{_("Deleted department")} {department_company.id_didattica_dipartimento}')

    department_company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Department removed successfully"))
    return redirect('ricerca_crud:crud_company_edit', code=code)


@login_required
@can_manage_companies
def company_delete(request, code, my_offices=None, company=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))
    logo = company.nome_file_logo.path

    company.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Company removed successfully"))
    try:
        os.remove(logo)
    except Exception:  # pragma: no cover
        logger.warning(f'File {logo} not found')

    return redirect('ricerca_crud:crud_companies')
