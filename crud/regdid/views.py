import datetime
import logging
import re

from django.contrib import messages
from django.contrib.admin.models import CHANGE, ADDITION, LogEntry
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.middleware.csrf import get_token
from django.db import transaction
from django.http import HttpResponse
from django.core.mail import send_mail

from django_xhtml2pdf.utils import pdf_decorator, fetch_resources
from xhtml2pdf import pisa

from ricerca_app.models import *
from ricerca_app.concurrency import acquire_lock, get_lock_from_cache
from ricerca_app.exceptions import *
from ricerca_app.settings import OFFICE_REGDIDS_DEPARTMENT, OFFICE_REGDIDS_REVISION, OFFICE_REGDIDS_APPROVAL

from .. utils.decorators import *
from .. utils.utils import log_action

from . forms import *
from . settings import *
from . utils import extractArticlesFromPdf

logger = logging.getLogger(__name__)

def _process_articles_request_data(data):
    mut_value = data._mutable
    data._mutable = True
    post_testo_it = data.get("testo_it", None)
    if post_testo_it:
        data["testo_it"] = sub(r"(\&nbsp\;)", " ", post_testo_it) # transforms &nbsp; to normal spaces
        if re.match(r"^<p>\s*<\/p>$", data["testo_it"]): # sets empty paragraphs to None
            data["testo_it"] = None
    post_testo_en = data.get("testo_en", None)
    if post_testo_en:
        data["testo_en"] = sub(r"(\&nbsp\;)", " ", post_testo_en) # transforms &nbsp; to normal spaces
        if re.match(r"^<p>\s*<\/p>$", data["testo_en"]): # sets empty paragraphs to None
            data["testo_en"] = None
    data._mutable = mut_value

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
@check_model_permissions(DidatticaCdsArticoliRegolamentoTestata)
def regdid_list(request):
    
    testata_user_offices = DidatticaCdsArticoliRegolamentoTestata._get_all_user_offices(request.user)
    show_pdf_import_button = testata_user_offices.filter(office__name__in=(OFFICE_REGDIDS_REVISION, OFFICE_REGDIDS_APPROVAL)).count()
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Didactic regulations')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist'),
               'show_pdf_import_button': show_pdf_import_button}
        
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
                    "id_didattica_cds_tipo_corso_id": 2,
                    "id_didattica_articoli_regolamento_titolo_id" : 2
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
def regdid_articles(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)    
    if regdid.cds.tipo_corso_cod not in REGDID_ALLOWED_COURSE_TYPES:
        return custom_message(request, _("Permission denied"))
    testata = DidatticaCdsArticoliRegolamentoTestata.objects.filter(cds_id=regdid.cds, aa=regdid.aa_reg_did).first()
    testata_status = None
    
    if testata is None:
        if not DidatticaCdsArticoliRegolamentoTestata.can_user_create_object(request.user, regdid=regdid):
            return custom_message(request, _("Didactic regulament must be edited by a department first"))
            
        # create Testata
        testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            cds = regdid.cds,
            aa=regdid.aa_reg_did,
            note = '',
            visibile = 1,
            dt_mod = datetime.datetime.now(),
            id_user_mod = request.user
        )
        
        status = get_object_or_404(DidatticaArticoliRegolamentoStatus, status_cod = '0')
        testata_status = DidatticaCdsTestataStatus.objects.create(
            id_didattica_articoli_regolamento_status = status,
            id_didattica_cds_articoli_regolamento_testata = testata,
            data_status = datetime.datetime.now(), 
            dt_mod = datetime.datetime.now(),
            id_user_mod = request.user
        )
        
        log_action( user=request.user,
                    obj=testata,
                    flag=ADDITION,
                    msg=_("Added didactic regulation testata"))
    else:
        testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
        
    # permissions 
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    titoli = DidatticaArticoliRegolamentoTitolo.objects.all()
    struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, aa=regdid.aa_reg_did).order_by("numero")    
                    
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
    
    # Status change reason
    didatticacdstestatastatusform = DidatticaCdsTestataStatusForm()
    
    if request.POST:
        if not user_permissions_and_offices['permissions']['edit']:
            messages.add_message(request, messages.ERROR, _("Unable to edit this item"))
            
        elif didatticacdsarticoliregolamentotestatanoteform.is_valid() and didatticacdsarticoliregolamentotestatanoteform.changed_data:  
            if not didatticacdsarticoliregolamentotestatanoteform.cleaned_data.get('note') == department_notes:
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
    
    # testata status history
    status_history = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status")
    
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   '#': regdid.cds.nome_cds_it.title() }

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
                      # Status Change
                      'didatticacdstestatastatusform': didatticacdstestatastatusform,
                      'status_history': status_history,
                      # Offices and Permissions
                      'user_permissions_and_offices': user_permissions_and_offices,
                      'testata_status': testata_status,
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
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
    
    # Revision notes
    can_edit_notes = True if (OFFICE_REGDIDS_REVISION in user_permissions_and_offices['offices']) and user_permissions_and_offices['permissions']['edit'] else False
    note_revisione = articolo.note
    
    # Testo_it / en
    _process_articles_request_data(request.POST)
        
    didatticacdsarticoliregolamentonoteform = DidatticaCdsArticoliRegolamentoNoteForm(data=request.POST if request.POST else None, instance=articolo)
    
    # Concurrency
    content_type_id = ContentType.objects.get_for_model(articolo.__class__).pk
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
        
    if request.POST:
        if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
            return custom_message(request, _("Permission denied"))
        try:
            if not user_permissions_and_offices['permissions']['edit'] or not user_permissions_and_offices['permissions']['lock']:
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
                    if didatticacdsarticoliregolamentonoteform.cleaned_data.get('note') != note_revisione:
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

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): regdid.cds.nome_cds_it.title(),
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
                      'testata_status': testata_status,
                  })
    
    

