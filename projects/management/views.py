import datetime
import logging

from addressbook.models import Personale
from addressbook.utils import get_personale_matricola
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.forms import ChoosenPersonForm
from generics.settings import ALLOWED_STRUCTURE_TYPES, STRUCTURES_FATHER
from generics.utils import decrypt, encrypt, log_action
from projects.models import (
    ProgettoDatiBase,
    ProgettoResponsabileScientifico,
    ProgettoRicercatore,
)
from structures.models import UnitaOrganizzativa

from .decorators import can_manage_projects
from .forms import (
    ProgettoDatiBaseForm,
    ProgettoResponsabileScientificoForm,
    ProgettoRicercatoreForm,
    ProgettoStrutturaForm,
)

logger = logging.getLogger(__name__)


@login_required
@can_manage_projects
def projects(request):
    """
    lista dei progetti
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("Projects")}
    context = {"breadcrumbs": breadcrumbs, "url": reverse("projects:apiv1:projects")}
    return render(request, "projects.html", context)


@login_required
@can_manage_projects
# @can_edit_project
def project(request, project_id, project=None):
    """
    modifica dati progetto
    """
    form = ProgettoDatiBaseForm(instance=project)

    researchers = ProgettoRicercatore.objects.filter(progetto=project)
    scientific_directors = ProgettoResponsabileScientifico.objects.filter(
        progetto=project
    )

    structure_data = get_object_or_404(ProgettoDatiBase, pk=project_id)

    if request.POST:
        form = ProgettoDatiBaseForm(instance=project, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            project.user_mod = request.user
            project.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=project,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Project edited successfully")
            )

            return redirect("projects:management:project-edit", project_id=project_id)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(project).pk,
        object_id=project.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        "#": project.titolo,
    }

    return render(
        request,
        "project.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "logs": logs,
            "project": project,
            "researchers": researchers,
            "scientific_directors": scientific_directors,
            "structure_data": structure_data,
        },
    )


@login_required
@can_manage_projects
def project_new(request):
    """
    nuovo progetto
    """
    # tre form
    # dati progetto, direttore e struttura
    form = ProgettoDatiBaseForm()
    structure_form = ProgettoStrutturaForm()

    # se la validazione dovesse fallire ritroveremmo
    # comunque la struttura senza doverli cercare
    # nuovamente dall'elenco
    structure = None

    if request.POST.get("choosen_structure", ""):
        structure = get_object_or_404(
            UnitaOrganizzativa,
            uo=(request.POST["choosen_structure"]),
            dt_fine_val__gte=datetime.datetime.today(),
        )

    if request.POST:
        form = ProgettoDatiBaseForm(data=request.POST)
        structure_form = ProgettoStrutturaForm(data=request.POST)

        # se tutti i form sono validi
        if form.is_valid() and structure_form.is_valid():
            project = form.save(commit=False)
            # struttura del progetto
            project.uo = structure
            project.save()

            log_action(
                user=request.user, obj=project, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request, messages.SUCCESS, _("Project created successfully")
            )
            return redirect("projects:management:projects")

        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

            for k, v in structure_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{structure_form.fields[k].label}</b>: {v}",
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        "#": _("New"),
    }

    allowed_structures_types = ""
    if ALLOWED_STRUCTURE_TYPES:
        allowed_structures_types = ",".join(ALLOWED_STRUCTURE_TYPES)

    return render(
        request,
        "project_new.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_structure": f"{structure.denominazione}" if structure else "",
            "form": form,
            "structures_api": f'{reverse("structures:apiv1:structures-list")}?father={STRUCTURES_FATHER}&type={allowed_structures_types}',
            "structure_form": structure_form,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
# @can_manage_projects
# # @can_edit_project
def project_delete(request, project_id, project=None):
    # ha senso?
    # if rgroup.user_ins != request.user:
    # if not request.user.is_superuser:
    # raise Exception(_('Permission denied'))

    project = get_object_or_404(ProgettoDatiBase, pk=project_id)
    project.delete()
    messages.add_message(request, messages.SUCCESS, _("Project removed successfully"))

    return redirect("projects:management:projects")


@login_required
@can_manage_projects
# @can_edit_project
def project_director_new(request, project_id, project=None):
    """
    nuovo direttore scientifico
    """
    external_form = ProgettoResponsabileScientificoForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoResponsabileScientificoForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                director_project_id = get_personale_matricola(form.cleaned_data["choosen_person"])
                director = get_object_or_404(Personale, matricola=director_project_id)
                nome_origine = f"{director.cognome} {director.nome}"
            else:
                director = None
                nome_origine = form.cleaned_data["nome_origine"]

            p = ProgettoResponsabileScientifico.objects.create(
                progetto=project, matricola=director, nome_origine=nome_origine
            )

            log_action(
                user=request.user,
                obj=project,
                flag=CHANGE,
                msg=f"Aggiunto nuovo direttore scientifico {p}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Director added successfully")
            )
            return redirect("projects:management:project-edit", project_id=project_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        reverse(
            "projects:management:project-edit", kwargs={"project_id": project_id}
        ): project.titolo,
        "#": _("New director"),
    }

    return render(
        request,
        "project_director.html",
        {
            "breadcrumbs": breadcrumbs,
            "external_form": external_form,
            "internal_form": internal_form,
            "project": project,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_projects
# @can_edit_project
def project_director_edit(request, project_id, director_id, project=None):
    """
    dettaglio direttore scientifico
    """
    project_director = get_object_or_404(
        ProgettoResponsabileScientifico.objects.select_related("matricola"),
        pk=director_id,
        progetto=project,
    )
    old_label = project_director.nome_origine
    director = project_director.matricola
    initial = {}
    director_data = ""
    if director:
        director_data = f"{director.cognome} {director.nome}"
        initial = {"choosen_person": encrypt(director.matricola)}

    external_form = ProgettoResponsabileScientificoForm(instance=project_director)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoResponsabileScientificoForm(
            instance=project_director, data=request.POST
        )

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                director_project_id = get_personale_matricola(form.cleaned_data["choosen_person"])
                director = get_object_or_404(Personale, matricola=director_project_id)
                project_director.matricola = director
                project_director.nome_origine = f"{director.cognome} {director.nome}"
            else:
                project_director.matricola = None
                project_director.nome_origine = form.cleaned_data["nome_origine"]

            project_director.save()

            if old_label != project_director.nome_origine:
                log_action(
                    user=request.user,
                    obj=project,
                    flag=CHANGE,
                    msg=f"Sostituito direttore scientifico {old_label} con {project_director}",
                )

            messages.add_message(
                request, messages.SUCCESS, _("Director data edited successfully")
            )
            return redirect("projects:management:project-edit", project_id=project_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        reverse(
            "projects:management:project-edit", kwargs={"project_id": project_id}
        ): project.titolo,
        "#": f'{_("Director")} {project_director}',
    }

    return render(
        request,
        "project_director.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": director_data,
            "external_form": external_form,
            "internal_form": internal_form,
            "project": project,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_projects
# @can_edit_project
def project_director_delete(request, project_id, director_id, project=None):
    """
    elimina dati direttore scientifico
    """
    director_project = get_object_or_404(
        ProgettoResponsabileScientifico, pk=director_id, progetto=project
    )

    log_action(
        user=request.user,
        obj=project,
        flag=CHANGE,
        msg=f"Rimosso direttore scientifico {director_project}",
    )

    director_project.delete()
    messages.add_message(request, messages.SUCCESS, _("Director removed successfully"))
    return redirect("projects:management:project-edit", project_id=project_id)


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_new(request, project_id, project=None):
    """
    nuovo ricercatore
    """
    external_form = ProgettoRicercatoreForm()
    internal_form = ChoosenPersonForm(required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoRicercatoreForm(data=request.POST)

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                researcher_project_id = get_personale_matricola(form.cleaned_data["choosen_person"])
                researcher = get_object_or_404(Personale, matricola=researcher_project_id)
                nome_origine = f"{researcher.cognome} {researcher.nome}"
            else:
                researcher = None
                nome_origine = form.cleaned_data["nome_origine"]

            p = ProgettoRicercatore.objects.create(
                progetto=project, matricola=researcher, nome_origine=nome_origine
            )
            log_action(
                user=request.user,
                obj=project,
                flag=CHANGE,
                msg=f"Aggiunto nuovo ricercatore {p}",
            )

            messages.add_message(
                request, messages.SUCCESS, _("Researcher added successfully")
            )
            return redirect("projects:management:project-edit", project_id=project_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        reverse(
            "projects:management:project-edit", kwargs={"project_id": project_id}
        ): project.titolo,
        "#": _("New researcher"),
    }

    return render(
        request,
        "project_researcher.html",
        {
            "breadcrumbs": breadcrumbs,
            "external_form": external_form,
            "internal_form": internal_form,
            "project": project,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_edit(request, project_id, researcher_id, project=None):
    """
    dettaglio ricercatore
    """
    project_researcher = get_object_or_404(
        ProgettoRicercatore.objects.select_related("matricola"),
        pk=researcher_id,
        progetto=project,
    )
    old_label = project_researcher.nome_origine
    researcher = project_researcher.matricola
    initial = {}
    researcher_data = ""
    if researcher:
        researcher_data = f"{researcher.cognome} {researcher.nome}"
        initial = {"choosen_person": encrypt(researcher.matricola)}

    external_form = ProgettoRicercatoreForm(instance=project_researcher)
    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        external_form = ProgettoRicercatoreForm(
            instance=project_researcher, data=request.POST
        )

        if "choosen_person" in request.POST:
            form = internal_form
        else:
            form = external_form

        if form.is_valid():
            if form.cleaned_data.get("choosen_person"):
                researcher_project_id = get_personale_matricola(form.cleaned_data["choosen_person"])
                researcher = get_object_or_404(Personale, matricola=researcher_project_id)
                project_researcher.matricola = researcher
                project_researcher.nome_origine = (
                    f"{researcher.cognome} {researcher.nome}"
                )
            else:
                project_researcher.matricola = None
                project_researcher.nome_origine = form.cleaned_data["nome_origine"]

            project_researcher.save()

            if old_label != project_researcher.nome_origine:
                log_action(
                    user=request.user,
                    obj=project,
                    flag=CHANGE,
                    msg=f"Sostituito ricercatore {old_label} con {project_researcher}",
                )

            messages.add_message(
                request, messages.SUCCESS, _("Researcher data edited successfully")
            )
            return redirect("projects:management:project-edit", project_id=project_id)
        else:
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        reverse(
            "projects:management:project-edit", kwargs={"project_id": project_id}
        ): project.titolo,
        "#": f'{_("Researcher")} {project_researcher}',
    }

    return render(
        request,
        "project_researcher.html",
        {
            "breadcrumbs": breadcrumbs,
            "choosen_person": researcher_data,
            "external_form": external_form,
            "internal_form": internal_form,
            "project": project,
            "url": reverse("teachers:apiv1:teachers-list"),
        },
    )


@login_required
@can_manage_projects
# @can_edit_project
def project_researcher_delete(request, project_id, researcher_id, project=None):
    """
    elimina ricercatore
    """
    researcher = get_object_or_404(
        ProgettoRicercatore, pk=researcher_id, progetto=project
    )

    log_action(
        user=request.user,
        obj=project,
        flag=CHANGE,
        msg=f"Rimosso ricercatore {researcher}",
    )

    researcher.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Researcher removed successfully")
    )
    return redirect("projects:management:project-edit", project_id=project_id)


@login_required
@can_manage_projects
# @can_edit_project
def project_structure_data_edit(request, project_id, data_id, project=None):
    """
    modifica struttura
    """
    structure_project = get_object_or_404(
        ProgettoDatiBase.objects.select_related("uo"), pk=data_id
    )

    structure = structure_project.uo
    form = ProgettoStrutturaForm(initial={"choosen_structure": structure.uo})

    if request.POST:
        form = ProgettoStrutturaForm(data=request.POST)
        if form.is_valid():
            structure_project_id = form.cleaned_data["choosen_structure"]
            new_structure = get_object_or_404(
                UnitaOrganizzativa,
                uo=structure_project_id,
                dt_fine_val__gte=datetime.datetime.today(),
            )
            structure_project.user_mod = request.user
            structure_project.uo = new_structure
            structure_project.save()

            if structure != new_structure:
                log_action(
                    user=request.user,
                    obj=project,
                    flag=CHANGE,
                    msg=f"Sostituita struttura {structure} con {new_structure}",
                )

            messages.add_message(
                request, messages.SUCCESS, _("Structure edited successfully")
            )

            return redirect("projects:management:project-edit", project_id=project_id)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("projects:management:projects"): _("Projects"),
        reverse(
            "projects:management:project-edit", kwargs={"project_id": project_id}
        ): project.titolo,
        "#": _("Structure"),
    }

    allowed_structures_types = ""
    if ALLOWED_STRUCTURE_TYPES:
        allowed_structures_types = ",".join(ALLOWED_STRUCTURE_TYPES)

    return render(
        request,
        "project_structure.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "project": project,
            "choosen_structure": structure.denominazione,
            "url": f'{reverse("structures:apiv1:structures-list")}?father={STRUCTURES_FATHER}&type={allowed_structures_types}',
        },
    )
