from addressbook.api.v1.serializers import SortingContactsSerializer
from cds.settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM
from django.utils.text import slugify
from generics.utils import decrypt
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.schemas.openapi import AutoSchema

from .filters import (
    ApiAllActivitiesListFilter,
    ApiCdsListFilter,
    ApiCdsWebsitesStudyPlansListFilter,
)
from .serializers import (
    AcademicYearsSerializer,
    CdsAreasSerializer,
    CdsInfoSerializer,
    CdSSerializer,
    CdSStudyPlanSerializer,
    CdSStudyPlansSerializer,
    CdsWebsitesStudyPlansSerializer,
    DegreeTypesSerializer,
    ErogationModesSerializer,
    StudyActivitiesSerializer,
    StudyActivityInfoSerializer,
    StudyPlansActivitiesSerializer,
)
from .services import ServiceDidatticaAttivitaFormativa, ServiceDidatticaCds


class ApiCdSList(ApiEndpointList):
    description = (
        "Restituisce un elenco di Corsi di studio con un set"
        " minimo di informazioni. Opera su "
        "“DIDATTICA_REGOLAMENTO” e restituisce tutti i record"
        " che corrispondono ai parametri impostati in input, "
        "ordinati secondo il parametro indicato, nella lingua"
        " selezionata (in mancanza, per le lingue straniere si"
        " restituiscono dati in inglese o, se non presenti,"
        " in italiano)"
    )
    serializer_class = CdSSerializer
    filter_backends = [ApiCdsListFilter]

    def get_queryset(self):
        return ServiceDidatticaCds.cdslist(self.language, self.request.query_params)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cache_key = f"cdslist_{self.language}_{slugify(self.request.query_params)}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiCdSDetail(ApiEndpointDetail):
    description = (
        "Restituisce le informazioni di uno specifico"
        " Corso di Studio che sono contenute nelle tabelle"
        " DIDATTICA_REGOLAMENTO e DIDATTICA_TESTI_REGOLAMENTO"
        " nella lingua indicata (in mancanza, si restituiscono"
        " dati in inglese per altre lingue straniere o, se non"
        " presenti, in italiano)"
    )
    serializer_class = CdsInfoSerializer
    filter_backends = []

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
            )
            if my_offices:
                only_active = False

        return ServiceDidatticaCds.cds(
            self.language, self.kwargs["regdidid"], only_active
        )


class ApiCdSStudyPlansList(ApiEndpointList):
    description = "Restituisce un elenco di Piani di Studio"
    serializer_class = CdSStudyPlansSerializer
    filter_backends = []

    def get_queryset(self):
        cdsid_param = str(self.kwargs["regdidid"])
        return ServiceDidatticaAttivitaFormativa.getStudyPlans(regdid_id=cdsid_param)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cdsid_param = str(self.kwargs["regdidid"])
        cache_key = f"cdsstudyplans_{self.language}__{cdsid_param}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiStudyPlanDetail(ApiEndpointDetail):
    description = "Restituisce i dettagli su un singolo piano di studi"
    serializer_class = CdSStudyPlanSerializer
    filter_backends = []

    def get_queryset(self):
        studyplanid = str(self.kwargs["studyplanid"])

        return ServiceDidatticaAttivitaFormativa.getStudyPlan(studyplanid=studyplanid)


class StudyPlanActivitiesList(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation["operationId"] = "listCdsStudyPlanActivities"
        return operation


class ApiStudyPlanActivitiesList(ApiEndpointList):
    description = (
        "Restituisce l’elenco degli insegnamenti"
        " di un Piano di Studio con info sintetiche"
    )
    serializer_class = StudyPlansActivitiesSerializer
    filter_backends = []
    schema = StudyPlanActivitiesList()

    def get_queryset(self):
        studyplanid = str(self.kwargs["studyplanid"])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid
        )


class ApiAllStudyActivitiesList(ApiEndpointList):
    description = (
        "Restituisce l’elenco degli insegnamenti"
        " di un Piano di Studio con info sintetiche"
    )
    serializer_class = StudyActivitiesSerializer
    filter_backends = [ApiAllActivitiesListFilter]

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
    description = (
        "Restituisce le informazioni" " dettagliate su un singolo “Insegnamento”"
    )
    serializer_class = StudyActivityInfoSerializer
    filter_backends = []

    def get_queryset(self):
        studyactivityid = str(self.kwargs["studyactivityid"])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language
        )


class StudyActivityInfo(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation["operationId"] = "retrieveCdsStudyPlanActivity"
        return operation


class ApiStudyActivityInfo(ApiEndpointDetail):
    description = (
        "Restituisce le informazioni" " dettagliate su un singolo “Insegnamento”"
    )
    serializer_class = StudyActivityInfoSerializer
    filter_backends = []
    schema = StudyActivityInfo()

    def get_queryset(self):
        studyactivityid = str(self.kwargs["studyactivityid"])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language
        )


class ApiDegreeTypesList(ApiEndpointList):
    description = "La funzione restituisce la lista delle tipologie di lauree"
    serializer_class = DegreeTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getDegreeTypes()


class ApiAcademicYearsList(ApiEndpointListSupport):
    description = "La funzione restituisce gli anni accademici"
    serializer_class = AcademicYearsSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getAcademicYears()


class ApiCdsAreasList(ApiEndpointListSupport):
    description = "La funzione restituisce la lista delle aree dei cds"
    serializer_class = CdsAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getCdsAreas()

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cache_key = "cdsareas"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)


class ApiSortingContacts(ApiEndpointList):
    description = "La funzione riceve in input il codice di un corso di studio e restituisce i docenti che appartengono a quel cds con dipartimento e uffici"
    serializer_class = SortingContactsSerializer
    filter_backends = []

    def get_queryset(self):
        cdscod = self.kwargs["cdscod"]
        return ServiceDidatticaCds.getContacts(cdscod)


class ApiErogationModesList(ApiEndpointList):
    description = "La funzione restituisce la lista delle modalità di erogazione"
    serializer_class = ErogationModesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getErogationModes()


class ApiCdsWebsitesStudyPlansList(ApiEndpointList):
    description = "Restituisce l’elenco dei piani di studio dei cds"
    serializer_class = CdsWebsitesStudyPlansSerializer
    filter_backends = [ApiCdsWebsitesStudyPlansListFilter]

    def get_queryset(self):
        cds_cod = self.request.query_params.get("cds_cod")
        year = self.request.query_params.get("year")
        # regdid = self.request.query_params.get('regdid')
        return ServiceDidatticaCds.getCdsWebsitesStudyPlans(cds_cod, year)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cds_cod = self.request.query_params.get("cds_cod")
        year = self.request.query_params.get("year")
        cache_key = f"cdswebsite_studyplanlist_{self.language}__{cds_cod}_{year}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)