@login_required
def regdid_articles_new(request, regdid_id, article_num):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    struttura_articolo = get_object_or_404(DidatticaArticoliRegolamentoStruttura, id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, numero=article_num)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
    
    if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    # Testo_it / en
    _process_articles_request_data(request.POST)
        
    didatticacdsarticoliregolamentoform = DidatticaCdsArticoliRegolamentoForm(data=request.POST if request.POST else None)
    
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
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): regdid.cds.nome_cds_it.title(),
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
                      'testata_status': testata_status,
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
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()

    if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
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
    
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
    
    # Revision Notes
    note_revisione = articolo.note
    
    # Testo_it / en
    _process_articles_request_data(request.POST)
        
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=sotto_articolo)
    
    # Concurrency
    content_type_id = ContentType.objects.get_for_model(sotto_articolo.__class__).pk
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
            return custom_message(request, _("Permission denied"))
        try:
            if not user_permissions_and_offices['permissions']['edit'] or not user_permissions_and_offices['permissions']['lock']:
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

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): regdid.cds.nome_cds_it.title(),
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
                      'testata_status': testata_status,
                  })
    

@login_required
def regdid_sub_articles_new(request, regdid_id, article_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    
    # permissions    
    user_permissions_and_offices = articolo.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    strutt_articolo = articolo.id_didattica_articoli_regolamento_struttura
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
    
    if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
        return custom_message(request, _("Permission denied"))
    
    # Revision Notes
    note_revisione = articolo.note
    
    # Testo_it / en
    _process_articles_request_data(request.POST)
        
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None)
    
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
                   reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}): regdid.cds.nome_cds_it.title(),
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
                      'testata_status': testata_status,
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
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()
    
    if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2', '3']:
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
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()

    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access'] or not user_permissions_and_offices['permissions']['edit']:
        return custom_message(request, _("Permission denied"))
    
    didatticacdstestatastatusform = DidatticaCdsTestataStatusForm(data = request.POST if request.POST else None)
    
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
        old_status = testata_status.id_didattica_articoli_regolamento_status
        status = get_object_or_404(DidatticaArticoliRegolamentoStatus, status_cod=status_cod)
        if old_status.status_cod == status_cod:
            messages.add_message(request, messages.ERROR, _("RegDid is already") + f" '{status.status_desc}'")
        
        # add status update
        else:
            motivazione = None
            # handle reopening / approval
            if old_status.status_cod == '3' or status_cod == '3':
                if not request.POST:
                    return custom_message(request, _("Permission denied"))
                if didatticacdstestatastatusform.is_valid():
                    motivazione = didatticacdstestatastatusform.cleaned_data.get('motivazione')
                else:
                    for k, v in didatticacdstestatastatusform.errors.items():
                        messages.add_message(request, messages.ERROR, f"<b>{didatticacdstestatastatusform.fields[k].label}</b>: {v}")
                    return redirect('crud_regdid:crud_regdid_articles', regdid_id=regdid_id)
            
            testata_status = DidatticaCdsTestataStatus.objects.create(
                id_didattica_articoli_regolamento_status = status,
                id_didattica_cds_articoli_regolamento_testata = testata,
                motivazione = motivazione,
                data_status = datetime.datetime.now(),
                dt_mod = datetime.datetime.now(),
                id_user_mod = request.user
            )
            
            # email
            regdid_articles_url = request.build_absolute_uri(reverse('crud_regdid:crud_regdid_articles', kwargs={"regdid_id":regdid_id}))
            
            active_offices_employees = OrganizationalStructureOfficeEmployee.objects.filter(office__is_active=True, office__organizational_structure__is_active=True)
            department_office_employees_email = active_offices_employees.filter(office__name=OFFICE_REGDIDS_DEPARTMENT,
                                                                                office__organizational_structure__unique_code=regdid.cds.dip.dip_cod)\
                                                                        .values_list('employee_id__email', flat=True)
            revision_office_employees_email = active_offices_employees.filter(office__name=OFFICE_REGDIDS_REVISION)\
                                                                      .values_list('employee_id__email', flat=True)
            approval_office_employees_email = active_offices_employees.filter(office__name=OFFICE_REGDIDS_APPROVAL)\
                                                                      .values_list('employee_id__email', flat=True)
                                                    
            recipients = []
            status_email_message = None
            if status_cod == '0': # send email to department
                recipients = list(set(department_office_employees_email))
                status_email_message = STATUS_EMAIL_MESSAGE_DEPARTMENT
            elif status_cod == '1': # send email to revision
                recipients = list(set(revision_office_employees_email))
                status_email_message = STATUS_EMAIL_MESSAGE_REVISION
            elif status_cod == '2': # send email to approval
                recipients = list(set(approval_office_employees_email))
                status_email_message = STATUS_EMAIL_MESSAGE_APPROVAL

            emails_sent = send_mail(
                STATUS_EMAIL_SUBJECT,
                f"{status_email_message} {regdid.cds.nome_cds_it.title()}: {regdid_articles_url}",
                STATUS_EMAIL_FROM,
                recipients,
                fail_silently=True,
            )
            
            logger.info(f"{regdid.aa_reg_did} - {regdid.cds.cds_cod} sent emails : {emails_sent}")
        
            log_action(user=request.user,
                    obj=testata,
                    flag=CHANGE,
                    msg=_("Changed regdid stataus to") + f" '{status.status_desc}'")
            
            messages.add_message(request, messages.SUCCESS, _("Regdid status updated successfully"))
    
    except LockCannotBeAcquiredException as lock_exception:
        messages.add_message(request, messages.ERROR, LOCK_MESSAGE.format(user=get_user_model().objects.filter(pk=lock_exception.lock[0]).first(),
                                                                          ttl=lock_exception.lock[1]))
        
    return redirect('crud_regdid:crud_regdid_articles', regdid_id=regdid_id)



