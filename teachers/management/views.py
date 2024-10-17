import datetime
import logging

from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from generics.utils import encrypt, log_action
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaAltriDati,
    DocentePtaBacheca,
)

from .decorators import can_edit_teacher, can_manage_teachers
from .forms import (
    DocenteMaterialeDidatticoForm,
    DocentePtaAltriDatiForm,
    DocentePtaBachecaForm,
)

logger = logging.getLogger(__name__)


@login_required
@can_manage_teachers
def teachers(request, my_offices=None, my_teacher_profile=None):
    """
    lista dei docenti
    """
    breadcrumbs = {reverse("generics:dashboard"): _("Dashboard"), "#": _("Teachers")}
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("teachers:apiv1:teachers-list"),
    }
    return render(request, "teachers.html", context)


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_detail(
    request, code, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    pagina dettaglio singolo docente
    """
    # dati docente
    other_data = DocentePtaAltriDati.objects.filter(matricola=teacher.matricola).first()

    # bacheca
    board = DocentePtaBacheca.objects.filter(matricola=teacher.matricola)

    # materiale didattico
    materials = DocenteMaterialeDidattico.objects.filter(matricola=teacher.matricola)

    logs = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(teacher).pk,
        object_id=teacher.pk,
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        "#": teacher,
    }

    m = encrypt(teacher.matricola)

    return render(
        request,
        "teacher_detail.html",
        {
            "board": board,
            "breadcrumbs": breadcrumbs,
            "code": code,
            "logs": logs,
            "other_data": other_data,
            "materials": materials,
            "teacher": teacher,
            "url_news": reverse("teachers:apiv1:teacher-news", kwargs={"teacherid": m}),
            "url_books": reverse(
                "teachers:apiv1:teacher-materials", kwargs={"teacherid": m}
            ),
        },
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_edit(
    request, code, data_id, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    modifica dati docente
    """
    other_data = get_object_or_404(DocentePtaAltriDati, pk=data_id, matricola=teacher)

    form = DocentePtaAltriDatiForm(instance=other_data)

    if request.POST:
        form = DocentePtaAltriDatiForm(
            instance=other_data, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save(commit=False)
            other_data.user_mod = request.user
            other_data.dt_mod = datetime.datetime.now()
            other_data.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=teacher,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Other data edited successfully")
            )

            return redirect("teachers:management:teacher-edit", code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("Edit data"),
    }

    return render(
        request,
        "teacher_other_data.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "teacher": teacher,
            "other_data": other_data,
        },
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_new(
    request, code, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    nuovo set di dati
    """
    other_data = DocentePtaAltriDati.objects.filter(matricola=teacher)

    if other_data:
        raise Exception(_("Other data set already existent for this teacher"))

    form = DocentePtaAltriDatiForm()

    if request.POST:
        form = DocentePtaAltriDatiForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.matricola = teacher
            data.user_mod = request.user
            data.dt_mod = datetime.datetime.now()
            data.save()

            log_action(
                user=request.user, obj=teacher, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Teacher other data set created successfully"),
            )
            return redirect(
                "teachers:management:teacher-edit",
                code=code,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("New data set"),
    }

    return render(
        request,
        "teacher_other_data_new.html",
        {"breadcrumbs": breadcrumbs, "form": form, "teacher": teacher},
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_other_data_delete(
    request,
    code,
    data_id,
    my_offices=None,
    teacher=None,
    materials=None,
    other_data=None,
    board=None,
    my_teacher_profile=None,
):
    """
    elimina set dati
    """
    other_data = get_object_or_404(DocentePtaAltriDati, pk=data_id, matricola=teacher)

    log_action(
        user=request.user, obj=teacher, flag=CHANGE, msg=f'{_("Deleted other data")}'
    )

    other_data.delete()

    messages.add_message(
        request, messages.SUCCESS, _("Teachers other data removed successfully")
    )
    return redirect("teachers:management:teacher-edit", code=code)


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_edit(
    request,
    code,
    data_id,
    my_offices=None,
    teacher=None,
    materials=None,
    other_data=None,
    board=None,
    my_teacher_profile=None,
):
    """
    modifica news bacheca
    """
    board = get_object_or_404(DocentePtaBacheca, pk=data_id, matricola=teacher)

    form = DocentePtaBachecaForm(instance=board)

    if request.POST:
        form = DocentePtaBachecaForm(instance=board, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            board.user_mod = request.user
            board.dt_mod = datetime.datetime.now()
            board.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=teacher,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request, messages.SUCCESS, _("Board data edited successfully")
            )

            return redirect("teachers:management:teacher-edit", code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("Edit board data"),
    }

    return render(
        request,
        "teacher_board_data.html",
        {"breadcrumbs": breadcrumbs, "form": form, "teacher": teacher, "board": board},
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_new(
    request, code, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    nuova news bacheca
    """
    form = DocentePtaBachecaForm()

    if request.POST:
        form = DocentePtaBachecaForm(data=request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.matricola = teacher
            board.user_mod = request.user
            board.dt_mod = datetime.datetime.now()
            board.dt_pubblicazione = datetime.datetime.now()
            board.save()

            log_action(
                user=request.user, obj=teacher, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Teacher board data set created successfully"),
            )
            return redirect(
                "teachers:management:teacher-edit",
                code=code,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("New board data"),
    }

    return render(
        request,
        "teacher_board_data_new.html",
        {"breadcrumbs": breadcrumbs, "form": form, "teacher": teacher},
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_board_data_delete(
    request, code, data_id, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    elimina news bacheca
    """
    board = get_object_or_404(DocentePtaBacheca, pk=data_id, matricola=teacher)

    board.delete()

    log_action(
        user=request.user, obj=teacher, flag=CHANGE, msg=f'{_("Deleted board data")}'
    )

    messages.add_message(
        request, messages.SUCCESS, _("Teachers board data removed successfully")
    )
    return redirect("teachers:management:teacher-edit", code=code)


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_edit(
    request, code, data_id, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    modifica materiale didattico
    """
    material = get_object_or_404(
        DocenteMaterialeDidattico, pk=data_id, matricola=teacher
    )

    form = DocenteMaterialeDidatticoForm(instance=material)

    if request.POST:
        form = DocenteMaterialeDidatticoForm(instance=material, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            material.user_mod = request.user
            material.dt_mod = datetime.datetime.now()
            material.save()

            if form.changed_data:
                changed_field_labels = _get_changed_field_labels_from_form(
                    form, form.changed_data
                )

                log_action(
                    user=request.user,
                    obj=teacher,
                    flag=CHANGE,
                    msg=[{"changed": {"fields": changed_field_labels}}],
                )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Teaching material data edited successfully"),
            )

            return redirect("teachers:management:teacher-edit", code=code)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("Teaching material data"),
    }

    return render(
        request,
        "teacher_materials_data.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "teacher": teacher,
            "materials": material,
        },
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_new(
    request, code, my_offices=None, teacher=None, my_teacher_profile=None
):
    """
    nuovo materiale didattico
    """
    form = DocenteMaterialeDidatticoForm()

    if request.POST:
        form = DocenteMaterialeDidatticoForm(data=request.POST)

        if form.is_valid():
            material = form.save(commit=False)
            material.matricola = teacher
            material.user_mod = request.user
            material.dt_mod = datetime.datetime.now()
            material.dt_pubblicazione = datetime.datetime.now()
            material.save()

            log_action(
                user=request.user, obj=teacher, flag=ADDITION, msg=[{"added": {}}]
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Teacher materials data set created successfully"),
            )
            return redirect(
                "teachers:management:teacher-edit",
                code=code,
            )
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(
                    request, messages.ERROR, f"<b>{form.fields[k].label}</b>: {v}"
                )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("teachers:management:teachers"): _("Teachers"),
        reverse("teachers:management:teacher-edit", kwargs={"code": code}): teacher,
        "#": _("New teaching material"),
    }

    return render(
        request,
        "teacher_materials_data_new.html",
        {"breadcrumbs": breadcrumbs, "form": form, "teacher": teacher},
    )


@login_required
@can_manage_teachers
@can_edit_teacher
def teacher_materials_data_delete(
    request,
    code,
    data_id,
    my_offices=None,
    teacher=None,
    materials=None,
    other_data=None,
    board=None,
    my_teacher_profile=None,
):
    """
    elimina materiale didattico
    """
    material = get_object_or_404(
        DocenteMaterialeDidattico, pk=data_id, matricola=teacher
    )

    material.delete()

    log_action(
        user=request.user,
        obj=teacher,
        flag=CHANGE,
        msg=f'{_("Deleted teacher materials data")}',
    )

    messages.add_message(
        request, messages.SUCCESS, _("Teachers materials data removed successfully")
    )
    return redirect("teachers:management:teacher-edit", code=code)
