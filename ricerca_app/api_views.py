

from rest_framework import generics, permissions
from rest_framework.response import Response

from .filters import *
from .models import DidatticaTestiRegolamento
from .serializers import *
from .services import *
from .pagination import UnicalStorageApiPaginationList


# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS
from .utils import encode_labels


class ApiEndpointList(generics.GenericAPIView):
    pagination_class = UnicalStorageApiPaginationList
    permission_classes = [permissions.AllowAny]
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

        if queryset is not None:
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


class ApiCdSList(ApiEndpointList):
    description = 'Restituisce un elenco di Corsi di studio con un set' \
                  ' minimo di informazioni. Opera su ' \
                  '“DIDATTICA_REGOLAMENTO” e restituisce tutti i record' \
                  ' che corrispondono ai parametri impostati in input, ' \
                  'ordinati secondo il parametro indicato, nella lingua' \
                  ' selezionata (in mancanza, per le lingue straniere si' \
                  ' restituiscono dati in inglese o, se non presenti,' \
                  ' in italiano)'
    serializer_class = CdSListSerializer
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
    filter_backends = [ApiCdsInfoFilter]

    def get_queryset(self):
        cdsid_param = self.kwargs['cdsid']
        res = DidatticaCds.objects.filter(
            didatticaregolamento__regdid_id=cdsid_param)
        langs = res.prefetch_related('didatticacdslingua')

        res = res.values(
            'didatticaregolamento__regdid_id',
            'didatticaregolamento__aa_reg_did',
            'didatticaregolamento__frequenza_obbligatoria',
            'dip__dip_cod',
            'dip__dip_des_it',
            'dip__dip_des_eng',
            'cds_cod',
            'cdsord_id',
            'nome_cds_it',
            'nome_cds_eng',
            'tipo_corso_cod',
            'cla_miur_cod',
            'cla_miur_des',
            'durata_anni',
            'valore_min',
            'codicione',
            'didatticaregolamento__stato_regdid_cod').distinct()
        res = list(res)

        if len(res) == 0:
            return None

        texts = DidatticaTestiRegolamento.objects.filter(
            regdid=cdsid_param) .values(
            'regdid__regdid_id',
            'clob_txt_ita',
            'clob_txt_eng',
            'tipo_testo_regdid_cod',
            'profilo',
            'profilo_eng')

        list_profiles = {}
        last_profile = ""

        res[0]['Languages'] = langs.values(
            "didatticacdslingua__lingua_des_it",
            "didatticacdslingua__lingua_des_eng").distinct()

        res[0]['URL_CDS_DOC'] = None
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
                if text['clob_txt_eng'] is None and self.language == "en":
                    res[0][text['tipo_testo_regdid_cod']] = text['clob_txt_ita']
                else:
                    res[0][text['tipo_testo_regdid_cod']] = text[
                        f'clob_txt_{self.language == "it" and "ita" or "eng"}']

            else:
                if self.language == "en" and text["profilo_eng"] is None:
                    if text["profilo"] != last_profile:
                        last_profile = text["profilo"]
                        list_profiles[last_profile] = {}
                elif text[f'{ self.language == "it" and "profilo" or "profilo_eng" }'] != last_profile:
                    last_profile = text[f'{self.language == "it" and "profilo" or "profilo_eng"}']
                    list_profiles[last_profile] = {}

                if text["clob_txt_eng"] is None and self.language == "en":
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text["clob_txt_ita"]
                else:
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text[f'clob_txt_{self.language == "it" and "ita" or "eng"}']
        res[0]['PROFILO'] = list_profiles
        return res


class ApiCdSStudyPlansList(ApiEndpointList):
    description = 'Restituisce un elenco di Piani di Studio'
    serializer_class = CdSStudyPlansSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        cdsid_param = str(self.kwargs['cdsid'])

        return ServiceDidatticaAttivitaFormativa.getStudyPlans(
            regdid_id=cdsid_param)


class ApiStudyPlanDetail(ApiEndpointDetail):
    description = 'Restituisce i dettagli su un singolo piano di studi'
    serializer_class = CdSStudyPlanSerializer
    filter_backends = [ApiStudyPlanDetailFilter]

    def get_queryset(self):
        studyplanid = str(self.kwargs['studyplanid'])

        return ServiceDidatticaAttivitaFormativa.getStudyPlan(
            studyplanid=studyplanid)


