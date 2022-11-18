import logging

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

from .. decorators import *
from .. forms import *
from .. utils import log_action


logger = logging.getLogger(__name__)


@login_required
@can_manage_doctorates
def doctorates(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   '#': _('Doctorates')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:phd-activities-list')}
    return render(request, 'doctorates/doctorates.html', context)


@login_required
@can_manage_doctorates
def doctorate_new(request, my_offices=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                   '#': _('New')}
    form = DidatticaDottoratoAttivitaFormativaForm()

    teacher_form = DidatticaDottoratoAttivitaFormativaDocenteForm()

    query_filter = Q()

    # already choosen before form fails
    teacher = None
    if request.POST.get('choosen_person', ''):
        teacher = get_object_or_404(Personale,
                                     matricola=(decrypt(request.POST['choosen_person'])))


    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaForm(data=request.POST)
        teacher_form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)



        if form.is_valid() and teacher_form.is_valid():
            teacher_code = decrypt(teacher_form.cleaned_data['choosen_person'])

            if teacher:
                teacher = get_object_or_404(Personale, matricola=teacher_code)


            # check if user can manage teacher structure
            if not request.user.is_superuser:

                query_filter = Q(office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id)

                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(query_filter,
                                                                                        employee=request.user,
                                                                                        office__name=OFFICE_DOCTORATES,
                                                                                        office__is_active=True,
                                                                                        office__organizational_structure__is_active=True
                                                                                        )
                if not structure_afforg:
                    raise Exception(_("Add teacher belonging to your structure"))

            doctorate = DidatticaDottoratoAttivitaFormativa.objects.create(
                nome_af=form.cleaned_data['nome_af'],
                ssd=form.cleaned_data['ssd'],
                numero_ore=form.cleaned_data['numero_ore'],
                cfu=form.cleaned_data['cfu'],
                tipo_af=form.cleaned_data['tipo_af'],
                rif_dottorato=form.cleaned_data['rif_dottorato'],
                id_struttura_proponente=form.cleaned_data['id_struttura_proponente'],
                struttura_proponente_origine=form.cleaned_data['struttura_proponente_origine'],
                contenuti_af=form.cleaned_data['contenuti_af'],
                prerequisiti=form.cleaned_data['prerequisiti'],
                num_min_studenti=form.cleaned_data['num_min_studenti'],
                num_max_studenti=form.cleaned_data['num_max_studenti'],
                verifica_finale=form.cleaned_data['verifica_finale'],
                modalita_verifica=form.cleaned_data['modalita_verifica'],
                avvio=form.cleaned_data['avvio'],
                fine=form.cleaned_data['fine'],
                orario_aule=form.cleaned_data['orario_aule'],
                note=form.cleaned_data['note'],
                visualizza_orario=form.cleaned_data['visualizza_orario'],

            )
            if teacher:
                DidatticaDottoratoAttivitaFormativaDocente.objects.create(id_didattica_dottorato_attivita_formativa=doctorate,
                                                               cognome_nome_origine=f'{teacher.cognome} {teacher.nome}',
                                                               matricola=teacher)
            else:
                DidatticaDottoratoAttivitaFormativaDocente.objects.create(id_didattica_dottorato_attivita_formativa=doctorate,
                                                                        cognome_nome_origine=teacher_form.cleaned_data['cognome_nome_origine'])
                teacher = DidatticaDottoratoAttivitaFormativaDocente.objects.values('cognome_nome_origine')


            log_action(user=request.user,
                       obj=doctorate,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Doctorate created successfully"))
            return redirect("ricerca_crud:crud_doctorates")

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")
            for k, v in teacher_form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{teacher_form.fields[k].label}</b>: {v}")


    return render(request,
                  'doctorates/doctorate_new.html',
                  {'breadcrumbs': breadcrumbs,
                   'choosen_person': f'{teacher.cognome} {teacher.nome}' if teacher else '',
                   'form': form,
                   'teachers_api': reverse('ricerca:teacherslist'),
                   'teacher_form': teacher_form})


@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate(request, code,
                  my_offices=None, doctorate=None, teachers=None, other_teachers=None):
    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                   '#': doctorate.nome_af}
    form = DidatticaDottoratoAttivitaFormativaForm(instance=doctorate)


    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaForm(instance=doctorate, data=request.POST)

        if form.is_valid():
            doctorate.user_mod = request.user
            doctorate.nome_af = form.cleaned_data['nome_af']
            doctorate.ssd = form.cleaned_data['ssd']
            doctorate.numero_ore = form.cleaned_data['numero_ore']
            doctorate.cfu = form.cleaned_data['cfu']
            doctorate.tipo_af = form.cleaned_data['tipo_af']
            doctorate.rif_dottorato = form.cleaned_data['rif_dottorato']
            doctorate.id_struttura_proponente = form.cleaned_data['id_struttura_proponente']
            doctorate.struttura_proponente_origine = form.cleaned_data['struttura_proponente_origine']
            doctorate.contenuti_af = form.cleaned_data['contenuti_af']
            doctorate.prerequisiti = form.cleaned_data['prerequisiti']
            doctorate.num_min_studenti = form.cleaned_data['num_min_studenti']
            doctorate.num_max_studenti = form.cleaned_data['num_max_studenti']
            doctorate.verifica_finale = form.cleaned_data['verifica_finale']
            doctorate.modalita_verifica = form.cleaned_data['modalita_verifica']
            doctorate.avvio = form.cleaned_data['avvio']
            doctorate.fine = form.cleaned_data['fine']
            doctorate.orario_aule = form.cleaned_data['orario_aule']
            doctorate.note = form.cleaned_data['note']
            doctorate.visualizza_orario = form.cleaned_data['visualizza_orario']
            doctorate.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=doctorate,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Doctorate edited successfully"))

            return redirect('ricerca_crud:crud_doctorate_edit',
                            code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(doctorate).pk,
                                   object_id=doctorate.pk)
    return render(request,
                  'doctorates/doctorate.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'logs': logs,
                   'doctorate': doctorate,
                   'teachers': teachers,
                   'other_teachers': other_teachers})

