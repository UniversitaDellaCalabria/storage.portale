import datetime
import logging

from django.contrib import messages
from django.contrib.admin.models import CHANGE, ADDITION, LogEntry
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.middleware.csrf import get_token
from django.db import transaction

from django_xhtml2pdf.utils import pdf_decorator

from ricerca_app.models import *
from ricerca_app.concurrency import acquire_lock, get_lock_from_cache
from ricerca_app.exceptions import *
from ricerca_app.settings import OFFICE_REGDIDS_DEPARTMENT, OFFICE_REGDIDS_REVISION, OFFICE_REGDIDS_APPROVAL

from .. utils.decorators import *
from .. utils.utils import log_action

from . forms import *

logger = logging.getLogger(__name__)


def _get_titoli_struttura_articoli_dict(regdid, testata):
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    titoli = DidatticaArticoliRegolamentoTitolo.objects.all()
    struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, aa=testata.aa).order_by("numero")
    articoli = DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata, id_didattica_articoli_regolamento_struttura__in=struttura_articoli)
    titoli_struttura_articoli_dict = {titolo : [] for titolo in titoli}
    for titolo in titoli_struttura_articoli_dict.keys():
        titoli_struttura_articoli_dict[titolo] = [
            {
                art_struttura: {
                    articoli.filter(id_didattica_articoli_regolamento_struttura=art_struttura).first(): DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=articoli.filter(id_didattica_articoli_regolamento_struttura=art_struttura).first()).order_by("ordine")}
                for art_struttura in struttura_articoli.filter(id_didattica_articoli_regolamento_titolo=titolo)
            }
        ]
    return titoli_struttura_articoli_dict         
    

@login_required
@check_model_permissions(DidatticaCdsArticoliRegolamento)
def regdid_list(request):
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Didactic regulations')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist'),}
    user_offices = DidatticaCdsArticoliRegolamento._get_all_user_offices(request.user)
    dep_office = user_offices.filter(office__name=OFFICE_REGDIDS_DEPARTMENT)
    # user only has a department office
    if user_offices.exists() and user_offices.count() == dep_office.count():
        context['department_code'] = dep_office.first().office.organizational_structure.unique_code
        
    return render(request, 'regdid_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def regdid_structure_import(request):
    
    didatticaarticoliregolamentostrutturaform = DidatticaArticoliRegolamentoStrutturaForm(data=request.POST if request.POST else None, initial={'structure': "{}"})
    
    if request.POST:
        if didatticaarticoliregolamentostrutturaform.is_valid():
            '''
            json structure:
            [
                {
                    "aa" : 2024,
                    "numero" : 1,
                    "titolo_it" : "Scopo del regolamento",
                    "titolo_en" : "Purpose of the regulation",
                    "ordine" : 0,
                    "id_didattica_cds_tipo_corso": 2,
                    "id_didattica_articoli_regolamento_titolo" : 2
                },
                ...
            ]
            '''
                   
            struttura = didatticaarticoliregolamentostrutturaform.cleaned_data.get('structure')
            
            objs_to_be_created = []
            objs_to_be_updated = []
            
            for struttura_articolo in struttura:
                struttura_articolo["id_user_mod_id"] = request.user.pk
                struttura_articolo["dt_mod"] = datetime.datetime.now().isoformat()
                struttura_articolo["visibile"] = True
                 
                old_obj = DidatticaArticoliRegolamentoStruttura.objects.filter(aa=struttura_articolo["aa"],
                                                                        id_didattica_cds_tipo_corso_id=struttura_articolo["id_didattica_cds_tipo_corso_id"],
                                                                        numero=struttura_articolo["numero"])
                if old_obj.exists():
                    objs_to_be_updated.append((old_obj, struttura_articolo))
                else:
                    objs_to_be_created.append(struttura_articolo)
                
            try:
                with transaction.atomic():
                    for o_obj, n_obj in objs_to_be_updated:
                       o_obj.update(**n_obj)
                    for c_obj in objs_to_be_created:
                        DidatticaArticoliRegolamentoStruttura.objects.create(**c_obj)

                    messages.add_message(request, messages.SUCCESS, _("Structure imported with success"))

            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Unable to import the structure") + f"{ - repr(e)}")
            
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   '#': _('Structure')}

    return render(request,
                  'regdid_structure_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'forms': [didatticaarticoliregolamentostrutturaform,],
                      'item_label': _('Didactic regulations structure')
                  })


