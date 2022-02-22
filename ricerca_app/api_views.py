from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView


from .filters import *
from .models import DidatticaTestiRegolamento, DidatticaCdsAltriDati, DidatticaCdsAltriDatiUfficio
from .serializers import *
from .services import *
from .pagination import UnicalStorageApiPaginationList


# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS
from .utils import encode_labels, encrypt, decrypt



class ApiEndpointList(generics.ListAPIView):
    pagination_class = UnicalStorageApiPaginationList
    permission_classes = [permissions.AllowAny]
    # filter_backends = [OrderingFilter]
    # ordering_fields = '__all__'
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None

    def get(self, obj, **kwargs):
        self.language = str(
            self.request.query_params.get(
                'lang', 'null')).lower()
        if self.language == 'null':
            self.language = self.request.LANGUAGE_CODE

        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        results = self.paginate_queryset(serializer.data)
        results = {
            'data': results,
            'language': self.language,
        }
        return self.get_paginated_response(results)

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
        return ServiceDidatticaCds.cdslist(
            self.language, self.request.query_params)


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
        cdsid_param = self.kwargs['regdidid']
        res = DidatticaCds.objects.filter(
            didatticaregolamento__regdid_id=cdsid_param)
        langs = res.prefetch_related('didatticacdslingua')

        res = res.values(
            'didatticaregolamento__regdid_id',
            'didatticaregolamento__aa_reg_did',
            'didatticaregolamento__frequenza_obbligatoria',
            'dip__dip_id',
            'dip__dip_cod',
            'dip__dip_des_it',
            'dip__dip_des_eng',
            'cds_id',
            'cds_cod',
            'cdsord_id',
            'nome_cds_it',
            'nome_cds_eng',
            'tipo_corso_cod',
            'tipo_corso_des',
            'cla_miur_cod',
            'cla_miur_des',
            'intercla_miur_cod',
            'intercla_miur_des',
            'durata_anni',
            'valore_min',
            'codicione',
            'didatticaregolamento__titolo_congiunto_cod',
            'didatticaregolamento__stato_regdid_cod',
            'area_cds',
            'area_cds_en',
        ).distinct()
        res = list(res)

        if len(res) == 0:
            return None

        texts = DidatticaTestiRegolamento.objects.filter(
            regdid=cdsid_param).values(
            'regdid__regdid_id',
            'clob_txt_ita',
            'clob_txt_eng',
            'testo_regdid_url',
            'tipo_testo_regdid_cod',
            'profilo',
            'profilo_eng')

        list_profiles = {}
        last_profile = ""

        res[0]['Languages'] = langs.values(
            "didatticacdslingua__lingua_des_it",
            "didatticacdslingua__lingua_des_eng").distinct()

        res[0]['URL_CDS_DOC'] = None
        res[0]['URL_CDS'] = None
        res[0]['INTRO_CDS_FMT'] = None
        res[0]['URL_CDS_VIDEO'] = None
        res[0]['DESC_COR_BRE'] = None
        res[0]['OBB_SPEC'] = None
        res[0]['REQ_ACC'] = None
        res[0]['REQ_ACC_2'] = None
        res[0]['PROFILO'] = None
        res[0]['PROVA_FINALE'] = None
        res[0]['PROVA_FINALE_2'] = None

        for text in texts:
            if text['tipo_testo_regdid_cod'] != 'FUNZIONI' and text['tipo_testo_regdid_cod'] != 'COMPETENZE' and text['tipo_testo_regdid_cod'] != 'SBOCCHI':
                if (text['clob_txt_eng'] is None and self.language !=
                        "it") or self.language == 'it':
                    res[0][text['tipo_testo_regdid_cod']] = text['clob_txt_ita']
                else:
                    res[0][text['tipo_testo_regdid_cod']] = text['clob_txt_eng']
            else:
                if (self.language !=
                        "it" and text["profilo_eng"] is None) or self.language == 'it':
                    if text["profilo"] != last_profile:
                        last_profile = text["profilo"]
                        list_profiles[last_profile] = {}
                elif text[f'{ self.language == "it" and "profilo" or "profilo_eng" }'] != last_profile:
                    last_profile = text[f'{self.language == "it" and "profilo" or "profilo_eng"}']
                    list_profiles[last_profile] = {}

                if (text["clob_txt_eng"] is None and self.language !=
                        "it") or self.language == 'it':
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text["clob_txt_ita"]
                else:
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text['clob_txt_eng']
        res[0]['PROFILO'] = list_profiles

        res[0]['OtherData'] = DidatticaCdsAltriDati.objects.filter(cds_id=res[0]['cds_id']).values(
            'matricola_coordinatore',
            'nome_origine_coordinatore',
            'matricola_vice_coordinatore',
            'nome_origine_vice_coordinatore',
            'num_posti',
            'modalita_iscrizione'
        ).distinct()

        res[0]['OfficesData'] = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=res[0]['cds_id']).values(
            'ordine',
            'nome_ufficio',
            'matricola_riferimento',
            'nome_origine_riferimento',
            'telefono',
            'email',
            'edificio',
            'piano',
            'orari',
            'sportello_online'
        ).distinct()

        return res