@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_main_teacher_data(request, code, teacher_id, doctorate=None, teachers=None, other_teachers=None, my_offices=None):

    teacher_data = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                    pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=teacher_data)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaDocenteForm(instance=teacher_data,
                                                data=request.POST)
        if form.is_valid():
            teacher_data.user_mod = request.user
            teacher_data.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']
            teacher_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=doctorate,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('ricerca_crud:crud_doctorate_main_teacher_data',
                            code=code,
                            teacher_id=teacher_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                   reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code }): doctorate.nome_af,
                   reverse('ricerca_crud:crud_doctorate_main_teacher_data', kwargs={'code': code, 'teacher_id': teacher_id}): _('Doctorate teacher data')
                   }

    return render(request,
                  'doctorates/doctorate_main_teacher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'doctorate': doctorate,
                   'teacher_data': teacher_data})



@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_main_teacher_data_edit(request, code, teacher_id, teachers=None, other_teachers=None,
                               my_offices=None, doctorate=None):


    teacher_doctorate = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                    pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    teacher = teacher_doctorate.matricola # mettere nel model il binding tra la tabella DidatticaDottoratoAttivitaFormativaDocente e Personale
    teacher_data = ()

    if teacher:
        teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
        form = DidatticaDottoratoAttivitaFormativaDocenteWithoutFieldsForm(initial={'choosen_person': teacher_data[0]})
    else:
        form = DidatticaDottoratoAttivitaFormativaDocenteWithoutFieldsForm()

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaDocenteWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            teacher_doctorate.matricola = new_teacher
            teacher_doctorate.cognome_nome_origine = f'{new_teacher.cognome} {new_teacher.nome}'
            teacher_doctorate.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed teacher")} {teacher.__str__()}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher.__str__()}'
            else:
                log_msg = f'{_("Changed teacher")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=doctorate,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('ricerca_crud:crud_doctorate_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorate'),
                   reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code}): doctorate.nome_af,
                   '#': _('Teacher')}
    return render(request,
                  'doctorates/doctorate_main_teacher_data_edit.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'doctorate': doctorate,
                   'teacher_id': teacher_id,
                   'choosen_person': teacher_data[1] if teacher_data  else None,
                   'url': reverse('ricerca:teacherslist')})