@login_required
@check_model_permissions(DidatticaCdsArticoliRegolamento)
def regdid_articles(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    titoli = DidatticaArticoliRegolamentoTitolo.objects.all()
    struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, aa=regdid.aa_reg_did).order_by("numero")
    
    # get or create Testata
    testata, created = DidatticaCdsArticoliRegolamentoTestata.objects.get_or_create(
        cds_id = regdid.cds,
        aa=regdid.aa_reg_did,
        defaults = {
            'cds_id': regdid.cds_id,
            'aa': regdid.aa_reg_did,
            'note': '',
            'id_didattica_articoli_regolamento_status': get_object_or_404(DidatticaArticoliRegolamentoStatus, status_cod=0),
            'visibile': 1,
            'dt_mod': datetime.datetime.now(),
            'id_user_mod': request.user
        }
    )
    
    if created:
        log_action( user=request.user,
                    obj=testata,
                    flag=ADDITION,
                    msg=_("Added regulament testata"))
    
    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
                
    articoli = DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata, id_didattica_articoli_regolamento_struttura__in=struttura_articoli)
    titoli_struttura_articoli_dict = {titolo : [] for titolo in titoli}
    for titolo in titoli_struttura_articoli_dict.keys():
        titoli_struttura_articoli_dict[titolo] = [
            {
                art_struttura: {
                    articoli.filter(id_didattica_articoli_regolamento_struttura=art_struttura).first(): DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=articoli.filter(id_didattica_articoli_regolamento_struttura=art_struttura).first()).order_by("ordine")}
                for art_struttura in struttura_articoli.filter(id_didattica_articoli_regolamento_titolo=titolo)
            }
        ]  
    # Department notes
    can_edit_notes = True if (OFFICE_REGDIDS_DEPARTMENT in user_permissions_and_offices['offices']) and user_permissions_and_offices['permissions']['edit'] else False
    didatticacdsarticoliregolamentotestatanoteform = DidatticaCdsArticoliRegolamentoTestataNoteForm(data=request.POST if request.POST else None, instance=testata)
    department_notes = testata.note
    if request.POST:
        if not user_permissions_and_offices['permissions']['edit']:
            messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
            
        elif didatticacdsarticoliregolamentotestatanoteform.is_valid() and didatticacdsarticoliregolamentotestatanoteform.changed_data:  
                
            note_dipartimento = didatticacdsarticoliregolamentotestatanoteform.save(commit=False)
            note_dipartimento.save(update_fields=['note',])

            log_action( user=request.user,
                        obj=testata,
                        flag=CHANGE,
                        msg=_("Edited department notes"))
            
            messages.add_message(request,
                                messages.SUCCESS,
                                _("Department notes edited successfully"))
        else:  # pragma: no cover
            for k, v in didatticacdsarticoliregolamentotestatanoteform.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{didatticacdsarticoliregolamentotestatanoteform.fields[k].label}</b>: {v}")  
    
    # logs
    logs_regdid_testata = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(testata).pk,
                                           object_id=testata.pk)
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   '#': _('Didactic regulation')}

    return render(request,
                  'regdid_articles.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'logs_regdid_testata': logs_regdid_testata,
                      'testata': testata,
                      'regdid': regdid,
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      # Notes
                      'department_notes_form': didatticacdsarticoliregolamentotestatanoteform,
                      'department_notes': department_notes,
                      'can_edit_notes': can_edit_notes,
                      # Offices and Permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                  })
    
    

@login_required
def regdid_articles_edit(request, regdid_id, article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    
    # permissions    
    user_permissions_and_offices = articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
        
    sub_art_list = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=article_id).order_by("ordine")
    didatticacdsarticoliregolamentoform = DidatticaCdsArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=articolo)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    # Revision notes
    can_edit_notes = True if (OFFICE_REGDIDS_REVISION in user_permissions_and_offices['offices']) and user_permissions_and_offices['permissions']['edit'] else False
    didatticacdsarticoliregolamentonoteform = DidatticaCdsArticoliRegolamentoNoteForm(data=request.POST if request.POST else None, instance=articolo)
    
    # Concurrency
    content_type_id = ContentType.objects.get_for_model(articolo.__class__).pk
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    note_revisione = articolo.note
    
    if request.POST:
        try:
            if not user_permissions_and_offices['permissions']['edit'] or not user_permissions_and_offices['permissions'].get('lock', False):
                messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
            elif didatticacdsarticoliregolamentoform.is_valid() and didatticacdsarticoliregolamentonoteform.is_valid():
                if didatticacdsarticoliregolamentoform.changed_data:
                    acquire_lock(request.user.pk, content_type_id, articolo.pk)    
                
                    articolo = didatticacdsarticoliregolamentoform.save(commit=False)
                    articolo.dt_mod = datetime.datetime.now()
                    articolo.id_user_mod = request.user
                    articolo.save(update_fields=didatticacdsarticoliregolamentoform.changed_data)
                    
                    log_action(user=request.user,
                                        obj=testata,
                                        flag=CHANGE,
                                        msg=_("Edited") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}")

                    messages.add_message(request,
                                            messages.SUCCESS,
                                            _("Article edited successfully"))
                    
                
                if 'note' in request.POST and didatticacdsarticoliregolamentonoteform.changed_data:
                    note_articolo = didatticacdsarticoliregolamentonoteform.save(commit=False)
                    note_articolo.save(update_fields=['note',])
                    
                    log_action( user=request.user,
                                obj=testata,
                                flag=CHANGE,
                                msg=_("Edited notes") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}")
                
                    messages.add_message(request, messages.SUCCESS, _("Notes edited successfully"))
                
                return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=articolo.pk)    
            
            else:  # pragma: no cover
                for k, v in didatticacdsarticoliregolamentoform.errors.items():
                    messages.add_message(request, messages.ERROR,
                                            f"<b>{didatticacdsarticoliregolamentoform.fields[k].label}</b>: {v}")   
        except LockCannotBeAcquiredException as lock_exception:
            pass
            # messages.add_message(request, messages.ERROR, LOCK_MESSAGE.format(user=get_user_model().objects.filter(pk=lock_exception.lock[0]).first(),
            #                                                                   ttl=lock_exception.lock[1]))

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): _('Articles'),
                   '#': f"Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}"}

    return render(request,
                  'regdid_article_unique_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'regdid': regdid,
                      'forms': [didatticacdsarticoliregolamentoform],
                      'article': articolo,
                      'testata': testata,
                      'sub_art_list': sub_art_list,
                      'item_label': f"Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}",
                      'show_sub_articles': 1,
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      # Notes
                      'revision_notes_form': didatticacdsarticoliregolamentonoteform,
                      'revision_notes': note_revisione,
                      'edit_notes': 1,
                      'can_edit_notes': can_edit_notes,
                      # Concurrency
                      'check_for_locks': 1,
                      'lock_obj_content_type_id': content_type_id,
                      'lock_obj_id': articolo.pk,
                      'lock_csrf': get_token(request),
                      # Offices and Permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                  })
    
    

@login_required
def regdid_articles_new(request, regdid_id, article_num):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    struttura_articolo = get_object_or_404(DidatticaArticoliRegolamentoStruttura, id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, numero=article_num)
    didatticacdsarticoliregolamentoform = DidatticaCdsArticoliRegolamentoForm(data=request.POST if request.POST else None)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    if testata.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    # check for existing article
    if DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata, id_didattica_articoli_regolamento_struttura=struttura_articolo).exists():
        return custom_message(request, _("Article already exists"))    
    
    if request.POST:
        if not user_permissions_and_offices['permissions']['edit']:
            messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
        
        elif didatticacdsarticoliregolamentoform.is_valid():
            articolo = didatticacdsarticoliregolamentoform.save(commit=False)
            articolo.id_didattica_articoli_regolamento_struttura = struttura_articolo
            articolo.id_didattica_cds_articoli_regolamento_testata = testata
            articolo.dt_mod = datetime.datetime.now()
            articolo.id_user_mod = request.user
            articolo.cds_id = regdid.cds_id
            articolo.visibile = True
            articolo.save()
            
            log_action(user=request.user,
                                obj=testata,
                                flag=CHANGE,
                                msg=_("Added") + f" Art. {struttura_articolo.numero} - {struttura_articolo.titolo_it}")

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Article added successfully"))

            return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=articolo.pk)

        else:  # pragma: no cover
            for k, v in didatticacdsarticoliregolamentoform.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{didatticacdsarticoliregolamentoform.fields[k].label}</b>: {v}")
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): _('Articles'),
                   '#': f" Art. {article_num} - {struttura_articolo.titolo_it}"}

    return render(request,
                  'regdid_article_unique_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'regdid': regdid,
                      'forms': [didatticacdsarticoliregolamentoform],
                      'item_label': f"Art. {article_num} - {struttura_articolo.titolo_it}",
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      'new_article': 1,
                      'article_num': int(article_num),
                      # Offices and permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                  })

@login_required
def regdid_articles_delete(request, regdid_id, article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    
    # permissions    
    user_permissions_and_offices = articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access'] or not user_permissions_and_offices['permissions']['edit']:
        return custom_message(request, _("Permission denied"))
    
    numero_articolo = articolo.id_didattica_articoli_regolamento_struttura.numero
    titolo_articolo = articolo.id_didattica_articoli_regolamento_struttura.titolo_it
    numero_sotto_art = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=article_id).count()
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    if testata.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    articolo.delete()
    
    log_action(user=request.user,
                        obj=testata,
                        flag=CHANGE,
                        msg=_("Deleted") + f" Art. {numero_articolo} - {titolo_articolo} (" + _("sub articles") + f": {numero_sotto_art})")

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Article deleted successfully"))

    return redirect('crud_regdid:crud_regdid_articles', regdid_id=regdid_id)    

 
# Sub articles

@login_required
def regdid_sub_articles_edit(request, regdid_id, article_id, sub_article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    sotto_articolo = get_object_or_404(DidatticaCdsSubArticoliRegolamento, pk=sub_article_id)
    
    # permissions    
    user_permissions_and_offices = sotto_articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=sotto_articolo)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    note_revisione = articolo.note
    
    # Concurrency
    content_type_id = ContentType.objects.get_for_model(sotto_articolo.__class__).pk
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        try:
            if not user_permissions_and_offices['permissions']['edit'] or not user_permissions_and_offices['permissions'].get('lock', False):
                messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
            elif didatticacdssubarticoliregolamentoform.is_valid():
                if didatticacdssubarticoliregolamentoform.changed_data:
                    acquire_lock(request.user.pk, content_type_id, sotto_articolo.pk)
                    sotto_articolo = didatticacdssubarticoliregolamentoform.save(commit=False)
                    sotto_articolo.dt_mod = datetime.datetime.now()
                    sotto_articolo.id_user_mod = request.user
                    sotto_articolo.save()
                    
                    log_action(user=request.user,
                                        obj=testata,
                                        flag=CHANGE,
                                        msg=_("Edited") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero}.{sotto_articolo.ordine} - {sotto_articolo.titolo_it}")

                    messages.add_message(request,
                                            messages.SUCCESS,
                                            _("Sub article edited successfully"))

                return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=articolo.pk)    
            
            else:  # pragma: no cover
                for k, v in didatticacdssubarticoliregolamentoform.errors.items():
                    messages.add_message(request, messages.ERROR,
                                            f"<b>{didatticacdssubarticoliregolamentoform.fields[k].label}</b>: {v}")
        except LockCannotBeAcquiredException as lock_exception:
            pass
            # messages.add_message(request, messages.ERROR, LOCK_MESSAGE.format(user=get_user_model().objects.filter(pk=lock_exception.lock[0]).first(),
            #                                                                   ttl=lock_exception.lock[1]))  

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): _('Articles'),
                   reverse('crud_regdid:crud_regdid_articles_edit', kwargs={"regdid_id":regdid_id, "article_id":articolo.pk}): f"Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}",
                   '#': f"{sotto_articolo.titolo_it}"}

    return render(request,
                  'regdid_article_unique_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'regdid': regdid,
                      'forms': [didatticacdssubarticoliregolamentoform],
                      'item_label': f"Art {sotto_articolo.id_didattica_cds_articoli_regolamento.id_didattica_articoli_regolamento_struttura.numero}.{sotto_articolo.ordine} - {sotto_articolo.titolo_it}",
                      'sub_article': sotto_articolo,
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      # Notes
                      'revision_notes': note_revisione,
                      # Concurrency
                      'check_for_locks': 1,
                      'lock_obj_content_type_id': content_type_id,
                      'lock_obj_id': sotto_articolo.pk,
                      'lock_csrf': get_token(request),
                      # Offices and permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                  })
    

@login_required
def regdid_sub_articles_new(request, regdid_id, article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    
    # permissions    
    user_permissions_and_offices = articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None)
    strutt_articolo = articolo.id_didattica_articoli_regolamento_struttura
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    if testata.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    note_revisione = articolo.note
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        if not user_permissions_and_offices['permissions']['edit']:
            messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
            
        elif didatticacdssubarticoliregolamentoform.is_valid():
            sotto_articolo = didatticacdssubarticoliregolamentoform.save(commit=False)
            sotto_articolo.id_didattica_cds_articoli_regolamento = articolo
            sotto_articolo.dt_mod = datetime.datetime.now()
            sotto_articolo.id_user_mod = request.user
            sotto_articolo.visibile = True
            sotto_articolo.save()
            
            log_action(user=request.user,
                                obj=testata,
                                flag=CHANGE,
                                msg=_("Added") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero}.{sotto_articolo.ordine} - {sotto_articolo.titolo_it}")

            messages.add_message(request,
                                    messages.SUCCESS,
                                    _("Sub article added successfully"))

            return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=articolo.pk)

        else:  # pragma: no cover
            for k, v in didatticacdssubarticoliregolamentoform.errors.items():
                messages.add_message(request, messages.ERROR,
                                        f"<b>{didatticacdssubarticoliregolamentoform.fields[k].label}</b>: {v}")
        
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): _('Articles'),
                   reverse('crud_regdid:crud_regdid_articles_edit', kwargs={"regdid_id":regdid_id, "article_id":articolo.pk}): f"Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}",
                   '#': _("New sub article")}

    return render(request,
                  'regdid_article_unique_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'regdid': regdid,
                      'forms': [didatticacdssubarticoliregolamentoform],
                      'item_label': _("New sub article for") + f" 'Art {strutt_articolo.numero} - {strutt_articolo.titolo_it}'",
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      # Notes
                      'revision_notes': note_revisione,
                      # Offices and permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                  })


@login_required
def regdid_sub_articles_delete(request, regdid_id, article_id, sub_article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    sotto_articolo = get_object_or_404(DidatticaCdsSubArticoliRegolamento, pk=sub_article_id)
    
    # permissions    
    user_permissions_and_offices = sotto_articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access'] or not user_permissions_and_offices['permissions']['edit']:
        return custom_message(request, _("Permission denied"))
    
    titolo_sotto_articolo = sotto_articolo.titolo_it
    ordine_sotto_articolo = sotto_articolo.ordine
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    if testata.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    sotto_articolo.delete()
    
    log_action(user=request.user,
                        obj=testata,
                        flag=CHANGE,
                        msg=_("Deleted") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero}.{ordine_sotto_articolo} - {titolo_sotto_articolo}")

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Sub article deleted successfully"))

    return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=article_id)


# Status
@login_required
def regdid_status_change(request, regdid_id, status_cod):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access'] or not user_permissions_and_offices['permissions']['edit']:
        return custom_message(request, _("Permission denied"))
    
    try:
        # check if there are any locks on articles or sub-articles
        articoli = DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata)
        sotto_articoli = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento__in=articoli)
        for articolo in articoli:
            content_type_id = ContentType.objects.get_for_model(articolo).pk
            lock = get_lock_from_cache(content_type_id, articolo.pk)
            if lock[0] and not lock[0] == request.user.pk:
                raise LockCannotBeAcquiredException(lock)
        
        for sotto_articolo in sotto_articoli:
            content_type_id = ContentType.objects.get_for_model(sotto_articolo).pk
            lock = get_lock_from_cache(content_type_id, sotto_articolo.pk)
            if lock[0] and not lock[0] == request.user.pk:
                raise LockCannotBeAcquiredException(lock)        
            
        # check status
        old_status = testata.id_didattica_articoli_regolamento_status
        if old_status.status_cod == status_cod:
            messages.add_message(request, messages.ERROR, _("RegDid is already") + f" '{status.status_desc}'")
        
        # update status
        else:
            status = get_object_or_404(DidatticaArticoliRegolamentoStatus, status_cod=status_cod)
            testata.id_didattica_articoli_regolamento_status = status
            testata.id_user_mod = request.user
            testata.dt_mod = datetime.datetime.now()
            testata.save()
            
            log_action(user=request.user,
                    obj=testata,
                    flag=CHANGE,
                    msg=_("Changed regdid stataus to") + f" '{status.status_desc}'")
    
    except LockCannotBeAcquiredException as lock_exception:
        messages.add_message(request, messages.ERROR, LOCK_MESSAGE.format(user=get_user_model().objects.filter(pk=lock_exception.lock[0]).first(),
                                                                          ttl=lock_exception.lock[1]))
        
    return redirect('crud_regdid:crud_regdid_articles', regdid_id=regdid_id)



# Regulament PDF
@login_required
@check_model_permissions(DidatticaCdsArticoliRegolamentoTestata)
@pdf_decorator(pdfname="test.pdf")
def regdid_articles_pdf(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    context = {
        'regdid': regdid,
        'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
    }    
    return render(request, 'regdid_generate_pdf.html', context)