import datetime
import logging

from django.http import FileResponse
from django.contrib import messages
from django.contrib.admin.models import CHANGE, ADDITION, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_xhtml2pdf.utils import pdf_decorator

from . decorators import *
from . forms import *
from . utils import generate_regulament_pdf_file

from ricerca_app.models import *
from .. utils.utils import log_action


logger = logging.getLogger(__name__)


def _get_titoli_struttura_articoli_dict(regdid, testata):
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    titoli = DidatticaArticoliRegolamentoTitolo.objects.all()
    struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso).order_by("numero")
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

def _validate_json_import(import_dict):
    errors = []
    result = True
    mandatory_fields = ['aa', 'numero', 'ordine', 'titolo_it']
    for tipo_corso_cod, articles_struct in import_dict.items():
        for art_struct in articles_struct:
            art_numbers = []
            if art_struct is not None:
                # check missing fields
                for mf in mandatory_fields:
                    if mf not in art_struct.keys():
                        result = False
                        if 'numero' in art_struct.keys():
                            errors.append(f"Course Type: '{tipo_corso_cod}' - Article number: {art_struct['numero']}: field <b>'{mf}'</b> is missing")
                        elif 'titolo_it' in art_struct.keys():
                            errors.append(f"Course Type: '{tipo_corso_cod}' - Article title: {art_struct['titolo_it']}: field <b>'{mf}'</b> is missing")
                        else:
                            errors.append(f"Course Type: '{tipo_corso_cod}': field <b>'{mf}'</b> is missing")
                # check duplicate article number
                if 'number' in art_struct.keys():
                    if art_struct['number'] in art_numbers:
                        result = False
                        errors.append(f"Course Type: '{tipo_corso_cod}': field <b>'number'</b> is duplicated")
                    art_numbers.append(art_struct['number'])
                if 'ordine' in art_struct.keys():
                    if art_struct['ordine'] in art_numbers:
                        result = False
                        errors.append(f"Course Type: '{tipo_corso_cod}': field <b>'ordine'</b> is duplicated")
    return result, errors
            
    

@login_required
@can_manage_regdid
def regdid_list(request, my_offices=None):
    breadcrumbs = {reverse('crud_utils:crud_dashboard'): _('Dashboard'),
                   '#': _('Didactic regulations')}
    context = {'breadcrumbs': breadcrumbs,
               'url': reverse('ricerca:cdslist'),}
    return render(request, 'regdid_list.html', context)


@login_required
@can_manage_regdid
def regdid_structure_import(request, my_offices=None):

    didatticaarticoliregolamentostrutturaform = DidatticaArticoliRegolamentoStrutturaForm(data=request.POST if request.POST else None, initial={'structure': "{}"})
    
    if request.POST:
        if didatticaarticoliregolamentostrutturaform.is_valid():
            
            classes = didatticaarticoliregolamentostrutturaform.cleaned_data.get('structure')
            
            result, errors = _validate_json_import(classes)
            if not result:
                for err in errors:
                    messages.add_message(request, messages.ERROR, f"{err}")
            
            # obj, created = DidatticaArticoliRegolamentoStruttura.objects.update_or_create(
            #     aa=L['numero'], numero=,
            #     defaults={'first_name': 'Bob'},
            # )
            
    
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
@can_manage_regdid
@can_edit_regdid
def regdid_articles(request, regdid_id, regdid=None, my_offices=None, roles=None):
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    titoli = DidatticaArticoliRegolamentoTitolo.objects.all()
    struttura_articoli = DidatticaArticoliRegolamentoStruttura.objects.filter(id_didattica_cds_tipo_corso=didattica_cds_tipo_corso).order_by("numero")
    
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
    didatticacdsarticoliregolamentotestatanoteform = DidatticaCdsArticoliRegolamentoTestataNoteForm(data=request.POST if request.POST else None, instance=testata)
    if request.POST:
        if didatticacdsarticoliregolamentotestatanoteform.is_valid():
            if (request.user.is_superuser or roles['department_operator'])\
               and didatticacdsarticoliregolamentotestatanoteform.changed_data:
                    
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
                      'department_notes_form': didatticacdsarticoliregolamentotestatanoteform,
                      'roles': roles,
                  })
    
    

@login_required
@can_manage_regdid
@can_edit_regdid
def regdid_articles_edit(request, regdid_id, article_id, regdid=None, my_offices=None, roles=None):
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    sub_art_list = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=article_id).order_by("ordine")
    didatticacdsarticoliregolamentoform = DidatticaCdsArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=articolo)
    didatticacdsarticoliregolamentonoteform = DidatticaCdsArticoliRegolamentoNoteForm(data=request.POST if request.POST else None, instance=articolo)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    note_revisione = articolo.note
    
    if request.POST:
        if didatticacdsarticoliregolamentoform.is_valid() and didatticacdsarticoliregolamentonoteform.is_valid():
            if didatticacdsarticoliregolamentoform.changed_data:
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
            
            if 'note' in request.POST\
                and (request.user.is_superuser or roles['revision_operator'])\
                and didatticacdsarticoliregolamentonoteform.changed_data:
                    
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
                      'sub_art_list': sub_art_list,
                      'item_label': f"Art. {articolo.id_didattica_articoli_regolamento_struttura.numero} - {articolo.id_didattica_articoli_regolamento_struttura.titolo_it}",
                      'show_sub_articles': 1,
                      'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
                      'review_notes_form': didatticacdsarticoliregolamentonoteform,
                      'review_notes': note_revisione,
                      'edit_notes': 1,
                      'roles': roles,
                  })
    
    