@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_main_teacher_new(request, code, my_offices=None, doctorate=None, teachers=None, other_teachers=None):
        breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                       reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                       reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code}): doctorate.nome_af,
                       '#': _('New teacher')}
        form = DidatticaDottoratoAttivitaFormativaDocenteForm()
        if request.POST:
            form = DidatticaDottoratoAttivitaFormativaDocenteForm(data=request.POST)
            if form.is_valid():

                p = DidatticaDottoratoAttivitaFormativaDocente.objects.create(
                    id_didattica_dottorato_attivita_formativa=doctorate,
                    cognome_nome_origine=form.cleaned_data['cognome_nome_origine']
                )
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                if teacher_code:
                    teacher = get_object_or_404(Personale, matricola=teacher_code)
                    p.matricola = teacher
                    p.cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
                    p.save()

                log_action(user=request.user,
                           obj=doctorate,
                           flag=CHANGE,
                           msg=f'{_("Added teacher")} {p.__str__()}')

                messages.add_message(request,
                                     messages.SUCCESS,
                                     _("Teacher added successfully"))
                return redirect('ricerca_crud:crud_doctorate_edit',
                                code=code)
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        return render(request,
                      'doctorates/doctorate_main_teacher.html',
                      {'breadcrumbs': breadcrumbs,
                       'form': form,
                       'doctorate': doctorate,
                       'url': reverse('ricerca:teacherslist')})



@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_main_teacher_delete(request, code, teacher_id,
                                 my_offices=None, doctorate=None, teachers=None, other_teachers=None):
    doctorate_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaDocente,
                                        pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    # if DidatticaDottoratoAttivitaFormativaDocente.objects.filter(id_didattica_dottorato_attivita_formativa=code).count() == 1:
    #     raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=doctorate,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {doctorate_teacher.cognome_nome_origine}')

    doctorate_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_doctorate_edit', code=code)




@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_other_teacher_data(request, code, teacher_id, teachers=None, other_teachers=None,
                               my_offices=None, doctorate=None):
    other_teacher_data = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                      pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=other_teacher_data)

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(instance=other_teacher_data,
                                                   data=request.POST)
        if form.is_valid():
            other_teacher_data.user_mod = request.user
            other_teacher_data.cognome_nome_origine = form.cleaned_data['cognome_nome_origine']
            other_teacher_data.save()

            changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                       form.changed_data)
            log_action(user=request.user,
                       obj=doctorate,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher data edited successfully"))

            return redirect('ricerca_crud:crud_doctorate_other_teacher_data',
                            code=code,
                            teacher_id=teacher_id)


        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                   reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code}): doctorate.nome_af,
                   reverse('ricerca_crud:crud_doctorate_other_teacher_data_edit',
                           kwargs={'code': code, 'teacher_id': teacher_id}): _('Doctorate teacher data')
                   }

    return render(request,
                  'doctorates/doctorate_other_teacher_data.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'doctorate': doctorate,
                   'other_teacher_data': other_teacher_data})


