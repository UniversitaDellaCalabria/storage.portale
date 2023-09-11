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
@can_manage_laboratories
def laboratories(request, laboratory=None):
    """
    lista dei laboratori
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Laboratories')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:laboratorieslist')}
    return render(request, 'laboratories.html', context)


@login_required
@can_manage_laboratories
def laboratory(request, code, laboratory=None):
    """
    dettaglio laboratorio
    """
    form = LaboratorioDatiBaseForm(instance=laboratory)


    referent_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)

    scientific_director_data = get_object_or_404(LaboratorioDatiBase,
                                      pk=code)

    # departments = SpinoffStartupDipartimento.objects.filter(
    #     id_spinoff_startup_dati_base=company)

    if request.POST:
        form = LaboratorioDatiBaseForm(instance=laboratory,
                                          data=request.POST,
                                          files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            laboratory.user_mod = request.user
            laboratory.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)

                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(laboratory).pk,
                                   object_id=laboratory.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratory'),
                   '#': laboratory.nome_laboratorio}

    return render(request,
                  'laboratory.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'laboratory': laboratory,
                   'referent_data': referent_data,
                   'scientific_director_data': scientific_director_data,
                   })


@login_required
@can_manage_laboratories
def laboratory_new(request, laboratory=None):
    """
    aggiungi nuovo laboratorio
    """

    #new
    form = LaboratorioDatiBaseForm()

    referent_internal_form = LaboratorioDatiBaseUnicalReferentChoosenPersonForm(required=True)
    referent_external_form = LaboratorioDatiBaseReferentForm()

    scientific_director_internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(required=True)
    scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    referent = None
    scientific_director = None


    if request.POST.get('choosen_unical_referent', ''):
        referent = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_unical_referent'])))

    if request.POST.get('choosen_scientific_director', ''):
        scientific_director = get_object_or_404(Personale,
                                    matricola=(decrypt(request.POST['choosen_scientific_director'])))

    # if request.POST:
    #     form = LaboratorioDatiBaseForm(
    #         data=request.POST, files=request.FILES)
    #     # department_form = SpinoffStartupDipartimentoForm(data=request.POST)
    #     #
    #     referent_form = ChoosenPersonForm(data=request.POST, required=True)
    #     if 'choosen_scientific_director' in request.POST:
    #         scientific_director_form = internal_form
    #     else:
    #         form = external_form
    #     scientific_director_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(data=request.POST, required=True)
    #     scientific_director_external_form = LaboratorioDatiBaseScientificDirectorForm()

    #     if form.is_valid() and referent_form.is_valid() and scientific_director_form.is_valid():
    #         laboratory = form.save(commit=False)
    #         #referente compilazione
    #         laboratory.referente_compilazione = f'{referent.cognome} {referent.nome}'
    #         laboratory.matricola_referente_compilazione = referent
    #         #responsabile scientifico
    #         laboratory.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
    #         laboratory.matricola_responsabile_scientifico = scientific_director           
    #         laboratory.save()

    #         # se viene scelto un dipartimento
    #         # questo viene associato all'impresa
    #         # if department:
    #         #     SpinoffStartupDipartimento.objects.create(id_spinoff_startup_dati_base=company,
    #         #                                               nome_origine_dipartimento=f'{department.dip_des_it}',
    #         #                                               id_didattica_dipartimento=department)

    #         log_action(user=request.user,
    #                    obj=laboratory,
    #                    flag=ADDITION,
    #                    msg=[{'added': {}}])

    #         messages.add_message(request,
    #                              messages.SUCCESS,
    #                              _("Laboratory created successfully"))
    #         return redirect("crud_laboratories:crud_laboratories")
    #     else:  # pragma: no cover
    #         for k, v in form.errors.items():
    #             messages.add_message(request, messages.ERROR,
    #                                  f"<b>{form.fields[k].label}</b>: {v}")
    #         # for k, v in department_form.errors.items():
    #         #     messages.add_message(request, messages.ERROR,
    #         #                          f"<b>{department_form.fields[k].label}</b>: {v}")
    #         for k, v in referent_form.errors.items():
    #             messages.add_message(request, messages.ERROR,
    #                                  f"<b>{referent_form.fields[k].label}</b>: {v}")
    #         for k, v in scientific_director_form.errors.items():
    #             messages.add_message(request, messages.ERROR,
    #                                  f"<b>{scientific_director_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   '#': _('New')}
    return render(request,
                  'laboratory_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'url': reverse('ricerca:teacherslist'),
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'form': form,
                   'unical_referent_lable' : 'choosen_unical_referent',
                   'scientific_director_lable' : 'choosen_scientific_director',
                   'choosen_unical_referent': f'{referent.cognome} {referent.nome}' if referent else '',
                   'choosen_scientific_director' : f'{scientific_director.cognome} {scientific_director.nome}' if scientific_director else '',
                   'referent_internal_form': referent_internal_form,
                   'referent_external_form': referent_external_form,
                   'scientific_director_internal_form': scientific_director_internal_form,
                   'scientific_director_external_form': scientific_director_external_form
                  })


@login_required
@can_manage_laboratories
def laboratory_unical_referent_edit(request, code, data_id, laboratory=None):
    """
    dettaglio referente Unical del laboratorio
    """
    laboratory_referent = get_object_or_404(LaboratorioDatiBase.objects.select_related('matricola_referente_compilazione'),
                                         pk=data_id)
    old_label = laboratory_referent.referente_compilazione
    referent = laboratory_referent.matricola_referente_compilazione
    initial = {}
    referent_data = ''
    if referent:
        referent_data = f'{referent.cognome} {referent.nome}'
        initial = {'choosen_person': encrypt(referent.matricola)}

    external_form = LaboratorioDatiBaseReferentForm(
        instance=laboratory_referent)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:

        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseReferentForm(instance=laboratory_referent,
                                                            data=request.POST)

        if 'choosen_person' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                referent_code = decrypt(form.cleaned_data['choosen_person'])
                referent = get_object_or_404(
                    Personale, matricola=referent_code)
                laboratory_referent.matricola_referente_compilazione = referent
                laboratory_referent.referente_compilazione = f'{referent.cognome} {referent.nome}'
                laboratory_referent.email_compilazione = referent.email
            else:
                laboratory_referent.matricola_referente_compilazione = None
                laboratory_referent.referente_compilazione = form.cleaned_data['referente_compilazione']
                laboratory_referent.email_compilazione = form.cleaned_data['email_compilazione']


            laboratory_referent.save()

            if old_label != laboratory_referent.referente_compilazione:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito referente {old_label} con {laboratory_referent.referente_compilazione}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory referent edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_unical_referent_edit', kwargs={'code': code, 'data_id': data_id}): _('Unical Referent')
                   }

    return render(request,
                  'laboratory_unical_referent.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_person': referent_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'url': reverse('ricerca:teacherslist')})

@login_required
@can_manage_laboratories
def laboratory_unical_department_data_edit(request, code, department_id,
                                        laboratory=None):
    """
    modifica dipartimento
    """
    department_laboratory = get_object_or_404(LaboratorioDatiBase.objects.select_related('id_didattica_dipartimento'),
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


# @login_required
# @can_manage_companies
# def company_unical_department_data_delete(request, code, department_id,
#                                           company=None):
#     """
#     elimina dipartimento
#     """
#     department_company = get_object_or_404(SpinoffStartupDipartimento.objects.select_related('id_didattica_dipartimento'),
#                                            id_spinoff_startup_dati_base=company,
#                                            pk=department_id)
#
#     # if SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base=company).count() == 1:
#     # raise Exception(_("Permission denied. Only one department remains"))
#
#     log_action(user=request.user,
#                obj=company,
#                flag=CHANGE,
#                msg=f'Rimosso dipartimento {department_company.id_didattica_dipartimento}')
#
#     department_company.delete()
#     messages.add_message(request,
#                          messages.SUCCESS,
#                          _("Department removed successfully"))
#     return redirect('crud_companies:crud_company_edit', code=code)
#
#
@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_companies
def laboratory_delete(request, code, laboratory=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    laboratory = get_object_or_404(LaboratorioDatiBase, pk=code)
    laboratory.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Laboratory removed successfully"))

    return redirect('crud_laboratories:crud_laboratories')




@login_required
@can_manage_laboratories
def laboratory_scientific_director_edit(request, code, data_id, laboratory=None):
    """
    dettaglio responsabile scientifico del laboratorio
    """
    laboratory_scientific_director = get_object_or_404(LaboratorioDatiBase.objects.select_related('matricola_responsabile_scientifico'),
                                         pk=data_id)
    old_label = laboratory_scientific_director.responsabile_scientifico
    scientific_director = laboratory_scientific_director.matricola_responsabile_scientifico
    initial = {}
    scientific_director_data = ''
    if scientific_director:
        scientific_director_data = f'{scientific_director.cognome} {scientific_director.nome}'
        initial = {'choosen_scientific_director': encrypt(scientific_director.matricola)}

    external_form = LaboratorioDatiBaseScientificDirectorForm(
        instance=laboratory_scientific_director)
    internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(initial=initial, required=True)

    if request.POST:

        internal_form = LaboratorioDatiBaseScientificDirectorChoosenPersonForm(data=request.POST, required=True)
        external_form = LaboratorioDatiBaseScientificDirectorForm(instance=laboratory_scientific_director,
                                                            data=request.POST)

        if 'choosen_scientific_director' in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get('choosen_scientific_director'):
                scientific_director_code = decrypt(form.cleaned_data['choosen_scientific_director'])
                scientific_director = get_object_or_404(
                    Personale, matricola=scientific_director_code)
                laboratory_scientific_director.matricola_responsabile_scientifico = scientific_director
                laboratory_scientific_director.responsabile_scientifico = f'{scientific_director.cognome} {scientific_director.nome}'
            else:
                laboratory_scientific_director.matricola_responsabile_scientifico = None
                laboratory_scientific_director.responsabile_scientifico = form.cleaned_data['responsabile_scientifico']

            laboratory_scientific_director.save()

            if old_label != laboratory_scientific_director.responsabile_scientifico:
                log_action(user=request.user,
                           obj=laboratory,
                           flag=CHANGE,
                           msg=f'Sostituito responsabile scientifico {old_label} con {laboratory_scientific_director.responsabile_scientifico}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Laboratory scientific director edited successfully"))

            return redirect('crud_laboratories:crud_laboratory_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_laboratories:crud_laboratories'): _('Laboratories'),
                   reverse('crud_laboratories:crud_laboratory_edit', kwargs={'code': code}): laboratory.nome_laboratorio,
                   reverse('crud_laboratories:crud_laboratory_scientific_director_edit', kwargs={'code': code, 'data_id': data_id}): _('Scientific Director')
                   }

    return render(request,
                  'laboratory_scientific_director.html',
                  {'breadcrumbs': breadcrumbs,
                   'laboratory': laboratory,
                   'choosen_scientific_director': scientific_director_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'url': reverse('ricerca:teacherslist')})