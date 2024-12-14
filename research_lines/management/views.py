import logging

from addressbook.models import Personale
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message, decrypt, encrypt, log_action
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)
from research_lines.settings import OFFICE_RESEARCH_LINES

from .decorators import (
    can_edit_applied_research_line,
    can_edit_base_research_line,
    can_manage_research_lines,
)
from .forms import (
    RicercaDocenteLineaApplicataForm,
    RicercaDocenteLineaBaseForm,
    RicercaLineaApplicataForm,
    RicercaLineaBaseForm,
)

logger = logging.getLogger(__name__)


@login_required
@can_manage_research_lines
def base_research_lines(request, my_offices=None):
    """
    lista delle linee di ricerca di base
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Base Research lines"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("research-lines:apiv1:all-research-lines")
        + "?exclude_applied=1",
    }
    return render(request, "base_researchlines.html", context)


@login_required
@can_manage_research_lines
def applied_research_lines(request, my_offices=None):
    """
    lista delle linee di ricerca applicata
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Applied Research lines"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("research-lines:apiv1:all-research-lines") + "?exclude_base=1",
    }
    return render(request, "applied_researchlines.html", context)


@login_required
@can_manage_research_lines
def applied_research_lines_new(request, my_offices=None):
    """
    nuova linea di ricerca applicata
    """
    form = RicercaLineaApplicataForm()
    teacher_form = RicercaDocenteLineaApplicataForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque il docente scelto senza doverlo cercare
    # nuovamente dall'elenco
    teacher = None
    if request.POST.get("choosen_person", ""):
        teacher = get_object_or_404(
            Personale, matricola=(decrypt(request.POST["choosen_person"]))
        )

    if request.POST:
        form = RicercaLineaApplicataForm(data=request.POST)
        teacher_form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            # se l'utente non è un superuser
            # verifica che il docente sia inserito
            # afferisca alla sua stessa struttura
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(
                    employee=request.user,
                    office__name=OFFICE_RESEARCH_LINES,
                    office__is_active=True,
                    office__organizational_structure__is_active=True,
                    office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id,
                )
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            # crea nuova linea di ricerca
            rline = form.save(commit=False)
            rline.user_ins = request.user
            rline.save()

            # crea nuovo docente associato alla linea di ricerca
            RicercaDocenteLineaApplicata.objects.create(
                user_ins=request.user,
                ricerca_linea_applicata=rline,
                dt_inizio=teacher_form.cleaned_data["dt_inizio"],
                dt_fine=teacher_form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(user=request.user, obj=rline, flag=ADDITION, msg=[{"added": {}}])

            messages.add_message(
                request, messages.SUCCESS, _("Research line created successfully")
            )
            return redirect("research-lines:management:applied-research-lines")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )
            for k, v in teacher_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{teacher_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:applied-research-lines"): _(
            "Applied Research lines"
        ),
        "#": _("New"),
    }

    return render(
        request,
        "researchline_new.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": f"{teacher.nome} {teacher.cognome}" if teacher else "",
            "form": form,
            "url": reverse("teachers:apiv1:teachers-list"),
            "teacher_form": teacher_form,
        },
    )


