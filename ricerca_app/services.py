import datetime
from functools import reduce
import operator

from django.db.models import CharField, Q, Value, Max
from .models import DidatticaCds, DidatticaAttivitaFormativa, \
    DidatticaTestiAf, DidatticaCopertura, Personale, DidatticaDipartimento, DidatticaDottoratoCds, \
    DidatticaPdsRegolamento, \
    UnitaOrganizzativa, DidatticaRegolamento, DidatticaCdsLingua, LaboratorioDatiBase, LaboratorioAttivita, \
    LaboratorioDatiErc1, LaboratorioPersonaleRicerca, LaboratorioPersonaleTecnico, LaboratorioServiziOfferti, \
    LaboratorioUbicazione, FunzioniUnitaOrganizzativa, LaboratorioAltriDipartimenti, PubblicazioneDatiBase, \
    PubblicazioneAutori, PubblicazioneCommunity


class ServiceQueryBuilder:
    @staticmethod
    def build_filter_chain(params_dict, query_params, *args):
        return reduce(operator.and_,
                      [Q(**{v: query_params.get(k)})
                       for (k, v) in params_dict.items() if query_params.get(k)] + list(args),
                      Q())


class ServiceDidatticaCds:
    @staticmethod
    def cdslist(language, query_params):
        didatticacds_params_to_query_field = {
            'courseclassid': 'cla_miur_cod',
            'courseclassname': 'cla_miur_des__icontains',
            # 'courseclassgroup': ... unspecified atm
            'departmentid': 'dip__dip_cod',
            'departmentname': f'dip__dip_des_{language == "it" and "it" or "eng"}__icontains',
        }

        didatticaregolamento_params_to_query_field = {
            'academicyear': 'didatticaregolamento__aa_reg_did__exact',
            'jointdegree': 'didatticaregolamento__titolo_congiunto_cod',
            'regdid_id': 'didatticaregolamento__regdid_id',
        }

        didatticacdslingua_params_to_query_field = {
            'cdslanguage': 'didatticacdslingua__iso6392_cod', }

        keywords = query_params.get('keywords', None)
        if keywords is not None:
            keywords = keywords.split(' ')

        courses_allowed = query_params.get('coursetype', '')
        if courses_allowed != '':
            courses_allowed = courses_allowed.split(",")

        q1 = ServiceQueryBuilder.build_filter_chain(
            didatticacds_params_to_query_field, query_params)
        q2 = ServiceQueryBuilder.build_filter_chain(
            didatticaregolamento_params_to_query_field, query_params)
        q3 = ServiceQueryBuilder.build_filter_chain(
            didatticacdslingua_params_to_query_field, query_params)

        q4 = Q()
        if keywords is None:
            q4 = Q(cds_id__isnull=False)
        else:
            for k in keywords:
                if language == "it":
                    q = Q(nome_cds_it__icontains=k)
                else:
                    q = Q(nome_cds_eng__icontains=k)
                q4 |= q

        if 'academicyear' not in query_params:
            last_active_year = DidatticaCds.objects.filter(
                didatticaregolamento__stato_regdid_cod__exact='A').aggregate(
                Max('didatticaregolamento__aa_reg_did'))['didatticaregolamento__aa_reg_did__max']
            if courses_allowed != '':
                items = DidatticaCds.objects \
                    .filter(q1, q2, q3, q4,
                            didatticacdslingua__lin_did_ord_id__isnull=False,
                            didatticaregolamento__stato_regdid_cod__exact='A',
                            didatticaregolamento__aa_reg_did=last_active_year,
                            tipo_corso_cod__in=courses_allowed)
            else:
                items = DidatticaCds.objects \
                    .filter(q4, q1, q2, q3,
                            didatticacdslingua__lin_did_ord_id__isnull=False,
                            didatticaregolamento__stato_regdid_cod__exact='A',
                            didatticaregolamento__aa_reg_did=last_active_year)
        else:
            if courses_allowed != '':
                items = DidatticaCds.objects \
                    .filter(q4, q1, q2, q3,
                            didatticacdslingua__lin_did_ord_id__isnull=False,
                            tipo_corso_cod__in=courses_allowed)
            else:
                items = DidatticaCds.objects \
                    .filter(q4, q1, q2, q3,
                            didatticacdslingua__lin_did_ord_id__isnull=False)

        items = items.values(
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
            'tipo_corso_des',
            'cla_miur_cod',
            'cla_miur_des',
            'durata_anni',
            'valore_min',
            'codicione',
            'didatticaregolamento__titolo_congiunto_cod',
            'didatticaregolamento__stato_regdid_cod').distinct()
        items = items.order_by(
            "nome_cds_it") if language == 'it' else items.order_by("nome_cds_eng")
        items = list(items)
        for item in items:
            item['Languages'] = DidatticaCdsLingua.objects.filter(
                cdsord_id=item['cdsord_id']).values(
                "lingua_des_it",
                "lingua_des_eng").distinct()

        return items

    @staticmethod
    def getDegreeTypes():
        query = DidatticaCds.objects.values(
            "tipo_corso_cod",
            "tipo_corso_des").order_by('tipo_corso_des').distinct()
        return query

    @staticmethod
    def getAcademicYears():
        query = DidatticaRegolamento.objects.values(
            "aa_reg_did").order_by('-aa_reg_did').distinct()
        return query


