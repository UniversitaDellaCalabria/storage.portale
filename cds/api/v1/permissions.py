from rest_framework.permissions import BasePermission

from organizational_area.models import OrganizationalStructureOfficeEmployee

from cds_brochure.settings import BROCHURES_CURRENT_YEAR
from generics.settings import CURRENT_YEAR
from regdid.settings import OFFICE_REGDIDS_DEPARTMENT, OFFICE_REGDIDS_REVISION, OFFICE_REGDIDS_APPROVAL
from ...settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM


class CdsListVisibilityPermission(BasePermission):
    def has_permission(self, request, view):
        academic_year = request.query_params.get("academicyear")
        max_year_to_check = max(int(CURRENT_YEAR), int(BROCHURES_CURRENT_YEAR))
        if academic_year and int(academic_year) > max_year_to_check:
            if not request.user.is_authenticated: return False
            if request.user.is_superuser: return True
            belongs_to_office = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name__in=[
                    OFFICE_CDS,
                    OFFICE_CDS_DOCUMENTS,
                    OFFICE_CDS_TEACHING_SYSTEM,
                    OFFICE_REGDIDS_DEPARTMENT,
                    OFFICE_REGDIDS_REVISION,
                    OFFICE_REGDIDS_APPROVAL
                ],
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).exists()
            return belongs_to_office
        return True
