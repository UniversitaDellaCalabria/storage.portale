import datetime
from functools import reduce
import operator

from django.db.models import Q, Max
from .models import DidatticaCds, DidatticaAttivitaFormativa, \
    DidatticaTestiAf, DidatticaCopertura, Personale, DidatticaDipartimento, DidatticaDottoratoCds, DidatticaRegolamento, \
    DidatticaPdsRegolamento, FunzioniUnitaOrganizzativa, UnitaOrganizzativa


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
        query_params_size = len(query_params)
        if 'page' in query_params:
            query_params_size -= 1
        if 'lang' in query_params:
            query_params_size -= 1

        if query_params_size == 0:
            currentAA = DidatticaRegolamento.objects.aggregate(
                Max('aa_reg_did'))
            items = DidatticaCds.objects.filter(
                didatticaregolamento__aa_reg_did__exact=currentAA['aa_reg_did__max'],
                didatticaregolamento__stato_regdid_cod='A',
                didatticacdslingua__lin_did_ord_id__isnull=False)
            if len(items) == 0:
                items = DidatticaCds.objects.filter(
                    didatticaregolamento__aa_reg_did__exact=(
                        currentAA['aa_reg_did__max'] - 1),
                    didatticaregolamento__stato_regdid_cod='A',
                    didatticacdslingua__lin_did_ord_id__isnull=False)

        else:
            didatticacds_params_to_query_field = {
                'coursetype': 'tipo_corso_cod',
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
                'cdslanguage': f'didatticacdslingua__lingua_des_{language == "it" and "it" or "eng"}__iexact', }

            keywords = set(
                query_params.get(
                    'keywords', '').split(','))

            q1 = ServiceQueryBuilder.build_filter_chain(
                didatticacds_params_to_query_field, query_params)
            q2 = ServiceQueryBuilder.build_filter_chain(
                didatticaregolamento_params_to_query_field, query_params)
            q3 = ServiceQueryBuilder.build_filter_chain(
                didatticacdslingua_params_to_query_field, query_params)

            items = DidatticaCds.objects \
                .filter(reduce(operator.and_,
                               [Q(**{f'nome_cds_{language == "it" and "it" or "eng"}__icontains': e})
                                for e in keywords],
                               Q()), q1, q2, q3,
                        didatticacdslingua__lin_did_ord_id__isnull=False)

        return items.values(
            'didatticaregolamento__regdid_id',
            'didatticaregolamento__aa_reg_did',
            'didatticaregolamento__frequenza_obbligatoria',
            'dip__dip_cod',
            'dip__dip_des_it',
            'dip__dip_des_eng',
            'didatticacdslingua__lingua_des_it',
            'didatticacdslingua__lingua_des_eng',
            'cds_cod',
            'nome_cds_it',
            'nome_cds_eng',
            'tipo_corso_cod',
            'cla_miur_cod',
            'cla_miur_des',
            'durata_anni',
            'valore_min',
            'codicione',
            'didatticaregolamento__stato_regdid_cod').distinct()

    @staticmethod
    def getDegreeTypes():
        query = DidatticaCds.objects.values(
            "tipo_corso_cod", "tipo_corso_des").distinct()
        return query


