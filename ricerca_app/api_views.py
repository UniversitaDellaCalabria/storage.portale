

from django.http import QueryDict
from rest_framework import generics, permissions


from .filters import *
from .serializers import *
from .services import *
from .pagination import UnicalStorageApiPagination


# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS

class ApiResourceList(generics.ListCreateAPIView):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    allowed_methods = ('GET',)

    def perform_create(self, serializer):
        serializer.save(user_ins=self.request.user)


class ApiResourceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    allowed_methods = ('GET',)

    def perform_update(self, serializer):
        serializer.save(user_mod=self.request.user)


# =================================================


class ApiPersonaleList(ApiResourceList):
    description = 'Available Personale, Professors and Researchers'
    queryset = Personale.objects.all()
    serializer_class = PersonaleSerializer


class ApiPersonaleDetail(ApiResourceDetail):
    description = 'Detail of Persona'
    queryset = Personale.objects.all()
    serializer_class = PersonaleSerializer


# =================================================

class ApiRicercaAster1List(ApiResourceList):
    description = 'Available Aster 1'
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer


class ApiRicercaAster1Detail(ApiResourceDetail):
    description = 'Aster 1 Details'
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer


# =================================================

class ApiRicercaAster2List(ApiResourceList):
    description = 'Available Aster 2'
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer


class ApiRicercaAster2Detail(ApiResourceDetail):
    description = 'Aster 2 Details'
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer


# =================================================

class ApiRicercaErc1List(ApiResourceList):
    description = 'Available Erc 1'
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer


class ApiRicercaErc1Detail(ApiResourceDetail):
    description = 'Erc 1 Details'
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer


# =================================================

class ApiRicercaErc2List(ApiResourceList):
    description = 'Available Erc 2'
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer


class ApiRicercaErc2Detail(ApiResourceDetail):
    description = 'Erc 2 Details'
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer


# =================================================

class ApiRicercaDocenteGruppoList(ApiResourceList):
    description = 'List of Professors/Researchers in which Research Groups'
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer


class ApiRicercaDocenteGruppoDetail(ApiResourceDetail):
    description = 'Details of Professors/Researchers in which Research Groups'
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer


# =================================================

class ApiRicercaDocenteLineaApplicataList(ApiResourceList):
    description = 'List of Professors/Researchers and Applied Lines'
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer


class ApiRicercaDocenteLineaApplicataDetail(ApiResourceDetail):
    description = 'Details of a Professor/Researcher in an Applied Line'
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer


# =================================================

class ApiRicercaDocenteLineaBaseList(ApiResourceList):
    description = 'List of Base Lines'
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer


class ApiRicercaDocenteLineaBaseDetail(ApiResourceDetail):
    description = 'Details about a Base Line'
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer


# =================================================

class ApiRicercaGruppoList(ApiResourceList):
    description = 'List of Research Groups'
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer


class ApiRicercaGruppoDetail(ApiResourceDetail):
    description = 'Details of a Research Group'
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer


# =================================================

class ApiRicercaLineaApplicataList(ApiResourceList):
    description = 'List of Applied Lines'
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer


class ApiRicercaLineaApplicataDetail(ApiResourceDetail):
    description = 'Detail of an Applied Line'
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer


# =================================================

class ApiRicercaLineaBaseList(ApiResourceList):
    description = 'List of Base Lines'
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer


class ApiRicercaLineaBaseDetail(ApiResourceDetail):
    description = 'Details of a Base Line'
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


class ApiEndpoint(generics.GenericAPIView):
    pagination_class = UnicalStorageApiPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None

    def get(self, obj):
        self.language = str(
            self.request.query_params.get(
                'language', 'it')).lower()
        queryset = self.get_queryset()

        # TODO: pagination custom
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        results = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(results)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'language': self.language})
        return context


# ----CdS----

class ApiCdSList(ApiEndpoint):
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


