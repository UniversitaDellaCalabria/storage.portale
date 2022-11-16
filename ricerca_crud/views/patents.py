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
from . .forms import *
from .. utils import log_action


logger = logging.getLogger(__name__)


@login_required
@can_manage_patents
def patents(request, my_offices=None, patent=None, inventors=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Patents')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:patents')}
    return render(request, 'patents/patents.html', context)


@login_required
@can_manage_patents
def patent_new(request, my_offices=None, patent=None, inventors=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   '#': _('New')}
    form = BrevettoDatiBaseForm()
    inventor_form = BrevettoInventoriForm()

    # already choosen before form fails
    inventor = None
    if request.POST.get('choosen_person', ''):
        inventor = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = BrevettoDatiBaseForm(data=request.POST, files=request.FILES)
        inventor_form = BrevettoInventoriForm(data=request.POST)

        if form.is_valid() and inventor_form.is_valid():
            inventor_code = decrypt(
                inventor_form.cleaned_data['choosen_person'])
            inventor = get_object_or_404(Personale, matricola=inventor_code)

            # check if user can manage teacher structure
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                        office__name=OFFICE_PATENTS,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True,
                                                                                        office__organizational_structure__unique_code=inventor.cd_uo_aff_org_id)
                if not structure_afforg:
                    raise Exception(
                        _("Add inventor belonging to your structure"))

            patent = BrevettoDatiBase.objects.create(
                id_univoco=form.cleaned_data['id_univoco'],
                titolo=form.cleaned_data['titolo'],
                url_immagine=form.cleaned_data['url_immagine'],
                breve_descrizione=form.cleaned_data['breve_descrizione'],
                id_area_tecnologica=form.cleaned_data['id_area_tecnologica'],
                url_knowledge_share=form.cleaned_data['url_knowledge_share'],
                applicazioni=form.cleaned_data['applicazioni'],
                vantaggi=form.cleaned_data['vantaggi'],
                trl_aggiornato=form.cleaned_data['trl_aggiornato'],
                proprieta=form.cleaned_data['proprieta'],
                id_status_legale=form.cleaned_data['id_status_legale'],
                data_priorita=form.cleaned_data['data_priorita'],
                territorio=form.cleaned_data['territorio'],
                id_diritto_commerciale=form.cleaned_data['id_diritto_commerciale'],
                id_disponibilita=form.cleaned_data['id_disponibilita'],
                area_ks=form.cleaned_data['area_ks'],
                nome_file_logo=form.cleaned_data['nome_file_logo'],
            )

            if inventor:
                BrevettoInventori.objects.create(id_brevetto=patent,
                                                 cognomenome_origine=f'{inventor.cognome} {inventor.nome}',
                                                 matricola_inventore=inventor)
            else:
                BrevettoInventori.objects.create(id_brevetto=patent,
                                                 cognomenome_origine=form.cleaned_data['cognomenome_origine'])
                inventor = BrevettoInventori.objects.values(
                    'cognomenome_origine')

            log_action(user=request.user,
                       obj=patent,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent created successfully"))
            return redirect("ricerca_crud:crud_patents")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in inventor_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{inventor_form.fields[k].label}</b>: {v}")
    return render(request,
                  'patents/patent_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{inventor.cognome} {inventor.nome}' if inventor else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'inventor_form': inventor_form})


@login_required
@can_manage_patents
def patent(request, code, my_offices=None, patent=None, inventors=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   '#': patent.titolo}
    form = BrevettoDatiBaseForm(instance=patent)

    if request.POST:
        form = BrevettoDatiBaseForm(
            instance=patent, data=request.POST, files=request.FILES)

        if form.is_valid():
            patent.user_mod = request.user
            patent.titolo = form.cleaned_data['titolo']
            patent.id_univoco = form.cleaned_data['id_univoco']
            patent.url_immagine = form.cleaned_data['url_immagine']
            patent.breve_descrizione = form.cleaned_data['breve_descrizione']
            patent.id_area_tecnologica = form.cleaned_data['id_area_tecnologica']
            patent.url_knowledge_share = form.cleaned_data['url_knowledge_share']
            patent.applicazioni = form.cleaned_data['applicazioni']
            patent.vantaggi = form.cleaned_data['vantaggi']
            patent.trl_aggiornato = form.cleaned_data['trl_aggiornato']
            patent.proprieta = form.cleaned_data['proprieta']
            patent.id_status_legale = form.cleaned_data['id_status_legale']
            patent.data_priorita = form.cleaned_data['data_priorita']
            patent.territorio = form.cleaned_data['territorio']
            patent.id_diritto_commerciale = form.cleaned_data['id_diritto_commerciale']
            patent.id_disponibilita = form.cleaned_data['id_disponibilita']
            patent.area_ks = form.cleaned_data['area_ks']
            patent.nome_file_logo = form.cleaned_data['nome_file_logo'] if form.cleaned_data.get(
                'nome_file_logo') else None
            patent.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent edited successfully"))

            return redirect('ricerca_crud:crud_patent_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(patent).pk,
                                   object_id=patent.pk)
    return render(request,
                  'patents/patent.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'patent': patent,
                   'inventors': inventors})