@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_other_teacher_data_edit(request, code, teacher_id, teachers, other_teachers=None,
                               my_offices=None, doctorate=None):


    other_teacher_doctorate = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                    pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    teacher = other_teacher_doctorate.matricola
    other_teacher_data = ()

    if teacher:
        other_teacher_data = (encrypt(teacher.matricola), f'{teacher.cognome} {teacher.nome}')
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiWithoutFieldsForm(initial={'choosen_person': other_teacher_data[0]})
    else:
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiWithoutFieldsForm()

    if request.POST:
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiWithoutFieldsForm(data=request.POST)
        if form.is_valid():
            teacher_code = decrypt(form.cleaned_data['choosen_person'])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_teacher_doctorate.matricola = new_teacher
            other_teacher_doctorate.cognome_nome_origine = f'{new_teacher.cognome} {new_teacher.nome}'
            other_teacher_doctorate.save()

            if teacher and teacher == new_teacher:
                log_msg = f'{_("Changed teacher")} {teacher.__str__()}'
            elif teacher and teacher!=new_teacher:
                log_msg = f'{teacher} {_("substituted with")} {new_teacher.__str__()}'
            else:
                log_msg = f'{_("Changed teacher")} {new_teacher.__str__()}'

            log_action(user=request.user,
                       obj=doctorate,
                       flag=CHANGE,
                       msg=log_msg)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Teacher edited successfully"))
            return redirect('ricerca_crud:crud_doctorate_edit',
                            code=code)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                   reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                   reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code}): doctorate.nome_af,
                   '#': _('Teacher')}
    return render(request,
                  'doctorates/doctorate_other_teacher.html',
                  {'breadcrumbs': breadcrumbs,
                   'form': form,
                   'doctorate': doctorate,
                   'teacher_id': teacher_id,
                   'choosen_person': other_teacher_data[1] if other_teacher_data  else None,
                   'url': reverse('ricerca:teacherslist')})




@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_other_teacher_new(request, code, my_offices=None, doctorate=None, teachers=None, other_teachers=None):
        breadcrumbs = {reverse('ricerca_crud:crud_dashboard'): _('Dashboard'),
                       reverse('ricerca_crud:crud_doctorates'): _('Doctorates'),
                       reverse('ricerca_crud:crud_doctorate_edit', kwargs={'code': code}): doctorate.nome_af,
                       '#': _('New teacher')}
        form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm()
        if request.POST:
            form = DidatticaDottoratoAttivitaFormativaAltriDocentiForm(data=request.POST)
            if form.is_valid():

                p = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(
                    id_didattica_dottorato_attivita_formativa=doctorate,
                    cognome_nome_origine=form.cleaned_data['cognome_nome_origine']
                )
                teacher_code = decrypt(form.cleaned_data['choosen_person'])
                if teacher_code:
                    teacher = get_object_or_404(Personale, matricola=teacher_code)
                    p.matricola = teacher
                    p.cognome_nome_origine = f'{teacher.cognome} {teacher.nome}'
                    p.save()

                log_action(user=request.user,
                           obj=doctorate,
                           flag=CHANGE,
                           msg=f'{_("Added teacher")} {p.__str__()}')

                messages.add_message(request,
                                     messages.SUCCESS,
                                     _("Teacher added successfully"))
                return redirect('ricerca_crud:crud_doctorate_edit',
                                code=code)
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        return render(request,
                      'doctorates/doctorate_other_teacher.html',
                      {'breadcrumbs': breadcrumbs,
                       'form': form,
                       'doctorate': doctorate,
                       'url': reverse('ricerca:teacherslist')})


@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_other_teacher_delete(request, code, teacher_id,
                                 my_offices=None, doctorate=None, teachers=None, other_teachers=None):
    doctorate_teacher = get_object_or_404(DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                        pk=teacher_id, id_didattica_dottorato_attivita_formativa=code)

    # if DidatticaDottoratoAttivitaFormativaDocente.objects.filter(id_didattica_dottorato_attivita_formativa=code).count() == 1:
    #     raise Exception(_("Permission denied. Only one teacher remains"))

    log_action(user=request.user,
               obj=doctorate,
               flag=CHANGE,
               msg=f'{_("Deleted teacher")} {doctorate_teacher.cognome_nome_origine}')

    doctorate_teacher.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Teacher removed successfully"))
    return redirect('ricerca_crud:crud_doctorate_edit', code=code)



@login_required
@can_manage_doctorates
@can_edit_doctorate
def doctorate_delete(request, code,
                         my_offices=None, doctorate=None, teachers=None, other_teachers=None):
    # ha senso?
    #if rgroup.user_ins != request.user:
    if not request.user.is_superuser:
        raise Exception(_('Permission denied'))

    doctorate.delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         _("Doctorate removed successfully"))

    return redirect('ricerca_crud:crud_doctorates')