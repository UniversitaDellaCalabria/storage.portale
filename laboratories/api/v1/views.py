from addressbook.models import Personale
from generics.views import ApiEndpointDetail, ApiEndpointList
from laboratories.models import LaboratorioDatiBase
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.api.v1.serializers import (
    Asters1Serializer,
    Asters2Serializer,
    Erc0Serializer,
    Erc1Serializer,
    Erc2Serializer,
)
from structures.api.v1.serializers import InfrastructuresSerializer

from .filters import ApiLaboratoriesListFilter
from .serializers import (
    LaboratoriesAreasSerializer,
    LaboratoriesScopesSerializer,
    LaboratoriesSerializer,
    LaboratoryDetailSerializer,
)
from .services import ServiceLaboratorio


class ApiLaboratoryDetail(ApiEndpointDetail):
    description = "La funzione restituisce un laboratorio specifico"
    serializer_class = LaboratoryDetailSerializer
    # filter_backends = [ApiAddressbookListFilter]

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
    description = "La funzione restituisce i laboratori"
    serializer_class = LaboratoriesSerializer
    filter_backends = [ApiLaboratoriesListFilter]

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
    description = "La funzione restituisce la lista degli ambiti dei laboratori"
    serializer_class = LaboratoriesAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getLaboratoriesAreasList()


class ApiErc1List(ApiEndpointList):
    description = "La funzione restituisce la lista degli erc1"
    serializer_class = Erc1Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getErc1List()


class ApiErc2List(ApiEndpointList):
    description = "La funzione restituisce la lista degli erc2"
    serializer_class = Erc2Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getErc2List()


class ApiErc0List(ApiEndpointList):
    description = "La funzione restituisce la lista degli erc0"
    serializer_class = Erc0Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getErc0List()


class ApiAster1List(ApiEndpointList):
    description = "La funzione restituisce la lista degli aster1"
    serializer_class = Asters1Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getAster1List()


class ApiAster2List(ApiEndpointList):
    description = "La funzione restituisce la lista degli aster2"
    serializer_class = Asters2Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getAster2List()


class ApiLaboratoriesScopesList(ApiEndpointList):
    description = "La funzione restituisce la lista delle finalità dei laboratori"
    serializer_class = LaboratoriesScopesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getScopes()


class ApiInfrastructuresList(ApiEndpointList):
    description = "La funzione restituisce la lista delle infrastrutture di riferimento"
    serializer_class = InfrastructuresSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getInfrastructures()