class ServiceDidatticaAttivitaFormativa:

    @staticmethod
    def getStudyPlans(regdid_id=None):
        if regdid_id is None:
            return
        # DidatticaPdsRegolamento.objects.filter(regdid=regdid_id)
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
        if studyplanid is None:
            return

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

    # TODO: aggiungere label e pushare
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
                'ciclo_des').first()

        attivita_mutuate_da_questa = DidatticaAttivitaFormativa.objects.filter(
            af_master_id=af_id, mutuata_flg=1) .exclude(
            af_id=af_id) .values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'ciclo_des')

        id_radice = query.first()['af_radice_id']
        activity_root = DidatticaAttivitaFormativa.objects.filter(
            af_id=id_radice).exclude(
            af_id=af_id).values(
            'af_id',
            'des',
            'af_gen_des_eng',
            'ciclo_des')
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
    def teachersList(regdid, dip, role):
        if dip:
            department = DidatticaDipartimento.objects.filter(
                dip_cod=dip).values(
                "dip_cod", "dip_des_it", "dip_des_eng").first()
            if department is None:
                return None
            query = Personale.objects.filter(
                fl_docente=1,
                aff_org=department["dip_cod"]) .values(
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "cd_ssd",
                "ds_ssd")
            if role:
                query = query.filter(cd_ruolo=role)
            query = list(query)

            for q in query:
                q["dip_cod"] = department['dip_cod']
                q["dip_des_it"] = department['dip_des_it']
                q["dip_des_eng"] = department["dip_des_eng"]

            return query

        elif regdid:
            if role:
                query = Personale.objects.filter(
                    fl_docente=1,
                    cd_ruolo=role,
                    didatticacopertura__af__isnull=False,
                    didatticacopertura__af__regdid__regdid_id=regdid)
            else:
                query = Personale.objects.filter(
                    fl_docente=1,
                    didatticacopertura__af__isnull=False,
                    didatticacopertura__af__regdid__regdid_id=regdid)
        else:
            if role:
                query = Personale.objects.filter(
                    fl_docente=1, flg_cessato=0, cd_ruolo=role)
            else:
                query = Personale.objects.filter(fl_docente=1, flg_cessato=0)

        dip_cods = query.values_list("aff_org", flat=True).distinct()
        dip_cods = list(dip_cods)

        query = query.values(
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "cd_ssd",
            "ds_ssd",
            "aff_org",
            "ds_ssd").distinct()

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
        query = query.values(
            "id_ab",
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "cd_ssd",
            "ds_ssd",
            "aff_org",
            "ds_aff_org",
            "telrif",
            "email")
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
    def getDepartmentsList():
        query = DidatticaDipartimento.objects.all().values(
            "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve")
        return query

    @staticmethod
    def getDepartment(departmentid):
        query = DidatticaDipartimento.objects.filter(
            dip_cod__exact=departmentid).values(
            "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve")
        return query

# TODO: API finita ma è troppo lenta, servirebbero due join, uno dalle
# strutture al personale e l'altro dai contatti al personale


class ServicePersonale:

    @staticmethod
    def getAddressbook(keywords=None, structureid=None):
        query_keywords = Q()
        query_structure = Q()
        if keywords is not None:
            for k in keywords.split(" "):
                q_cognome = Q(cognome__icontains=k)
                query_keywords |= q_cognome
        if structureid is not None:
            query_structure = Q(aff_org__exact=structureid)

        query = Personale.objects.filter(
            query_keywords, query_structure, flg_cessato=0)

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
            personalecontatti__cd_tipo_cont__descr_contatto__in=contacts_to_take)
        query = query.values("nome", "middle_name",
                             "cognome", "cd_ruolo",
                             "ds_ruolo",
                             "aff_org",
                             "id_ab", "matricola")
        query = list(query)

        for q in query:
            f = FunzioniUnitaOrganizzativa.objects.filter(
                id_ab=q['id_ab'], termine__gte=datetime.datetime.today()).values("ds_funzione")
            s = UnitaOrganizzativa.objects.filter(
                uo__exact=q['aff_org']).values("denominazione")
            for c in contacts_to_take:
                q[c] = []
            contacts_temp = contacts.filter(
                id_ab=q['id_ab']).values(
                "personalecontatti__cd_tipo_cont__descr_contatto",
                "personalecontatti__contatto")
            for c in contacts_temp:
                q[c['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    c['personalecontatti__contatto'])

            if len(f) > 0:
                q['Funzione'] = f[0]['ds_funzione']
            else:
                q['Funzione'] = None

            if len(s) > 0:
                q['Struttura'] = s.first()['denominazione']
            else:
                q['Struttura'] = None

        return query
