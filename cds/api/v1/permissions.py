from rest_framework.permissions import BasePermission

from organizational_area.models import OrganizationalStructureOfficeEmployee

from generics.settings import CURRENT_YEAR

from ...settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM


class CdsVisibilityPermission(BasePermission):
    def has_permission(self, request, view):
        academic_year = request.query_params.get("academicyear")
        if academic_year and academic_year > CURRENT_YEAR:
            if not request.user.is_authenticated: return False
            if request.user.is_superuser: return True
            belongs_to_office = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name__in=[
                    OFFICE_CDS,
                    OFFICE_CDS_DOCUMENTS,
                    OFFICE_CDS_TEACHING_SYSTEM
                ],
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).exists()
            return belongs_to_office
        return True