# Regulament PDF
@login_required
def regdid_articles_pdf(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access']:
        return custom_message(request, _("Permission denied"))
    
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)                     

    tipo_corso_cod = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod).tipo_corso_cod
    tipo_corso_des = 'Laurea'
    if tipo_corso_cod == 'LM':
        tipo_corso_des = 'Laurea Magistrale'
    elif tipo_corso_cod == 'LM5':
        tipo_corso_des = 'Laurea Magistrale a ciclo unico 5 anni'
    elif tipo_corso_cod == 'LM6':
        tipo_corso_des = 'Laurea Magistrale a ciclo unico 6 anni'
        
    nome_cds_it = regdid.cds.nome_cds_it
    cla_cod = regdid.cds.cla_miur_cod
    cla_des = regdid.cds.cla_miur_des
    icla_cod = regdid.cds.intercla_miur_cod
    icla_des = regdid.cds.intercla_miur_des
    
    nome_corso=f"Corso di {tipo_corso_des} in {nome_cds_it}"
    classe_laurea_desc = f'{cla_cod} - {cla_des}'
    if icla_cod and icla_des:
        classe_laurea_desc += f' & {icla_cod} - {icla_des}'
        
    classe_laurea_desc = re.sub('classe delle lauree(\w|\s)+in', '', classe_laurea_desc, flags=re.IGNORECASE)
    
    context = {
        'regdid': regdid,
        'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
        'nome_corso': nome_corso,
        'classe_laurea_desc': classe_laurea_desc,
    }
    
    cds_name = nome_cds_it.replace(" ", "_").title()
    pdf_file_name=f"Regolamento_{cla_cod}_{cds_name}_{datetime.datetime.now().strftime('%m_%d_%Y')}"
    pdf_file_name=pdf_file_name
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={pdf_file_name}.pdf'
    template = render(request, 'regdid_generate_pdf.html', context)
    html_src_b = template.getvalue()

    pisa.CreatePDF(
        html_src_b,
        dest=response,
        link_callback=fetch_resources)
    return response