@login_required
@can_manage_research_lines
def base_research_line_new(request, my_offices=None):
    """
    nuova linea di ricerca di base
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:base-research-lines"): _(
            "Base Research lines"
        ),
        "#": _("New"),
    }
    form = RicercaLineaBaseForm()
    teacher_form = RicercaDocenteLineaBaseForm()

    # se l'utente non è un superuser
    # verifica che il docente sia inserito
    # afferisca alla sua stessa struttura
    teacher = None
    if request.POST.get("choosen_person", ""):
        teacher = get_object_or_404(
            Personale, matricola=(decrypt(request.POST["choosen_person"]))
        )

    if request.POST:
        form = RicercaLineaBaseForm(data=request.POST)
        teacher_form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            # se l'utente non è un superuser
            # verifica che il docente sia inserito
            # afferisca alla sua stessa struttura
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(
                    employee=request.user,
                    office__name=OFFICE_RESEARCH_LINES,
                    office__is_active=True,
                    office__organizational_structure__is_active=True,
                    office__organizational_structure__unique_code=teacher.cd_uo_aff_org_id,
                )
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            # crea nuova linea di ricerca
            rline = form.save(commit=False)
            rline.user_ins = request.user
            rline.save()

            # crea nuovo docente associato alla linea di ricerca
            RicercaDocenteLineaBase.objects.create(
                user_ins=request.user,
                ricerca_linea_base=rline,
                dt_inizio=teacher_form.cleaned_data["dt_inizio"],
                dt_fine=teacher_form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(user=request.user, obj=rline, flag=ADDITION, msg=[{"added": {}}])

            messages.add_message(
                request, messages.SUCCESS, _("Research line created successfully")
            )
            return redirect("research-lines:management:base-research-lines")
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )
            for k, v in teacher_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{teacher_form.fields[k].label}</b>: {v}",
                )

    return render(
        request,
        "researchline_new.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": f"{teacher.nome} {teacher.cognome}" if teacher else "",
            "form": form,
            "url": reverse("teachers:apiv1:teachers-list"),
            "teacher_form": teacher_form,
        },
    )


@login_required
@can_manage_research_lines
@can_edit_base_research_line
def base_research_line(request, rline_id, my_offices=None, rline=None, teachers=None):
    """
    dettaglio linea di ricerca applicata con form di modifica
    """
    form = RicercaLineaBaseForm(instance=rline)
    if request.POST:
        form = RicercaLineaBaseForm(instance=rline, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            rline.user_mod = request.user
            rline.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=rline,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Research line edited successfully")
            )

            return redirect(
                "research-lines:management:base-research-line-edit", rline_id=rline_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(rline).pk, object_id=rline.pk
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:base-research-lines"): _(
            "Base Research lines"
        ),
        "#": rline.descrizione,
    }

    return render(
        request,
        "base_researchline.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "logs": logs,
            "rline": rline,
            "teachers": teachers,
        },
    )


@login_required
@can_manage_research_lines
@can_edit_applied_research_line
def applied_research_line(request, rline_id, my_offices=None, rline=None, teachers=None):
    """
    dettaglio linea di ricerca di base con form di modifica
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:applied-research-lines"): _(
            "Applied Research lines"
        ),
        "#": rline.descrizione,
    }
    form = RicercaLineaApplicataForm(instance=rline)
    if request.POST:
        form = RicercaLineaApplicataForm(instance=rline, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            rline.user_mod = request.user
            rline.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=rline,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Research line edited successfully")
            )

            return redirect(
                "research-lines:management:applied-research-line-edit", rline_id=rline_id
            )

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(rline).pk, object_id=rline.pk
    )

    return render(
        request,
        "applied_researchline.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "logs": logs,
            "rline": rline,
            "teachers": teachers,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
# attualmente solo i superuser possono effetture l'operazione
# @can_manage_research_lines
# @can_edit_base_research_line
def base_research_line_delete(
    request, rline_id, my_offices=None, rline=None, teachers=None
):
    """
    elimina linea di ricerca di base
    """
    # ha senso?
    # if rline.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    rline = get_object_or_404(RicercaLineaBase, pk=rline_id)
    rline.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Research line removed successfully")
    )
    return redirect("research-lines:management:base-research-lines")


@login_required
@can_manage_research_lines
@user_passes_test(lambda u: u.is_superuser)
# attualmente solo i superuser possono effetture l'operazione
# @can_manage_research_lines
# @can_edit_applied_research_line
def applied_research_lines_delete(
    request, rline_id, my_offices=None, rline=None, teachers=None
):
    """
    elimina linea di ricerca applicata
    """
    # ha senso?
    # if rline.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    rline = get_object_or_404(RicercaLineaApplicata, pk=rline_id)
    rline.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Research line removed successfully")
    )
    return redirect("research-lines:management:applied-research-lines")


