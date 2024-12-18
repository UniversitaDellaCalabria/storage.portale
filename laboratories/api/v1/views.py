from addressbook.models import Personale
from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.api.v1.serializers import (
    Asters1Serializer,
    Asters2Serializer,
    Erc0Serializer,
    Erc1Serializer,
    Erc2Serializer,
)
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from structures.api.v1.serializers import InfrastructuresSerializer

from laboratories.models import LaboratorioDatiBase
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS

from .filters import LaboratoriesListFilter
from .serializers import (
    LaboratoriesAreasSerializer,
    LaboratoriesScopesSerializer,
    LaboratoriesSerializer,
    LaboratoryDetailSerializer,
)
from .services import ServiceLaboratorio


class ApiLaboratoryDetail(ApiEndpointDetail):
    description = "Retrieves the detail of a specific laboratory."
    serializer_class = LaboratoryDetailSerializer
    #schema = AgidAutoSchema(tags=["public"], operation_id_base="Laboratory")

    def get_queryset(self):
        laboratoryid = self.kwargs["laboratoryid"]
        request = self.request

        # CRUD
        only_active = True
        if request.user.is_superuser:
            only_active = False  # pragma: no cover

        elif request.user.is_authenticated:  # pragma: no cover
            user_profile = None
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(
                    cod_fis=request.user.taxpayer_id
                ).first()

            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )

            is_scientific_director = (
                user_profile is not None
                and LaboratorioDatiBase.objects.filter(
                    matricola_responsabile_scientifico=user_profile
                ).exists()
            )
            is_operator = offices.filter(office__name=OFFICE_LABORATORIES).exists()
            is_validator = offices.filter(
                office__name=OFFICE_LABORATORY_VALIDATORS
            ).exists()
            if is_operator or is_validator or is_scientific_director:
                only_active = False

        return ServiceLaboratorio.getLaboratory(
            self.language, laboratoryid, only_active
        )


class ApiLaboratoriesList(ApiEndpointList):
    description = "Retrieves a list of laboratories."
    serializer_class = LaboratoriesSerializer
    filter_backends = [LaboratoriesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        area = request.query_params.get("area")
        department = request.query_params.get("department")
        erc1 = request.query_params.get("erc1")
        teacher = request.query_params.get("teacher")
        infrastructure = request.query_params.get("infrastructure")
        scope = request.query_params.get("scope")
        teacher = request.query_params.get("teacher")

        # CRUD
        only_active = True
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        elif request.user.is_authenticated:  # pragma: no cover
            user_profile = None
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(
                    cod_fis=request.user.taxpayer_id
                ).first()

            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )

            is_scientific_director = (
                user_profile is not None
                and LaboratorioDatiBase.objects.filter(
                    matricola_responsabile_scientifico=user_profile
                ).exists()
            )
            is_operator = offices.filter(office__name=OFFICE_LABORATORIES).exists()
            is_validator = offices.filter(
                office__name=OFFICE_LABORATORY_VALIDATORS
            ).exists()
            if is_operator or is_validator or is_scientific_director:
                only_active = False

        return ServiceLaboratorio.getLaboratoriesList(
            language=self.language,
            search=search,
            ambito=area,
            dip=department,
            erc1=erc1,
            teacher=teacher,
            infrastructure=infrastructure,
            scope=scope,
            is_active=only_active,
        )


class ApiLaboratoriesAreasList(ApiEndpointList):
    description = "Retrieves a list of research areas of the laboratories."
    serializer_class = LaboratoriesAreasSerializer

    def get_queryset(self):
        return ServiceLaboratorio.getLaboratoriesAreasList()


class ApiErc0List(ApiEndpointList):
    description = "Retrieves a list of top-level ERC classifications, which represent broad scientific areas."
    serializer_class = Erc0Serializer

    def get_queryset(self):
        return ServiceLaboratorio.getErc0List()


class ApiErc1List(ApiEndpointList):
    description = "Retrieves a list of second-level ERC classifications, which provide more detailed categories within the broad areas defined by ERC0."
    serializer_class = Erc1Serializer

    def get_queryset(self):
        return ServiceLaboratorio.getErc1List()


class ApiErc2List(ApiEndpointList):
    description = "Retrieves a list of third-level ERC classifications, which offer specific scientific topics within the detailed ERC1 categories."
    serializer_class = Erc2Serializer

    def get_queryset(self):
        return ServiceLaboratorio.getErc2List()


class ApiAster1List(ApiEndpointList):
    description = "Retrieves a list of broad research sectors."
    serializer_class = Asters1Serializer

    def get_queryset(self):
        return ServiceLaboratorio.getAster1List()


class ApiAster2List(ApiEndpointList):
    description = "Retrieves a list of specific research and innovation areas."
    serializer_class = Asters2Serializer

    def get_queryset(self):
        return ServiceLaboratorio.getAster2List()


class ApiLaboratoriesScopesList(ApiEndpointList):
    description = "Retrieves a list of scopes of the laboratories."
    serializer_class = LaboratoriesScopesSerializer

    def get_queryset(self):
        return ServiceLaboratorio.getScopes()


class ApiInfrastructuresList(ApiEndpointList):
    description = "Retrieves a list of infrastructures of the laboratories."
    serializer_class = InfrastructuresSerializer

    def get_queryset(self):
        return ServiceLaboratorio.getInfrastructures()
