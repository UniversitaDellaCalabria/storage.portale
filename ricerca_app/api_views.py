import base64
import datetime
import requests
import json

from django.core.cache import cache
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from . filters import *
from . pagination import UnicalStorageApiPaginationList
from . serializers import *
from . services import *

# Esse3 utils
from . esse3.services import getEsse3Appelli
from . esse3.serializers import esse3AppelliSerializer

# University Planner utils
from . up.serializers import upImpegniSerializer
from . up.services import getUPImpegni

### useful for storage backend only ###
from organizational_area.models import OrganizationalStructureOfficeEmployee
from crud.phd.settings import PHD_CYCLES
from crud.utils.settings import *
### end useful for storage backend only ###

# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS
from . models import DidatticaAttivitaFormativaEsse3, DidatticaCdsEsse3
from . concurrency import LOCK_MESSAGE, acquire_lock, get_lock_from_cache
from . utils import encode_labels, encrypt, decrypt
from . exceptions import *

class ApiEndpointList(generics.ListAPIView):
    pagination_class = UnicalStorageApiPaginationList
    permission_classes = [permissions.AllowAny]
    # filter_backends = [OrderingFilter]
    # ordering_fields = '__all__'
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None

    def prepare_data(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return serializer

    def get(self, obj, **kwargs):
        if not self.language:
            lang = self.request.LANGUAGE_CODE
            self.language = self.request.query_params.get('lang', lang).lower()

        # cache
        if kwargs.get('cache_key'):
            cache_key = kwargs['cache_key']
            if cache.get(cache_key):
                data = cache.get(cache_key)
            else:
                serializer = self.prepare_data(**kwargs)
                data = serializer.data
                cache.set(cache_key, data)
        else:
            serializer = self.prepare_data(**kwargs)
            data = serializer.data

        results = self.paginate_queryset(data)
        response = {
            'data': results,
            'language': self.language,
        }
        return self.get_paginated_response(response)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'language': self.language})
        return context


class ApiEndpointDetail(ApiEndpointList):

    def get(self, obj, **kwargs):
        self.language = str(
            self.request.query_params.get(
                'lang', 'null')).lower()
        if self.language == 'null':
            self.language = self.request.LANGUAGE_CODE

        queryset = self.get_queryset()
        if queryset is not None and len(queryset) > 0:
            serializer = self.get_serializer(queryset[0], many=False)
            return Response({
                'results': serializer.data,
                'labels': encode_labels(serializer.data, self.language)
            })

        return Response({
            'results': {},
            'labels': {}
        })


class ApiEndpointListSupport(ApiEndpointList):
    pagination_class = None
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)

    def get(self, obj, **kwargs):
        self.language = str(
            self.request.query_params.get(
                'lang', 'null')).lower()
        if self.language == 'null':
            self.language = self.request.LANGUAGE_CODE

        queryset = self.get_queryset()

        if queryset is not None and len(queryset) > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'labels': encode_labels(list(serializer.data)[0], self.language)
            })

        return Response({
            'results': {},
            'labels': {}
        })

# ----CdS----

# class ApiStatus(APIView):
#
#     description = 'Restituisce lo stato( health check API ) '
#
#
#     def get(self, *args, **kwargs):
#
#         return Response(content_type='application/problem+json')


class ApiCdSList(ApiEndpointList):
    description = 'Restituisce un elenco di Corsi di studio con un set' \
                  ' minimo di informazioni. Opera su ' \
                  '“DIDATTICA_REGOLAMENTO” e restituisce tutti i record' \
                  ' che corrispondono ai parametri impostati in input, ' \
                  'ordinati secondo il parametro indicato, nella lingua' \
                  ' selezionata (in mancanza, per le lingue straniere si' \
                  ' restituiscono dati in inglese o, se non presenti,' \
                  ' in italiano)'
    serializer_class = CdSSerializer
    filter_backends = [ApiCdsListFilter]

    def get_queryset(self):
        return ServiceDidatticaCds.cdslist(self.language,
                                           self.request.query_params)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get('lang', lang).lower()
        cache_key = f"cdslist_{self.language}_{slugify(self.request.query_params)}"
        kwargs['cache_key'] = cache_key
        return super().get(*args, **kwargs)


class ApiCdSDetail(ApiEndpointDetail):
    description = 'Restituisce le informazioni di uno specifico' \
                  ' Corso di Studio che sono contenute nelle tabelle' \
                  ' DIDATTICA_REGOLAMENTO e DIDATTICA_TESTI_REGOLAMENTO' \
                  ' nella lingua indicata (in mancanza, si restituiscono' \
                  ' dati in inglese per altre lingue straniere o, se non' \
                  ' presenti, in italiano)'
    serializer_class = CdsInfoSerializer
    filter_backends = []

    def get_queryset(self):

        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name__in=[OFFICE_CDS,OFFICE_CDS_DOCUMENTS,
                                                                                                OFFICE_CDS_TEACHING_SYSTEM],
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices: only_active = False

        return ServiceDidatticaCds.cds(
            self.language,
            self.kwargs['regdidid'],
            only_active)


class ApiCdSStudyPlansList(ApiEndpointList):
    description = 'Restituisce un elenco di Piani di Studio'
    serializer_class = CdSStudyPlansSerializer
    filter_backends = []

    def get_queryset(self):
        cdsid_param = str(self.kwargs['regdidid'])
        return ServiceDidatticaAttivitaFormativa.getStudyPlans(regdid_id=cdsid_param)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get('lang', lang).lower()
        cdsid_param = str(self.kwargs['regdidid'])
        cache_key = f"cdsstudyplans_{self.language}__{cdsid_param}"
        kwargs['cache_key'] = cache_key
        return super().get(*args, **kwargs)


