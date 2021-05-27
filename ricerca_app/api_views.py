

from django.http import QueryDict
from rest_framework import generics, permissions


from .filters import *
from .models import DidatticaTestiRegolamento
from .serializers import *
from .services import *
from .pagination import UnicalStorageApiPagination


# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS

class ApiEndpoint(generics.GenericAPIView):
    pagination_class = UnicalStorageApiPagination
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None

    def get(self, obj, **kwargs):
        self.language = str(
            self.request.query_params.get(
                'language', 'it')).lower()
        queryset = self.get_queryset()

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


class ApiCdSDetail(ApiEndpoint):
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
        res = ServiceDidatticaCds.cdslist(
            self.language, QueryDict(
                'regdid_id=' + str(cdsid_param)))
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


class ApiCdSStudyPlansList(ApiEndpoint):
    description = 'Restituisce un elenco di Piani di Studio'
    serializer_class = CdSStudyPlansSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        cdsid_param = str(self.kwargs['cdsid'])

        return ServiceDidatticaAttivitaFormativa.getListAttivitaFormativa(
            regdid_id=cdsid_param)


class ApiCdSStudyPlansUniqueList(ApiEndpoint):
    description = 'Restituisce un elenco di Piani di Studio senza attività formative correlate'
    serializer_class = CdSStudyPlansUniqueSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        cdsid_param = str(self.kwargs['cdsid'])

        return ServiceDidatticaAttivitaFormativa.getStudyPlans(
            regdid_id=cdsid_param)


class ApiStudyPlanActivitiesList(ApiEndpoint):
    description = 'Restituisce l’elenco degli insegnamenti' \
                  ' di un Piano di Studio con info sintetiche'
    serializer_class = StudyPlansActivitiesSerializer
    filter_backends = [ApiCdSStudyPlansFilter]

    def get_queryset(self):
        studyplanid_param = str(self.kwargs['studyplanid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
            studyplanid=studyplanid_param)


class ApiStudyActivityDetail(ApiEndpoint):
    description = 'Restituisce le informazioni' \
                  ' dettagliate su un singolo “Insegnamento”'
    serializer_class = StudyActivityInfoSerializer
    filter_backends = [ApiStudyActivityInfoFilter]

    def get_queryset(self):
        studyactivityid = str(self.kwargs['studyactivityid'])

        return ServiceDidatticaAttivitaFormativa.getAttivitaFormativaWithSubModules(
            af_id=studyactivityid, language=self.language)


class ApiCdSMainTeachersList(ApiEndpoint):
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


class ApiTeacherResearchGroupsList(ApiEndpoint):
    description = 'La funzione restituisce l’elenco ' \
                  'dei gruppi di ricerca del docente ordinati per nome.'
    serializer_class = TeacherResearchGroupsSerializer
    filter_backends = [ApiTeacherResearchGroupsFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

        return ServiceDocente.getResearchGroups(teacher_id)


class ApiTeacherResearchLinesList(ApiEndpoint):
    description = 'La funzione restituisce l’elenco delle Linee di' \
                  ' ricerca del docente ordinati ' \
                  'per Tipo (applicata/di base) e Nome.'
    serializer_class = TeacherResearchLinesSerializer
    filter_backends = [ApiTeacherResearchLinesFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

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


class ApiTeacherStudyActivitiesList(ApiEndpoint):
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


class ApiTeacherDetail(ApiEndpoint):
    description = 'La funzione restituisce la scheda informativa' \
                  ' dettagliata di un docente'
    serializer_class = TeacherInfoSerializer
    filter_backends = [ApiTeacherInfoFilter]

    def get_queryset(self):
        teacher_id = self.kwargs['teacherid']

        return ServiceDocente.getDocenteInfo(teacher_id)

# ----Dottorati----


class ApiDoctoratesList(ApiEndpoint):
    description = 'La funzione restituisce una lista di dottorati'
    serializer_class = DoctoratesListSerializer
    filter_backends = [ApiDoctoratesListFilter]

    def get_queryset(self):
        return ServiceDottorato.getDoctorates(self.request.query_params)