class ApiStudyPlanActivitiesList(ApiEndpointList):
    description = 'Restituisce l’elenco degli insegnamenti' \
                  ' di un Piano di Studio con info sintetiche'
    serializer_class = StudyPlansActivitiesSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        studyplanid_param = str(self.kwargs['studyplanid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid_param)


class ApiStudyActivityDetail(ApiEndpointDetail):
    description = 'Restituisce le informazioni' \
                  ' dettagliate su un singolo “Insegnamento”'
    serializer_class = StudyActivityInfoSerializer
    filter_backends = [ApiStudyActivityInfoFilter]

    def get_queryset(self):
        studyactivityid = str(self.kwargs['studyactivityid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language)


class ApiCdSMainTeachersList(ApiEndpointList):
    description = 'Fornisce l’elenco dei docenti di riferimento' \
                  ' (o di tutti i docenti ???) associati ad un CdS.' \
                  ' Per ogni docente riporta poche informazioni' \
                  ' identificative: Nome, Ruolo, Settore scientifico' \
                  ' disciplinare, …'
    serializer_class = CdSMainTeachersSerializer
    filter_backends = [ApiCdSMainTeachersFilter]

    def get_queryset(self):
        regdid_id = self.request.query_params.get('cdsid')
        if not regdid_id:
            return None

        return ServiceDidatticaAttivitaFormativa.getDocentiPerReg(regdid_id)

# ----Ricerca----


class ApiTeacherResearchGroupsList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco ' \
                  'dei gruppi di ricerca del docente ordinati per nome.'
    serializer_class = TeacherResearchGroupsSerializer
    filter_backends = [ApiTeacherResearchGroupsFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

        return ServiceDocente.getResearchGroups(teacher_id)


class ApiTeacherResearchLinesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca del docente ordinati ' \
                  'per Tipo (applicata/di base) e Nome.'
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = [ApiTeacherResearchLinesFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

        return ServiceDocente.getResearchLines(teacher_id)


# ----Docenti----

class ApiTeachersList(ApiEndpointList):
    description = 'Restituisce un elenco di Docenti con un set minimo di ' \
                  'informazioni identificative: Nome, Ruolo, ' \
                  'Settore scientifico disciplinare, …'
    serializer_class = TeachersListSerializer
    filter_backends = [ApiTeachersListFilter]

    def get_queryset(self):
        regdid = self.request.query_params.get('cdsid')
        dip = self.request.query_params.get('departmentid')
        role = self.request.query_params.get('role')

        return ServiceDocente.teachersList(regdid, dip, role)


class ApiTeacherStudyActivitiesList(ApiEndpointList):
    description = 'La funzione restituisce l’elenco degli insegnamenti' \
                  ' (per gli ultimi anni) ordinati per anno e nome' \
                  ' dell’insegnamento.'
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [ApiTeacherStudyActivitiesFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']
        year = self.request.query_params.get('year')
        yearFrom = self.request.query_params.get('yearFrom')
        yearTo = self.request.query_params.get('yearTo')

        return ServiceDocente.getAttivitaFormativeByDocente(
            teacher_id, year, yearFrom, yearTo)


class ApiTeacherDetail(ApiEndpointDetail):
    description = 'La funzione restituisce la scheda informativa' \
                  ' dettagliata di un docente'
    serializer_class = TeacherInfoSerializer
    filter_backends = [ApiTeacherInfoFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

        return ServiceDocente.getDocenteInfo(teacher_id)

# ----Dottorati----


class ApiDoctoratesList(ApiEndpointList):
    description = 'La funzione restituisce una lista di dottorati'
    serializer_class = DoctoratesListSerializer
    filter_backends = [ApiDoctoratesListFilter]

    def get_queryset(self):
        return ServiceDottorato.getDoctorates(self.request.query_params)

# ---- Tipologie Lauree ----


class ApiDegreeTypesList(ApiEndpointList):
    description = 'La funzione restituisce la lista delle tipologie di lauree'
    serializer_class = DegreeTypesListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getDegreeTypes()


# ---- Dipartimenti ----


class ApiDepartmentsList(ApiEndpointList):
    description = 'La funzione restituisce la lista dei dipartimenti'
    serializer_class = DepartmentsListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDipartimento.getDepartmentsList(self.language)


class ApiDepartmentDetail(ApiEndpointDetail):
    description = 'La funzione restituisce uno specifico dipartimento'
    serializer_class = DepartmentsListSerializer
    filter_backends = [ApiDoctoratesListFilter]

    def get_queryset(self):
        departmentid = self.kwargs['departmentid']
        return ServiceDipartimento.getDepartment(departmentid)


class ApiAddressbookList(ApiEndpointList):
    description = 'La funzione restituisce la rubrica telefonica del personale'
    serializer_class = AddressbookListSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        keywords = self.request.query_params.get('keywords')
        structureid = self.request.query_params.get('structureid')
        roles = self.request.query_params.get('roles')
        return ServicePersonale.getAddressbook(keywords, structureid, roles)


class ApiStructuresList(ApiEndpointListSupport):
    description = 'La funzione restituisce le strutture organizzative'
    serializer_class = StructuresListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServicePersonale.getStructuresList()


class ApiStructureTypesList(ApiEndpointList):
    description = 'La funzione restituisce le tipologie di strutture organizzative'
    serializer_class = StructureTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServicePersonale.getStructureTypes()


class ApiAcademicYearsList(ApiEndpointListSupport):
    description = 'La funzione restituisce gli anni accademici'
    serializer_class = AcademicYearsListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getAcademicYears()

# Api che definisce il dettaglio della struttura, al momento è stato bloccato
# class ApiStructureDetail(ApiEndpointDetail):
#     description = 'La funzione restituisce una specifica struttura'
#     serializer_class = StructuresListSerializer
#     filter_backends = [ApiStructuresListFilter]
#
#     def get_queryset(self):
#         structureid = self.kwargs['structureid']
#         return ServicePersonale.getStructure(structureid)


class ApiRolesList(ApiEndpointListSupport):
    description = 'La funzione restituisce i ruoli'
    serializer_class = RolesListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDocente.getRoles()


class ApiPersonaleDetail(ApiEndpointDetail):
    description = 'La funzione restituisce una specifica persona'
    serializer_class = AddressbookListSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        personale_id = self.kwargs['personaleid']

        return ServicePersonale.getPersonale(personale_id)