@login_required
@can_manage_regdid
@can_edit_regdid
def regdid_articles_new(request, regdid_id, article_num, regdid=None, my_offices=None, roles=None):
    didattica_cds_tipo_corso = get_object_or_404(DidatticaCdsTipoCorso, tipo_corso_cod__iexact=regdid.cds.tipo_corso_cod)
    struttura_articolo = get_object_or_404(DidatticaArticoliRegolamentoStruttura, id_didattica_cds_tipo_corso=didattica_cds_tipo_corso, numero=article_num)
    didatticacdsarticoliregolamentoform = DidatticaCdsArticoliRegolamentoForm(data=request.POST if request.POST else None)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        if didatticacdsarticoliregolamentoform.is_valid():
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
                      'roles': roles,
                  })

@login_required
@can_manage_regdid
@can_edit_regdid
def regdid_articles_delete(request, regdid_id, article_id, regdid=None, my_offices=None, roles=None):
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    numero_articolo = articolo.id_didattica_articoli_regolamento_struttura.numero
    titolo_articolo = articolo.id_didattica_articoli_regolamento_struttura.titolo_it
    numero_sotto_art = DidatticaCdsSubArticoliRegolamento.objects.filter(id_didattica_cds_articoli_regolamento=article_id).count()
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
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
@can_manage_regdid
@can_edit_regdid
def regdid_sub_articles_edit(request, regdid_id, article_id, sub_article_id, regdid=None, my_offices=None, roles=None):
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    sotto_articolo = get_object_or_404(DidatticaCdsSubArticoliRegolamento, pk=sub_article_id)
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None, instance=sotto_articolo)
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    note_revisione = articolo.note
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        if didatticacdssubarticoliregolamentoform.is_valid():
            if didatticacdssubarticoliregolamentoform.changed_data:
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
                      'review_notes': note_revisione,
                      'roles': roles,
                  })
    

@login_required
@can_manage_regdid
@can_edit_regdid
def regdid_sub_articles_new(request, regdid_id, article_id, regdid=None, my_offices=None, roles=None):
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    didatticacdssubarticoliregolamentoform = DidatticaCdsSubArticoliRegolamentoForm(data=request.POST if request.POST else None)
    strutt_articolo = articolo.id_didattica_articoli_regolamento_struttura
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    note_revisione = articolo.note
    
    # Nav-bar items
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    
    if request.POST:
        if didatticacdssubarticoliregolamentoform.is_valid():
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
                      'review_notes': note_revisione,
                      'roles': roles,
                  })


@login_required
@can_manage_regdid
@can_edit_regdid
def regdid_sub_articles_delete(request, regdid_id, article_id, sub_article_id, regdid=None, my_offices=None, roles=None):
    articolo = get_object_or_404(DidatticaCdsArticoliRegolamento, pk=article_id)
    sotto_articolo = get_object_or_404(DidatticaCdsSubArticoliRegolamento, pk=sub_article_id)
    titolo_sotto_articolo = sotto_articolo.titolo_it
    ordine_sotto_articolo = sotto_articolo.ordine
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    sotto_articolo.delete()
    
    log_action(user=request.user,
                        obj=testata,
                        flag=CHANGE,
                        msg=_("Deleted") + f" Art. {articolo.id_didattica_articoli_regolamento_struttura.numero}.{ordine_sotto_articolo} - {titolo_sotto_articolo}")

    messages.add_message(request,
                            messages.SUCCESS,
                            _("Sub article deleted successfully"))

    return redirect('crud_regdid:crud_regdid_articles_edit', regdid_id=regdid_id, article_id=article_id)


# Regulament PDF
@login_required
@can_manage_regdid
@can_edit_regdid
@pdf_decorator(pdfname="test.pdf")
def regdid_articles_pdf(request, regdid_id, regdid=None, my_offices=None, roles=None):
    testata = get_object_or_404(DidatticaCdsArticoliRegolamentoTestata, cds_id=regdid.cds, aa=regdid.aa_reg_did)
    titoli_struttura_articoli_dict = _get_titoli_struttura_articoli_dict(regdid, testata)
    context = {
        'regdid': regdid,
        'titoli_struttura_articoli_dict': titoli_struttura_articoli_dict,
        'roles': roles,
    }    
    return render(request, 'regdid_generate_pdf.html', context)