# PDF import
@login_required
def regdid_articles_import_pdf(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    testata = DidatticaCdsArticoliRegolamentoTestata.objects.filter(cds_id=regdid.cds, aa=regdid.aa_reg_did).first()
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata).order_by("-data_status").first()

    if testata is not None:
        # permissions 
        user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
        if not user_permissions_and_offices['permissions']['edit']:
            return custom_message(request, _("Permission denied"))
        if testata_status.id_didattica_articoli_regolamento_status.status_cod in ['2','3']:
            return custom_message(request, _("Regdid status must be") + " 'In bozza'/'In revisione' " + _("to be imported from file"))
        
        messages.add_message(request, messages.WARNING, _("Regdid was previously edited, the import opertation will overwrite every article"))
    
    elif not DidatticaCdsArticoliRegolamentoTestata.can_user_create_object(request.user, regdid=regdid, importing=True):
        return custom_message(request, _("Permission denied"))
    
    
    regolamentopdfimportform = RegolamentoPdfImportForm(data = request.POST if request.POST else None,
                                                        files = request.FILES if request.FILES else None)
    
    if request.POST:
        if regolamentopdfimportform.is_valid():
            try:
                first_page = regolamentopdfimportform.cleaned_data.get("first_page")
                last_page = regolamentopdfimportform.cleaned_data.get("last_page")
                pdf = regolamentopdfimportform.cleaned_data.get("pdf")
                parsed_articles = extractArticlesFromPdf(pdf, first_page, last_page)
                didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
                struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, aa=regdid.aa_reg_did)
                if len(parsed_articles) != struttura_articoli.count(): raise Exception()
                
                with transaction.atomic():
                    if testata is None:
                        testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
                            cds = regdid.cds,
                            aa=regdid.aa_reg_did,
                            note = '',
                            visibile = 1,
                            dt_mod = datetime.datetime.now(),
                            id_user_mod = request.user
                        )
                    
                    status = DidatticaArticoliRegolamentoStatus.objects.get(status_cod='1')
                    testata_status = DidatticaCdsTestataStatus.objects.create(
                        id_didattica_articoli_regolamento_status = status,
                        id_didattica_cds_articoli_regolamento_testata = testata,
                        motivazione = "Importazione da file",
                        data_status = datetime.datetime.now(), 
                        dt_mod = datetime.datetime.now(),
                        id_user_mod = request.user
                    )
                    
                    # delete all the articles    
                    DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata).delete()
                    
                    # insert new articles
                    for parsed_article in parsed_articles:
                        if parsed_article["testo_it"] is None: continue
                        parsed_article["id_user_mod_id"] = request.user.pk
                        parsed_article["dt_mod"] = datetime.datetime.now().isoformat()
                        parsed_article["visibile"] = True
                        parsed_article["id_didattica_cds_articoli_regolamento_testata_id"] = testata.pk
                        parsed_article["id_didattica_articoli_regolamento_struttura_id"] = struttura_articoli.get(numero=parsed_article["numero"]).pk
                        del parsed_article["numero"]

                        DidatticaCdsArticoliRegolamento.objects.create(**parsed_article)
                        
                log_action(user=request.user,
                           obj=testata,
                           flag=CHANGE,
                           msg=_("Didactic regulation imported from file") + f" - '{status.status_desc}'")
                
                messages.add_message(request, messages.SUCCESS, _("Didactic regulation imported successfully"))
            
            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Didactic regulation import failed"))
            

    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   reverse('crud_regdid:crud_regdid'): _('Didactic regulations'),
                   '#': regdid.cds.nome_cds_it.title() }

    return render(request,
                  'regdid_pdf_import_form.html',
                  {
                      'breadcrumbs': breadcrumbs,
                      'regdid': regdid,
                      'form': regolamentopdfimportform,
                      'item_label': regdid.cds.nome_cds_it.title(),
                      'show_goto_regdid_button': testata is not None,
                  })
    
    
