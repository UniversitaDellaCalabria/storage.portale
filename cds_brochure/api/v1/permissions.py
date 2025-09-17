from rest_framework.permissions import BasePermission

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ...models import CdsBrochure
from ...settings import BROCHURES_VISIBLE, OFFICE_CDS_BROCHURE


class BrochureVisibilityPermission(BasePermission):
    def has_permission(self, request, view):
        if BROCHURES_VISIBLE: return True
        if not request.user.is_authenticated: return False
        if request.user.is_superuser: return True
        belongs_to_office = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_CDS_BROCHURE,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        ).exists()
        return belongs_to_office