class ApiCdSStudyPlansList(ApiEndpointList):
    description = 'Restituisce un elenco di Piani di Studio'
    serializer_class = CdSStudyPlansSerializer
    filter_backends = []

    def get_queryset(self):
        cdsid_param = str(self.kwargs['regdidid'])

        return ServiceDidatticaAttivitaFormativa.getStudyPlans(
            regdid_id=cdsid_param)


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

        search = self.request.query_params.get('search')
        teacher = decrypt(self.request.query_params.get('teacher'))
        department = self.request.query_params.get('department')
        cod = self.request.query_params.get('coderc1')

        return ServiceDocente.getAllResearchGroups(search, teacher, department, cod)


class ApiTeacherResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca del docente ordinati ' \
                  'per Tipo (applicata/di base) e Nome.'
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = []

    def get_queryset(self):
        teacherid = decrypt(self.kwargs['teacherid'])

        return ServiceDocente.getResearchLines(teacherid)


class ApiBaseResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca di base'
    serializer_class = BaseResearchLinesSerializer
    filter_backends = [ApiBaseResearchLinesListFilter]

    def get_queryset(self):

        search = self.request.query_params.get('search')
        teacher = decrypt(self.request.query_params.get('teacher'))
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')

        return ServiceDocente.getBaseResearchLines(
            search, teacher, department, year)


class ApiAppliedResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca applicate'
    serializer_class = AppliedResearchLinesSerializer
    filter_backends = [ApiAppliedResearchLinesListFilter]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        teacher = decrypt(self.request.query_params.get('teacher'))
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')

        return ServiceDocente.getAppliedResearchLines(
            search, teacher, department, year)


class ApiAllResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco di tutte le Linee di' \
                  ' ricerca'
    serializer_class = AllResearchLinesSerializer
    filter_backends = [ApiAllResearchLinesListFilter]

    def get_queryset(self):

        search = self.request.query_params.get('search')
        year = self.request.query_params.get('year')
        department = self.request.query_params.get('department')
        ercs = self.request.query_params.get('ercs')
        asters = self.request.query_params.get('asters')
        exclude_base = self.request.query_params.get('exclude_base')
        exclude_applied = self.request.query_params.get('exclude_applied')



        return ServiceDocente.getAllResearchLines(search, year, department, ercs, asters, exclude_base, exclude_applied)

# ----Docenti----


class ApiTeachersList(ApiEndpointList):
    description = 'Restituisce un elenco di Docenti che hanno una copertura attiva in ateneo, con un set minimo di ' \
                  'informazioni identificative: Nome, Ruolo, ' \
                  'Settore scientifico disciplinare, …'
    serializer_class = TeachersSerializer
    filter_backends = [ApiTeachersListFilter]

    def get_queryset(self):

        search = self.request.query_params.get('search')
        regdidid = self.request.query_params.get('regdid')
        department = self.request.query_params.get('department')
        role = self.request.query_params.get('role')
        cds = self.request.query_params.get('cds')

        return ServiceDocente.teachersList(
            search, regdidid, department, role, cds)


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

        search = self.request.query_params.get('search')
        regdidid = self.request.query_params.get('regdid')
        department = self.request.query_params.get('department')
        role = self.request.query_params.get('role')
        cds = self.request.query_params.get('cds')

        return ServiceDocente.teachingCoveragesList(
            search, regdidid, department, role, cds)


class ApiTeacherStudyActivitiesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco degli insegnamenti' \
                  ' (per gli ultimi anni) ordinati per anno e nome' \
                  ' dell’insegnamento.'
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [ApiTeacherStudyActivitiesFilter]

    def get_queryset(self):
        teacherid = decrypt(self.kwargs['teacherid'])
        year = self.request.query_params.get('year')
        yearFrom = self.request.query_params.get('yearFrom')
        yearTo = self.request.query_params.get('yearTo')

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


class TeachingCoveragesInfo(AutoSchema):
    def get_operation_id(self, path, method):
        return 'retrieveTeachingCoverageInfo'


class ApiTeachingCoverageDetail(ApiTeacherDetail):
    schema = TeachingCoveragesInfo()


# ----Dottorati----


class ApiDoctoratesList(ApiEndpointList):
    description = 'La funzione restituisce una lista di dottorati'
    serializer_class = DoctoratesSerializer
    filter_backends = [ApiDoctoratesListFilter]

    def get_queryset(self):
        return ServiceDottorato.getDoctorates(self.request.query_params)

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


class DepartmentsFilterList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'ApiDepartmentsFilterList'


class ApiDepartmentsFilterList(ApiEndpointListSupport):
    description = 'La funzione restituisce la lista dei dipartimenti senza paginazione'
    serializer_class = DepartmentSerializer
    filter_backends = []
    schema = DepartmentsFilterList()

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
        search = self.request.query_params.get('search')
        structureid = self.request.query_params.get('structure')
        structuretypes = self.request.query_params.get('structuretypes')
        roles = self.request.query_params.get('role')
        structuretree = self.request.query_params.get('structuretree')

        return ServicePersonale.getAddressbook(
            search, structureid, structuretypes, roles, structuretree)