@login_required
@can_manage_patents
def patent_inventor_data(request, code, inventor_id, patent=None, inventors=None, my_offices=None):

    inventor_data = get_object_or_404(BrevettoInventori,
                                      pk=inventor_id, id_brevetto=code)

    form = BrevettoInventoriForm(instance=inventor_data)

    if request.POST:
        form = BrevettoInventoriForm(instance=inventor_data,
                                     data=request.POST)
        if form.is_valid():
            inventor_data.user_mod = request.user
            inventor_data.cognomenome_origine = form.cleaned_data['cognomenome_origine']
            inventor_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor data edited successfully"))

            return redirect('ricerca_crud:crud_project_inventor_data',
                            code=code,
                            inventor_id=inventor_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   reverse('ricerca_crud:crud_patent_inventor_data_edit', kwargs={'code': code, 'inventor_id': inventor_id}): _('Patent inventor data')
                   }

    return render(request,
                  'patents/patent_inventor_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_data': inventor_data})


@login_required
@can_manage_patents
def patent_inventor_data_edit(request, code, inventor_id, inventors=None,
                              my_offices=None, patent=None):

    inventor_patent = get_object_or_404(BrevettoInventori,
                                        pk=inventor_id, id_brevetto=code)

    inventor = inventor_patent.matricola_inventore
    inventor_data = ()

    if inventor:
        inventor_data = (encrypt(inventor.matricola),
                         f'{inventor.cognome} {inventor.nome}')
        form = BrevettoInventoriWithoutFieldsForm(
            initial={'choosen_person': inventor_data[0]})
    else:
        form = BrevettoInventoriWithoutFieldsForm()

    if request.POST:
        form = BrevettoInventoriWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            inventor_code = decrypt(form.cleaned_data['choosen_person'])
            new_inventor = get_object_or_404(
                Personale, matricola=inventor_code)
            inventor_patent.matricola_inventore = new_inventor
            inventor_patent.cognomenome_origine = f'{new_inventor.cognome} {new_inventor.nome}'
            inventor_patent.save()

            if inventor and inventor == new_inventor:
                log_msg = f'{_("Changed inventor")} {inventor.__str__()}'
            elif inventor and inventor != new_inventor:
                log_msg = f'{inventor} {_("substituted with")} {new_inventor.__str__()}'
            else:
                log_msg = f'{_("Changed inventor")} {new_inventor.__str__()}'

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor edited successfully"))
            return redirect('ricerca_crud:crud_patent_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   '#': _('Inventor')}
    return render(request,
                  'patents/patent_inventor_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_id': inventor_id,
                   'choosen_person': inventor_data[1] if inventor_data else None,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_new(request, code, my_offices=None, patent=None, inventors=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_patents'): _('Patents'),
                   reverse('ricerca_crud:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   '#': _('New inventor')}
    form = BrevettoInventoriForm()
    if request.POST:
        form = BrevettoInventoriForm(data=request.POST)
        if form.is_valid():

            b = BrevettoInventori.objects.create(
                id_brevetto=patent,
                cognomenome_origine=form.cleaned_data['cognomenome_origine']
            )
            inventor_code = decrypt(form.cleaned_data['choosen_person'])
            if inventor_code:
                inventor = get_object_or_404(
                    Personale, matricola=inventor_code)
                b.matricola_inventore = inventor
                b.cognomenome_origine = f'{inventor.cognome} {inventor.nome}'
                b.save()

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=f'{_("Added inventor")} {b.__str__()}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor added successfully"))
            return redirect('ricerca_crud:crud_patent_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    return render(request,
                  'patents/patent_inventor_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_delete(request, code, inventor_id,
                           my_offices=None, patent=None, inventors=None):
    inventor_patent = get_object_or_404(BrevettoInventori,
                                        pk=inventor_id, id_brevetto=code)

    if BrevettoInventori.objects.filter(id_brevetto=code).count() == 1:
        raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=patent,
               flag=CHANGE,
               msg=f'{_("Deleted inventor")} {inventor_patent.cognomenome_origine}')

    inventor_patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Inventor removed successfully"))
    return redirect('ricerca_crud:crud_patent_edit', code=code)


@login_required
@can_manage_patents
def patent_delete(request, code, my_offices=None, patent=None, inventors=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))
    logo = patent.nome_file_logo.path

    patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Patent removed successfully"))
    try:
        os.remove(logo)
    except Exception:  # pragma: no cover
        logger.warning(f'File {logo} not found')

    return redirect('ricerca_crud:crud_patents')
