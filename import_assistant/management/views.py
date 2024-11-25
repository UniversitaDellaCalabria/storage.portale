import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from import_assistant.exceptions import BaseImportError

from .forms import CdsImportForm, RegdidStructureImportForm
from .utils.cds_export_utils import gen_xlsx_for_cds_export
from .utils.cds_import_utils import handle_cds_import
from .utils.regdid_export_utils import gen_json_regdid_structures_for_export
from .utils.regdid_import_utils import handle_regdid_structures_import

logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    cds_import_form = CdsImportForm(
        request.POST if request.POST else None, request.FILES if request.FILES else None
    )
    regdid_structure_import_form = RegdidStructureImportForm(
        request.POST if request.POST else None
    )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Import assistant"),
    }

    return render(
        request,
        "import_assistant_dashboard.html",
        {
            "breadcrumbs": breadcrumbs,
            "cds_import_form": cds_import_form,
            "regdid_structure_import_form": regdid_structure_import_form,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cds_import(request):
    cds_import_form = CdsImportForm(
        request.POST if request.POST else None, request.FILES if request.FILES else None
    )

    if request.method == "POST":
        if cds_import_form.is_valid():
            excel_file = cds_import_form.cleaned_data["cds_list_file"]
            academic_year = int(cds_import_form.cleaned_data["year"])
            try:
                total_rows, skipped_rows = handle_cds_import(
                    request, excel_file, academic_year
                )
                imported_rows = total_rows - skipped_rows
                if imported_rows == total_rows:
                    messages.success(
                        request,
                        _("Imported {} rows out of {}").format(
                            imported_rows, total_rows
                        ),
                    )
                else:
                    messages.warning(
                        request,
                        _("Imported {} rows out of {}").format(
                            imported_rows, total_rows
                        ),
                    )
            except BaseImportError as e:
                logger.error(str(e))
                messages.error(request, str(e))
        else:
            for k, v in cds_import_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{cds_import_form.fields[k].label}</b>: {v}",
                )

    return redirect("import-assistant:management:dashboard")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cds_export(request):
    buffer = gen_xlsx_for_cds_export()

    response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="cds_import.xlsx"'
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def regdid_structure_import(request):
    regdid_structure_import_form = RegdidStructureImportForm(
        request.POST if request.POST else None
    )

    if request.method == "POST":
        if regdid_structure_import_form.is_valid():
            try:
                data = regdid_structure_import_form.cleaned_data["data"]
                year = int(regdid_structure_import_form.cleaned_data["year"])
                copy_previous = regdid_structure_import_form.cleaned_data[
                    "copy_previous"
                ]
                total_created, total_updated = handle_regdid_structures_import(
                    request, data, year, copy_previous
                )
                if total_created + total_updated == len(data):
                    messages.success(
                        request,
                        _("Done. Structures created {}, updated {} out of {}").format(
                            total_created, total_updated, len(data)
                        ),
                    )
                else:
                    messages.warning(
                        request,
                        _("Done. Structures created {}, updated {} out of {}").format(
                            total_created, total_updated, len(data)
                        ),
                    )
            except BaseImportError as e:
                logger.error(str(e))
                messages.error(request, str(e))
        else:
            for k, v in regdid_structure_import_form.errors.items():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"<b>{regdid_structure_import_form.fields[k].label}</b>: {v}",
                )

    return redirect("import-assistant:management:dashboard")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def regdid_structure_export(request):
    data = gen_json_regdid_structures_for_export()

    response = HttpResponse(data, content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="regdid_structure.json"'
    return response
