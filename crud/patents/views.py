import logging
import os

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
from .. utils.utils import custom_message, log_action

from . decorators import *
from . forms import *


logger = logging.getLogger(__name__)


@login_required
@can_manage_patents
def patents(request, patent=None):
    """
    lista dei brevetti
    """
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Patents')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:patents')}
    return render(request, 'patents.html', context)


@login_required
@can_manage_patents
def patent_new(request, patent=None):
    """
    nuovo brevetto
    """
    form = BrevettoDatiBaseForm()

    if request.POST:
        form = BrevettoDatiBaseForm(data=request.POST,
                                    files=request.FILES)

        if form.is_valid():

            patent = form.save()
            log_action(user=request.user,
                       obj=patent,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent created successfully"))
            return redirect("crud_patents:crud_patents")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   '#': _('New')}

    return render(request,
                  'patent_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form})


@login_required
@can_manage_patents
def patent(request, code, patent=None):
    """
    modifica brevetto
    """
    form = BrevettoDatiBaseForm(instance=patent)
    inventors = BrevettoInventori.objects.filter(id_brevetto=patent)

    if request.POST:
        form = BrevettoDatiBaseForm(instance=patent,
                                    data=request.POST,
                                    files=request.FILES)

        if form.is_valid():
            form.save(commit=False)
            patent.user_mod = request.user
            patent.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            if changed_field_labels:
                log_action(user=request.user,
                           obj=patent,
                           flag=CHANGE,
                           msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent edited successfully"))

            return redirect('crud_patents:crud_patent_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(patent).pk,
                                   object_id=patent.pk)

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   '#': patent.titolo}

    return render(request,
                  'patent.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'patent': patent,
                   'inventors': inventors})


@login_required
@can_manage_patents
def patent_inventor_new(request, code, patent=None):
    """
    nuovo inventore
    """
    external_form = BrevettoInventoriForm()
    internal_form = ChoosenPersonForm(required=True)
    if request.POST:
        if 'choosen_person' in request.POST:
            form = ChoosenPersonForm(data=request.POST, required=True)
        else:
            form = BrevettoInventoriForm(data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                inventor_code = decrypt(form.cleaned_data['choosen_person'])
                inventor = get_object_or_404(
                    Personale, matricola=inventor_code)
                cognomenome_origine = f'{inventor.cognome} {inventor.nome}'
            else:
                inventor = None
                cognomenome_origine = form.cleaned_data['cognomenome_origine']

            b = BrevettoInventori.objects.create(
                id_brevetto=patent,
                matricola_inventore=inventor,
                cognomenome_origine=cognomenome_origine
            )

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=f'Aggiunto nuovo inventore {b}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor added successfully"))
            return redirect('crud_patents:crud_patent_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   reverse('crud_patents:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   '#': _('New inventor')}

    return render(request,
                  'patent_inventor.html',
                  {'breadcrumbs': breadcrumbs,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'patent': patent,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_edit(request, code, inventor_id, patent=None):
    """
    dettaglio dati inventore
    """
    patent_inventor = get_object_or_404(BrevettoInventori.objects.select_related('matricola_inventore'),
                                        pk=inventor_id,
                                        id_brevetto=code)
    old_label = patent_inventor.cognomenome_origine
    inventor = patent_inventor.matricola_inventore
    initial = {}
    inventor_data = ''
    if inventor:
        inventor_data = f'{inventor.cognome} {inventor.nome}'
        initial = {'choosen_person': encrypt(inventor.matricola)}

    external_form = BrevettoInventoriForm(instance=patent_inventor)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        if 'choosen_person' in request.POST:
            form = ChoosenPersonForm(data=request.POST, required=True)
        else:
            form = BrevettoInventoriForm(instance=patent_inventor,
                                         data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get('choosen_person'):
                inventor_code = decrypt(form.cleaned_data['choosen_person'])
                inventor = get_object_or_404(
                    Personale, matricola=inventor_code)
                patent_inventor.matricola_inventore = inventor
                patent_inventor.cognomenome_origine = f'{inventor.cognome} {inventor.nome}'
            else:
                patent_inventor.matricola_inventore = None
                patent_inventor.cognomenome_origine = form.cleaned_data['cognomenome_origine']

            patent_inventor.save()

            if old_label != patent_inventor.cognomenome_origine:
                log_action(user=request.user,
                           obj=patent,
                           flag=CHANGE,
                           msg=f'Sostituito inventore {old_label} con {patent_inventor}')

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Patent inventor edited successfully"))

            return redirect('crud_patents:crud_patent_edit', code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   reverse('crud_patents:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   reverse('crud_patents:crud_patent_inventor_edit', kwargs={'code': code, 'inventor_id': inventor_id}): _('Patent inventor data')
                   }

    return render(request,
                  'patent_inventor.html',
                  {'breadcrumbs': breadcrumbs,
                   'patent': patent,
                   'choosen_person': inventor_data,
                   'external_form': external_form,
                   'internal_form': internal_form,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_delete(request, code, inventor_id, patent=None):
    """
    elimina inventore
    """
    inventor = get_object_or_404(BrevettoInventori,
                                 pk=inventor_id,
                                 id_brevetto=code)

    # if BrevettoInventori.objects.filter(id_brevetto=code).count() == 1:
    # return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=patent,
               flag=CHANGE,
               msg=f'Rimosso inventore {inventor}')

    inventor.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Inventor removed successfully"))
    return redirect('crud_patents:crud_patent_edit', code=code)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_patents
def patent_delete(request, code, patent=None):
    """
    rimuovi brevetto
    """
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    #     raise Exception(_('Permission denied'))

    patent = get_object_or_404(BrevettoDatiBase, pk=code)
    logo = patent.nome_file_logo.path

    if logo:
        try:
            os.remove(logo)
        except:  # pragma: no cover
            logger.warning(f'File {logo} not found')

    patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Patent removed successfully"))

    return redirect('crud_patents:crud_patents')
