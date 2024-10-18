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
from research_groups.models import RicercaDocenteGruppo, RicercaGruppo
from research_groups.settings import OFFICE_RESEARCH_GROUPS

from .decorators import can_edit_research_group, can_manage_research_groups
from .forms import RicercaGruppoDocenteForm, RicercaGruppoForm

logger = logging.getLogger(__name__)


@login_required
@can_manage_research_groups
def researchgroups(request, my_offices=None):
    """
    lista dei gruppi di ricerca
    """
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Research groups"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("research-groups:apiv1:research-groups"),
    }
    return render(request, "researchgroups.html", context)


@login_required
@can_manage_research_groups
@can_edit_research_group
def researchgroup(request, rgroup_id, my_offices=None, rgroup=None, teachers=None):
    """
    dettaglio gruppo di ricerca con form di modifica
    """
    form = RicercaGruppoForm(instance=rgroup)
    if request.POST:
        form = RicercaGruppoForm(instance=rgroup, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            rgroup.user_mod = request.user
            rgroup.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=rgroup,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Research group edited successfully")
            )

            return redirect("research-groups:management:research-group-edit", rgroup_id=rgroup_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(rgroup).pk,
        object_id=rgroup.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-groups:management:research-groups"): _("Research groups"),
        "#": rgroup.nome,
    }

    return render(
        request,
        "researchgroup.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "logs": logs,
            "rgroup": rgroup,
            "teachers": teachers,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
# attualmente solo i superuser possono effetture l'operazione
# @can_manage_research_groups
# @can_edit_research_group
def researchgroup_delete(request, rgroup_id, my_offices=None, rgroup=None, teachers=None):
    """
    elimina gruppo di ricerca
    """
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    rgroup = get_object_or_404(RicercaGruppo, pk=rgroup_id)
    rgroup.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Research group removed successfully")
    )
    return redirect("research-groups:management:research-groups")


@login_required
@can_manage_research_groups
def researchgroup_new(request, my_offices=None):
    """
    nuovo gruppo di ricerca
    """
    # utilizziamo due form
    # uno per i dati del gruppo di ricerca e uno per il docente
    form = RicercaGruppoForm()
    teacher_form = RicercaGruppoDocenteForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque il docente scelto senza doverlo cercare
    # nuovamente dall'elenco
    teacher = None
    if request.POST.get("choosen_person", ""):
        teacher = get_object_or_404(
            Personale, matricola=(decrypt(request.POST["choosen_person"]))
        )

    if request.POST:
        form = RicercaGruppoForm(data=request.POST)
        teacher_form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid() and teacher_form.is_valid():
            # se l'utente non è un superuser
            # verifica che il docente inserito
            # afferisca alla sua stessa struttura
            if not request.user.is_superuser:
                structure_afforg = OrganizationalStructureOfficeEmployee.objects.filter(
                    employee=request.user,
                    office__name=OFFICE_RESEARCH_GROUPS,
                    office__is_active=True,
                    office__organizational_structure__is_active=True,
                    office__organizational_structure__unique_rgroup_id=teacher.cd_uo_aff_org_id,
                )
                if not structure_afforg:
                    raise Exception(_("Add a teacher belonging to your structure"))

            # crea il nuovo gruppo di ricerca
            rgroup = form.save(commit=False)
            rgroup.user_ins = request.user
            rgroup.save()

            # crea il nuovo docente da associare al gruppo
            RicercaDocenteGruppo.objects.create(
                user_ins=request.user,
                ricerca_gruppo=rgroup,
                dt_inizio=teacher_form.cleaned_data["dt_inizio"],
                dt_fine=teacher_form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(
                user=request.user, obj=rgroup, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request, messages.SUCCESS, _("Research group created successfully")
            )
            return redirect(
                "research-groups:management:research-group-edit", rgroup_id=rgroup.pk
            )
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
        reverse("research-groups:management:research-groups"): _("Research groups"),
        "#": _("New"),
    }

    return render(
        request,
        "researchgroup_new.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": f"{teacher.nome} {teacher.cognome}" if teacher else "",
            "form": form,
            "url": reverse("teachers:apiv1:teachers-list"),
            "teacher_form": teacher_form,
        },
    )