class ApiStudyPlanDetail(ApiEndpointDetail):
    description = 'Restituisce i dettagli su un singolo piano di studi'
    serializer_class = CdSStudyPlanSerializer
    filter_backends = []

    def get_queryset(self):
        studyplanid = str(self.kwargs['studyplanid'])

        return ServiceDidatticaAttivitaFormativa.getStudyPlan(
            studyplanid=studyplanid)


class StudyPlanActivitiesList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'listCdsStudyPlanActivities'


class ApiStudyPlanActivitiesList(ApiEndpointList):
    description = 'Restituisce l’elenco degli insegnamenti' \
                  ' di un Piano di Studio con info sintetiche'
    serializer_class = StudyPlansActivitiesSerializer
    filter_backends = []
    schema = StudyPlanActivitiesList()

    def get_queryset(self):
        studyplanid = str(self.kwargs['studyplanid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid)


class ApiAllStudyActivitiesList(ApiEndpointList):
    description = 'Restituisce l’elenco degli insegnamenti' \
                  ' di un Piano di Studio con info sintetiche'
    serializer_class = StudyActivitiesSerializer
    filter_backends = [ApiAllActivitiesListFilter]

    def get_queryset(self):
        request = self.request
        department = request.query_params.get('department')
        cds = request.query_params.get('cds')
        academic_year = request.query_params.get('academic_year')
        period = request.query_params.get('period')
        ssd = request.query_params.get('ssd')
        teaching = request.query_params.get('teaching')
        teacher = request.query_params.get('teacher')
        course_year = request.query_params.get('course_year')
        cds_cod = request.query_params.get('cds_cod')
        teacher_code = decrypt(request.query_params.get('teacher_code'))

        return ServiceDidatticaAttivitaFormativa.getAllActivities(self.language, department, cds, academic_year, period, ssd, teacher, teaching, course_year, cds_cod, teacher_code)


class ApiStudyActivityDetail(ApiEndpointDetail):
    description = 'Restituisce le informazioni' \
                  ' dettagliate su un singolo “Insegnamento”'
    serializer_class = StudyActivityInfoSerializer
    filter_backends = []

    def get_queryset(self):

        studyactivityid = str(self.kwargs['studyactivityid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language)


class StudyActivityInfo(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveCdsStudyPlanActivity'


class ApiStudyActivityInfo(ApiEndpointDetail):
    description = 'Restituisce le informazioni' \
                  ' dettagliate su un singolo “Insegnamento”'
    serializer_class = StudyActivityInfoSerializer
    filter_backends = []
    schema = StudyActivityInfo()

    def get_queryset(self):
        studyactivityid = str(self.kwargs['studyactivityid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language)


# class ApiCdSMainTeachersList(ApiEndpointList):
#     description = 'Fornisce l’elenco dei docenti di riferimento' \
#                   ' (o di tutti i docenti ???) associati ad un CdS.' \
#                   ' Per ogni docente riporta poche informazioni' \
#                   ' identificative: Nome, Ruolo, Settore scientifico' \
#                   ' disciplinare, …'
#     serializer_class = CdSMainTeachersSerializer
#     filter_backends = [ApiCdSMainTeachersFilter]
#
#     def get_queryset(self):
#         regdid_id = self.request.query_params.get('cdsid')
#         if not regdid_id:
#             return None
#
#         return ServiceDidatticaAttivitaFormativa.getDocentiPerReg(regdid_id)

# ----Ricerca----


# class ApiTeacherResearchGroupsList(ApiEndpointList):
#     description = 'La funzione restituisce l’elenco ' \
#                   'dei gruppi di ricerca del docente ordinati per nome.'
#     serializer_class = TeacherResearchGroupsSerializer
#     filter_backends = []
#
#     def get_queryset(self):
#         teacherid = self.kwargs['teacherid']
#
#         return ServiceDocente.getResearchGroups(teacherid)


class ApiResearchGroupsList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco ' \
                  'dei gruppi di ricerca ordinati per nome.'
    serializer_class = AllResearchGroupsSerializer
    filter_backends = [ApiResearchGroupsListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        teacher = decrypt(request.query_params.get('teacher'))
        department = request.query_params.get('department')
        cod = request.query_params.get('coderc1')

        return ServiceDocente.getAllResearchGroups(search, teacher, department, cod)


class ApiTeacherResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca del docente ordinati ' \
                  'per Tipo (applicata/di base) e Nome.'
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = []

    def get_queryset(self):
        teacherid = decrypt(self.kwargs['teacherid'])

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        request = self.request
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_RESEARCHLINES,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False

        return ServiceDocente.getResearchLines(teacherid, only_active)


class ApiBaseResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca di base'
    serializer_class = BaseResearchLinesSerializer
    filter_backends = [ApiBaseResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        teacher = decrypt(self.request.query_params.get('teacher'))
        department = request.query_params.get('department')
        year = request.query_params.get('year')

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_RESEARCHLINES,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False

        return ServiceDocente.getBaseResearchLines(
            search, teacher, department, year, only_active)


class ApiAppliedResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca applicate'
    serializer_class = AppliedResearchLinesSerializer
    filter_backends = [ApiAppliedResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        teacher = decrypt(self.request.query_params.get('teacher'))
        department = request.query_params.get('department')
        year = request.query_params.get('year')

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_RESEARCHLINES,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False

        return ServiceDocente.getAppliedResearchLines(
            search, teacher, department, year, only_active)


class ApiAllResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco di tutte le Linee di' \
                  ' ricerca'
    serializer_class = AllResearchLinesSerializer
    filter_backends = [ApiAllResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        year = request.query_params.get('year')
        department = request.query_params.get('department')
        ercs = request.query_params.get('ercs')
        asters = request.query_params.get('asters')
        exclude_base = request.query_params.get('exclude_base')
        exclude_applied = request.query_params.get('exclude_applied')

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_RESEARCHLINES,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False

        return ServiceDocente.getAllResearchLines(search,
                                                  year,
                                                  department,
                                                  ercs,
                                                  asters,
                                                  exclude_base,
                                                  exclude_applied,
                                                  only_active)

# ----Docenti----


class ApiTeachersList(ApiEndpointList):
    description = 'Restituisce un elenco di Docenti che hanno una copertura attiva in ateneo, con un set minimo di ' \
                  'informazioni identificative: Nome, Ruolo, ' \
                  'Settore scientifico disciplinare, …'
    serializer_class = TeachersSerializer
    filter_backends = [ApiTeachersListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        regdidid = request.query_params.get('regdid')
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        cds = request.query_params.get('cds')
        year = request.query_params.get('year')

        return ServiceDocente.teachersList(
            search, regdidid, department, role, cds, year)


class TeachingCoveragesList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'listTeachingCoverages'


class ApiTeachingCoveragesList(ApiEndpointList):
    description = 'Restituisce un elenco di Docenti con il fl_docente=1 e fl_cessato=0'\
        'con un set minimo di informazioni identificative: Nome, Ruolo, ' \
                  'Settore scientifico disciplinare, …'
    serializer_class = TeachersSerializer
    filter_backends = [ApiTeachersListFilter]
    schema = TeachingCoveragesList()

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        regdidid = request.query_params.get('regdid')
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        cds = request.query_params.get('cds')
        year = request.query_params.get('year')

        return ServiceDocente.teachingCoveragesList(
            search, regdidid, department, role, cds, year)


class ApiTeacherStudyActivitiesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco degli insegnamenti' \
                  ' (per gli ultimi anni) ordinati per anno e nome' \
                  ' dell’insegnamento.'
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [ApiTeacherStudyActivitiesFilter]

    def get_queryset(self):
        request = self.request
        teacherid = decrypt(self.kwargs['teacherid'])
        year = request.query_params.get('year')
        yearFrom = request.query_params.get('yearFrom')
        yearTo = request.query_params.get('yearTo')

        return ServiceDocente.getAttivitaFormativeByDocente(
            teacherid, year, yearFrom, yearTo)


class TeachingCoverageStudyActivitiesList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'listTeachingCoverageStudyActivities'


class ApiTeachingCoverageActivitiesList(ApiTeacherStudyActivitiesList):
    schema = TeachingCoverageStudyActivitiesList()


class ApiTeacherDetail(ApiEndpointDetail):
    description = 'La funzione restituisce la scheda informativa' \
                  ' dettagliata di un docente'
    serializer_class = TeacherInfoSerializer
    filter_backends = []

    def get_queryset(self):

        teacherid = decrypt(self.kwargs['teacherid'])

        return ServiceDocente.getDocenteInfo(teacherid)


class ApiTeacherMaterials(ApiEndpointList):
    description = 'La funzione restituisce il materiale didattico di un docente'
    serializer_class = TeacherMaterialsSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        teacherid = decrypt(self.kwargs['teacherid'])
        return ServiceDocente.getDocenteMaterials(request.user, teacherid, search)


# class ApiTeacherMaterial(ApiEndpointDetail):
    # description = 'La funzione restituisce il materiale diddattico specifico di un docente'
    # serializer_class = TeacherMaterialsSerializer
    # filter_backends = []

    # def get_queryset(self):
        # teacherid = decrypt(self.kwargs['teacherid'])
        # return ServiceDocente.getDocenteMaterials(teacherid)


class ApiTeacherNews(ApiEndpointList):
    description = 'La funzione restituisce le news di un docente'
    serializer_class = TeacherNewsSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        teacherid = decrypt(self.kwargs['teacherid'])

        return ServiceDocente.getDocenteNews(request.user, teacherid, search)


class TeachingCoveragesInfo(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveTeachingCoverageInfo'


class ApiTeachingCoverageDetail(ApiTeacherDetail):
    schema = TeachingCoveragesInfo()


# ----Dottorati----


class ApiPhdList(ApiEndpointList):
    description = 'La funzione restituisce una lista di dottorati'
    serializer_class = PhdSerializer
    filter_backends = [ApiPhdListFilter]

    def get_queryset(self):
        return ServiceDottorato.getPhd(self.request.query_params)

# ---- Tipologie Lauree ----


class ApiDegreeTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle tipologie di lauree'
    serializer_class = DegreeTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getDegreeTypes()


# ---- Dipartimenti ----


class ApiDepartmentsList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei dipartimenti'
    serializer_class = DepartmentSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDipartimento.getDepartmentsList(self.language)


class ApiDepartmentDetail(ApiEndpointDetail):
    description = 'La funzione restituisce uno specifico dipartimento'
    serializer_class = DepartmentSerializer
    filter_backends = []

    def get_queryset(self):
        departmentcod = self.kwargs['departmentcod']
        return ServiceDipartimento.getDepartment(departmentcod)


class ApiAddressbookList(ApiEndpointList):
    description = 'La funzione restituisce la rubrica telefonica del personale'
    serializer_class = AddressbookSerializer
    filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        phone = request.query_params.get('phone')
        structureid = request.query_params.get('structure')
        structuretypes = request.query_params.get('structuretypes')
        role = request.query_params.get('role')
        structuretree = request.query_params.get('structuretree')

        return ServicePersonale.getAddressbook(
            search, structureid, structuretypes, role, structuretree, phone)


class ApiAddressbookFullList(ApiEndpointList):
    description = 'La funzione restituisce la rubrica telefonica del personale arricchita con dati riguardanti il contratto'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressbookFullSerializer
    filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        phone = request.query_params.get('phone')
        structureid = request.query_params.get('structure')
        structuretypes = request.query_params.get('structuretypes')
        role = request.query_params.get('role')
        structuretree = request.query_params.get('structuretree')
        taxpayer_id=request.query_params.get('taxpayer_id')

        return ServicePersonale.getAddressbook(
            search=search,
            structureid=structureid,
            structuretypes=structuretypes,
            role=role,
            structuretree=structuretree,
            phone=phone,
            taxpayer_id=taxpayer_id,
            full=True)


class ApiStructuresList(ApiEndpointList):
    description = 'La funzione restituisce le strutture organizzative'
    serializer_class = StructuresSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        father = request.query_params.get('father')
        depth = request.query_params.get('depth')
        type = request.query_params.get('type')
        return ServicePersonale.getStructuresList(search, father, type, depth)


class ApiStructureTypesList(ApiEndpointListSupport):
    description = 'La funzione restituisce le tipologie di strutture organizzative'
    serializer_class = StructureTypesSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        father = self.request.query_params.get('father')
        return ServicePersonale.getStructureTypes(father)


class ApiAcademicYearsList(ApiEndpointListSupport):
    description = 'La funzione restituisce gli anni accademici'
    serializer_class = AcademicYearsSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getAcademicYears()


class ApiStructureDetail(ApiEndpointDetail):
    description = 'La funzione restituisce una specifica struttura'
    serializer_class = StructureDetailSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        structureid = self.kwargs['structureid']
        return ServicePersonale.getStructure(structureid)


class ApiRolesList(ApiEndpointListSupport):
    description = 'La funzione restituisce i ruoli'
    serializer_class = RolesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDocente.getRoles()


class ApiPersonaleDetail(ApiEndpointDetail):
    description = 'La funzione restituisce una specifica persona'
    serializer_class = PersonaleSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        personaleid = decrypt(self.kwargs['personaleid'])

        return ServicePersonale.getPersonale(personaleid)


class ApiPersonaleFullDetail(ApiEndpointDetail):
    description = 'La funzione restituisce una specifica persona con i dati sul contratto'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaleFullSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        personaleid = self.kwargs['personaleid']
        return ServicePersonale.getPersonale(personale_id=personaleid, full=True)


class ApiLaboratoryDetail(ApiEndpointDetail):
    description = 'La funzione restituisce un laboratorio specifico'
    serializer_class = LaboratoryDetailSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        laboratoryid = self.kwargs['laboratoryid']
        request = self.request

        #CRUD
        only_active = True
        if request.user.is_superuser: only_active = False # pragma: no cover

        elif request.user.is_authenticated: # pragma: no cover
            user_profile = None
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(cod_fis=request.user.taxpayer_id).first()

            offices = OrganizationalStructureOfficeEmployee\
                .objects\
                .filter(employee=request.user,
                        office__is_active=True,
                        office__organizational_structure__is_active=True)

            is_scientific_director = user_profile is not None and LaboratorioDatiBase.objects.filter(matricola_responsabile_scientifico = user_profile).exists()
            is_operator = offices.filter(office__name=OFFICE_LABORATORIES).exists()
            is_validator = offices.filter(office__name=OFFICE_LABORATORY_VALIDATORS).exists()
            if(is_operator or is_validator or is_scientific_director):
                only_active = False

        return ServiceLaboratorio.getLaboratory(self.language, laboratoryid, only_active)


class ApiLaboratoriesList(ApiEndpointList):
    description = 'La funzione restituisce i laboratori'
    serializer_class = LaboratoriesSerializer
    filter_backends = [ApiLaboratoriesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        area = request.query_params.get('area')
        department = request.query_params.get('department')
        erc1 = request.query_params.get('erc1')
        teacher = decrypt(request.query_params.get('teacher'))
        infrastructure = request.query_params.get('infrastructure')
        scope = request.query_params.get('scope')

        #CRUD
        only_active = True
        if request.user.is_superuser: only_active = False # pragma: no cover
        elif request.user.is_authenticated: # pragma: no cover
            user_profile = None
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(cod_fis=request.user.taxpayer_id).first()

            offices = OrganizationalStructureOfficeEmployee\
                .objects\
                .filter(employee=request.user,
                        office__is_active=True,
                        office__organizational_structure__is_active=True)

            is_scientific_director = user_profile is not None and LaboratorioDatiBase.objects.filter(matricola_responsabile_scientifico = user_profile).exists()
            is_operator = offices.filter(office__name=OFFICE_LABORATORIES).exists()
            is_validator = offices.filter(office__name=OFFICE_LABORATORY_VALIDATORS).exists()
            if(is_operator or is_validator or is_scientific_director):
                only_active = False

        return ServiceLaboratorio.getLaboratoriesList(
            self.language, search, area, department, erc1, teacher, infrastructure, scope, only_active)


class ApiLaboratoriesAreasList(ApiEndpointList):
    description = 'La funzione restituisce la lista degli ambiti dei laboratori'
    serializer_class = LaboratoriesAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getLaboratoriesAreasList()


class ApiErc1List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli erc1'
    serializer_class = Erc1Serializer
    filter_backends = []

    def get_queryset(self):


        return ServiceLaboratorio.getErc1List()


class ApiErc2List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli erc2'
    serializer_class = Erc2Serializer
    filter_backends = []

    def get_queryset(self):

        return ServiceLaboratorio.getErc2List()


class ApiErc0List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli erc0'
    serializer_class = Erc0Serializer
    filter_backends = []

    def get_queryset(self):

        return ServiceLaboratorio.getErc0List()


class ApiPublicationsList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle pubblicazioni di un dato docente'
    serializer_class = PublicationsSerializer
    filter_backends = [ApiPublicationsListFilter]

    def get_queryset(self):
        request = self.request
        teacherid = decrypt(self.kwargs.get('teacherid')) if self.kwargs.get('teacherid') else ''
        search = request.query_params.get('search')
        year = request.query_params.get('year')
        pub_type = request.query_params.get('type')
        structure = request.query_params.get('structure')

        return ServiceDocente.getPublicationsList(
            teacherid, search, year, pub_type, structure)


class TeachingCoveragePublicationsList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'listTeachingCoveragePublications'


class ApiTeachingCoveragePublicationsList(ApiPublicationsList):
    schema = TeachingCoveragePublicationsList()


class TeacherPublicationsList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'listTeacherPublications'


class ApiTeacherPublicationsList(ApiPublicationsList):
    schema = TeacherPublicationsList()


class ApiPublicationsCommunityTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle tipologie di pubblicazioni'
    serializer_class = PublicationsCommunityTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDocente.getPublicationsCommunityTypesList()


class ApiPublicationDetail(ApiEndpointDetail):
    description = 'La funzione restituisce il dettaglio di una pubblicazione'
    serializer_class = PublicationSerializer
    filter_backends = []

    def get_queryset(self):
        publicationid = self.kwargs['publicationid']

        return ServiceDocente.getPublication(publicationid)


class TeacherPublicationDetail(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveTeacherPublication'


class ApiTeacherPublicationDetail(ApiPublicationDetail):
    schema = TeacherPublicationDetail()


class TeachingCoveragePublicationsDetail(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveTeachingCoveragePublication'


class ApiTeachingCoveragePublicationDetail(ApiPublicationDetail):
    schema = TeachingCoveragePublicationsDetail()


class ApiAddressbookStructuresList(ApiEndpointList):
    description = 'La funzione restituisce le strutture organizzative a cui un docente afferisce'
    serializer_class = AddressbookStructuresSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        father = request.query_params.get('father')
        type = request.query_params.get('type')

        return ServicePersonale.getAllStructuresList(search, father, type)


class AddressbookStructureDetail(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveAddressbookStructureDetail'


class ApiAddressbookStructureDetail(ApiStructureDetail):
    schema = AddressbookStructureDetail()


class ApiInfrastructuresList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle infrastrutture di riferimento'
    serializer_class = InfrastructuresSerializer
    filter_backends = []

    def get_queryset(self):

        return ServiceLaboratorio.getInfrastructures()


class ApiPatentsList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei brevetti'
    serializer_class = PatentsSerializer
    filter_backends = [ApiPatentsListFilter]

    def get_queryset(self):
        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_PATENTS,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False
        # end get active/all elements

        search = request.query_params.get('search')
        techarea = request.query_params.get('techarea')
        structure = request.query_params.get('structure')

        return ServiceBrevetto.getPatents(search, techarea, structure, only_active)


class ApiPatentDetail(ApiEndpointDetail):
    description = 'La funzione restituisce uno specifico brevetto'
    serializer_class = PatentsSerializer
    filter_backends = []

    def get_queryset(self):

        patentid = self.kwargs['patentid']

        return ServiceBrevetto.getPatentDetail(patentid)


class ApiLaboratoriesScopesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle finalità dei laboratori'
    serializer_class = LaboratoriesScopesSerializer
    filter_backends = []

    def get_queryset(self):

        return ServiceLaboratorio.getScopes()


class ApiCompaniesList(ApiEndpointList):
    description = 'La funzione restituisce la lista degli spin-off'
    serializer_class = CompaniesSerializer
    filter_backends = [ApiCompaniesListFilter]

    def get_queryset(self):
        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_COMPANIES,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False
        # end get active/all elements

        search = request.query_params.get('search')
        techarea = request.query_params.get('techarea')
        spinoff = request.query_params.get('spinoff')
        startup = request.query_params.get('startup')
        departments = request.query_params.get('departments')

        return ServiceCompany.getCompanies(search, techarea, spinoff, startup, departments, only_active)


class ApiCompanyDetail(ApiEndpointDetail):
    description = 'La funzione restituisce un particolare spinoff/startup'
    serializer_class = CompaniesSerializer
    filter_backends = []

    def get_queryset(self):

        companyid = self.kwargs['companyid']

        return ServiceCompany.getCompanyDetail(companyid)


class ApiTechAreasList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle aree tecnologiche'
    serializer_class = TechAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceCompany.getTechAreas()


class ApiProjectsList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei progetti'
    serializer_class = ProjectSerializer
    filter_backends = [ApiProjectsListFilter, OrderingFilter]

    def get_queryset(self):
        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser: only_active = False # pragma: no cover
        if request.user.is_authenticated: # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                              office__name=OFFICE_PROJECTS,
                                                                              office__is_active=True,
                                                                              office__organizational_structure__is_active=True)
            if my_offices.exists(): only_active = False
        # end get active/all elements

        search = request.query_params.get('search')
        techarea = request.query_params.get('techarea')
        infrastructure = request.query_params.get('infrastructure')
        programtype = request.query_params.get('programtype')
        territorialscope = request.query_params.get('territorialscope')
        notprogramtype = request.query_params.get('-programtype')
        year =request.query_params.get('year')

        return ServiceProgetto.getProjects(search,
                                           techarea,
                                           infrastructure,
                                           programtype,
                                           territorialscope,
                                           notprogramtype,
                                           year,
                                           only_active)


class ApiProjectDetail(ApiEndpointDetail):
    description = 'La funzione restituisce il dettaglio'
    serializer_class = ProjectSerializer
    filter_backends = []

    def get_queryset(self):
        projectid = self.kwargs['projectid']
        return ServiceProgetto.getProjectDetail(projectid)


class ApiStructureFunctionsList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle funzioni della unità organizzativa'
    serializer_class = StructureFunctionsSerializer
    filter_backends = []

    def get_queryset(self):
        return ServicePersonale.getStructureFunctions()


class ApiProjectsTerritorialScopesList(ApiEndpointList):
    description = 'La funzione restituisce la lista degli ambiti territoriali'
    serializer_class = TerritorialScopesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceProgetto.getTerritorialScopes()


class ApiProjectsProgramTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle tipologie di programmi di progetto'
    serializer_class = ProgramTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceProgetto.getProgramTypes()


class ApiCdsAreasList(ApiEndpointListSupport):
    description = 'La funzione restituisce la lista delle aree dei cds'
    serializer_class = CdsAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getCdsAreas()

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get('lang', lang).lower()
        cache_key = "cdsareas"
        kwargs['cache_key'] = cache_key
        return super().get(*args, **kwargs)

class ApiProjectsInfrastructuresList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle infrastrutture dei progetti'
    serializer_class = ProjectInfrastructuresSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceProgetto.getProjectInfrastructures()


class ApiPersonnelCfList(ApiEndpointList):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = 'La funzione restituisce la lista dei cf del personale'
    serializer_class = PersonnelCfSerializer
    filter_backends = []

    def get_queryset(self):
        roles = self.request.query_params.get('roles')
        return ServicePersonale.getPersonnelCfs(roles)


class ApiSortingContacts(ApiEndpointList):
    description = 'La funzione riceve in input il codice di un corso di studio e restituisce i docenti che appartengono a quel cds con dipartimento e uffici'
    serializer_class = SortingContactsSerializer
    filter_backends = []

    def get_queryset(self):
        cdscod = self.kwargs['cdscod']
        return ServiceDidatticaCds.getContacts(cdscod)


class ApiHighFormationMastersList(ApiEndpointList):
    description = 'La funzione restituisce i master alta formazione'
    serializer_class = HighFormationMastersSerializer
    filter_backends = [ApiHighFormationMastersListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        director = request.query_params.get('director')
        coursetype = request.query_params.get('coursetype')
        erogation = request.query_params.get('erogation')
        department = request.query_params.get('department')
        language = request.query_params.get('language')
        year = request.query_params.get('year')


        return ServiceDidatticaCds.getHighFormationMasters(search, director, coursetype, erogation, department, language, year)


class ApiHighFormationMastersDetail(ApiEndpointDetail):
    description = 'La funzione restituisce il dettaglio di un master'
    serializer_class = HighFormationMastersSerializer
    filter_backends = [ApiHighFormationMastersListFilter]

    def get_queryset(self):
        master_id = self.kwargs['id']
        return ServiceDidatticaCds.getHighFormationMaster(master_id)


class ApiErogationModesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle modalità di erogazione'
    serializer_class = ErogationModesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getErogationModes()


class ApiHighFormationCourseTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei tipi di corso dell\'alta formazione'
    serializer_class = HighFormationCourseTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getHighFormationCourseTypes()


class ApiPersonIdSchema(AutoSchema):
    def get_operation_id(self, path, method):
        return 'getPersonId'


class ApiPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = 'La funzione restituisce il codice criptato di una persona'
    schema = ApiPersonIdSchema()

    def post(self, request, *args, **kwargs):
        data = request.data
        matricola = data.get("id","")
        if not matricola:
            return Response("Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND)
        p = Personale.objects.filter(matricola=matricola).first()
        if not p:
            return Response("Il dato non esiste", status=status.HTTP_404_NOT_FOUND)
        return Response(encrypt(matricola))


class ApiDecryptedPersonIdSchema(AutoSchema):
    def get_operation_id(self, path, method):
        return 'getDecryptedPersonId'


class ApiDecryptedPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = 'La funzione restituisce la matricola in chiaro una persona'
    schema = ApiDecryptedPersonIdSchema()

    def post(self, request, *args, **kwargs):
        data = request.data
        encrypted_matricola = data.get("id","")
        if not encrypted_matricola:
            return Response("Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND)
        try:
            m = decrypt(encrypted_matricola)
            return Response(m)
        except:
            return Response("Non è stato possibile decriptare il dato", status=status.HTTP_404_NOT_FOUND)


class ApiAster1List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli aster1'
    serializer_class = Asters1Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getAster1List()


class ApiAster2List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli aster2'
    serializer_class = Asters2Serializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getAster2List()


class ApiPhdCycles(APIView):
    def get(self, request):
        result = {}
        for cycle in PHD_CYCLES:
            result[cycle[0]] = cycle[1]
        return Response(result)


class ApiPhdActivitiesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle attività dei dottorati'
    serializer_class = PhdActivitiesSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get('search')
        structure = request.query_params.get('structure')
        phd = request.query_params.get('phd')
        cycle = request.query_params.get('cycle')
        ssd = request.query_params.get('ssd')
        teacher = request.query_params.get('teacher')
        typology = request.query_params.get('typology')

        return ServiceDottorato.getPhdActivities(search, structure, phd, ssd, teacher, cycle, typology)


class ApiPhdActivityDetail(ApiEndpointDetail):
    description = 'La funzione restituisce il dettaglio di una attività riferita ad un dottorato'
    serializer_class = PhdActivitiesSerializer
    filter_backends = []

    def get_queryset(self):
        activity_id = self.kwargs['id']
        return ServiceDottorato.getPhdActivity(activity_id)


class ApiRefPhdList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei dottorati di riferimento'
    serializer_class = RefPhdSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getRefPhd()


class ApiRefStructuresList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle strutture di riferimento'
    serializer_class = RefStructuresSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getRefStructures()


class ApiPhdSsdList(ApiEndpointList):
    description = 'La funzione restituisce la lista degli ssd dei dottorati'
    serializer_class = PhdSsdListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdSsdList()


class ApiPhdActivityTypeList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei tipi di attività di dottorato'
    serializer_class = PhdActivityTypeSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypeList()


class ApiPhdActivityTypologies(ApiEndpointList):
    description = 'La funzione restituisce la lista delle tipologie di attività di dottorato'
    serializer_class = PhdActivityTypologySerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypologies()


class ApiCdsWebsiteList(ApiEndpointList):
    description = 'Restituisce l’elenco dei siti dei corsi di studio'
    serializer_class = CdsWebsiteLightSerializer
    filter_backends = [ApiCdsWebsitesListFilter]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        return ServiceDidatticaCds.getCdsWebsites(search)


class ApiCdsWebsiteDetail(ApiEndpointDetail):
    description = 'Restituisce il dettaglio di siti un corso di studio'
    serializer_class = CdsWebsiteSerializer
    filter_backends = []

    def get_queryset(self):
        cds_cod = self.kwargs['cdswebsitecod']
        return ServiceDidatticaCds.getCdsWebsite(cds_cod)


# class ApiCdsWebsitesDegreeTypes(ApiEndpointList):
    # description = 'Restituisce l’elenco dei siti delle classi di laurea per i siti web dei cds'
    # serializer_class = CdsWebsitesDegreeTypesSerializer
    # filter_backends = []

    # def get_queryset(self):
        # return ServiceDidatticaCds.getCdsWebsitesDegreeTypes()


class ApiCdsWebsitesTopicList(ApiEndpointList):
    description = 'Restituisce l’elenco dei topic per i siti web dei cds'
    serializer_class = CdsWebsitesTopicSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getCdsWebsitesTopics()


class ApiCdsWebsitesTopicArticlesList(ApiEndpointList):
    description = 'Restituisce l’elenco dei topic per i siti web dei cds'
    serializer_class = CdsWebsitesTopicArticlesSerializer
    filter_backends = [ApiCdsWebsitesTopicArticlesListFilter]

    def get_queryset(self):

        request = self.request
        cds_cod = self.request.query_params.get('cds_cod')
        topic_id = self.request.query_params.get('topic_id')

        # get only active elements if public
        # get all elements if in CRUD backend
        only_active = True
        if request.user.is_superuser: only_active = False # pragma: no cover
        elif request.user.is_authenticated: # pragma: no cover
            offices = OrganizationalStructureOfficeEmployee\
                .objects\
                .filter(employee=request.user,
                        office__is_active=True,
                        office__name=OFFICE_CDS_PAGES,
                        office__organizational_structure__is_active=True)

            if(offices.exists()):
                only_active = False

        return ServiceDidatticaCds.getCdsWebsitesTopicArticles(cds_cod, topic_id, only_active)



class ApiCdsWebsitesStudyPlansList(ApiEndpointList):
    description = 'Restituisce l’elenco dei piani di studio dei cds'
    serializer_class = CdsWebsitesStudyPlansSerializer
    filter_backends = [ApiCdsWebsitesStudyPlansListFilter]

    def get_queryset(self):
        cds_cod = self.request.query_params.get('cds_cod')
        year = self.request.query_params.get('year')
        # regdid = self.request.query_params.get('regdid')
        return ServiceDidatticaCds.getCdsWebsitesStudyPlans(cds_cod, year)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get('lang', lang).lower()
        cds_cod = self.request.query_params.get('cds_cod')
        year = self.request.query_params.get('year')
        cache_key = f"cdswebsite_studyplanlist_{self.language}__{cds_cod}_{year}"
        kwargs['cache_key'] = cache_key
        return super().get(*args, **kwargs)


class ApiCdsWebsiteTimetable(APIView): # pragma: no cover
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_types = ['AD']

    def get(self, obj, **kwargs):
        cds_cod = self.kwargs['cdswebsitecod']
        current_year = timezone.localtime(timezone.now().replace(tzinfo=timezone.utc)).year
        academic_year = self.request.query_params.get('academic_year', current_year)
        try:
            year = int(self.request.query_params.get('year'))
        except:
            year = 1
        # cds = ServiceDidatticaCds.getCdsWebsite(cds_cod)
        date_month = self.request.query_params.get('date_month', '')
        date_year = self.request.query_params.get('date_year', '')
        af_name = self.request.query_params.get('af_name', '')
        af_cod = self.request.query_params.get('af_cod', '')
        search_teacher = self.request.query_params.get('search_teacher', '')
        search_location = self.request.query_params.get('search_location', '')
        show_past = self.request.query_params.get('show_past', 'true')
        show_past = 0 if show_past == 'false' else 1

        search = {'search_teacher': search_teacher,
                  'search_location': search_location}

        search_key = base64.b64encode(str(search).encode())
        # if cds:
        cache_key = f"cdswebsite_timetable_{cds_cod}_{academic_year}_{year}_{date_month}_{date_year}_{slugify(self.event_types)}_{af_cod}_{search_key.decode()}_{show_past}"
        if not cache.get(cache_key):
            impegni = getUPImpegni(request=self.request,
                                   aa=academic_year,
                                   year=year,
                                   date_month=date_month,
                                   date_year=date_year,
                                   cds_cod=cds_cod,
                                   types=self.event_types,
                                   af_cod=af_cod,
                                   filter_by_af_cod='ES' not in self.event_types)
            impegni_json = upImpegniSerializer(impegni=impegni,
                                               year=year,
                                               af_name=af_name,
                                               search=search,
                                               show_past=show_past)

            # if Exams, search in Esse3 too
            if 'ES' in self.event_types:
                cds_id = DidatticaCdsEsse3.objects.get(cds_cod=cds_cod).cds_id_esse3
                af_id = DidatticaAttivitaFormativaEsse3.objects.get(ad_cod=af_cod).ad_id_esse3

                appelli_esse3 = getEsse3Appelli(request=self.request,
                                                cds_id=cds_id,
                                                af_id=af_id,
                                                aa=academic_year)
                appelli_esse3_json = esse3AppelliSerializer(appelli=appelli_esse3,
                                                            show_past=show_past)

                duplicates_to_remove = []
                for iu in impegni_json:
                    for ae3 in appelli_esse3_json:
                        if ae3['dataInizio'] == iu['dataInizio'] and ae3['orarioInizio'] == iu['orarioInizio']:
                            if not ae3['aula']:
                                ae3['aula'] = iu['aula']
                            duplicates_to_remove.append(iu)
                            break

                for delete in duplicates_to_remove:
                    a = impegni_json.remove(delete)

                all_events = impegni_json + appelli_esse3_json
                impegni_json = sorted(all_events, key= lambda x: (x['dataInizio'], x['orarioInizio']))
            cache.set(cache_key, impegni_json)

        return Response(cache.get(cache_key))


class ApiCdsWebsiteExams(ApiCdsWebsiteTimetable): # pragma: no cover
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_types = ['ES']


class ApiCdsWebsitesPortalObjectPreview(APIView): # pragma: no cover
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, objectid, objectclass, **kwargs):
        UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
        UNICMS_ROOT_URL = getattr(settings, 'UNICMS_ROOT_URL', '')
        UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', {})

        head = {'Authorization': 'Token {}'.format(UNICMS_AUTH_TOKEN)}
        res = {
            "status_code": 500
        }
        try:
            if objectclass not in UNICMS_OBJECT_API.keys():
                res["status_code"] = 400
            api_url = UNICMS_OBJECT_API[objectclass].format(objectid)
            response = requests.get(api_url, headers=head, timeout=(10, 10))
            res["status_code"] = response.status_code
            if response.status_code == 200:
                json_response = json.loads(response._content)
                res["object_class"] = objectclass
                if objectclass == "Publication":
                    res["content"] = json_response.get("content", None)
                    res["title"] = json_response.get("title", None)
                    res["subheading"] = json_response.get("subheading", None)
                    res["preview_image"] = json_response.get("preview_image", None)
                    res["presentation_image"] = json_response.get("presentation_image", None)
                else:
                    res["name"] = json_response.get("name", None)
                    res["content"] = UNICMS_ROOT_URL + json_response.get("get_full_path", None)
        except requests.exceptions.RequestException:
            pass
        finally:
            return Response(res)


# Lock
class LockView(APIView):
    description = ""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        content_type_id = self.kwargs['content_type_id']
        object_id = self.kwargs['object_id']
        lock = get_lock_from_cache(content_type_id, object_id)
        if lock[0] and not lock[0] == request.user.pk: # pragma: no cover
            owner_user = get_user_model().objects.filter(pk=lock[0]).first()
            return Response({'lock': lock,
                             'message': LOCK_MESSAGE.format(user=owner_user,
                                                            ttl=lock[1])})
        return Response({})


class LockSetView(APIView):
    description = ""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        content_type_id = request.data.get('content_type_id', None)
        object_id = request.data.get('object_id', None)

        if not all([content_type_id, object_id]):
            raise Http404

        ct = get_object_or_404(ContentType, pk=content_type_id)
        obj = get_object_or_404(ct.model_class(), pk=object_id)

        try:
            permissions_and_offices = obj.get_user_permissions_and_offices(request.user)
            if not permissions_and_offices['permissions']['lock']:
                raise PermissionDenied()

            acquire_lock(user_id=request.user.pk,
                        content_type_id=content_type_id,
                        object_id=object_id)
            return Response({'message': _('Lock successfully set')})

        except AttributeError:
            raise PermissionDenied()

        except LockCannotBeAcquiredException as lock_exception:
            return Response({'lock': lock_exception.lock,
                             'message': LOCK_MESSAGE.format(user=get_user_model().objects.filter(pk=lock_exception.lock[0]).first(),
                                                            ttl=lock_exception.lock[1])})
