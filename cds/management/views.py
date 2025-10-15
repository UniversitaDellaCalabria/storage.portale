import datetime
import logging
import os
from pathlib import Path

from addressbook.models import Personale
from addressbook.utils import get_personale_matricola
from cds.models import (
    DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti,
    DidatticaRegolamento,
    DidatticaRegolamentoAltriDati,
    DidatticaRegolamentoTipologiaAltriDati,
)
from cds.settings import REGDID_OTHER_DATA_TYPES_MAPPINGS, cds_multimedia_media_path
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message, decrypt, encrypt, log_action

from .decorators import (
    can_edit_cds,
    can_manage_cds,
    can_manage_cds_documents,
    can_manage_cds_teaching_system,
)
from .forms import (
    ChoosenPersonForm,
    DidatticaCdsAltriDatiCoordinatorForm,
    DidatticaCdsAltriDatiForm,
    DidatticaCdsAltriDatiUfficioForm,
    DidatticaCdsGruppoComponenteForm,
    DidatticaCdsGruppoForm,
    DidatticaCdsManifestoRegolamentoForm,
    DidatticaCdsOrdinamentoForm,
    DidatticaRegolamentoAltriDatiForm,
)

logger = logging.getLogger(__name__)


def _file_exists(file_rel_path):
    try:
        file_rel_path_uq = file_rel_path
        file_abs_path = os.path.join(settings.MEDIA_ROOT, file_rel_path_uq)
        if os.path.isfile(file_abs_path):
            return True
    except Exception:
        pass
    return False


def _get_django_file(file_rel_path):
    output = None
    try:
        file_rel_path_uq = file_rel_path
        file_abs_path = os.path.join(settings.MEDIA_ROOT, file_rel_path_uq)
        with open(file_abs_path, "r") as clob_ita_file:
            output = File(clob_ita_file)
            output.url = default_storage.url(file_rel_path)
    except Exception:
        pass
    return output


def _handle_regdid_other_data_file_upload(files, file_name, field_name):
    try:
        file_name_uq = file_name
        clob_rel_path = cds_multimedia_media_path(None, filename=file_name_uq)
        clob_abs_path = os.path.join(settings.MEDIA_ROOT, clob_rel_path)
        output = None
        Path(clob_abs_path).parent.mkdir(
            parents=True, exist_ok=True
        )  # create dir if it does not exist
        if os.path.isfile(clob_abs_path):
            abs_filename, extension = os.path.splitext(clob_abs_path)
            counter = 1
            while os.path.exists(clob_abs_path):
                clob_abs_path = abs_filename + " (" + str(counter) + ")" + extension
                counter += 1

            with open(clob_abs_path, "wb+") as destination:
                for chunk in files[field_name].chunks():
                    destination.write(chunk)

            rel_filename, extension = os.path.splitext(clob_rel_path)
            rel_filename_q = rel_filename
            clob_rel_path = rel_filename_q + " (" + str(counter - 1) + ")" + extension
            output = clob_rel_path
        else:
            with open(clob_abs_path, "wb+") as destination:
                for chunk in files[field_name].chunks():
                    destination.write(chunk)
                output = clob_rel_path
    except Exception:
        pass
    return output


def _handle_regdid_other_data_file_delete(file_rel_path, field_name, regdid_id):
    try:
        clob_path = os.path.join(settings.MEDIA_ROOT, file_rel_path)
        q = {field_name: file_rel_path}
        if os.path.isfile(clob_path):
            occurrences_count = (
                DidatticaRegolamentoAltriDati.objects.exclude(regdid_id=regdid_id)
                .filter(**q)
                .count()
            )
            if occurrences_count == 0:  # safe to remove
                os.remove(clob_path)
                return True
    except Exception:
        pass
    return False