@login_required
@can_manage_research_groups
@can_edit_research_group
def researchgroup_teacher_new(
    request, rgroup_id, my_offices=None, rgroup=None, teachers=None
):
    """
    nuovo docente per il gruppo di ricerca
    """
    form = RicercaGruppoDocenteForm()
    if request.POST:
        form = RicercaGruppoDocenteForm(data=request.POST)
        if form.is_valid():
            teacher_rgroup_id = decrypt(form.cleaned_data["choosen_person"])
            teacher = get_object_or_404(Personale, matricola=teacher_rgroup_id)
            RicercaDocenteGruppo.objects.create(
                user_ins=request.user,
                ricerca_gruppo=rgroup,
                dt_inizio=form.cleaned_data["dt_inizio"],
                dt_fine=form.cleaned_data["dt_fine"],
                personale=teacher,
            )

            log_action(
                user=request.user,
                obj=rgroup,
                flag=CHANGE,
                msg=f"Aggiunto nuovo docente {teacher}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Teacher added successfully")
            )
            return redirect("research-groups:management:research-group-edit", rgroup_id=rgroup_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-groups:management:research-groups"): _("Research groups"),
        reverse(
            "research-groups:management:research-group-edit", kwargs={"rgroup_id": rgroup_id}
        ): rgroup.nome,
        "#": _("New teacher"),
    }

    return render(
        request,
        "researchgroup_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rgroup": rgroup,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_groups
@can_edit_research_group
def researchgroup_teacher_edit(
    request, rgroup_id, teacher_rgroup_id, my_offices=None, rgroup=None, teachers=None
):
    """
    modifica un docente del gruppo di ricerca
    """
    teacher_rgroup = get_object_or_404(
        RicercaDocenteGruppo.objects.select_related("personale"), pk=teacher_rgroup_id
    )
    teacher = teacher_rgroup.personale
    teacher_rgroup_id = encrypt(teacher.matricola)
    teacher_data = f"{teacher.nome} {teacher.cognome}"

    form = RicercaGruppoDocenteForm(
        instance=teacher_rgroup, initial={"choosen_person": teacher_rgroup_id}
    )

    if request.POST:
        form = RicercaGruppoDocenteForm(instance=teacher_rgroup, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            teacher_rgroup_id = decrypt(form.cleaned_data["choosen_person"])
            new_teacher = get_object_or_404(Personale, matricola=teacher_rgroup_id)
            teacher_rgroup.user_mod = request.user
            teacher_rgroup.personale = new_teacher
            teacher_rgroup.save()

            if teacher != new_teacher:
                log_msg = f"Sotituito docente {teacher} con {new_teacher}"
                log_action(user=request.user, obj=rgroup, flag=CHANGE, msg=log_msg)

            messages.add_message(
                request, messages.SUCCESS, _("Teacher edited successfully")
            )
            return redirect("research-groups:management:research-group-edit", rgroup_id=rgroup_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("research-groups:management:research-groups"): _("Research groups"),
        reverse(
            "research-groups:management:research-group-edit", kwargs={"rgroup_id": rgroup_id}
        ): rgroup.nome,
        "#": teacher_data,
    }

    return render(
        request,
        "researchgroup_teacher.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "rgroup": rgroup,
            "teacher_rgroup_id": teacher_rgroup_id,
            "choosen_person": teacher_data,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_research_groups
@can_edit_research_group
def researchgroup_teacher_delete(
    request, rgroup_id, teacher_rgroup_id, my_offices=None, rgroup=None, teachers=None
):
    """
    elimina un docente dal gruppo di ricerca
    """
    teacher_rgroup = get_object_or_404(
        RicercaDocenteGruppo.objects.select_related("personale"),
        ricerca_gruppo=rgroup,
        pk=teacher_rgroup_id,
    )

    # un gruppo di ricerca deve avere almeno un docente
    if RicercaDocenteGruppo.objects.filter(ricerca_gruppo=rgroup).count() == 1:
        return custom_message(
            request, _("Operation not permitted. At least one teacher must be present")
        )

    log_action(
        user=request.user,
        obj=rgroup,
        flag=CHANGE,
        msg=f"Rimosso docencte {teacher_rgroup.personale}",
    )

    teacher_rgroup.delete()

    messages.add_message(request, messages.SUCCESS, _("Teacher removed successfully"))
    return redirect("research-groups:management:research-group-edit", rgroup_id=rgroup_id)