class ServiceDidatticaAttivitaFormativa:

    @staticmethod
    def getStudyPlans(regdid_id=None):

        query = DidatticaAttivitaFormativa.objects.filter(regdid=regdid_id)
        query = query.order_by(
            'pds_regdid_id__pds_des_it').values(
            'regdid_id',
            'pds_regdid_id',
            'pds_cod',
            'pds_regdid_id__pds_des_it',
            'pds_regdid_id__pds_des_eng').distinct()
        query = list(query)
        for q in query:
            activities = ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                q['pds_regdid_id'], group=True)
            q['StudyActivities'] = activities  # list(activities)
        return query

    @staticmethod
    def getStudyPlan(studyplanid=None):

        query = DidatticaPdsRegolamento.objects.filter(
            pds_regdid_id=studyplanid)
        query = query.order_by(
            'pds_des_it').values(
            'regdid__regdid_id',
            'pds_regdid_id',
            'pds_cod',
            'pds_des_it',
            'pds_des_eng')
        query = list(query)
        for q in query:
            activities = ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                q['pds_regdid_id'], group=True)
            q['StudyActivities'] = activities  # list(activities)
        return query

    @staticmethod
    def getAttivitaFormativaByStudyPlan(studyplanid, group=False):
        if group:
            total_years = DidatticaPdsRegolamento.objects.filter(pds_regdid_id=studyplanid).values(
                "regdid__cds__durata_anni").first()['regdid__cds__durata_anni']
            final_query = {}
            for i in range(total_years):
                query = DidatticaAttivitaFormativa.objects.filter(
                    pds_regdid__pds_regdid_id=studyplanid, af_id__isnull=False, anno_corso=(i + 1))
                new_query = DidatticaAttivitaFormativa.objects.none()
                for q in query:
                    if q.checkIfMainCourse():
                        new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                            af_id=q.af_id)
                final_query[i + 1] = new_query.order_by(
                    'ciclo_des') .values(
                    'af_id',
                    'des',
                    'af_gen_des_eng',
                    'cds__cds_cod',
                    'regdid__regdid_id',
                    'anno_corso',
                    'ciclo_des',
                    'peso',
                    'sett_des',
                    'freq_obblig_flg',
                    'cds__nome_cds_it',
                    'cds__nome_cds_eng')
            return final_query
        else:
            query = DidatticaAttivitaFormativa.objects.filter(
                pds_regdid__pds_regdid_id=studyplanid, af_id__isnull=False)
            new_query = DidatticaAttivitaFormativa.objects.none()
            for q in query:
                if q.checkIfMainCourse():
                    new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                        af_id=q.af_id)

            return new_query.order_by(
                'anno_corso',
                'ciclo_des') .values(
                'af_id',
                'des',
                'af_gen_des_eng',
                'cds__cds_cod',
                'regdid__regdid_id',
                'anno_corso',
                'ciclo_des',
                'peso',
                'sett_des',
                'freq_obblig_flg',
                'cds__nome_cds_it',
                'cds__nome_cds_eng')

    @staticmethod
    def getAttivitaFormativaWithSubModules(af_id, language):
        list_submodules = DidatticaAttivitaFormativa.objects.filter(
            af_radice_id=af_id) .exclude(
            af_id=af_id) .values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'ciclo_des')

        query = DidatticaAttivitaFormativa.objects.filter(
            af_id=af_id).order_by(
            'anno_corso',
            'ciclo_des') .values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'cds__cds_cod',
            'regdid__regdid_id',
            'anno_corso',
            'ciclo_des',
            'peso',
            'sett_des',
            'freq_obblig_flg',
            'cds__nome_cds_it',
            'cds__nome_cds_eng',
            'tipo_af_des',
            'matricola_resp_did',
            'mutuata_flg',
            'af_master_id',
            'af_radice_id',
        )

        id_master = None
        mutuata_da = None
        if query.first()['mutuata_flg'] == 1:
            id_master = query.first()['af_master_id']
            mutuata_da = DidatticaAttivitaFormativa.objects.filter(
                af_id=id_master).values(
                'af_id',
                'des',
                'af_gen_des_eng',
                'ciclo_des',
                'regdid__regdid_id').first()

        attivita_mutuate_da_questa = DidatticaAttivitaFormativa.objects.filter(
            af_master_id=af_id, mutuata_flg=1) .exclude(
            af_id=af_id) .values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'ciclo_des',
            'regdid__regdid_id')

        id_radice = query.first()['af_radice_id']
        activity_root = DidatticaAttivitaFormativa.objects.filter(
            af_id=id_radice).exclude(
            af_id=af_id).values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'ciclo_des',
            'regdid__regdid_id')
        if len(activity_root) == 0:
            activity_root = None
        else:
            activity_root = activity_root.first()

        copertura = DidatticaCopertura.objects.filter(
            af_id=af_id).values(
            'personale__id',
            'personale__nome',
            'personale__cognome',
            'personale__middle_name',
            'personale__matricola')
        query = list(query)

        query[0]['BorrowedFrom'] = mutuata_da
        query[0]['ActivitiesBorrowedFromThis'] = attivita_mutuate_da_questa

        query[0]['ActivityRoot'] = activity_root

        query[0]['StudyActivityTeacherID'] = None
        query[0]['StudyActivityTeacherName'] = None

        for q in copertura:
            if q['personale__matricola'] == query[0]['matricola_resp_did']:
                query[0]['StudyActivityTeacherID'] = q['personale__matricola']
                query[0]['StudyActivityTeacherName'] = q['personale__cognome'] + " " + q['personale__nome'] + \
                    (" " + q['personale__middle_name'] if q['personale__middle_name'] is not None else "")

        texts_af = DidatticaTestiAf.objects.filter(
            af_id=af_id).values(
            'tipo_testo_af_cod',
            'testo_af_ita',
            'testo_af_eng')

        query[0]['MODULES'] = list()
        for i in range(len(list_submodules)):
            query[0]['MODULES'].append({
                'StudyActivityID': list_submodules[i]['af_id'],
                'StudyActivityName': list_submodules[i]['des'] if language == 'it' or list_submodules[i]['af_gen_des_eng'] is None else list_submodules[i]['af_gen_des_eng'],
                'StudyActivitySemester': list_submodules[i]['ciclo_des'],
            })

        query[0]['StudyActivityContent'] = None
        query[0]['StudyActivityProgram'] = None
        query[0]['StudyActivityLearningOutcomes'] = None
        query[0]['StudyActivityMethodology'] = None
        query[0]['StudyActivityEvaluation'] = None
        query[0]['StudyActivityTextbooks'] = None
        query[0]['StudyActivityWorkload'] = None
        query[0]['StudyActivityElearningLink'] = None
        query[0]['StudyActivityElearningInfo'] = None
        query[0]['StudyActivityPrerequisites'] = None

        dict_activity = {
            'CONTENUTI': 'StudyActivityContent',
            'PROGR_EST': 'StudyActivityProgram',
            'OBIETT_FORM': 'StudyActivityLearningOutcomes',
            'METODI_DID': 'StudyActivityMethodology',
            'MOD_VER_APPR': 'StudyActivityEvaluation',
            'TESTI_RIF': 'StudyActivityTextbooks',
            'STIMA_CAR_LAV': 'StudyActivityWorkload',
            'PREREQ': 'StudyActivityPrerequisites',
            'LINK_TEAMS': 'StudyActivityElearningLink',
            'CODICE_TEAMS': 'StudyActivityElearningInfo',
            'PROPEDE': None,
            'LINGUA_INS': None,
            'PAG_WEB_DOC': None,
            'ALTRO': None,
        }

        for text in texts_af:
            query[0][dict_activity[text['tipo_testo_af_cod']]
                     ] = text['testo_af_ita'] if language == 'it' or text['testo_af_eng'] is None else text['testo_af_eng']

        return query

    @staticmethod
    def getDocentiPerReg(regdid_id):

        query = DidatticaAttivitaFormativa.objects.filter(
            didatticacopertura__personale__fl_docente=1,
            regdid__regdid_id=regdid_id,
            didatticacopertura__personale__isnull=False) .order_by(
            'didatticacopertura__personale__cd_ruolo',
            'didatticacopertura__personale__cognome',
            'didatticacopertura__personale__nome') .values(
            'didatticacopertura__personale__matricola',
            'didatticacopertura__personale__nome',
            'didatticacopertura__personale__cognome',
            'didatticacopertura__personale__middle_name',
            'didatticacopertura__personale__cd_ruolo',
            'didatticacopertura__personale__cd_ssd').distinct()

        return query


