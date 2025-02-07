from addressbook.api.v1.serializers import SortingContactsSerializer
from django.utils.text import slugify
from generics.utils import decrypt
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from rest_framework.views import APIView

from cds.settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM

from .filters import (
    AllActivitiesListFilter,
    CdsExpiredFilter,
    CdsListFilter,
)
from .permissions import CdsListVisibilityPermission
from .schemas import ApiStudyActivityDetailSchema
from .serializers import (
    AcademicYearsSerializer,
    CdsAreasSerializer,
    CdsExpiredSerializer,
    CdsInfoSerializer,
    CdSSerializer,
    CdsStudyPlansActivitiesSerializer,
    CdSStudyPlanSerializer,
    CdSStudyPlansSerializer,
    DegreeTypesSerializer,
    StudyActivitiesSerializer,
    StudyActivityInfoSerializer,
)
from .services import ServiceDidatticaAttivitaFormativa, ServiceDidatticaCds


class ApiCdSList(ApiEndpointList):
    description = """
        Retrieves a list of courses of study with a minimal set of information.
        Operates on 'DIDATTICA_REGOLAMENTO' and returns records
        ordered by course of study name, in the selected language
        (if not specified, data is returned in English
        or, if not available, in Italian for foreign languages).
        If no academicyear is specified, only the courses of study with
        an active didactic regulation are returned."""

    serializer_class = CdSSerializer
    filter_backends = [CdsListFilter]
    permission_classes = [CdsListVisibilityPermission]

    def get_queryset(self):
        return ServiceDidatticaCds.cdslist(self.language, self.request.query_params)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cache_key = f"cdslist_{self.language}_{slugify(self.request.query_params)}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiCdSInfo(ApiEndpointDetail):
    description = """
        Retrieves information about a specific course of study contained in the 'DIDATTICA_REGOLAMENTO'
        and 'DIDATTICA_TESTI_REGOLAMENTO' tables, in the specified language. If the data is not
        available in the selected language, it returns the information in English or, if not available, in Italian."""

    serializer_class = CdsInfoSerializer

    def get_queryset(self):
        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name__in=[
                    OFFICE_CDS,
                    OFFICE_CDS_DOCUMENTS,
                    OFFICE_CDS_TEACHING_SYSTEM,
                ],
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).exists()
            if my_offices:
                only_active = False

        return ServiceDidatticaCds.cds(
            self.language, self.kwargs["regdidid"], only_active
        )


class ApiCdSStudyPlansList(ApiEndpointList):
    description = "Retrieves a list of study plans."
    serializer_class = CdSStudyPlansSerializer

    def get_queryset(self):
        regdid_id = str(self.kwargs["regdidid"])
        return ServiceDidatticaAttivitaFormativa.getStudyPlans(regdid_id=regdid_id)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        regdid_id = str(self.kwargs["regdidid"])
        cache_key = f"cdsstudyplans_{self.language}__{regdid_id}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiStudyPlanDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a specific study plan."
    serializer_class = CdSStudyPlanSerializer

    def get_queryset(self):
        studyplanid = str(self.kwargs["studyplanid"])

        return ServiceDidatticaAttivitaFormativa.getStudyPlan(studyplanid=studyplanid)


class ApiStudyPlanActivitiesList(ApiEndpointList):
    description = "Retrieves a list of courses in a study plan with brief information."
    serializer_class = CdsStudyPlansActivitiesSerializer

    def get_queryset(self):
        studyplanid = str(self.kwargs["studyplanid"])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid
        )


class ApiAllStudyActivitiesList(ApiEndpointList):
    description = "Retrieves a list of courses with brief information."
    serializer_class = StudyActivitiesSerializer
    filter_backends = [AllActivitiesListFilter]

    def get_queryset(self):
        request = self.request
        department = request.query_params.get("department")
        cds = request.query_params.get("cds")
        academic_year = request.query_params.get("academic_year")
        period = request.query_params.get("period")
        ssd = request.query_params.get("ssd")
        teaching = request.query_params.get("teaching")
        teacher = request.query_params.get("teacher")
        course_year = request.query_params.get("course_year")
        cds_cod = request.query_params.get("cds_cod")
        teacher_code = decrypt(request.query_params.get("teacher_code"))

        return ServiceDidatticaAttivitaFormativa.getAllActivities(
            self.language,
            department,
            cds,
            academic_year,
            period,
            ssd,
            teacher,
            teaching,
            course_year,
            cds_cod,
            teacher_code,
        )


class ApiStudyActivityDetail(ApiEndpointDetail):
    description = "Retrieves detailed information about a specific course."
    serializer_class = StudyActivityInfoSerializer
    schema = ApiStudyActivityDetailSchema(tags=["public"])

    def get_queryset(self):
        studyactivityid = str(self.kwargs["studyactivityid"])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language
        )


class ApiDegreeTypesList(ApiEndpointList):
    description = "Retrieves the list of degree types."
    serializer_class = DegreeTypesSerializer

    def get_queryset(self):
        return ServiceDidatticaCds.getDegreeTypes()


class ApiAcademicYearsList(ApiEndpointListSupport):
    description = "Retrieves the list of academic years."
    serializer_class = AcademicYearsSerializer

    def get_queryset(self):
        return ServiceDidatticaCds.getAcademicYears()


class ApiCdsAreasList(ApiEndpointListSupport):
    description = "Retrieves the list of course of study areas."
    serializer_class = CdsAreasSerializer

    def get_queryset(self):
        return ServiceDidatticaCds.getCdsAreas()

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cache_key = "cdsareas"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiSortingContacts(ApiEndpointList):
    description = "Retrieves a list of teachers belonging to a course of study, along with department and office information."
    serializer_class = SortingContactsSerializer

    def get_queryset(self):
        cdscod = self.kwargs["cdscod"]
        return ServiceDidatticaCds.getContacts(cdscod)


class ApiCdsMorphList(APIView):
    permission_classes = [permissions.AllowAny]
    schema = AgidAutoSchema(tags=["api"])

    description = "Retrieves a list of CDS_COD which contains all the previous CDS_COD."

    def get(self, request, *args, **kwargs):
        return Response(ServiceDidatticaCds.getPreviousCdsCods())


class ApiCdsMorphDetail(APIView):
    permission_classes = [permissions.AllowAny]
    schema = AgidAutoSchema(tags=["api"])

    description = "Retrieves a list of CDS_COD which, starting from the given one, contains all the previous CDS_COD."

    def get(self, request, *args, **kwargs):
        cds_cod = kwargs.get("cds_cod", None)
        return Response(ServiceDidatticaCds.getPreviousSingleCdsCods(cds_cod))


class ApiCdsExpired(ApiEndpointList):
    description = "Retrieves the cds which have expired."
    serializer_class = CdsExpiredSerializer
    filter_backends = [CdsExpiredFilter]

    def get_queryset(self):
        yearfrom = self.request.query_params.get("yearfrom", None)
        coursetypes = self.request.query_params.get("coursetypes", None)
        return ServiceDidatticaCds.getExpiredCds(
            yearfrom=yearfrom, coursetypes=coursetypes
        )