class ApiStructuresList(ApiEndpointList):
    description = 'La funzione restituisce le strutture organizzative'
    serializer_class = StructuresSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        father = self.request.query_params.get('father')
        type = self.request.query_params.get('type')

        return ServicePersonale.getStructuresList(search, father, type)


class StructuresFilterList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'ApiStructuresFilterList'


class ApiStructuresFilterList(ApiEndpointListSupport):
    description = 'La funzione restituisce le strutture organizzative senza paginazione'
    serializer_class = StructuresSerializer
    filter_backends = [ApiStructuresListFilter]
    schema = StructuresFilterList()

    def get_queryset(self):

        father = self.request.query_params.get('father')

        type = self.request.query_params.get('type')

        return ServicePersonale.getStructuresList(father=father, type=type)


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


class ApiLaboratoryDetail(ApiEndpointDetail):
    description = 'La funzione restituisce un laboratorio specifico'
    serializer_class = LaboratoryDetailSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        laboratoryid = self.kwargs['laboratoryid']

        return ServiceLaboratorio.getLaboratory(self.language, laboratoryid)


class ApiLaboratoriesList(ApiEndpointList):
    description = 'La funzione restituisce i laboratori'
    serializer_class = LaboratoriesSerializer
    filter_backends = [ApiLaboratoriesListFilter]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        area = self.request.query_params.get('area')
        department = self.request.query_params.get('department')
        erc1 = self.request.query_params.get('erc1')
        teacher = decrypt(self.request.query_params.get('teacher'))
        infrastructure = self.request.query_params.get('infrastructure')
        scope = self.request.query_params.get('scope')

        return ServiceLaboratorio.getLaboratoriesList(
            self.language, search, area, department, erc1, teacher, infrastructure, scope)


class ApiLaboratoriesAreasList(ApiEndpointList):
    description = 'La funzione restituisce la lista degli ambiti dei laboratori'
    serializer_class = LaboratoriesAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceLaboratorio.getLaboratoriesAreasList()


class ApiErc1List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli erc1'
    serializer_class = Erc1Serializer
    filter_backends = [ApiErc1ListFilter]

    def get_queryset(self):

        laboratory = self.request.query_params.get('laboratory')

        return ServiceLaboratorio.getErc1List(laboratory)


class ApiErc2List(ApiEndpointList):
    description = 'La funzione restituisce la lista degli erc2'
    serializer_class = Erc2Serializer
    filter_backends = []

    def get_queryset(self):

        return ServiceLaboratorio.getErc2List()


class Erc1FilterList(AutoSchema):
    def get_operation_id(self, path, method):
        return 'ApiErc1FilterList'


class ApiErc1FilterList(ApiEndpointListSupport):
    description = 'La funzione restituisce la lista degli erc1 senza paginazione'
    serializer_class = Erc1Serializer
    filter_backends = [ApiErc1ListFilter]
    schema = Erc1FilterList()

    def get_queryset(self):

        laboratory = self.request.query_params.get('laboratory')

        return ServiceLaboratorio.getErc1List(laboratory)


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
        teacherid = decrypt(self.kwargs.get('teacherid')) if self.kwargs.get('teacherid') else ''
        search = self.request.query_params.get('search')
        year = self.request.query_params.get('year')
        type = self.request.query_params.get('type')
        structure = self.request.query_params.get('structure')

        return ServiceDocente.getPublicationsList(
            teacherid, search, year, type, structure)


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

        search = self.request.query_params.get('search')
        father = self.request.query_params.get('father')
        type = self.request.query_params.get('type')

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

        search = self.request.query_params.get('search')
        techarea = self.request.query_params.get('techarea')
        structure = self.request.query_params.get('structure')

        return ServiceBrevetto.getPatents(search, techarea, structure)


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

        search = self.request.query_params.get('search')
        techarea = self.request.query_params.get('techarea')
        spinoff = self.request.query_params.get('spinoff')
        startup = self.request.query_params.get('startup')

        return ServiceCompany.getCompanies(search, techarea, spinoff, startup)


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

        search = self.request.query_params.get('search')
        techarea = self.request.query_params.get('techarea')
        infrastructure = self.request.query_params.get('infrastructure')
        programtype = self.request.query_params.get('programtype')
        territorialscope = self.request.query_params.get('territorialscope')
        notprogramtype = self.request.query_params.get('-programtype')


        return ServiceProgetto.getProjects(
            search, techarea, infrastructure, programtype, territorialscope, notprogramtype)


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

        search = self.request.query_params.get('search')
        director = self.request.query_params.get('director')
        coursetype = self.request.query_params.get('coursetype')
        erogation = self.request.query_params.get('erogation')
        department = self.request.query_params.get('department')


        return ServiceDidatticaCds.getHighFormationMasters(search, director, coursetype, erogation, department)


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


class ApiCourseTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei tipi di corso'
    serializer_class = CourseTypesSerializer
    filter_backends = []

    def get_queryset(self):

        return ServiceDidatticaCds.getCourseTypes()


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