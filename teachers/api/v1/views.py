from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES
from rest_framework.schemas.openapi import AutoSchema
from teachers.api.v1.services import ServiceDocente

from .filters import (
    ApiPublicationsListFilter,
    ApiTeachersListFilter,
    ApiTeacherStudyActivitiesFilter,
)
from .serializers import (
    PublicationsCommunityTypesSerializer,
    PublicationSerializer,
    PublicationsSerializer,
    TeacherInfoSerializer,
    TeacherMaterialsSerializer,
    TeacherNewsSerializer,
    TeacherResearchLinesSerializer,
    TeachersSerializer,
    TeacherStudyActivitiesSerializer,
)


class ApiTeachersList(ApiEndpointList):
    description = (
        "Restituisce un elenco di Docenti che hanno una copertura attiva in ateneo, con un set minimo di "
        "informazioni identificative: Nome, Ruolo, "
        "Settore scientifico disciplinare, …"
    )
    serializer_class = TeachersSerializer
    filter_backends = [ApiTeachersListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        regdidid = request.query_params.get("regdid")
        department = request.query_params.get("department")
        role = request.query_params.get("role")
        cds = request.query_params.get("cds")
        year = request.query_params.get("year")

        return ServiceDocente.teachersList(
            search, regdidid, department, role, cds, year
        )


class TeachingCoveragesList(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "listTeachingCoverages" 
        return operation
    

class ApiTeachingCoveragesList(ApiEndpointList):
    description = (
        "Restituisce un elenco di Docenti con il fl_docente=1 e fl_cessato=0"
        "con un set minimo di informazioni identificative: Nome, Ruolo, "
        "Settore scientifico disciplinare, …"
    )
    serializer_class = TeachersSerializer
    filter_backends = [ApiTeachersListFilter]
    schema = TeachingCoveragesList()

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        regdidid = request.query_params.get("regdid")
        department = request.query_params.get("department")
        role = request.query_params.get("role")
        cds = request.query_params.get("cds")
        year = request.query_params.get("year")

        return ServiceDocente.teachingCoveragesList(
            search, regdidid, department, role, cds, year
        )


class ApiTeacherResearchLinesList(ApiEndpointList):
    description = (
        "La funzione restituisce l’elenco delle Linee di"
        " ricerca del docente ordinati "
        "per Tipo (applicata/di base) e Nome."
    )
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = []

    def get_queryset(self):
        teacherid = self.kwargs["teacherid"]
        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        request = self.request
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        return ServiceDocente.getResearchLines(
            teacher_id=teacherid, only_active=only_active
        )


class ApiTeacherStudyActivitiesList(ApiEndpointList):
    description = (
        "La funzione restituisce l’elenco degli insegnamenti"
        " (per gli ultimi anni) ordinati per anno e nome"
        " dell’insegnamento."
    )
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [ApiTeacherStudyActivitiesFilter]

    def get_queryset(self):
        request = self.request
        teacherid = self.kwargs["teacherid"]
        year = request.query_params.get("year")
        yearFrom = request.query_params.get("yearFrom")
        yearTo = request.query_params.get("yearTo")

        return ServiceDocente.getAttivitaFormativeByDocente(
            teacher=teacherid, year=year, yearFrom=yearFrom, yearTo=yearTo
        )


class TeachingCoverageStudyActivitiesList(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "listTeachingCoverageStudyActivities" 
        return operation
    

class ApiTeachingCoverageActivitiesList(ApiTeacherStudyActivitiesList):
    schema = TeachingCoverageStudyActivitiesList()


class ApiTeacherDetail(ApiEndpointDetail):
    description = (
        "La funzione restituisce la scheda informativa" " dettagliata di un docente"
    )
    serializer_class = TeacherInfoSerializer
    filter_backends = []

    def get_queryset(self):
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteInfo(teacher=teacherid)


class ApiTeacherMaterials(ApiEndpointList):
    description = "La funzione restituisce il materiale didattico di un docente"
    serializer_class = TeacherMaterialsSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteMaterials(
            user=request.user, teacher=teacherid, search=search
        )


class ApiTeacherNews(ApiEndpointList):
    description = "La funzione restituisce le news di un docente"
    serializer_class = TeacherNewsSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteNews(
            user=request.user, teacher=teacherid, search=search
        )


class TeachingCoveragesInfo(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "retrieveTeachingCoverageInfo" 
        return operation
    

class ApiTeachingCoverageDetail(ApiTeacherDetail):
    schema = TeachingCoveragesInfo()


class ApiPublicationsList(ApiEndpointList):
    description = (
        "La funzione restituisce la lista delle pubblicazioni di un dato docente"
    )
    serializer_class = PublicationsSerializer
    filter_backends = [ApiPublicationsListFilter]

    def get_queryset(self):
        request = self.request
        teacherid = self.kwargs.get("teacherid") or ""
        search = request.query_params.get("search")
        year = request.query_params.get("year")
        pub_type = request.query_params.get("type")
        structure = request.query_params.get("structure")
        return ServiceDocente.getPublicationsList(
            teacherid=teacherid,
            search=search,
            year=year,
            pub_type=pub_type,
            structure=structure,
        )


class TeachingCoveragePublicationsList(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "listTeachingCoveragePublications" 
        return operation
    

class ApiTeachingCoveragePublicationsList(ApiPublicationsList):
    schema = TeachingCoveragePublicationsList()


class TeacherPublicationsList(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "listTeacherPublications" 
        return operation
    

class ApiTeacherPublicationsList(ApiPublicationsList):
    schema = TeacherPublicationsList()


class ApiPublicationsCommunityTypesList(ApiEndpointList):
    description = "La funzione restituisce la lista delle tipologie di pubblicazioni"
    serializer_class = PublicationsCommunityTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDocente.getPublicationsCommunityTypesList()


class ApiPublicationDetail(ApiEndpointDetail):
    description = "La funzione restituisce il dettaglio di una pubblicazione"
    serializer_class = PublicationSerializer
    filter_backends = []

    def get_queryset(self):
        publicationid = self.kwargs["publicationid"]

        return ServiceDocente.getPublication(publicationid)


class TeacherPublicationDetail(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "retrieveTeacherPublication" 
        return operation
    

class ApiTeacherPublicationDetail(ApiPublicationDetail):
    schema = TeacherPublicationDetail()


class TeachingCoveragePublicationsDetail(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "retrieveTeachingCoveragePublication" 
        return operation
    

class ApiTeachingCoveragePublicationDetail(ApiPublicationDetail):
    schema = TeachingCoveragePublicationsDetail()