class ApiCdSInfo(ApiEndpoint):
    description = 'Restituisce le informazioni di uno specifico' \
                  ' Corso di Studio che sono contenute nelle tabelle' \
                  ' DIDATTICA_REGOLAMENTO e DIDATTICA_TESTI_REGOLAMENTO' \
                  ' nella lingua indicata (in mancanza, si restituiscono' \
                  ' dati in inglese per altre lingue straniere o, se non' \
                  ' presenti, in italiano)'
    serializer_class = CdsInfoSerializer
    filter_backends = [ApiCdsInfoFilter]

    # [?] Required Parameters (e.g. cdsid in this case), handle via urls?
    def get_queryset(self):
        cdsid_param = self.request.query_params.get('cdsid')
        if not cdsid_param:
            return None

        res = ServiceDidatticaCds.cdslist(
            self.language, QueryDict(
                'regdid_id=' + cdsid_param))
        res = list(res)

        if(len(res) == 0):
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

        res[0]['DESC_COR_BRE'] = None
        res[0]['OBB_SPEC'] = None
        res[0]['REQ_ACC'] = None
        res[0]['REQ_ACC_2'] = None
        res[0]['PROFILO'] = None
        res[0]['PROVA_FINALE'] = None
        res[0]['PROVA_FINALE_2'] = None

        for text in texts:
            if text['tipo_testo_regdid_cod'] != 'FUNZIONI' and text['tipo_testo_regdid_cod'] != 'COMPETENZE' and text['tipo_testo_regdid_cod'] != 'SBOCCHI':
                res[0][text['tipo_testo_regdid_cod']] = text[
                    f'clob_txt_{self.language == "it" and "ita" or "eng"}']
            else:
                if text[f'{ self.language == "it" and "profilo" or "profilo_eng" }'] != last_profile:
                    last_profile = text[f'{self.language == "it" and "profilo" or "profilo_eng"}']
                    list_profiles[last_profile] = {}
                list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                            ] = text[f'clob_txt_{self.language == "it" and "ita" or "eng"}']

        res[0]['PROFILO'] = list_profiles
        return res


class ApiCdSStudyPlans(ApiEndpoint):
    description = 'Restituisce un elenco di Piani di Studio'
    serializer_class = CdSStudyPlansSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        cdsid_param = self.request.query_params.get('cdsid')
        if not cdsid_param:
            return None

        return ServiceDidatticaAttivitaFormativa.getListAttivitaFormativa(
            regdid_id=cdsid_param)


class ApiStudyPlansActivities(ApiEndpoint):
    description = 'Restituisce l’elenco degli insegnamenti' \
                  ' di un Piano di Studio con info sintetiche'
    serializer_class = StudyPlansActivitiesSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        studyplanid_param = self.request.query_params.get('studyplanid')
        if not studyplanid_param:
            return None

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid_param)


class ApiStudyActivityInfo(ApiEndpoint):
    description = 'Restituisce le informazioni' \
                  ' dettagliate su un singolo “Insegnamento”'
    serializer_class = StudyActivityInfoSerializer
    filter_backends = [ApiStudyActivityInfoFilter]

    def get_queryset(self):
        studyactivityid = self.request.query_params.get('studyactivityid')
        if not studyactivityid:
            return None

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language)


class ApiCdSMainTeachers(ApiEndpoint):
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


class ApiTeacherResearchGroups(ApiEndpoint):
    description = 'La funzione restituisce l’elenco ' \
                  'dei gruppi di ricerca del docente ordinati per nome.'
    serializer_class = TeacherResearchGroupsSerializer
    filter_backends = [ApiTeacherResearchGroupsFilter]

    def get_queryset(self):
        teacher_id = self.request.query_params.get('teacherid')
        if not teacher_id:
            return None

        return ServiceDocente.getResearchGroups(teacher_id)


class ApiTeacherResearchLines(ApiEndpoint):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca del docente ordinati ' \
                  'per Tipo (applicata/di base) e Nome.'
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = [ApiTeacherResearchLinesFilter]

    def get_queryset(self):
        teacher_id = self.request.query_params.get('teacherid')
        if not teacher_id:
            return None
        return ServiceDocente.getResearchLines(teacher_id)


# ----Docenti----

class ApiTeachersList(ApiEndpoint):
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


class ApiTeacherStudyActivities(ApiEndpoint):
    description = 'La funzione restituisce l’elenco degli insegnamenti' \
                  ' (per gli ultimi anni) ordinati per anno e nome' \
                  ' dell’insegnamento.'
    serializer_class = TeacherStudyActivitiesSerializer
    filter_backends = [ApiTeacherStudyActivitiesFilter]

    def get_queryset(self):
        teacher = self.request.query_params.get('teacherid')
        if not teacher:
            return None
        year = self.request.query_params.get('year')
        yearFrom = self.request.query_params.get('yearFrom')
        yearTo = self.request.query_params.get('yearTo')

        return ServiceDocente.getAttivitaFormativeByDocente(
            teacher, year, yearFrom, yearTo)


class ApiTeacherInfo(ApiEndpoint):
    description = 'La funzione restituisce la scheda informativa' \
                  ' dettagliata di un docente'
    serializer_class = TeacherInfoSerializer
    filter_backends = [ApiTeacherInfoFilter]

    def get_queryset(self):
        teacher = self.request.query_params.get('teacherid')
        if not teacher:
            return None

        return ServiceDocente.getDocenteInfo(teacher)

# ----Dottorati----


class ApiDoctoratesList(ApiEndpoint):
    description = 'La funzione restituisce una lista di dottorati'
    serializer_class = DoctoratesListSerializer
    filter_backends = [ApiDoctoratesListFilter]

    def get_queryset(self):
        return ServiceDottorato.getDoctorates(self.request.query_params)