@login_required
@can_manage_cds
def cds(request, my_offices=None):
    """
    lista dei corsi di studio
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("CdS")}
    context = {"breadcrumbs": breadcrumbs, "url": reverse("cds:apiv1:cds-list")}
    return render(request, "cds.html", context)


@login_required
@can_manage_cds
# @can_edit_cds
def cds_detail(request, regdid_id, my_offices=None, regdid=None):
    """
    dettaglio corso di studio
    """

    # altri dati regolamento didattico
    regdid_other_data = DidatticaRegolamentoAltriDati.objects.filter(
        regdid_id=regdid_id
    ).exclude(tipo_testo_regdid_cod="URL_CDS")
    regdid_other_data_types = DidatticaRegolamentoTipologiaAltriDati.objects.exclude(
        tipo_testo_regdid_cod="URL_CDS"
    )
    regdid_other_data_dict = {}
    for roat in regdid_other_data_types:
        instance = regdid_other_data.filter(
            tipo_testo_regdid_cod__tipo_testo_regdid_cod=roat.tipo_testo_regdid_cod
        ).first()
        clob_type = ""
        type_mappings = REGDID_OTHER_DATA_TYPES_MAPPINGS[roat.tipo_testo_regdid_cod]
        if len(type_mappings) == 1:
            clob_type = type_mappings[0]
        else:
            if instance is not None:  # check type
                if _file_exists(instance.clob_txt_ita):
                    clob_type = "PDF"
                if _file_exists(instance.clob_txt_eng):
                    clob_type = "PDF"
                if clob_type != "PDF":
                    try:
                        url_validator = URLValidator()
                        url_validator(instance.clob_txt_ita)
                        clob_type = "URL"
                    except Exception:
                        pass
        regdid_other_data_dict[roat] = {"instance": instance, "clob_type": clob_type}

    # altri dati corso di studio
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id).first()

    # dati uffici corso di studio
    regdid = (
        DidatticaRegolamento.objects.filter(pk=regdid_id).select_related("cds").first()
    )
    office_data = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=regdid.cds.pk)

    # dati gruppi cds
    cds_groups = DidatticaCdsGruppi.objects.filter(didattica_cds=regdid.cds.pk)

    # dati gruppi dipartimento
    # department_groups = DidatticaDipartimentoGruppi.objects.filter(
    # id_didattica_dipartimento=regdid.cds.dip.pk)

    # logs
    logs_regdid = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(regdid).pk,
        object_id=regdid.pk,
    )

    logs_cds = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(regdid.cds).pk,
        object_id=regdid.cds.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        "#": regdid.cds.nome_cds_it,
    }

    return render(
        request,
        "cds_detail.html",
        {
            "breadcrumbs": breadcrumbs,
            "logs_regdid": logs_regdid,
            "logs_cds": logs_cds,
            "other_data": other_data,
            "office_data": office_data,
            "regdid": regdid,
            "cds_groups": cds_groups,
            "regdid_other_data_dict": regdid_other_data_dict,
        },
    )
    # 'department_groups': department_groups,})
    # 'gruppi_cds': gruppi_cds,
    # 'gruppi_dip': gruppi_dip})


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_import(request, regdid_id, regdid=None, my_offices=None):
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id).first()
    previous_regdid = DidatticaRegolamento.objects.filter(
        cds_id=regdid.cds_id, aa_reg_did=regdid.aa_reg_did - 1
    ).first()

    if not previous_regdid:
        messages.add_message(request, messages.ERROR, _("There is no data to import"))
        return redirect("cds:management:cds-detail", regdid_id=regdid_id)

    other_data_previous_year = DidatticaCdsAltriDati.objects.filter(
        regdid_id=previous_regdid.regdid_id
    ).first()

    if not other_data_previous_year:
        messages.add_message(request, messages.ERROR, _("There is no data to import"))
        return redirect("cds:management:cds-detail", regdid_id=regdid_id)

    if other_data:
        other_data.matricola_coordinatore = (
            other_data_previous_year.matricola_coordinatore
        )
        other_data.nome_origine_coordinatore = (
            other_data_previous_year.nome_origine_coordinatore
        )
        other_data.nome_origine_vice_coordinatore = (
            other_data_previous_year.nome_origine_vice_coordinatore
        )
        other_data.save()
    else:
        DidatticaCdsAltriDati.objects.create(
            regdid=regdid,
            matricola_coordinatore=other_data_previous_year.matricola_coordinatore,
            nome_origine_coordinatore=other_data_previous_year.nome_origine_coordinatore,
            nome_origine_vice_coordinatore=other_data_previous_year.nome_origine_vice_coordinatore,
        )

    log_action(
        user=request.user,
        obj=regdid,
        flag=CHANGE,
        msg=_("Imported course information from previous year"),
    )

    messages.add_message(
        request,
        messages.SUCCESS,
        _("Successfully imported course information from last year"),
    )

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):
    """
    modifica altri dati corso di studio
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati, pk=data_id, regdid_id=regdid_id
    )
    form = DidatticaCdsAltriDatiForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsAltriDatiForm(
            instance=other_data, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save(commit=False)
            other_data.user_mod = request.user
            if (
                not form.cleaned_data["nome_origine_coordinatore"]
                and other_data.matricola_coordinatore
            ):
                other_data.nome_origine_coordinatore = f"{other_data.matricola_coordinatore.nome} {other_data.matricola_coordinatore.cognome}"
            if (
                not form.cleaned_data["nome_origine_vice_coordinatore"]
                and other_data.matricola_vice_coordinatore
            ):
                other_data.nome_origine_vice_coordinatore = f"{other_data.matricola_vice_coordinatore.nome} {other_data.matricola_vice_coordinatore.cognome}"

            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )
                log_action(
                    user=request.user,
                    obj=regdid,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Other data edited successfully")
            )

            return redirect(
                "cds:management:cds-other-data-edit",
                regdid_id=regdid_id,
                data_id=data_id,
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-other-data-edit",
            kwargs={"regdid_id": regdid_id, "data_id": data_id},
        ): _("Other data"),
    }

    return render(
        request,
        "cds_other_data.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "regdid": regdid,
            "other_data": other_data,
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    modifica coordinatore corso di studio
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati.objects.select_related("matricola_coordinatore"),
        pk=data_id,
        regdid_id=regdid_id,
    )

    teacher = other_data.matricola_coordinatore
    teacher_data = ""
    initial = {}

    if teacher:
        teacher_data = f"{teacher.nome} {teacher.cognome}"
        initial = {"choosen_person": encrypt(teacher.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = get_personale_matricola(form.cleaned_data["choosen_person"])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_coordinatore = new_teacher

            if not other_data.nome_origine_coordinatore:
                other_data.nome_origine_coordinatore = (
                    f"{new_teacher.nome} {new_teacher.cognome}"
                )

            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = ""
            elif teacher and teacher != new_teacher:
                log_msg = f"Sostituito link coordinatore {teacher} con {new_teacher}"
            else:
                log_msg = f"Aggiunto link coordinatore a {new_teacher}"

            if log_msg:
                log_action(user=request.user, obj=regdid, flag=CHANGE, msg=log_msg)

            messages.add_message(
                request, messages.SUCCESS, _("Coordinator edited successfully")
            )
            return redirect(
                "cds:management:cds-other-data-edit",
                regdid_id=regdid_id,
                data_id=data_id,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-other-data-edit",
            kwargs={"regdid_id": regdid_id, "data_id": data_id},
        ): _("Other data"),
        "#": _("Coordinator"),
    }

    return render(
        request,
        "cds_other_data_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "regdid": regdid,
            "data_id": data_id,
            "choosen_person": teacher_data,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    modifica vice coordinatore corso di studio
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati.objects.select_related("matricola_vice_coordinatore"),
        pk=data_id,
        regdid_id=regdid_id,
    )

    teacher = other_data.matricola_vice_coordinatore
    teacher_data = ""
    initial = {}

    if teacher:
        teacher_data = f"{teacher.nome} {teacher.cognome}"
        initial = {"choosen_person": encrypt(teacher.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            teacher_code = get_personale_matricola(form.cleaned_data["choosen_person"])
            new_teacher = get_object_or_404(Personale, matricola=teacher_code)
            other_data.matricola_vice_coordinatore = new_teacher

            if not other_data.nome_origine_vice_coordinatore:
                other_data.nome_origine_vice_coordinatore = (
                    f"{new_teacher.nome} {new_teacher.cognome}"
                )

            other_data.save()

            if teacher and teacher == new_teacher:
                log_msg = ""
            elif teacher and teacher != new_teacher:
                log_msg = (
                    f"Sostituito link vice-coordinatore {teacher} con {new_teacher}"
                )
            else:
                log_msg = f"Aggiunto link vice-coordinatore a {new_teacher}"

            if log_msg:
                log_action(user=request.user, obj=regdid, flag=CHANGE, msg=log_msg)

            messages.add_message(
                request, messages.SUCCESS, _("Deputy Coordinator edited successfully")
            )
            return redirect(
                "cds:management:cds-other-data-edit",
                regdid_id=regdid_id,
                data_id=data_id,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-other-data-edit",
            kwargs={"regdid_id": regdid_id, "data_id": data_id},
        ): _("Other data"),
        "#": _("Deputy coordinator"),
    }

    return render(
        request,
        "cds_other_data_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "regdid": regdid,
            "data_id": data_id,
            "choosen_person": teacher_data,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    elimina altri dati
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati, pk=data_id, regdid_id=regdid_id
    )

    other_data.delete()

    log_action(user=request.user, obj=regdid, flag=CHANGE, msg="Set di dati eliminato")

    messages.add_message(
        request, messages.SUCCESS, _("Other data removed successfully")
    )
    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_new(request, regdid_id, my_offices=None, regdid=None):
    """
    nuovi altri dati per il corso di studio
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=regdid_id)

    if other_data:
        raise Exception(_("Other data set already existent for this cds"))

    DidatticaCdsAltriDati.objects.create(regdid_id=regdid_id)

    log_action(
        user=request.user, obj=regdid, flag=CHANGE, msg="Creato nuovo set di dati"
    )

    messages.add_message(
        request, messages.SUCCESS, _("Other data created successfully")
    )
    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_coordinator_delete(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    elimina coordinatore
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati, pk=data_id, regdid_id=regdid_id
    )

    other_data.matricola_coordinatore = None
    other_data.save()

    log_action(
        user=request.user, obj=regdid, flag=CHANGE, msg="Rimosso link a coordinatore"
    )

    messages.add_message(
        request, messages.SUCCESS, _("Coordinator data removed successfully")
    )
    return redirect(
        "cds:management:cds-other-data-edit", regdid_id=regdid_id, data_id=data_id
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_other_data_deputy_coordinator_delete(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    elimina vice coordinatore
    """
    other_data = get_object_or_404(
        DidatticaCdsAltriDati, pk=data_id, regdid_id=regdid_id
    )

    other_data.matricola_vice_coordinatore = None
    other_data.save()

    log_action(
        user=request.user,
        obj=regdid,
        flag=CHANGE,
        msg="Rimosso link a vice-coordinatore",
    )

    messages.add_message(
        request, messages.SUCCESS, _("Deputy coordinator data removed successfully")
    )
    return redirect(
        "cds:management:cds-other-data-edit", regdid_id=regdid_id, data_id=data_id
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_delete(request, regdid_id, data_id, my_offices=None, regdid=None):
    """
    elimina dati ufficio per il corso di studio
    """
    office_data = get_object_or_404(
        DidatticaCdsAltriDatiUfficio, pk=data_id, cds=regdid.cds
    )

    office_data.delete()

    log_action(
        user=request.user, obj=regdid.cds, flag=CHANGE, msg="Rimosso set dati ufficio"
    )

    messages.add_message(
        request, messages.SUCCESS, _("Office data removed successfully")
    )
    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_edit(request, regdid_id, data_id, regdid=None, my_offices=None):
    """
    modifica dati ufficio per il corso di studio
    """
    office_data = get_object_or_404(
        DidatticaCdsAltriDatiUfficio.objects.select_related("matricola_riferimento"),
        pk=data_id,
        cds=regdid.cds,
    )

    form = DidatticaCdsAltriDatiUfficioForm(instance=office_data)

    if request.POST:
        form = DidatticaCdsAltriDatiUfficioForm(instance=office_data, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            office_data.user_mod = request.user

            # se è valorizzato il link a una Persona
            # e non viene definita un'etichetta per il responsabile
            # questa viene impostata automaticamente
            # con i dati dell'oggetto linkato
            if (
                not form.cleaned_data["nome_origine_riferimento"]
                and office_data.matricola_riferimento
            ):
                persona = office_data.matricola_riferimento
                office_data.nome_origine_riferimento = (
                    f"{persona.nome} {persona.cognome}"
                )

            office_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=regdid.cds,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Office data edited successfully")
            )

            return redirect(
                "cds:management:cds-office-data-edit",
                regdid_id=regdid_id,
                data_id=data_id,
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": _("Office data"),
    }

    return render(
        request,
        "cds_office_data.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "regdid": regdid,
            "office_data": office_data,
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_new(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi dati ufficio al corso di studio
    """
    new = DidatticaCdsAltriDatiUfficio.objects.create(cds=regdid.cds, ordine=10)

    log_action(
        user=request.user,
        obj=regdid.cds,
        flag=CHANGE,
        msg="Aggiunto nuovo set dati ufficio",
    )

    messages.add_message(
        request, messages.SUCCESS, _("Office data created successfully")
    )

    return redirect(
        "cds:management:cds-office-data-edit", regdid_id=regdid_id, data_id=new.pk
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    modifica il responsabile dell'ufficio
    """
    office_data = get_object_or_404(
        DidatticaCdsAltriDatiUfficio.objects.select_related("matricola_riferimento"),
        pk=data_id,
        cds=regdid.cds,
    )

    person = office_data.matricola_riferimento
    person_data = ""
    initial = {}
    if person:
        person_data = f"{person.nome} {person.cognome}"
        initial = {"choosen_person": encrypt(person.matricola)}

    form = DidatticaCdsAltriDatiCoordinatorForm(initial=initial)

    if request.POST:
        form = DidatticaCdsAltriDatiCoordinatorForm(data=request.POST)
        if form.is_valid():
            person_code = get_personale_matricola(form.cleaned_data["choosen_person"])
            new_person = get_object_or_404(Personale, matricola=person_code)
            office_data.matricola_riferimento = new_person
            if not office_data.nome_origine_riferimento:
                office_data.nome_origine_riferimento = (
                    f"{new_person.nome} {new_person.cognome}"
                )
            office_data.save()

            if person and person == new_person:
                log_msg = ""
            elif person and person != new_person:
                log_msg = f"Sostituito link responsabile {person} con {new_person}"
            else:
                log_msg = f"Aggiunto link responsabile a {new_person}"

            log_action(user=request.user, obj=regdid.cds, flag=CHANGE, msg=log_msg)

            messages.add_message(
                request, messages.SUCCESS, _("Coordinator edited successfully")
            )
            return redirect(
                "cds:management:cds-office-data-edit",
                regdid_id=regdid_id,
                data_id=data_id,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-office-data-edit",
            kwargs={"regdid_id": regdid_id, "data_id": data_id},
        ): _("Office data"),
        "#": _("Responsible"),
    }

    return render(
        request,
        "cds_office_data_responsible.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "regdid": regdid,
            "data_id": data_id,
            "choosen_person": person_data,
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_office_data_responsible_delete(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    """
    elimina responsabile ufficio
    """
    office_data = get_object_or_404(
        DidatticaCdsAltriDatiUfficio.objects.select_related("matricola_riferimento"),
        pk=data_id,
        cds=regdid.cds,
    )
    office_data.matricola_riferimento = None
    office_data.save()

    log_action(
        user=request.user,
        obj=regdid.cds,
        flag=CHANGE,
        msg="Rimosso link a responsabile",
    )

    messages.add_message(
        request, messages.SUCCESS, _("Responsible data removed successfully")
    )
    return redirect(
        "cds:management:cds-office-data-edit", regdid_id=regdid_id, data_id=data_id
    )


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_teaching_system
def cds_doc_teaching_system(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi/modifica ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid=regdid).first()
    form = DidatticaCdsOrdinamentoForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsOrdinamentoForm(instance=other_data, files=request.FILES)
        if form.is_valid():
            other_data = form.save(commit=False)
            other_data.regdid = regdid
            # other_data.user_mod = request.user
            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=regdid,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Teaching system file edited successfully")
            )

            return redirect("cds:management:cds-detail", regdid_id=regdid_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": _("Teaching system"),
    }

    return render(
        request,
        "cds_teaching_system.html",
        {"breadcrumbs": breadcrumbs, "form": form, "regdid": regdid},
    )


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_teaching_system
def cds_doc_teaching_system_delete(request, regdid_id, my_offices=None, regdid=None):
    """
    elimina ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid=regdid).first()
    if other_data:
        try:
            path = other_data.ordinamento_didattico.path
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        # other_data.user_mod = request.user
        other_data.ordinamento_didattico = None
        other_data.save()
        # other_data.save(update_fields=['ordinamento_didattico','user_mod'])

        log_action(
            user=request.user,
            obj=regdid,
            flag=CHANGE,
            msg=_("Teaching system file removed"),
        )

        messages.add_message(
            request, messages.SUCCESS, _("Teaching system file removed successfully")
        )

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_manifesto_regulation(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi/modifica ordinamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid=regdid).first()
    form = DidatticaCdsManifestoRegolamentoForm(instance=other_data)

    if request.POST:
        form = DidatticaCdsManifestoRegolamentoForm(
            instance=other_data, files=request.FILES
        )
        if form.is_valid():
            other_data = form.save(commit=False)
            # other_data.user_mod = request.user
            other_data.regdid = regdid
            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=regdid,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Documents edited successfully")
            )

            return redirect("cds:management:cds-detail", regdid_id=regdid_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": _("Teaching system"),
    }

    return render(
        request,
        "cds_manifesto_regulation.html",
        {"breadcrumbs": breadcrumbs, "form": form, "regdid": regdid},
    )


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_study_manifesto_delete(request, regdid_id, my_offices=None, regdid=None):
    """
    elimina manifesto studi
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid=regdid).first()
    if other_data:
        try:
            path = other_data.manifesto_studi.path
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        # other_data.user_mod = request.user
        other_data.manifesto_studi = None
        other_data.save()
        # other_data.save(update_fields=['manifesto_studi','user_mod'])

        log_action(
            user=request.user,
            obj=regdid,
            flag=CHANGE,
            msg=_("Study manifesto file removed"),
        )

        messages.add_message(
            request, messages.SUCCESS, _("Study manifesto file removed successfully")
        )

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
# @can_manage_cds
# @can_edit_cds
@can_manage_cds_documents
def cds_doc_didactic_regulation_delete(
    request, regdid_id, my_offices=None, regdid=None
):
    """
    elimina regolamento didattico
    """
    other_data = DidatticaCdsAltriDati.objects.filter(regdid=regdid).first()
    if other_data:
        try:
            path = other_data.regolamento_didattico.path
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

        # other_data.user_mod = request.user
        other_data.regolamento_didattico = None
        # other_data.save(update_fields=['regolamento_didattico','user_mod'])
        other_data.save()

        log_action(
            user=request.user,
            obj=regdid,
            flag=CHANGE,
            msg=_("Didactic regulation file removed"),
        )

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Didactic regulation file removed successfully"),
        )

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_group_new(request, regdid_id, my_offices=None, regdid=None):
    """
    aggiungi gruppo cds
    """
    form = DidatticaCdsGruppoForm()

    if request.POST:
        form = DidatticaCdsGruppoForm(data=request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.didattica_cds = regdid.cds
            group.user_mod = request.user
            group.dt_mod = datetime.datetime.now()
            group.save()

            log_action(
                user=request.user, obj=regdid.cds, flag=CHANGE, msg=_("Added Group")
            )

            messages.add_message(
                request, messages.SUCCESS, _("Group successfully added")
            )

            return redirect("cds:management:cds-detail", regdid_id=regdid_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    return render(
        request,
        "cds_group.html",
        {
            "form": form,
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_group(request, regdid_id, group_id, my_offices=None, regdid=None):
    """
    modifica gruppo cds
    """
    group = get_object_or_404(DidatticaCdsGruppi, pk=group_id, didattica_cds=regdid.cds)
    form = DidatticaCdsGruppoForm(instance=group)

    if request.POST:
        form = DidatticaCdsGruppoForm(instance=group, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            group.didattica_cds = regdid.cds
            group.user_mod = request.user
            group.dt_mod = datetime.datetime.now()
            group.save()

            changed_field_labels = _get_changed_field_labels_from_form(
                form, form.changed_data
            )

            log_action(
                user=request.user,
                obj=regdid.cds,
                flag=CHANGE,
                # msg=[{'changed': {"fields": changed_field_labels}}])
                msg=f"Modificato {changed_field_labels} al gruppo {group}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Group successfully edited")
            )

            return redirect(
                "cds:management:cds-group", regdid_id=regdid_id, group_id=group_id
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": group.descr_breve_it,
    }

    return render(
        request,
        "cds_group.html",
        {"breadcrumbs": breadcrumbs, "form": form, "group": group, "regdid": regdid},
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_group_members_new(request, regdid_id, group_id, my_offices=None, regdid=None):
    """
    aggiungi nuovo componente al gruppo
    """
    group = get_object_or_404(DidatticaCdsGruppi, pk=group_id, didattica_cds=regdid.cds)

    external_form = DidatticaCdsGruppoComponenteForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = DidatticaCdsGruppoComponenteForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                # matricola
                member_code = get_personale_matricola(form.cleaned_data["choosen_person"])
                matricola = get_object_or_404(Personale, matricola=member_code)
                nome = matricola.nome
                cognome = matricola.cognome
            else:
                matricola = None
                nome = form.cleaned_data["nome"]
                cognome = form.cleaned_data["cognome"]

            c = DidatticaCdsGruppiComponenti.objects.create(
                didattica_cds_gruppi=group,
                matricola=matricola,
                cognome=cognome,
                nome=nome,
                funzione_it=form.cleaned_data.get("funzione_it"),
                funzione_en=form.cleaned_data.get("funzione_en"),
                ordine=form.cleaned_data.get("ordine"),
                visibile=form.cleaned_data.get("visibile"),
                dt_mod=datetime.datetime.now(),
                user_mod=request.user,
            )

            log_action(
                user=request.user,
                obj=regdid.cds,
                flag=CHANGE,
                msg=f"Aggiunto nuovo componente {c} al gruppo {group}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Member added successfully")
            )
            return redirect(
                "cds:management:cds-group", regdid_id=regdid_id, group_id=group_id
            )
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-group",
            kwargs={"regdid_id": regdid_id, "group_id": group_id},
        ): group.descr_breve_it,
        "#": _("New member"),
    }

    return render(
        request,
        "cds_group_member.html",
        {
            "breadcrumbs": breadcrumbs,
            "external_form": external_form,
            "internal_form": internal_form,
            "group": group,
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_group_member_edit(
    request, regdid_id, group_id, member_id, my_offices=None, regdid=None
):
    group = get_object_or_404(DidatticaCdsGruppi, pk=group_id, didattica_cds=regdid.cds)

    member = get_object_or_404(
        DidatticaCdsGruppiComponenti, pk=member_id, didattica_cds_gruppi=group
    )

    member_data = ""
    initial = {}

    if member.matricola:
        member_data = f"{member.matricola.cognome} {member.matricola.nome}"
        initial = {"choosen_person": encrypt(member.matricola.matricola)}

    external_form = DidatticaCdsGruppoComponenteForm(instance=member)
    internal_form = ChoosenPersonForm(initial=initial, instance=member, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(
            instance=member, data=request.POST, required=True
        )
        external_form = DidatticaCdsGruppoComponenteForm(
            instance=member, data=request.POST
        )

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                # matricola
                member_code = get_personale_matricola(form.cleaned_data["choosen_person"])
                matricola = get_object_or_404(Personale, matricola=member_code)
                member.matricola = matricola
                member.nome = matricola.nome
                member.cognome = matricola.cognome
            else:
                member.matricola = None
                member.nome = form.cleaned_data["nome"]
                member.cognome = form.cleaned_data["cognome"]

            member.dt_mod = datetime.datetime.now()
            member.user_mod = request.user

            member.save()

            log_action(
                user=request.user,
                obj=regdid.cds,
                flag=CHANGE,
                msg=f"Modificato componente {member} al gruppo {group}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Member edited successfully")
            )
            return redirect(
                "cds:management:cds-group", regdid_id=regdid_id, group_id=group_id
            )
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        reverse(
            "cds:management:cds-group",
            kwargs={"regdid_id": regdid_id, "group_id": group_id},
        ): group.descr_breve_it,
        "#": _("Edit member"),
    }

    return render(
        request,
        "cds_group_member.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": member_data,
            "external_form": external_form,
            "internal_form": internal_form,
            "group": group,
            "url": reverse("addressbook:apiv1:addressbook-list"),
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_group_delete(request, regdid_id, group_id, my_offices=None, regdid=None):
    """
    elimina gruppo
    """

    group = get_object_or_404(DidatticaCdsGruppi, pk=group_id, didattica_cds=regdid.cds)

    group_name = group.descr_breve_it
    group.delete()

    log_action(
        user=request.user,
        obj=regdid.cds,
        flag=CHANGE,
        msg=f"Eliminato gruppo {group_name}",
    )

    messages.add_message(request, messages.SUCCESS, _("Group deleted successfully"))

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)


@login_required
@can_manage_cds
@can_edit_cds
def cds_group_member_delete(
    request, regdid_id, group_id, member_id, my_offices=None, regdid=None
):
    """
    elimina componente di un gruppo
    """

    group = get_object_or_404(DidatticaCdsGruppi, pk=group_id, didattica_cds=regdid.cds)

    member = get_object_or_404(
        DidatticaCdsGruppiComponenti, pk=member_id, didattica_cds_gruppi=group
    )
    member_name = f"{member.cognome} {member.nome}"
    member.delete()

    log_action(
        user=request.user,
        obj=regdid.cds,
        flag=CHANGE,
        msg=f"Eliminato componente {member_name} dal gruppo {group}",
    )

    messages.add_message(request, messages.SUCCESS, _("Member deleted successfully"))

    return redirect("cds:management:cds-group", regdid_id=regdid_id, group_id=group.pk)


# regdid other data
@login_required
@can_manage_cds
@can_edit_cds
def cds_regdid_other_data_delete(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    redirect_to_new = request.GET.get("redirect_to_new")

    other_data = get_object_or_404(DidatticaRegolamentoAltriDati, pk=data_id)
    other_data_type = other_data.tipo_testo_regdid_cod.tipo_testo_regdid_cod
    type_mappings = REGDID_OTHER_DATA_TYPES_MAPPINGS[other_data_type]

    # If the element is a file and is not present in any other record, it can be deleted on the server
    if "PDF" in type_mappings:
        _handle_regdid_other_data_file_delete(
            other_data.clob_txt_ita, "clob_txt_ita", regdid_id
        )
        _handle_regdid_other_data_file_delete(
            other_data.clob_txt_eng, "clob_txt_eng", regdid_id
        )

    other_data.delete()

    log_message = (
        _("Deleted")
        + f" multimedia {other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des}"
    )

    log_action(user=request.user, obj=regdid, flag=CHANGE, msg=log_message)

    messages.add_message(
        request,
        messages.SUCCESS,
        f"{other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des} "
        + _("removed successfully"),
    )

    if redirect_to_new != "yes":
        return redirect("cds:management:cds-detail", regdid_id=regdid_id)
    else:
        return redirect(
            "cds:management:cds-regdid-other-data-new",
            regdid_id=regdid_id,
            other_data_type_id=other_data.tipo_testo_regdid_cod.pk,
        )


@login_required
@can_manage_cds
@can_edit_cds
def cds_regdid_other_data_edit(
    request, regdid_id, data_id, my_offices=None, regdid=None
):
    other_data = get_object_or_404(DidatticaRegolamentoAltriDati, pk=data_id)
    other_data_type = other_data.tipo_testo_regdid_cod.tipo_testo_regdid_cod
    other_data_des = other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des
    other_data_des_formatted = other_data_des.lower().capitalize()

    initial_clob_txt_ita = other_data.clob_txt_ita
    initial_clob_txt_eng = other_data.clob_txt_eng

    type_mappings = REGDID_OTHER_DATA_TYPES_MAPPINGS[other_data_type]

    multiple_types = 1 if len(type_mappings) > 1 else 0
    clob_type = type_mappings[0]

    if multiple_types == 1:
        if _file_exists(other_data.clob_txt_ita):
            clob_type = "PDF"
            initial_clob_txt_ita = _get_django_file(other_data.clob_txt_ita)
        if _file_exists(other_data.clob_txt_eng):
            clob_type = "PDF"
            initial_clob_txt_eng = _get_django_file(other_data.clob_txt_eng)
        if clob_type != "PDF":
            try:
                url_validator = URLValidator()
                url_validator(other_data.clob_txt_ita)
                clob_type = "URL"
            except Exception:
                pass

    form_name_dict = {
        clob_type: DidatticaRegolamentoAltriDatiForm(
            instance=other_data,
            data=request.POST if request.POST else None,
            files=request.FILES if request.FILES else None,
            clob_type=clob_type,
            clob_label=other_data_des_formatted,
            tipo_testo_regdid_cod=other_data_type,
            form_name=clob_type,
            initial={
                "clob_txt_ita": initial_clob_txt_ita,
                "clob_txt_eng": initial_clob_txt_eng,
            },
        )
    }

    form_name = next(iter(form_name_dict))

    if request.POST:
        form = form_name_dict[form_name]
        if form.is_valid():
            old_instance = get_object_or_404(DidatticaRegolamentoAltriDati, pk=data_id)
            instance = form.save(commit=False)
            errors = False
            if clob_type == "PDF":
                # if clob_txt_ita is updated
                if request.FILES.get("clob_txt_ita", None) is not None:
                    if _file_exists(old_instance.clob_txt_ita):
                        _handle_regdid_other_data_file_delete(
                            old_instance.clob_txt_ita, "clob_txt_ita", regdid_id
                        )
                    clob_txt_ita = _handle_regdid_other_data_file_upload(
                        request.FILES, instance.clob_txt_ita, "clob_txt_ita"
                    )
                    if clob_txt_ita is None:
                        errors = True
                        messages.add_message(
                            request,
                            messages.ERROR,
                            _("Something went wrong with file upload (ita)"),
                        )

                    instance.clob_txt_ita = clob_txt_ita

                # if clob_txt_eng is updated
                if request.FILES.get("clob_txt_eng", None) is not None:
                    if _file_exists(old_instance.clob_txt_eng):
                        _handle_regdid_other_data_file_delete(
                            old_instance.clob_txt_eng, "clob_txt_eng", regdid_id
                        )
                    clob_txt_eng = _handle_regdid_other_data_file_upload(
                        request.FILES, instance.clob_txt_eng, "clob_txt_eng"
                    )
                    if clob_txt_eng is None:
                        errors = True
                        messages.add_message(
                            request,
                            messages.ERROR,
                            _("Something went wrong with file upload (eng)"),
                        )

                    instance.clob_txt_eng = clob_txt_eng

                # if clear checkbox selected on clob_txt_eng
                if old_instance.clob_txt_eng and instance.clob_txt_eng == "False":
                    _handle_regdid_other_data_file_delete(
                        old_instance.clob_txt_eng, "clob_txt_eng", regdid_id
                    )
                    instance.clob_txt_eng = None

            if not errors:
                instance.dt_mod = datetime.datetime.now()
                instance.user_mod = request.user
                instance.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des} "
                    + _("updated successfully"),
                )

                log_action(
                    user=request.user,
                    obj=regdid,
                    flag=CHANGE,
                    msg=_("Updated")
                    + " multimedia "
                    + other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des,
                )

                return redirect("cds:management:cds-detail", regdid_id=regdid_id)

        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": _("Edit") + f" {other_data.tipo_testo_regdid_cod.tipo_testo_regdid_des}",
    }

    return render(
        request,
        "cds_regdid_other_data_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "regdid": regdid,
            "edit": 1,
            "multiple_types": multiple_types,
            "other_data": other_data,
            "item_label": other_data_des.lower(),
            "form_name_dict": form_name_dict,
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_regdid_other_data_new(
    request, regdid_id, other_data_type_id, my_offices=None, regdid=None
):
    other_data_type = get_object_or_404(
        DidatticaRegolamentoTipologiaAltriDati, pk=other_data_type_id
    )
    other_data_cod = other_data_type.tipo_testo_regdid_cod
    other_data_des = other_data_type.tipo_testo_regdid_des
    other_data_des_formatted = other_data_des.lower().capitalize()

    if DidatticaRegolamentoAltriDati.objects.filter(
        regdid_id=regdid_id, tipo_testo_regdid_cod=other_data_cod
    ).exists():
        return custom_message(
            request,
            _("Multimedia content of the same type already exists for this CdS"),
        )

    types_mappings = REGDID_OTHER_DATA_TYPES_MAPPINGS[other_data_cod]
    excusive_form = 1 if len(types_mappings) > 1 else 0
    form_name_dict = {}
    for type in types_mappings:
        form_name_dict[type] = DidatticaRegolamentoAltriDatiForm(
            clob_type=type,
            clob_label=other_data_des_formatted,
            tipo_testo_regdid_cod=other_data_cod,
            form_name=type,
        )
    selected_form_name = next(iter(form_name_dict))

    if request.POST:
        selected_form_name = request.POST.get("form_name")
        form = DidatticaRegolamentoAltriDatiForm(
            data=request.POST if request.POST else None,
            files=request.FILES if request.FILES else None,
            clob_type=selected_form_name,
            clob_label=other_data_des_formatted,
            tipo_testo_regdid_cod=other_data_cod,
            form_name=selected_form_name,
        )
        form_name_dict[selected_form_name] = form
        if form.is_valid():
            instance = form.save(commit=False)
            errors = False
            if request.FILES.get("clob_txt_ita", None) is not None:
                clob_txt_ita = _handle_regdid_other_data_file_upload(
                    request.FILES, instance.clob_txt_ita, "clob_txt_ita"
                )
                if clob_txt_ita is None:
                    errors = True
                    messages.add_message(
                        request,
                        messages.ERROR,
                        _("Something went wrong with file upload (ita)"),
                    )
                instance.clob_txt_ita = clob_txt_ita

            if not errors and request.FILES.get("clob_txt_eng", None) is not None:
                clob_txt_eng = _handle_regdid_other_data_file_upload(
                    request.FILES, instance.clob_txt_eng, "clob_txt_eng"
                )
                if clob_txt_eng is None:
                    errors = True
                    messages.add_message(
                        request,
                        messages.ERROR,
                        _("Something went wrong with file upload (eng)"),
                    )
                instance.clob_txt_eng = clob_txt_eng

            is_clob_empty = (
                instance.clob_txt_ita is None and instance.clob_txt_eng is None
            )
            if is_clob_empty:
                errors = True
                messages.add_message(
                    request, messages.ERROR, _("At least one field must be provided")
                )

            if not errors:
                instance.regdid_id = regdid_id
                instance.tipo_testo_regdid_cod_id = request.POST.get(
                    "tipo_testo_regdid_cod"
                )
                instance.dt_mod = datetime.datetime.now()
                instance.user_mod = request.user
                instance.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{other_data_des} " + _("added successfully"),
                )

                log_action(
                    user=request.user,
                    obj=regdid,
                    flag=CHANGE,
                    msg=_("Added") + " multimedia " + other_data_des,
                )

                return redirect("cds:management:cds-detail", regdid_id=regdid_id)

        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("cds:management:cds"): _("CdS"),
        reverse(
            "cds:management:cds-detail", kwargs={"regdid_id": regdid_id}
        ): regdid.cds.nome_cds_it,
        "#": _("New") + f" {other_data_des_formatted}",
    }

    return render(
        request,
        "cds_regdid_other_data_form.html",
        {
            "breadcrumbs": breadcrumbs,
            "regdid": regdid,
            "item_label": other_data_des.lower(),
            "form_name_dict": form_name_dict,
            "exclusive_form": excusive_form,
            "selected_form_name": selected_form_name,
        },
    )


@login_required
@can_manage_cds
@can_edit_cds
def cds_regdid_other_data_import(request, regdid_id, my_offices=None, regdid=None):
    previous_regdid = DidatticaRegolamento.objects.filter(
        cds_id=regdid.cds_id, aa_reg_did=regdid.aa_reg_did - 1
    ).first()

    if not previous_regdid:
        messages.add_message(request, messages.ERROR, _("There is no data to import"))
        return redirect("cds:management:cds-detail", regdid_id=regdid_id)

    regdid_other_data_previous_year = DidatticaRegolamentoAltriDati.objects.filter(
        regdid_id=previous_regdid.regdid_id
    ).exclude(tipo_testo_regdid_cod="URL_CDS")

    if not regdid_other_data_previous_year.exists():
        messages.add_message(request, messages.ERROR, _("There is no data to import"))

        return redirect("cds:management:cds-detail", regdid_id=regdid_id)

    for regdid_oa_py in regdid_other_data_previous_year:
        # update existing record
        current = DidatticaRegolamentoAltriDati.objects.filter(
            regdid_id=regdid_id,
            tipo_testo_regdid_cod=regdid_oa_py.tipo_testo_regdid_cod.tipo_testo_regdid_cod,
        ).first()
        if current:
            # delete files if present
            if (
                "PDF"
                in REGDID_OTHER_DATA_TYPES_MAPPINGS[
                    current.tipo_testo_regdid_cod.tipo_testo_regdid_cod
                ]
            ):
                if _file_exists(current.clob_txt_ita):
                    _handle_regdid_other_data_file_delete(
                        current.clob_txt_ita, "clob_txt_ita", regdid_id
                    )
                if _file_exists(current.clob_txt_eng):
                    _handle_regdid_other_data_file_delete(
                        current.clob_txt_eng, "clob_txt_eng", regdid_id
                    )
            # update instance
            current.clob_txt_ita = regdid_oa_py.clob_txt_ita
            current.clob_txt_eng = regdid_oa_py.clob_txt_eng
            current.dt_mod = datetime.datetime.now()
            current.user_mod = request.user
            current.save()
        else:  # create new record
            DidatticaRegolamentoAltriDati.objects.create(
                regdid_id=regdid_id,
                tipo_testo_regdid_cod=regdid_oa_py.tipo_testo_regdid_cod,
                clob_txt_ita=regdid_oa_py.clob_txt_ita,
                clob_txt_eng=regdid_oa_py.clob_txt_eng,
                dt_mod=datetime.datetime.now(),
                user_mod=request.user,
            )

    log_action(
        user=request.user,
        obj=regdid,
        flag=CHANGE,
        msg=_("Imported multimedia contents from previous year"),
    )

    messages.add_message(
        request,
        messages.SUCCESS,
        _("Successfully imported multimedia contents from last year"),
    )

    return redirect("cds:management:cds-detail", regdid_id=regdid_id)