class ServiceDocente:
    @staticmethod
    def getResearchGroups(teacher_id):

        query = Personale.objects.filter(
            matricola__exact=teacher_id,
            fl_docente=1,
            ricercadocentegruppo__dt_fine__isnull=True) .order_by('ricercadocentegruppo__ricerca_gruppo__nome') .values(
            'ricercadocentegruppo__ricerca_gruppo__id',
            'ricercadocentegruppo__ricerca_gruppo__nome',
            'ricercadocentegruppo__ricerca_gruppo__descrizione').distinct()

        return query

    @staticmethod
    def getResearchLines(teacher_id):
        linea_applicata = Personale.objects.filter(
            matricola__exact=teacher_id,
            fl_docente=1,
            ricercadocentelineaapplicata__dt_fine__isnull=True) .order_by('ricercadocentelineaapplicata__ricerca_linea_applicata__id') .values(
            'ricercadocentelineaapplicata__ricerca_linea_applicata__id',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description').distinct()

        linea_base = Personale.objects.filter(
            matricola__exact=teacher_id,
            fl_docente=1,
            ricercadocentelineabase__dt_fine__isnull=True) .order_by('ricercadocentelineabase__ricerca_linea_base__id') .values(
            'ricercadocentelineabase__ricerca_linea_base__id',
            'ricercadocentelineabase__ricerca_linea_base__descrizione',
            'ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto',
            'ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod',
            'ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description').distinct()

        linea_applicata = list(linea_applicata)
        for linea in linea_applicata:
            linea['Tipologia'] = 'applicata'
        linea_base = list(linea_base)
        for linea in linea_base:
            linea['Tipologia'] = 'base'

        linea_applicata.extend(linea_base)

        return linea_applicata

    @staticmethod
    def teachersList(keywords, regdid, dip, role):

        query_keywords = Q()

        if keywords is not None:
            for k in keywords.split(" "):
                q_cognome = Q(cognome__icontains=k)
                query_keywords &= q_cognome

        if dip:
            department = DidatticaDipartimento.objects.filter(
                dip_cod=dip).values(
                "dip_cod", "dip_des_it", "dip_des_eng").first()
            if department is None:
                return None
            query = Personale.objects.filter(
                query_keywords,
                fl_docente=1,
                aff_org=department["dip_cod"]) .values(
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "ds_ruolo_locale",
                "cd_ssd",
                "ds_ssd",
                "cv_full_it",
                "cv_short_it",
                "cv_full_eng",
                "cv_short_eng").order_by('cognome', 'nome', 'middle_name')
            if role:
                query = query.filter(query_keywords, cd_ruolo=role)
            query = list(query)

            for q in query:
                q["dip_cod"] = department['dip_cod']
                q["dip_des_it"] = department['dip_des_it']
                q["dip_des_eng"] = department["dip_des_eng"]

            return query

        elif regdid:
            if role:
                query = Personale.objects.filter(
                    query_keywords,
                    fl_docente=1,
                    cd_ruolo=role,
                    didatticacopertura__af__isnull=False,
                    didatticacopertura__af__regdid__regdid_id=regdid)
            else:
                query = Personale.objects.filter(
                    query_keywords,
                    fl_docente=1,
                    didatticacopertura__af__isnull=False,
                    didatticacopertura__af__regdid__regdid_id=regdid)
        else:
            if role:
                query = Personale.objects.filter(
                    query_keywords,
                    fl_docente=1, flg_cessato=0, cd_ruolo=role)
            else:
                query = Personale.objects.filter(
                    query_keywords, fl_docente=1, flg_cessato=0)

        dip_cods = query.values_list("aff_org", flat=True).distinct()
        dip_cods = list(dip_cods)

        query = query.values(
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_ssd",
            "ds_ssd",
            "aff_org",
            "ds_ssd",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng"
        ).distinct().order_by('cognome', 'nome', 'middle_name')

        query = list(query)

        departments = DidatticaDipartimento.objects.filter(
            dip_cod__in=dip_cods).values(
            "dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

        for q in query:
            found = False
            for dep in departments:
                if dep['dip_cod'] == q['aff_org']:
                    q["dip_cod"] = dep['dip_cod']
                    q["dip_des_it"] = dep['dip_des_it']
                    q["dip_des_eng"] = dep["dip_des_eng"]
                    found = True
                    break

            if not found:
                q["dip_cod"] = None
                q["dip_des_it"] = None
                q["dip_des_eng"] = None

        return query

    @staticmethod
    def getAttivitaFormativeByDocente(teacher, year, yearFrom, yearTo):

        if year:
            query = Personale.objects.filter(
                fl_docente=1,
                matricola__exact=teacher,
                didatticacopertura__af__isnull=False,
                didatticacopertura__aa_id=year)
        elif yearFrom and yearTo:
            query = Personale.objects.filter(
                fl_docente=1,
                matricola__exact=teacher,
                didatticacopertura__af__isnull=False,
                didatticacopertura__aa_id__gte=yearFrom,
                didatticacopertura__aa_id__lte=yearTo)
        elif yearFrom:
            query = Personale.objects.filter(
                fl_docente=1,
                matricola__exact=teacher,
                didatticacopertura__af__isnull=False,
                didatticacopertura__aa_id__gte=yearFrom)
        elif yearTo:
            query = Personale.objects.filter(
                fl_docente=1,
                matricola__exact=teacher,
                didatticacopertura__af__isnull=False,
                didatticacopertura__aa_id__lte=yearTo)
        else:
            query = Personale.objects.filter(
                fl_docente=1,
                matricola__exact=teacher,
                didatticacopertura__af__isnull=False)

        return query.order_by(
            'didatticacopertura__aa_id',
            'didatticacopertura__af__anno_corso',
            'didatticacopertura__af__des',
            'didatticacopertura__af__af_gen_des_eng') .values(
            'didatticacopertura__af__af_id',
            'didatticacopertura__af__des',
            'didatticacopertura__af__af_gen_des_eng',
            'didatticacopertura__af__regdid__regdid_id',
            'didatticacopertura__af__anno_corso',
            'didatticacopertura__af__ciclo_des',
            'didatticacopertura__af__peso',
            'didatticacopertura__af__sett_des',
            'didatticacopertura__af__freq_obblig_flg',
            'didatticacopertura__af__cds__nome_cds_it',
            'didatticacopertura__af__cds__nome_cds_eng',
            'didatticacopertura__af__lista_lin_did_af',
            'didatticacopertura__aa_id',
            'didatticacopertura__af__cds_id')

    @staticmethod
    def getDocenteInfo(teacher):
        query = Personale.objects.filter(
            fl_docente=1,
            matricola__exact=teacher)
        contacts_to_take = [
            'Posta Elettronica',
            'Fax',
            'POSTA ELETTRONICA CERTIFICATA',
            'Telefono Cellulare Ufficio',
            'Telefono Ufficio',
            'Riferimento Ufficio',
            'URL Sito WEB',
            'URL Sito WEB Curriculum Vitae']
        contacts = query.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=contacts_to_take).values(
            "personalecontatti__cd_tipo_cont__descr_contatto",
            "personalecontatti__contatto")
        contacts = list(contacts)

        functions = FunzioniUnitaOrganizzativa.objects.filter(
            matricola=teacher,
            termine__gt=datetime.datetime.now(),
            decorrenza__lt=datetime.datetime.now()).values(
            "ds_funzione",
            "unita_organizzativa_id__uo",
            "unita_organizzativa_id__denominazione")

        query = query.values(
            "id_ab",
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_ssd",
            "ds_ssd",
            "aff_org",
            "ds_aff_org",
            "telrif",
            "email",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng"
        )
        for q in query:
            for c in contacts_to_take:
                q[c] = []
            for c in contacts:
                q[c['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    c['personalecontatti__contatto'])

            dep = DidatticaDipartimento.objects.filter(dip_cod=q["aff_org"]) \
                .values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
            if len(dep) == 0:
                q["dip_cod"] = None
                q["dip_des_it"] = None
                q["dip_des_eng"] = None
            else:
                dep = dep.first()
                q["dip_cod"] = dep['dip_cod']
                q["dip_des_it"] = dep['dip_des_it']
                q["dip_des_eng"] = dep["dip_des_eng"]

            if len(functions) == 0:
                q["Functions"] = None
            else:
                q["Functions"] = functions

        return query

    @staticmethod
    def getRoles():
        query = Personale.objects.all().values("cd_ruolo",
                                               "ds_ruolo_locale").order_by('ds_ruolo_locale').distinct()

        return query

    @staticmethod
    def getPublicationsList(
            teacherid=None,
            keywords=None,
            year=None,
            type=None):
        query_keywords = Q()
        query_year = Q()
        query_type = Q()

        if keywords is not None:
            for k in keywords.split(" "):
                q_title = Q(title__icontains=k)
                query_keywords &= q_title
        if year is not None:
            query_year = Q(date_issued_year=year)
        if type is not None:
            query_type = Q(collection_id__community_id__community_id=type)

        query = PubblicazioneDatiBase.objects.filter(
            query_keywords,
            query_year,
            query_type,
            pubblicazioneautori__id_ab__matricola=teacherid).values(
            "item_id",
            "title",
            "des_abstract",
            "des_abstracteng",
            "collection_id__collection_name",
            "collection_id__community_id__community_name",
            "pubblicazione",
            "label_pubblicazione",
            "contributors",
            'date_issued_year',
            'url_pubblicazione').order_by(
            "-date_issued_year",
            "title").distinct()
        for q in query:
            autori = PubblicazioneAutori.objects.filter(
                item_id=q['item_id']).values(
                "id_ab__nome",
                "id_ab__cognome",
                "id_ab__middle_name",
                "id_ab__matricola",
                "first_name",
                "last_name")
            if len(autori) == 0:
                q['Authors'] = []
            else:
                q['Authors'] = autori

            q['ReferenceAuthor'] = teacherid

        return query

    @staticmethod
    def getPublication(publicationid=None, teacherid=None):

        query = PubblicazioneDatiBase.objects.filter(
            item_id=publicationid).values(
            "item_id",
            "title",
            "des_abstract",
            "des_abstracteng",
            "collection_id__collection_name",
            "collection_id__community_id__community_name",
            "pubblicazione",
            "label_pubblicazione",
            "contributors",
            'date_issued_year',
            'url_pubblicazione').order_by(
            "date_issued_year",
            "title").distinct()

        for q in query:
            autori = PubblicazioneAutori.objects.filter(
                item_id=publicationid).values(
                "id_ab__nome",
                "id_ab__cognome",
                "id_ab__middle_name",
                "id_ab__matricola",
                "first_name",
                "last_name")
            if len(autori) == 0:
                q['Authors'] = []
            else:
                q['Authors'] = autori

            q['ReferenceAuthor'] = teacherid

        return query

    @staticmethod
    def getPublicationsCommunityTypesList():
        query = PubblicazioneCommunity.objects.all().values(
            "community_id", "community_name").order_by("community_id").distinct()
        return query


class ServiceDottorato:
    @staticmethod
    def getDoctorates(query_params):

        params_to_query_field = {
            'year': 'idesse3_ddr__aa_regdid_id__exact',
            'yearFrom': 'idesse3_ddr__aa_regdid_id__gte',
            'yearTo': 'idesse3_ddr__aa_regdid_id__lte',
            'regdid': 'idesse3_ddr__regdid_id_esse3__exact',
            'departmentid': 'dip_cod__dip_cod__exact',
            'cdscod': 'cds_cod__exact',
            'pdscod': 'idesse3_ddpds__pds_cod__exact',
            'cycle': 'idesse3_ddr__num_ciclo',
        }

        query = DidatticaDottoratoCds.objects.filter(
            ServiceQueryBuilder.build_filter_chain(
                params_to_query_field, query_params))

        return query.order_by(
            'idesse3_ddr__aa_regdid_id',
            'dip_cod__dip_cod',
            'cds_cod',
            'idesse3_ddpds__pds_cod') .values(
            'dip_cod__dip_cod',
            'dip_cod__dip_des_it',
            'dip_cod__dip_des_eng',
            'cds_cod',
            'cdsord_des',
            'tipo_corso_cod',
            'tipo_corso_des',
            'durata_anni',
            'valore_min',
            'idesse3_ddr__aa_regdid_id',
            'idesse3_ddr__regdid_cod',
            'idesse3_ddr__frequenza_obbligatoria',
            'idesse3_ddr__num_ciclo',
            'idesse3_ddpds__pds_cod',
            'idesse3_ddpds__pds_des',
            'idesse3_ddr__regdid_id_esse3')


class ServiceDipartimento:

    @staticmethod
    def getDepartmentsList(language):
        query = DidatticaDipartimento.objects.all().values(
            "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve")
        return query.order_by(
            "dip_des_it") if language == 'it' else query.order_by("dip_des_eng")

    @staticmethod
    def getDepartment(departmentid):
        query = DidatticaDipartimento.objects.filter(
            dip_cod__exact=departmentid).values(
            "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve")
        return query


class ServicePersonale:

    @staticmethod
    def getAddressbook(
            keywords=None,
            structureid=None,
            structuretypes=None,
            roles=None,
            structuretree=None):

        query_keywords = Q()
        query_structure = Q()
        query_roles = Q()
        query_structuretree = Q()

        if keywords is not None:
            for k in keywords.split(" "):
                q_cognome = Q(cognome__icontains=k)
                query_keywords |= q_cognome
        if structureid is not None:
            query_structure = Q(aff_org__exact=structureid)
        if roles is not None:
            roles = roles.split(",")
            query_roles = Q(cd_ruolo__in=roles)
        if structuretree is not None:
            query_structuretree = ServicePersonale.getStructurePersonnelChild(
                Q(), structuretree)
            query_structuretree |= Q(aff_org=structuretree)

        query = Personale.objects.filter(
            query_keywords,
            query_structure,
            query_roles,
            query_structuretree,
            flg_cessato=0,
            aff_org__isnull=False)

        if structuretypes is not None:
            structuretypes = structuretypes.split(",")
            query = query.extra(
                select={
                    'denominazione': 'UNITA_ORGANIZZATIVA.DENOMINAZIONE',
                    'structure_type_cod': 'UNITA_ORGANIZZATIVA.CD_TIPO_NODO',
                    'structure_type_name': 'UNITA_ORGANIZZATIVA.DS_TIPO_NODO'},
                tables=['UNITA_ORGANIZZATIVA'],
                where=[
                    'UNITA_ORGANIZZATIVA.UO=PERSONALE.AFF_ORG',
                    'UNITA_ORGANIZZATIVA.CD_TIPO_NODO IN %s'
                ],
                params=(structuretypes,))
        else:
            query = query.extra(
                select={
                    'denominazione': 'UNITA_ORGANIZZATIVA.DENOMINAZIONE',
                    'structure_type_cod': 'UNITA_ORGANIZZATIVA.CD_TIPO_NODO',
                    'structure_type_name': 'UNITA_ORGANIZZATIVA.DS_TIPO_NODO'},
                tables=['UNITA_ORGANIZZATIVA'],
                where=[
                    'UNITA_ORGANIZZATIVA.UO=PERSONALE.AFF_ORG',
                ])

        query = query.values(
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "aff_org",
            "id_ab",
            "matricola",
            'personalecontatti__cd_tipo_cont__descr_contatto',
            'personalecontatti__contatto',
            'funzioniunitaorganizzativa__ds_funzione',
            'funzioniunitaorganizzativa__termine',
            'denominazione',
            'structure_type_cod',
            'structure_type_name',
            'fl_docente',
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng"
        )

        if structureid is None and structuretypes is None and structuretree is None:
            query2 = Personale.objects.filter(
                query_keywords,
                query_roles,
                flg_cessato=0,
                aff_org__isnull=True).annotate(
                denominazione=Value(
                    None,
                    output_field=CharField())).annotate(
                structure_type_cod=Value(
                    None,
                    output_field=CharField())).annotate(
                        structure_type_name=Value(
                            None,
                            output_field=CharField())).order_by("cognome").values(
                                "nome",
                                "middle_name",
                                "cognome",
                                "cd_ruolo",
                                "ds_ruolo_locale",
                                "aff_org",
                                "id_ab",
                                "matricola",
                                'personalecontatti__cd_tipo_cont__descr_contatto',
                                'personalecontatti__contatto',
                                'funzioniunitaorganizzativa__ds_funzione',
                                'funzioniunitaorganizzativa__termine',
                                'denominazione',
                                'structure_type_cod',
                                'structure_type_name',
                                'fl_docente',
                                "cv_full_it",
                                "cv_short_it",
                                "cv_full_eng",
                                "cv_short_eng",
            )
            from itertools import chain
            query = list(chain(*[query, query2]))

        query = list(query)
        query.sort(key=lambda x: x.get('cognome'), reverse=False)

        contacts_to_take = [
            'Posta Elettronica',
            'Fax',
            'POSTA ELETTRONICA CERTIFICATA',
            'Telefono Cellulare Ufficio',
            'Telefono Ufficio',
            'Riferimento Ufficio',
            'URL Sito WEB',
            'URL Sito WEB Curriculum Vitae']

        grouped = {}
        last_id = -1
        final_query = []
        for q in query:
            if q['id_ab'] not in grouped:
                grouped[q['id_ab']] = {
                    'id_ab': q['id_ab'],
                    'nome': q['nome'],
                    'middle_name': q['middle_name'],
                    'cognome': q['cognome'],
                    'cd_ruolo': q['cd_ruolo'],
                    'ds_ruolo_locale': q['ds_ruolo_locale'],
                    'aff_org': q['aff_org'],
                    'matricola': q['matricola'],
                    'Funzione': q['funzioniunitaorganizzativa__ds_funzione'] if q['funzioniunitaorganizzativa__termine'] is not None and q['funzioniunitaorganizzativa__termine'] >= datetime.datetime.today() else None,
                    'Struttura': q['denominazione'] if 'denominazione' in q.keys() else None,
                    'TipologiaStrutturaCod': q['structure_type_cod'] if 'structure_type_cod' in q.keys() else None,
                    'TipologiaStrutturaNome': q['structure_type_name'] if 'structure_type_name' in q.keys() else None,
                    'fl_docente': q['fl_docente'],
                    'cv_full_it': q['cv_full_it'],
                    'cv_full_eng': q['cv_full_eng'],
                    'cv_short_it': q['cv_short_it'],
                    'cv_short_eng': q['cv_short_eng'],

                }
                for c in contacts_to_take:
                    grouped[q['id_ab']][c] = []

            if q['personalecontatti__cd_tipo_cont__descr_contatto'] in contacts_to_take:
                grouped[q['id_ab']][q['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    q['personalecontatti__contatto'])

            if last_id == -1 or last_id != q['id_ab']:
                last_id = q['id_ab']
                final_query.append(grouped[q['id_ab']])
        return final_query

    @staticmethod
    def getStructuresList(keywords=None, father=None, type=None):

        query_keywords = Q()
        query_father = Q()
        query_type = Q()

        if father == 'None':
            query_father = Q(uo_padre__isnull=True)
        elif father:
            query_father = Q(uo_padre=father)

        if keywords is not None:
            for k in keywords.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_keywords &= q_denominazione

        if type:
            for k in type.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type

        query = UnitaOrganizzativa.objects.filter(
            query_keywords,
            query_father,
            query_type,
            dt_fine_val__gte=datetime.datetime.today()).values(
            "uo",
            "denominazione",
            "ds_tipo_nodo",
            "cd_tipo_nodo").distinct().order_by('denominazione')

        return query

    @staticmethod
    def getStructureTypes(father=None):
        father_query = Q()
        if father is not None:
            father_query = Q(uo_padre=father)
        query = UnitaOrganizzativa.objects.filter(father_query).values(
            "ds_tipo_nodo", "cd_tipo_nodo").distinct()
        return query

    @staticmethod
    def getPersonale(personale_id):
        query = Personale.objects.filter(matricola__exact=personale_id)
        if query.values('aff_org').first()['aff_org'] is None:
            query = query.filter(
                flg_cessato=0,
            ).annotate(
                Struttura=Value(
                    None,
                    output_field=CharField())).annotate(
                TipologiaStrutturaCod=Value(None, output_field=CharField())).annotate(
                TipologiaStrutturaNome=Value(None, output_field=CharField()))
        else:
            query = query.filter(
                flg_cessato=0,
            ).extra(
                select={
                    'Struttura': 'UNITA_ORGANIZZATIVA.DENOMINAZIONE',
                    'TipologiaStrutturaCod': 'UNITA_ORGANIZZATIVA.CD_TIPO_NODO',
                    'TipologiaStrutturaNome': 'UNITA_ORGANIZZATIVA.DS_TIPO_NODO'},
                tables=['UNITA_ORGANIZZATIVA'],
                where=[
                    'UNITA_ORGANIZZATIVA.UO=PERSONALE.AFF_ORG',
                ])
        contacts_to_take = [
            'Posta Elettronica',
            'Fax',
            'POSTA ELETTRONICA CERTIFICATA',
            'Telefono Cellulare Ufficio',
            'Telefono Ufficio',
            'Riferimento Ufficio',
            'URL Sito WEB',
            'URL Sito WEB Curriculum Vitae']
        contacts = query.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=contacts_to_take).values(
            "personalecontatti__cd_tipo_cont__descr_contatto",
            "personalecontatti__contatto")
        contacts = list(contacts)
        query = query.values(
            "id_ab",
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_ssd",
            "ds_ssd",
            "aff_org",
            "ds_aff_org",
            "telrif",
            "email",
            "Struttura",
            'TipologiaStrutturaCod',
            'TipologiaStrutturaNome',
            'funzioniunitaorganizzativa__ds_funzione',
            'funzioniunitaorganizzativa__termine',
            'fl_docente',
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng"
        )
        for q in query:
            if q["funzioniunitaorganizzativa__termine"] is not None and q["funzioniunitaorganizzativa__termine"] >= datetime.datetime.today():
                q["Funzione"] = q["funzioniunitaorganizzativa__ds_funzione"]
            else:
                q["Funzione"] = None
            for c in contacts_to_take:
                q[c] = []
            for c in contacts:
                q[c['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    c['personalecontatti__contatto'])
        return query

    @staticmethod
    def getStructure(structureid):
        query = UnitaOrganizzativa.objects.filter(
            uo__exact=structureid)
        contacts_to_take = [
            'EMAIL',
            'PEC',
            'TFR',
        ]
        contacts = query.filter(
            unitaorganizzativacontatti__cd_tipo_cont__in=contacts_to_take).values(
            "unitaorganizzativacontatti__cd_tipo_cont",
            "unitaorganizzativacontatti__contatto")
        contacts = list(contacts)
        query = query.values(
            'uo',
            'denominazione',
            'uo_padre',
            'denominazione_padre',
            "ds_tipo_nodo",
            "cd_tipo_nodo",
        )
        for q in query:
            for c in contacts_to_take:
                q[c] = []
            for c in contacts:
                q[c['unitaorganizzativacontatti__cd_tipo_cont']].append(
                    c['unitaorganizzativacontatti__contatto'])
            funzioni_personale = FunzioniUnitaOrganizzativa.objects.filter(
                unita_organizzativa__uo=q['uo'],
                termine__gt=datetime.datetime.now()).values(
                "ds_funzione",
                "cod_fis__nome",
                "cod_fis__cognome",
                "cod_fis__middle_name",
                "cod_fis__matricola")
            if len(funzioni_personale) > 0:
                q['FunzioniPersonale'] = funzioni_personale
            else:
                q['FunzioniPersonale'] = None

        return query

    @staticmethod
    def getStructurePersonnelChild(structures_tree, structureid=None):
        child_structures = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid).values("uo")

        for child in child_structures:
            structures_tree |= Q(aff_org=child["uo"])
            structures_tree = ServicePersonale.getStructurePersonnelChild(
                structures_tree, child['uo'])

        return structures_tree


class ServiceLaboratorio:

    @staticmethod
    def getLaboratoriesList(language, keywords, ambito, dip, erc1, teacher):
        query_keywords = Q()
        query_ambito = Q()
        query_dip = Q()
        query_erc1 = Q()
        query_teacher = Q()

        if keywords:
            for k in keywords.split(" "):
                q_nome = Q(nome_laboratorio__icontains=k)
                query_keywords &= q_nome
        if ambito:
            query_ambito = Q(ambito__exact=ambito)
        if dip:
            query_dip = Q(id_dipartimento_riferimento__dip_cod__exact=dip)
            query_dip |= Q(laboratorioaltridipartimenti__id_dip__dip_cod=dip)
        if erc1:
            erc1_allowed = erc1.split(",")
            query_erc1 = Q(
                laboratoriodatierc1__id_ricerca_erc1__cod_erc1__in=erc1_allowed)
        if teacher:
            query_teacher = Q(
                matricola_responsabile_scientifico__exact=teacher)

        query = LaboratorioDatiBase.objects.filter(
            query_keywords, query_ambito, query_dip, query_erc1, query_teacher
        ).values(
            'id',
            'nome_laboratorio',
            'ambito',
            'dipartimento_riferimento',
            'id_dipartimento_riferimento__dip_cod',
            'sede_dimensione',
            'responsabile_scientifico',
            'matricola_responsabile_scientifico',
            'laboratorio_interdipartimentale',
        ).distinct()

        for q in query:
            if q['laboratorio_interdipartimentale'] == 'SI':
                other_dep = LaboratorioAltriDipartimenti.objects.filter(
                    id_laboratorio_dati=q['id']).values(
                    "id_dip__dip_cod",
                    "id_dip__dip_des_it",
                    "id_dip__dip_des_eng").distinct()
                q['ExtraDepartments'] = other_dep.order_by(
                    "id_dip__dip_des_it") if language == "it" else other_dep.order_by("id_dip__dip_des_eng")
            else:
                q['ExtraDepartments'] = []

        return query

    @staticmethod
    def getLaboratory(language, laboratoryid):
        query = LaboratorioDatiBase.objects.filter(
            id__exact=laboratoryid).values(
            "id",
            "referente_compilazione",
            "matricola_referente_compilazione",
            "nome_laboratorio",
            "acronimo",
            "logo_laboratorio",
            "id_dipartimento_riferimento__dip_cod",
            "id_dipartimento_riferimento__dip_des_it",
            "id_dipartimento_riferimento__dip_des_eng",
            "ambito",
            "finalita_servizi_it",
            "finalita_servizi_en",
            "finalita_ricerca_it",
            "finalita_ricerca_en",
            "finalita_didattica_en",
            "finalita_didattica_it",
            "responsabile_scientifico",
            "matricola_responsabile_scientifico",
            'laboratorio_interdipartimentale',
            'sito_web',
            'strumentazione_descrizione',)
        activities = LaboratorioAttivita.objects.filter(
            id_laboratorio_dati__id=laboratoryid).values("tipologia_attivita")
        erc1 = ServiceLaboratorio.getErc1List(laboratoryid)
        personale_ricerca = LaboratorioPersonaleRicerca.objects.filter(
            id_laboratorio_dati__id=laboratoryid).values(
            "matricola_personale_ricerca__matricola",
            "matricola_personale_ricerca__nome",
            "matricola_personale_ricerca__cognome",
            "matricola_personale_ricerca__middle_name")
        personale_tecnico = LaboratorioPersonaleTecnico.objects.filter(
            id_laboratorio_dati__id=laboratoryid).values(
            "matricola_personale_tecnico__matricola",
            "matricola_personale_tecnico__nome",
            "matricola_personale_tecnico__cognome",
            "matricola_personale_tecnico__middle_name",
            "ruolo")
        servizi_offerti = LaboratorioServiziOfferti.objects.filter(
            id_laboratorio_dati__id=laboratoryid).values(
            "nome_servizio", "descrizione_servizio")
        ubicazione = LaboratorioUbicazione.objects.filter(
            id_laboratorio_dati__id=laboratoryid).values(
            "edificio", "piano", "note")

        other_dep = LaboratorioAltriDipartimenti.objects.filter(
            id_laboratorio_dati=laboratoryid).values(
            "id_dip__dip_cod",
            "id_dip__dip_des_it",
            "id_dip__dip_des_eng").distinct()
        query = list(query)
        for q in query:
            q['Activities'] = activities
            q['Erc1'] = erc1
            q['ResearchPersonnel'] = personale_ricerca
            q['TechPersonnel'] = personale_tecnico
            q['OfferedServices'] = servizi_offerti
            if len(ubicazione) > 0:
                q['Location'] = ubicazione.first()
            else:
                q['Location'] = None

            if q['laboratorio_interdipartimentale'] == 'SI':
                q['ExtraDepartments'] = other_dep.order_by(
                    "id_dip__dip_des_it") if language == "it" else other_dep.order_by("id_dip__dip_des_eng")
            else:
                q['ExtraDepartments'] = []

        return query

    @staticmethod
    def getLaboratoriesAreasList():
        return LaboratorioDatiBase.objects.all().values(
            "ambito").distinct().order_by("ambito")

    @staticmethod
    def getErc1List(laboratorio):

        query_laboratorio = Q()

        if laboratorio:
            query_laboratorio = Q(id_laboratorio_dati__exact=laboratorio)

        query = LaboratorioDatiErc1.objects.filter(
            query_laboratorio,
        ).values(
            'id_ricerca_erc1__ricerca_erc0_cod__erc0_cod',
            'id_ricerca_erc1__ricerca_erc0_cod__description',
            'id_ricerca_erc1__ricerca_erc0_cod__description_en').distinct()

        query = list(query)

        for q in query:

            q['Erc1'] = LaboratorioDatiErc1.objects.filter(
                query_laboratorio,
                id_ricerca_erc1__ricerca_erc0_cod=q['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod']).values(
                'id_ricerca_erc1__cod_erc1',
                'id_ricerca_erc1__descrizione').distinct()

        return query

    @staticmethod
    def getErc0List():

        query = LaboratorioDatiErc1.objects.all(). values(
            'id_ricerca_erc1__ricerca_erc0_cod__erc0_cod',
            'id_ricerca_erc1__ricerca_erc0_cod__description',
            'id_ricerca_erc1__ricerca_erc0_cod__description_en').distinct()

        return query