@login_required
@can_manage_research_lines
@can_edit_base_research_line
def base_research_line_teacher_new(
    request, rline_id, my_offices=None, rline=None, teachers=None
):
    """
    nuovo docente linea di ricerca di base
    """
    form = RicercaDocenteLineaBaseForm()
    if request.POST:
        form = RicercaDocenteLineaBaseForm(data=request.POST)
        if form.is_valid():
            teacher_rline_id = decrypt(form.cleaned_data["choosen_person"])
            teacher = get_object_or_404(Personale, matricola=teacher_rline_id)
            RicercaDocenteLineaBase.objects.create(
                user_ins=request.user,
                ricerca_linea_base=rline,
                dt_inizio=form.cleaned_data["dt_inizio"],
                dt_fine=form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(
                user=request.user,
                obj=rline,
                flag=CHANGE,
                msg=f"Aggiunto nuovo docente {teacher}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Teacher added successfully")
            )
            return redirect(
                "research-lines:management:base-research-line-edit", rline_id=rline_id
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:base-research-lines"): _("Research lines"),
        reverse(
            "research-lines:management:base-research-line-edit", kwargs={"rline_id": rline_id}
        ): rline.descrizione,
        "#": _("New teacher"),
    }

    return render(
        request,
        "researchline_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rline": rline,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_lines
@can_edit_applied_research_line
def applied_researchline_teacher_new(
    request, rline_id, my_offices=None, rline=None, teachers=None
):
    """
    nuovo docente linea di ricerca applicata
    """
    form = RicercaDocenteLineaApplicataForm()
    if request.POST:
        form = RicercaDocenteLineaApplicataForm(data=request.POST)
        if form.is_valid():
            teacher_rline_id = decrypt(form.cleaned_data["choosen_person"])
            teacher = get_object_or_404(Personale, matricola=teacher_rline_id)
            RicercaDocenteLineaApplicata.objects.create(
                user_ins=request.user,
                ricerca_linea_applicata=rline,
                dt_inizio=form.cleaned_data["dt_inizio"],
                dt_fine=form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(
                user=request.user,
                obj=rline,
                flag=CHANGE,
                msg=f"Aggiunto nuovo docente {teacher}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Teacher added successfully")
            )
            return redirect(
                "research-lines:management:applied-research-line-edit", rline_id=rline_id
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:applied-research-lines"): _(
            "Research lines"
        ),
        reverse(
            "research-lines:management:applied-research-line-edit",
            kwargs={"rline_id": rline_id},
        ): rline.descrizione,
        "#": _("New teacher"),
    }

    return render(
        request,
        "researchline_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rline": rline,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_lines
@can_edit_base_research_line
def base_research_line_teacher_edit(
    request, rline_id, teacher_rline_id, my_offices=None, rline=None, teachers=None
):
    """
    modifica un docente della linea di ricerca di base
    """
    teacher_rline = get_object_or_404(
        RicercaDocenteLineaBase.objects.select_related("personale"), pk=teacher_rline_id
    )
    teacher = teacher_rline.personale
    teacher_matricola = encrypt(teacher.matricola)
    teacher_data = f"{teacher.nome} {teacher.cognome}"
    form = RicercaDocenteLineaBaseForm(
        instance=teacher_rline, initial={"choosen_person": teacher_matricola}
    )

    if request.POST:
        form = RicercaDocenteLineaBaseForm(instance=teacher_rline, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            teacher_rline_id = decrypt(form.cleaned_data["choosen_person"])
            new_teacher = get_object_or_404(Personale, matricola=teacher_matricola)
            teacher_rline.user_mod = request.user
            teacher_rline.personale = new_teacher
            teacher_rline.save()

            if teacher != new_teacher:
                log_msg = f"Sotituito docente {teacher} con {new_teacher}"
                log_action(
                    user=request.user, obj=teacher_rline, flag=CHANGE, msg=log_msg
                )

            messages.add_message(
                request, messages.SUCCESS, _("Teacher edited successfully")
            )
            return redirect(
                "research-lines:management:base-research-line-edit", rline_id=rline_id
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:base-research-lines"): _("Research lines"),
        reverse(
            "research-lines:management:base-research-line-edit", kwargs={"rline_id": rline_id}
        ): rline.descrizione,
        "#": teacher_data,
    }

    return render(
        request,
        "researchline_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rline": rline,
            "teacher_rline_id": teacher_rline_id,
            "choosen_person": teacher_data,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_lines
@can_edit_applied_research_line
def applied_researchline_teacher_edit(
    request, rline_id, teacher_rline_id, my_offices=None, rline=None, teachers=None
):
    """
    modifica un docente della linea di ricerca applicata
    """
    teacher_rline = get_object_or_404(
        RicercaDocenteLineaApplicata.objects.select_related("personale"),
        pk=teacher_rline_id,
    )
    teacher = teacher_rline.personale
    teacher_matricola = encrypt(teacher.matricola)
    teacher_data = f"{teacher.nome} {teacher.cognome}"
    form = RicercaDocenteLineaApplicataForm(
        instance=teacher_rline, initial={"choosen_person": teacher_matricola}
    )

    if request.POST:
        form = RicercaDocenteLineaApplicataForm(
            instance=teacher_rline, data=request.POST
        )
        if form.is_valid():
            form.save(commit=False)
            teacher_rline_id = decrypt(form.cleaned_data["choosen_person"])
            new_teacher = get_object_or_404(Personale, matricola=teacher_matricola)
            teacher_rline.user_mod = request.user
            teacher_rline.personale = new_teacher
            teacher_rline.save()

            if teacher != new_teacher:
                log_msg = f"Sotituito docente {teacher} con {new_teacher}"
                log_action(
                    user=request.user, obj=teacher_rline, flag=CHANGE, msg=log_msg
                )

            messages.add_message(
                request, messages.SUCCESS, _("Teacher edited successfully")
            )
            return redirect(
                "research-lines:management:applied-research-line-edit", rline_id=rline_id
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-lines:management:applied-research-lines"): _(
            "Research lines"
        ),
        reverse(
            "research-lines:management:applied-research-line-edit",
            kwargs={"rline_id": rline_id},
        ): rline.descrizione,
        "#": teacher_data,
    }

    return render(
        request,
        "researchline_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rline": rline,
            "teacher_rline_id": teacher_rline_id,
            "choosen_person": teacher_data,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_lines
@can_edit_base_research_line
def base_research_line_teacher_delete(
    request, rline_id, teacher_rline_id, my_offices=None, rline=None, teachers=None
):
    """
    elimina docente dalla linea di ricerca
    """
    teacher_rline = get_object_or_404(
        RicercaDocenteLineaBase.objects.select_related("personale"),
        ricerca_linea_base=rline,
        pk=teacher_rline_id,
    )

    # una linea di ricerca deve avere almeno un docente
    if RicercaDocenteLineaBase.objects.filter(ricerca_linea_base=rline).count() == 1:
        return custom_message(
            request, _("Operation not permitted. At least one teacher must be present")
        )

    log_action(
        user=request.user,
        obj=rline,
        flag=CHANGE,
        msg=f"Rimosso docente {teacher_rline.personale}",
    )

    teacher_rline.delete()

    messages.add_message(request, messages.SUCCESS, _("Teacher removed successfully"))
    return redirect("research-lines:management:base-research-line-edit", rline_id=rline_id)


@login_required
@can_manage_research_lines
@can_edit_applied_research_line
def applied_researchline_teacher_delete(
    request, rline_id, teacher_rline_id, my_offices=None, rline=None, teachers=None
):
    """
    elimina docente dalla linea di ricerca
    """
    teacher_rline = get_object_or_404(
        RicercaDocenteLineaApplicata.objects.select_related("personale"),
        ricerca_linea_applicata=rline,
        pk=teacher_rline_id,
    )

    # una linea di ricerca deve avere almeno un docente
    if (
        RicercaDocenteLineaApplicata.objects.filter(
            ricerca_linea_applicata=rline
        ).count()
        == 1
    ):
        return custom_message(
            request, _("Operation not permitted. At least one teacher must be present")
        )

    log_action(
        user=request.user,
        obj=rline,
        flag=CHANGE,
        msg=f"Rimosso docente {teacher_rline.personale}",
    )

    teacher_rline.delete()

    messages.add_message(request, messages.SUCCESS, _("Teacher removed successfully"))
    return redirect("research-lines:management:applied-research-line-edit", rline_id=rline_id)