# Publish
@login_required
@user_passes_test(lambda u: u.is_superuser)
def regdid_articles_publish(request, regdid_id):
    regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    testata_status = DidatticaCdsTestataStatus.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata.pk).order_by("-data_status").first()

    # permissions    
    user_permissions_and_offices = testata.get_user_permissions_and_offices(request.user)
    if not user_permissions_and_offices['permissions']['access'] or not user_permissions_and_offices['permissions']['edit'] or not testata_status.id_didattica_articoli_regolamento_status.status_cod == '3':
        return custom_message(request, _("Permission denied"))
    
    # Regulation Articles
    articoli = DidatticaCdsArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento_testata=testata)
    
    # Old SitoWebCdsTopicArticoliReg/SitoWebCdsSubArticoliRegolamento records
    old_swcta_reg = SitoWebCdsTopicArticoliReg.objects.filter(id_didattica_cds_articoli_regolamento__in=articoli)
    
    # SitoWebCdsTopicArticoliReg to be published
    strutture_topic = (SitoWebArticoliRegolamentoStrutturaTopic.objects
                       .select_related('id_sito_web_cds_topic', 'id_did_art_regolamento_struttura')
                       .filter(visibile=True))
        
    articles_to_publish = (DidatticaCdsArticoliRegolamento.objects
                           .select_related('id_didattica_articoli_regolamento_struttura', 'id_didattica_cds_articoli_regolamento_testata')
                           .filter(id_didattica_articoli_regolamento_struttura__in=strutture_topic.values_list('id_did_art_regolamento_struttura', flat=True),
                                   id_didattica_cds_articoli_regolamento_testata=testata,
                                   visibile=True)
                           .order_by('id_didattica_articoli_regolamento_struttura__numero'))
    
    try:
        with transaction.atomic():             
            # Delete (swcta_reg that doesn't match any article that should be published)
            swcta_reg_to_delete = old_swcta_reg.exclude(id_didattica_cds_articoli_regolamento__in=articles_to_publish)
            swcta_reg_to_delete.delete()
            
            # Delete (swcsa_regolamento)
            swcsa_regolamento_to_delete = SitoWebCdsSubArticoliRegolamento.objects.filter(id_sito_web_cds_topic_articoli_reg__in=old_swcta_reg)
            swcsa_regolamento_to_delete.delete()
            
            # Update
            swcta_reg_to_update = old_swcta_reg.filter(id_didattica_cds_articoli_regolamento__in=articles_to_publish)
            for swcta_reg in swcta_reg_to_update:
                _strutture_topic = (strutture_topic
                                    .filter(id_did_art_regolamento_struttura=swcta_reg.id_didattica_cds_articoli_regolamento.id_didattica_articoli_regolamento_struttura,
                                            id_sito_web_cds_topic=swcta_reg.id_sito_web_cds_topic))

                for struttura_topic in _strutture_topic:
                    articolo = articles_to_publish.get(id=swcta_reg.id_didattica_cds_articoli_regolamento.pk)
                    swcta_reg.titolo_it = struttura_topic.titolo_it
                    swcta_reg.titolo_en = struttura_topic.titolo_en
                    swcta_reg.testo_it = articolo.testo_it
                    swcta_reg.testo_en = articolo.testo_en
                    swcta_reg.ordine = struttura_topic.ordine
                    swcta_reg.visibile = True
                    swcta_reg.dt_mod = datetime.datetime.now()
                    swcta_reg.id_user_mod = request.user
                    swcta_reg.save()
                    
                    sotto_articoli = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=articolo, visibile=True)
                    ordine_sotto_articolo = 0
                    for sotto_articolo in sotto_articoli:
                        ordine_sotto_articolo += 10
                        SitoWebCdsSubArticoliRegolamento.objects.create(
                            id_sito_web_cds_topic_articoli_reg = swcta_reg,
                            titolo_it = sotto_articolo.titolo_it,
                            titolo_en = sotto_articolo.titolo_en,
                            testo_it = sotto_articolo.testo_it,
                            testo_en = sotto_articolo.testo_en,
                            ordine = ordine_sotto_articolo,
                            visibile = True,
                            dt_mod = datetime.datetime.now(),
                            id_user_mod = request.user
                        )
                    
            # Create
            dca_regolamento_for_creation = articles_to_publish.exclude(id__in=swcta_reg_to_update.values_list('id_didattica_cds_articoli_regolamento', flat=True))
            
            for articolo in dca_regolamento_for_creation:
                _strutture_topic = strutture_topic.filter(id_did_art_regolamento_struttura=articolo.id_didattica_articoli_regolamento_struttura)
                for struttura_topic in _strutture_topic:
                    swcta_reg = SitoWebCdsTopicArticoliReg.objects.create(
                        titolo_it = struttura_topic.titolo_it,
                        titolo_en = struttura_topic.titolo_en,
                        testo_it = articolo.testo_it,
                        testo_en = articolo.testo_en,
                        id_sito_web_cds_topic = struttura_topic.id_sito_web_cds_topic,
                        id_sito_web_cds_oggetti_portale = None,
                        id_didattica_cds_articoli_regolamento = articolo,
                        ordine = struttura_topic.ordine,
                        visibile = True,
                        dt_mod = datetime.datetime.now(),
                        id_user_mod = request.user
                    )
                    
                    sotto_articoli = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=articolo, visibile=True)
                    ordine_sotto_articolo = 0
                    for sotto_articolo in sotto_articoli:
                        ordine_sotto_articolo += 10
                        SitoWebCdsSubArticoliRegolamento.objects.create(
                            id_sito_web_cds_topic_articoli_reg = swcta_reg,
                            titolo_it = sotto_articolo.titolo_it,
                            titolo_en = sotto_articolo.titolo_en,
                            testo_it = sotto_articolo.testo_it,
                            testo_en = sotto_articolo.testo_en,
                            ordine = ordine_sotto_articolo,
                            visibile = True,
                            dt_mod = datetime.datetime.now(),
                            id_user_mod = request.user
                        )   
        
        messages.add_message(request, messages.SUCCESS, _("Didactic regulation published successfully"))
            
        log_action(user=request.user,
                obj=testata,
                flag=CHANGE,
                msg=_("Published didactic regulation"))
    
    except Exception as e:
        messages.add_message(request, messages.ERROR, _("Didactic regulation publishing failed"))
    
    return redirect('crud_regdid:crud_regdid_articles', regdid_id=regdid_id)
        