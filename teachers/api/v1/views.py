from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES

from teachers.api.v1.services import ServiceDocente

from rest_framework.schemas.openapi_agid import AgidAutoSchema

from .filters import (
    PublicationsListFilter,
    TeacherMaterialsAndNewsFilter,
    TeachersListFilter,
    TeacherStudyActivitiesFilter,
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
    description = "Retrieves a list of teachers that have an active coverage, together with a minimum set of identifying information."
    serializer_class = TeachersSerializer
    filter_backends = [TeachersListFilter]

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


class ApiTeachingCoveragesList(ApiEndpointList):
    description = "Retrieves a list of teachers that have fl_docente=1 e fl_cessato=0, together with a minimum set of identifying information."
    serializer_class = TeachersSerializer
    filter_backends = [TeachersListFilter]
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeachingCoverage")

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
        "Retrieves a list of research lines of a teacher ordered by type and name."
    )
    serializer_class = TeacherResearchLinesSerializer

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
    description = "Retrieves a list of courses (for the latest years) ordered by year and course name."
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [TeacherStudyActivitiesFilter]

    def get_queryset(self):
        request = self.request
        teacherid = self.kwargs["teacherid"]
        year = request.query_params.get("year")
        yearFrom = request.query_params.get("yearFrom")
        yearTo = request.query_params.get("yearTo")

        return ServiceDocente.getAttivitaFormativeByDocente(
            teacher=teacherid, year=year, yearFrom=yearFrom, yearTo=yearTo
        )


class ApiTeachingCoverageActivitiesList(ApiTeacherStudyActivitiesList):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeachingCoverageStudyActivities")
    pass


class ApiTeacherDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a teacher."
    serializer_class = TeacherInfoSerializer

    def get_queryset(self):
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteInfo(teacher=teacherid)


class ApiTeacherMaterials(ApiEndpointList):
    description = "Retrieves the teaching materials of a teacher."
    serializer_class = TeacherMaterialsSerializer
    filter_backends = [TeacherMaterialsAndNewsFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteMaterials(
            user=request.user, teacher=teacherid, search=search
        )


class ApiTeacherNews(ApiEndpointList):
    description = "Retrieves a list of news of a teacher."
    serializer_class = TeacherNewsSerializer
    filter_backends = [TeacherMaterialsAndNewsFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacherid = self.kwargs["teacherid"]
        return ServiceDocente.getDocenteNews(
            user=request.user, teacher=teacherid, search=search
        )


class ApiPublicationsList(ApiEndpointList):
    description = "Retrieves a list of publications of a teacher."
    serializer_class = PublicationsSerializer
    filter_backends = [PublicationsListFilter]

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


class ApiTeachingCoverageDetail(ApiTeacherDetail):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeachingCoverageInfo")
    pass

class ApiTeachingCoveragePublicationsList(ApiPublicationsList):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeachingCoveragePublication")
    pass

class ApiTeacherPublicationsList(ApiPublicationsList):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeacherPublication")
    pass

class ApiPublicationsCommunityTypesList(ApiEndpointList):
    description = "Retrieves a list of typologies of publications."
    serializer_class = PublicationsCommunityTypesSerializer

    def get_queryset(self):
        return ServiceDocente.getPublicationsCommunityTypesList()


class ApiPublicationDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a pubication."
    serializer_class = PublicationSerializer

    def get_queryset(self):
        publicationid = self.kwargs["publicationid"]

        return ServiceDocente.getPublication(publicationid)


class ApiTeacherPublicationDetail(ApiPublicationDetail):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeacherPublication")
    pass


class ApiTeachingCoveragePublicationDetail(ApiPublicationDetail):
    #schema = AgidAutoSchema(tags=['public'], operation_id_base="TeachingCoveragePublication")
    pass
