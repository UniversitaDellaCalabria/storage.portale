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
def patents(request, my_offices=None, patent=None, inventors=None):
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
def patent_new(request, my_offices=None, patent=None, inventors=None):
    """
    nuovo brevetto
    """

    # due form, uno per i dati del brevetto
    # e uno per l'inventore iniziale
    form = BrevettoDatiBaseForm()
    inventor_form = BrevettoInventoriForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque l'inventore scelto senza doverlo cercare
    # nuovamente dall'elenco
    inventor = None
    if request.POST.get('choosen_person', ''):
        inventor = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))

    if request.POST:
        form = BrevettoDatiBaseForm(data=request.POST,
                                    files=request.FILES)
        inventor_form = BrevettoInventoriForm(data=request.POST)

        # entrambi i form devono essere validi
        if form.is_valid() and inventor_form.is_valid():

            patent = form.save()

            new_inventor = BrevettoInventori.objects.create(id_brevetto=patent,
                                                            cognomenome_origine=inventor_form.cleaned_data['cognomenome_origine'],
                                                            matricola_inventore=inventor)

            # se non viene inserita l'etichetta ma solo il link
            # questa viene generata automaticamente
            if inventor and not inventor_form.cleaned_data['cognomenome_origine']:
                new_inventor.cognomenome_origine=f'{inventor.nome} {inventor.cognome}'
                new_inventor.save()

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
            for k, v in inventor_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{inventor_form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   '#': _('New')}

    return render(request,
                  'patent_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{inventor.nome} {inventor.cognome}' if inventor else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'inventor_form': inventor_form})


@login_required
@can_manage_patents
def patent(request, code, my_offices=None, patent=None, inventors=None):
    """
    modifica brevetto
    """
    form = BrevettoDatiBaseForm(instance=patent)

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
def patent_inventor_data(request, code, inventor_id, patent=None,
                         inventors=None, my_offices=None):
    """
    dettaglio dati inventore
    """
    inventor_data = get_object_or_404(BrevettoInventori.objects.select_related('matricola_inventore'),
                                      pk=inventor_id,
                                      id_brevetto=code)

    form = BrevettoInventoriForm(instance=inventor_data)

    if request.POST:
        form = BrevettoInventoriForm(instance=inventor_data,
                                     data=request.POST)
        if form.is_valid():
            inventor_data.user_mod = request.user
            inventor_data.cognomenome_origine = form.cleaned_data['cognomenome_origine']

            if not form.cleaned_data['cognomenome_origine'] and inventor_data.matricola_inventore:
                inventor_data.cognomenome_origine = f'{inventor_data.matricola_inventore.nome} {inventor_data.matricola_inventore.cognome}'

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

            return redirect('crud_patents:crud_patent_inventor_data',
                            code=code,
                            inventor_id=inventor_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   reverse('crud_patents:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   reverse('crud_patents:crud_patent_inventor_data_edit', kwargs={'code': code, 'inventor_id': inventor_id}): _('Patent inventor data')
                   }

    return render(request,
                  'patent_inventor_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_data': inventor_data})


@login_required
@can_manage_patents
def patent_inventor_data_edit(request, code, inventor_id, inventors=None,
                              my_offices=None, patent=None):
    """
    modifica dati inventore
    """
    inventor_patent = get_object_or_404(BrevettoInventori.objects.select_related('matricola_inventore'),
                                        pk=inventor_id,
                                        id_brevetto=code)

    inventor = inventor_patent.matricola_inventore
    inventor_data = ''
    initial = {}
    if inventor:
        inventor_data = f'{inventor.nome} {inventor.cognome}'
        initial={'choosen_person':  encrypt(inventor.matricola)}

    form = ChoosenPersonForm(initial=initial)

    if request.POST:
        form = ChoosenPersonForm(data=request.POST)
        if form.is_valid():
            inventor_code = decrypt(form.cleaned_data['choosen_person'])
            new_inventor = get_object_or_404(Personale,
                                             matricola=inventor_code)
            inventor_patent.matricola_inventore = new_inventor
            if not inventor_patent.cognomenome_origine:
                inventor_patent.cognomenome_origine = f'{new_inventor.nome} {new_inventor.cognome}'
            inventor_patent.save()

            if inventor and inventor == new_inventor:
                log_msg = f'{_("Changed inventor")} {inventor}'
            elif inventor and inventor != new_inventor:
                log_msg = f'{inventor} {_("substituted with")} {new_inventor}'
            else:
                log_msg = f'{_("Changed inventor")} {new_inventor}'

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Inventor edited successfully"))
            return redirect('crud_patents:crud_patent_inventor_data',
                            code=code,
                            inventor_id=inventor_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_patents:crud_patents'): _('Patents'),
                   reverse('crud_patents:crud_patent_edit', kwargs={'code': code}): patent.titolo,
                   reverse('crud_patents:crud_patent_inventor_data', kwargs={'code': code,
                                                                             'inventor_id': inventor_id}): _('Patent inventor data'),
                   '#': _('Edit')}
    return render(request,
                  'patent_inventor_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'inventor_id': inventor_id,
                   'choosen_person': inventor_data,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_new(request, code, my_offices=None, patent=None, inventors=None):
    """
    nuovo inventore
    """
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
                inventor = get_object_or_404(Personale,
                                             matricola=inventor_code)
                b.matricola_inventore = inventor

                if not form.cleaned_data['cognomenome_origine']:
                    b.cognomenome_origine = f'{inventor.nome} {inventor.cognome}'
                b.save()

            log_action(user=request.user,
                       obj=patent,
                       flag=CHANGE,
                       msg=f'{_("Added inventor")} {b}')

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
                  'patent_inventor_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'patent': patent,
                   'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_patents
def patent_inventor_delete(request, code, inventor_id,
                           my_offices=None, patent=None, inventors=None):
    """
    elimina inventore
    """
    inventor_patent = get_object_or_404(BrevettoInventori,
                                        pk=inventor_id,
                                        id_brevetto=code)

    if BrevettoInventori.objects.filter(id_brevetto=code).count() == 1:
        return custom_message(request, _("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=patent,
               flag=CHANGE,
               msg=f'{_("Deleted inventor")} {inventor_patent.cognomenome_origine}')

    inventor_patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Inventor removed successfully"))
    return redirect('crud_patents:crud_patent_edit', code=code)


@login_required
@can_manage_patents
def patent_inventor_link_delete(request, code, inventor_id,
                                my_offices=None, patent=None, inventors=None):
    """
    rimuovi link inventore a Persona
    """
    inventor = get_object_or_404(BrevettoInventori.objects.select_related('matricola_inventore'),
                                 pk=inventor_id,
                                 id_brevetto=code)

    log_action(user=request.user,
               obj=patent,
               flag=CHANGE,
               msg=f'{_("Deleted inventor link")} {inventor.matricola_inventore}')

    inventor.matricola_inventore = None
    inventor.save()

    messages.add_message(request,
                         messages.SUCCESS,
                         _("Inventor link removed successfully"))
    return redirect('crud_patents:crud_patent_inventor_data',
                    code=code, inventor_id=inventor_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_patents
def patent_delete(request, code, my_offices=None, patent=None, inventors=None):
    """
    rimuovi brevetto
    """
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    #     raise Exception(_('Permission denied'))

    patent = get_object_or_404(BrevettoDatiBase, pk=code)
    logo = patent.nome_file_logo.path

    patent.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Patent removed successfully"))
    try:
        os.remove(logo)
    except Exception:  # pragma: no cover
        logger.warning(f'File {logo} not found')

    return redirect('crud_patents:crud_patents')
