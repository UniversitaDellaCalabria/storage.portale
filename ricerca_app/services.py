import datetime
import operator
import re

from django.conf import settings
from django.db.models import CharField, Q, Value, F
from django.http import Http404

from functools import reduce

from .models import DidatticaCds, DidatticaAttivitaFormativa, \
    DidatticaTestiAf, DidatticaCopertura, Personale, DidatticaDipartimento, DidatticaDottoratoCds, \
    DidatticaPdsRegolamento, DidatticaDipartimentoUrl, \
    UnitaOrganizzativa, DidatticaRegolamento, DidatticaCdsLingua, LaboratorioDatiBase, LaboratorioAttivita, \
    LaboratorioDatiErc1, LaboratorioPersonaleRicerca, LaboratorioPersonaleTecnico, LaboratorioServiziOfferti, \
    LaboratorioUbicazione, UnitaOrganizzativaFunzioni, LaboratorioAltriDipartimenti, PubblicazioneDatiBase, \
    PubblicazioneAutori, PubblicazioneCommunity, RicercaGruppo, RicercaDocenteGruppo, RicercaLineaBase, RicercaDocenteLineaBase, \
    RicercaLineaApplicata, RicercaDocenteLineaApplicata, RicercaErc2, LaboratorioInfrastruttura, BrevettoDatiBase, BrevettoInventori, LaboratorioTipologiaAttivita, \
    SpinoffStartupDatiBase, TipologiaAreaTecnologica, ProgettoDatiBase, ProgettoResponsabileScientifico, UnitaOrganizzativaTipoFunzioni, ProgettoAmbitoTerritoriale, \
    ProgettoTipologiaProgramma, ProgettoRicercatore, AltaFormazioneDatiBase, AltaFormazionePartner,AltaFormazioneTipoCorso, AltaFormazionePianoDidattico, \
    AltaFormazioneIncaricoDidattico, AltaFormazioneModalitaSelezione, AltaFormazioneModalitaErogazione, AltaFormazioneConsiglioScientificoInterno, AltaFormazioneConsiglioScientificoEsterno, \
    RicercaAster1, RicercaAster2, RicercaErc0, DidatticaCdsAltriDatiUfficio, DidatticaCdsAltriDati, DidatticaCoperturaDettaglioOre, \
    DidatticaAttivitaFormativaModalita, RicercaErc1, DidatticaDottoratoAttivitaFormativa, DidatticaDottoratoAttivitaFormativaAltriDocenti, DidatticaDottoratoAttivitaFormativaDocente, \
    SpinoffStartupDipartimento, PersonaleAttivoTuttiRuoli, PersonalePrioritaRuolo, DocentePtaBacheca, DocentePtaAltriDati, DocenteMaterialeDidattico, SitoWebCdsDatiBase, SitoWebCdsSlider, SitoWebCdsLink, \
    SitoWebCdsExStudenti, SitoWebCdsTopic, SitoWebCdsTopicArticoliReg, SitoWebCdsArticoliRegolamento, \
    SitoWebCdsTopicArticoliRegAltriDati, \
    SitoWebCdsOggettiPortale, SitoWebCdsArticoliRegolamento, \
    DidatticaPianoRegolamento, DidatticaPianoSche, DidatticaPianoSceltaSchePiano, DidatticaPianoSceltaVincoli, DidatticaPianoSceltaFilAnd, DidatticaAmbiti, DidatticaPianoSceltaAf, \
    DidatticaCdsGruppi, DidatticaCdsGruppiComponenti, DidatticaTestiRegolamento, DidatticaCdsPeriodi
from . serializers import StructuresSerializer
from . settings import PERSON_CONTACTS_TO_TAKE


PERSON_CONTACTS_TO_TAKE = getattr(settings, 'PERSON_CONTACTS_TO_TAKE', PERSON_CONTACTS_TO_TAKE)


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
            'courseclasscod': 'cla_miur_cod',
            'courseclassname': 'cla_miur_des__icontains',
            'cdscod': 'cds_cod',
            # 'courseclassgroup': ... unspecified atm
            'departmentid': 'dip__dip_id',
            'departmentcod': 'dip__dip_cod',
            'departmentname': f'dip__dip_des_{language == "it" and "it" or "eng"}__icontains',
            'area': 'area_cds__icontains',
        }

        didatticaregolamento_params_to_query_field = {
            'academicyear': 'didatticaregolamento__aa_reg_did__exact',
            'jointdegree': 'didatticaregolamento__titolo_congiunto_cod',
            'regdid': 'didatticaregolamento__regdid_id',
        }

        didatticacdslingua_params_to_query_field = {
            'cdslanguage': 'didatticacdslingua__iso6392_cod', }

        search = query_params.get('search', None)
        if search is not None:
            search = search.split(' ')

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

        if search is None:
            q4 = Q(cds_id__isnull=False)
        else:
            for k in search:
                if language == "it":
                    q = Q(nome_cds_it__icontains=k)
                else:
                    q = Q(nome_cds_eng__icontains=k)
                q4 |= q

        items = DidatticaCds.objects \
            .filter(q4, q1, q2, q3)
        # didatticacdslingua__lin_did_ord_id__isnull=False

        if 'academicyear' not in query_params:
            # last_active_year = DidatticaCds.objects.filter(
            #     didatticaregolamento__stato_regdid_cod__exact='A').aggregate(
            #     Max('didatticaregolamento__aa_reg_did'))['didatticaregolamento__aa_reg_did__max']

            items = items.filter(
                didatticaregolamento__stato_regdid_cod__exact='A')

        if courses_allowed != '':
            items = items.filter(tipo_corso_cod__in=courses_allowed)

        items = items.values(
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
            'area_cds_en').distinct()
        items = items.order_by("nome_cds_it") if language == 'it' else items.order_by(
            F("nome_cds_eng").asc(nulls_last=True))
        for i in items:
            erogation_mode = DidatticaRegolamento.objects.filter(cds_id=i['cds_id'],
                                                                 stato_regdid_cod__exact='A').values(
            'modalita_erogazione'
            )
            if (len(erogation_mode) != 0):
                i['ErogationMode'] = erogation_mode
            else:
                i['ErogationMode'] = None # pragma: no cover

        items = list(items)
        for item in items:
            item['Languages'] = DidatticaCdsLingua.objects.filter(
                cdsord_id=item['cdsord_id']).values(
                "lingua_des_it",
                "lingua_des_eng").distinct()

            item['OtherData'] = DidatticaCdsAltriDati.objects.filter(regdid_id=item['didatticaregolamento__regdid_id']).values(
                'matricola_coordinatore',
                'nome_origine_coordinatore',
                'matricola_vice_coordinatore',
                'nome_origine_vice_coordinatore',
                'num_posti',
                'modalita_iscrizione',
                'manifesto_studi',
                'regolamento_didattico',
                'ordinamento_didattico'
            ).distinct()

            item['OfficesData'] = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=item['cds_id']).values(
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

        return items

    @staticmethod
    def cds(language, cdsid_param, only_active=True):
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

        for r in res:
            erogation_mode = DidatticaRegolamento.objects.filter(cds_id=r['cds_id'],
                                                                 stato_regdid_cod__exact='A').values(
            'modalita_erogazione'
            )
            if (len(erogation_mode) != 0):
                r['ErogationMode'] = erogation_mode
            else:
                r['ErogationMode'] = None

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
                if (text['clob_txt_eng'] is None and language !=
                        "it") or language == 'it':
                    res[0][text['tipo_testo_regdid_cod']] = text['clob_txt_ita']
                else:
                    res[0][text['tipo_testo_regdid_cod']] = text['clob_txt_eng']
            else:
                if (language !=
                        "it" and text["profilo_eng"] is None) or language == 'it':
                    if text["profilo"] != last_profile:
                        last_profile = text["profilo"]
                        list_profiles[last_profile] = {}
                elif text[f'{ language == "it" and "profilo" or "profilo_eng" }'] != last_profile: # pragma: no cover
                    last_profile = text[f'{language == "it" and "profilo" or "profilo_eng"}']
                    list_profiles[last_profile] = {}

                if (text["clob_txt_eng"] is None and language !=
                        "it") or language == 'it':
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text["clob_txt_ita"]
                else:
                    list_profiles[last_profile][text['tipo_testo_regdid_cod']
                                                ] = text['clob_txt_eng']
        res[0]['PROFILO'] = list_profiles

        res[0]['OtherData'] = DidatticaCdsAltriDati.objects.filter(regdid_id=cdsid_param).values(
            'matricola_coordinatore',
            'nome_origine_coordinatore',
            'matricola_vice_coordinatore',
            'nome_origine_vice_coordinatore',
            'num_posti',
            'modalita_iscrizione',
            'manifesto_studi',
            'regolamento_didattico',
            'ordinamento_didattico'
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

        query_visibile = Q(visibile=True) if only_active else Q()
        res[0]['CdsGroups'] = DidatticaCdsGruppi.objects.filter(query_visibile,
                                                                id_didattica_cds=res[0]['cds_id']).values(
            'ordine',
            'id',
            'descr_breve_it',
            'descr_breve_en',
            'descr_lunga_it',
            'descr_lunga_en'
        ).distinct()

        res[0]['CdsPeriods'] = DidatticaCdsPeriodi.objects.filter(cds_cod=res[0]['cds_cod'],
                                                                  aa_id=res[0]['didatticaregolamento__aa_reg_did']).values(
            'ciclo_des',
            'tipo_ciclo_des',
            'tipo_ciclo_des_eng',
            'data_inizio',
            'data_fine'
        )

        for group in res[0]['CdsGroups']:
            members = DidatticaCdsGruppiComponenti.objects.filter(query_visibile,
                                                                  id_didattica_cds_gruppi=group['id']).values(
                'ordine',
                'id',
                'matricola',
                'cognome',
                'nome',
                'funzione_it',
                'funzione_en'
            ).distinct()
            group['members'] = members

        return res

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

    @staticmethod
    def getCdsAreas():
        query = DidatticaCds.objects.values(
            "area_cds",
            "area_cds_en",
        ).distinct()

        query = list(query)
        res = []
        for q in query:
            res.append(q['area_cds'])

        res = list(dict.fromkeys(res))
        temp = []
        for q in query:
            if q['area_cds'] not in temp and q['area_cds'] in res and q['area_cds'] is not None:
                temp.append(q)
                res.remove(q['area_cds'])

        return temp

    @staticmethod
    def getContacts(cdscod):
        date = datetime.date.today()
        last_year = int(date.strftime("%Y")) - 1
        current_year = int(date.strftime("%Y"))
        years = [last_year,current_year]
        query = DidatticaCopertura.objects.filter(
            cds_cod=cdscod,
            aa_off_id__in=years,
            personale__flg_cessato=0,
            personale__fl_docente=1,
        ).values(
            'personale__nome',
            'personale__cognome',
            'personale__middle_name',
            'personale__matricola',
            'personale__cd_uo_aff_org',
            'personale__ds_aff_org'
        ).order_by('personale__cognome')
        for q in query:
            q['DepartmentUrl'] = DidatticaDipartimentoUrl.objects.filter(dip_cod=q['personale__cd_uo_aff_org']).values(
                'dip_url'
            )
        return query


    @staticmethod
    def getHighFormationMasters(search, director, coursetype, erogation, department, language, year):

        query_search = Q()
        query_director = Q()
        query_coursetype = Q()
        query_erogation = Q()
        query_department = Q()
        query_language = Q()
        query_year = Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(titolo_it__icontains=k) | Q(matricola_direttore_scientifico__cognome__istartswith=k)
                query_search &= q_nome
        if director:
            query_director = Q(matricola_direttore_scientifico__exact=director)
        if coursetype:
            coursetypes = coursetype.split(",")
            query_coursetype = Q(id_alta_formazione_tipo_corso__in=coursetypes)
        if erogation:
            query_erogation = Q(id_alta_formazione_mod_erogazione=erogation)
        if department:
            query_department = Q(id_dipartiento_riferimento__dip_cod=department)
        if language:
            query_language = Q(lingua__exact=language)
        if year:
            query_year = Q(anno_rilevazione__exact=year)

        query = AltaFormazioneDatiBase.objects.filter(
            query_search,
            query_director,
            query_erogation,
            query_coursetype,
            query_department,
            query_language,
            query_year,
        ).values(
            'id',
            'titolo_it',
            'titolo_en',
            'id_alta_formazione_tipo_corso',
            'id_alta_formazione_tipo_corso__tipo_corso_descr',
            'id_alta_formazione_mod_erogazione',
            'id_alta_formazione_mod_erogazione__descrizione',
            'lingua',
            'ore',
            'mesi',
            'anno_rilevazione',
            'id_dipartiento_riferimento',
            'id_dipartiento_riferimento__dip_cod',
            'id_dipartiento_riferimento__dip_des_it',
            'id_dipartiento_riferimento__dip_des_eng',
            'sede_corso',
            'num_min_partecipanti',
            'num_max_partecipanti',
            'uditori_ammessi',
            'num_max_uditori',
            'requisiti_ammissione',
            'titolo_rilasciato',
            'doppio_titolo',
            'matricola_direttore_scientifico',
            'nome_origine_direttore_scientifico',
            'quota_iscrizione',
            'quota_uditori',
            'funzione_lavoro',
            'obiettivi_formativi_summer_school',
            'competenze',
            'sbocchi_occupazionali',
            'obiettivi_formativi_corso',
            'modalita_svolgimento_prova_finale',
            'numero_moduli',
            'stage_tirocinio',
            'ore_stage_tirocinio',
            'cfu_stage',
            'mesi_stage',
            'tipo_aziende_enti_tirocinio',
            'contenuti_tempi_criteri_cfu',
            'project_work'
        ).order_by('titolo_it','id')

        for q in query:
            partners = AltaFormazionePartner.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                    "id",
                    "denominazione",
                    "tipologia",
                    "sito_web"
            ).distinct()

            if len(partners) == 0:
                q['Partners'] = []
            else:
                q['Partners'] = partners

            selections = AltaFormazioneModalitaSelezione.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                    "id",
                    "tipo_selezione",
            ).distinct()

            if len(selections) == 0:
                q['Selections'] = []
            else:
                q['Selections'] = selections

            internal_scientific_council = AltaFormazioneConsiglioScientificoInterno.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                'matricola_cons',
                'nome_origine_cons'
            )

            if len(internal_scientific_council) == 0:
                q['InternalCouncil'] = []
            else:
                q['InternalCouncil'] = internal_scientific_council

            external_scientific_council = AltaFormazioneConsiglioScientificoEsterno.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                'nome_cons',
                'ruolo_cons',
                'ente_cons'
            )

            if len(external_scientific_council) == 0:
                q['ExternalCouncil'] = []
            else:
                q['ExternalCouncil'] = external_scientific_council

            teaching_plan = AltaFormazionePianoDidattico.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                'id',
                'modulo',
                'ssd',
                'num_ore',
                'cfu',
                'verifica_finale'
            )

            if len(teaching_plan) == 0:
                q['TeachingPlan'] = []
            else:
                q['TeachingPlan'] = teaching_plan

            teaching_assignments = AltaFormazioneIncaricoDidattico.objects.filter(
                id_alta_formazione_dati_base=q['id']).values(
                'id',
                'modulo',
                'num_ore',
                'docente',
                'qualifica',
                'ente',
                'tipologia'
            )

            if len(teaching_assignments) == 0:
                q['TeachingAssignments'] = []
            else:
                q['TeachingAssignments'] = teaching_assignments

        return query

    @staticmethod
    def getHighFormationMaster(master_id):


        query = AltaFormazioneDatiBase.objects.filter(
            id=master_id
        ).values(
            'id',
            'titolo_it',
            'titolo_en',
            'id_alta_formazione_tipo_corso',
            'id_alta_formazione_tipo_corso__tipo_corso_descr',
            'id_alta_formazione_mod_erogazione',
            'id_alta_formazione_mod_erogazione__descrizione',
            'ore',
            'mesi',
            'lingua',
            'anno_rilevazione',
            'id_dipartiento_riferimento',
            'id_dipartiento_riferimento__dip_cod',
            'id_dipartiento_riferimento__dip_des_it',
            'id_dipartiento_riferimento__dip_des_eng',
            'sede_corso',
            'num_min_partecipanti',
            'num_max_partecipanti',
            'uditori_ammessi',
            'num_max_uditori',
            'requisiti_ammissione',
            'titolo_rilasciato',
            'doppio_titolo',
            'matricola_direttore_scientifico',
            'nome_origine_direttore_scientifico',
            'quota_iscrizione',
            'quota_uditori',
            'funzione_lavoro',
            'obiettivi_formativi_summer_school',
            'competenze',
            'sbocchi_occupazionali',
            'obiettivi_formativi_corso',
            'modalita_svolgimento_prova_finale',
            'numero_moduli',
            'stage_tirocinio',
            'ore_stage_tirocinio',
            'cfu_stage',
            'mesi_stage',
            'tipo_aziende_enti_tirocinio',
            'contenuti_tempi_criteri_cfu',
            'project_work'
        ).order_by('titolo_it', 'id')

        query = list(query)

        query[0]['Partners'] = AltaFormazionePartner.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            "id",
            "denominazione",
            "tipologia",
            "sito_web"
        ).distinct()


        query[0]['Selections'] = AltaFormazioneModalitaSelezione.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            "id",
            "tipo_selezione",
        ).distinct()

        query[0]['InternalCouncil'] = AltaFormazioneConsiglioScientificoInterno.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            'matricola_cons',
            'nome_origine_cons'
        ).distinct()

        query[0]['ExternalCouncil'] = AltaFormazioneConsiglioScientificoEsterno.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            'nome_cons',
            'ruolo_cons',
            'ente_cons'
        ).distinct()

        query[0]['TeachingPlan'] = AltaFormazionePianoDidattico.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            'id',
            'modulo',
            'ssd',
            'num_ore',
            'cfu',
            'verifica_finale'
        ).distinct()

        query[0]['TeachingAssignments'] = AltaFormazioneIncaricoDidattico.objects.filter(
            id_alta_formazione_dati_base=master_id).values(
            'id',
            'modulo',
            'num_ore',
            'docente',
            'qualifica',
            'ente',
            'tipologia'
        ).distinct()

        return query


    @staticmethod
    def getErogationModes():

        query = AltaFormazioneModalitaErogazione.objects.values(
            'id',
            'descrizione'
        )

        return query

    @staticmethod
    def getHighFormationCourseTypes():

        query = AltaFormazioneTipoCorso.objects.values(
            'id',
            'tipo_corso_descr'
        )

        return query

    @staticmethod
    def getCdsWebsites(search, academic_year, cdslanguage, course_class):
        query_search = Q()
        query_year = Q()
        query_cdslanguage = Q()
        query_courseclass = Q()

        if search:
            for k in search.split(" "):
                q_nome_corso_it = Q(nome_corso_it__icontains=k)
                query_search &= q_nome_corso_it
        if academic_year:
            query_year = Q(aa=academic_year)
        if cdslanguage:
            for k in cdslanguage.split(" "):
                q_cdslanguage = Q(lingua_it__icontains=k) | Q(lingua_en__icontains=k)
                query_cdslanguage &= q_cdslanguage
        if course_class:
            query_courseclass = Q(classe_laurea_it=course_class) | Q(classe_laurea_en=course_class)

        query = SitoWebCdsDatiBase.objects.filter(
            query_search,
            query_year,
            query_cdslanguage,
            query_courseclass
            ).values(
            "id",
            'cds_id',
            "cds_cod",
            'aa',
            "nome_corso_it",
            "nome_corso_en",
            "classe_laurea_it",
            "classe_laurea_en",
            "classe_laurea_interclasse_it",
            "classe_laurea_interclasse_en",
            "lingua_it",
            "lingua_en",
            "durata",
            "num_posti",
            "link_video_cds_it",
            "link_video_cds_en",
            "descrizione_corso_it",
            "descrizione_corso_en",
            "accesso_corso_it",
            "accesso_corso_en",
            "obiettivi_corso_it",
            "obiettivi_corso_en",
            "sbocchi_professionali_it",
            "sbocchi_professionali_en",
            "tasse_contributi_esoneri_it",
            "tasse_contributi_esoneri_en",
            "borse_studio_it",
            "borse_studio_en",
            "agevolazioni_it",
            "agevolazioni_en",
            "corso_in_pillole_it",
            "corso_in_pillole_en",
            "cosa_si_studia_it",
            "cosa_si_studia_en",
            "come_iscriversi_it",
            "come_iscriversi_en",
            "sito_web_it",
            "sito_web_en",
            "sito_web_cds_status",
            'id_didattica_regolamento'
        )

        query = list(query)

        for q in query:

            languages_it = q['lingua_it'].split(', ')
            languages_en = q['lingua_en'].split(', ')

            q['lingua_it'] = languages_it
            q['lingua_en'] = languages_en


            ex_studenti = SitoWebCdsExStudenti.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'ordine',
                'nome',
                'profilo_it',
                'profilo_en',
                'link_it',
                'link_en',
                'foto'
            ).order_by('ordine')
            if len(ex_studenti) > 0:
                q['ExStudents'] = ex_studenti
            else:
                q['ExStudents'] = []
            links = SitoWebCdsLink.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'ordine',
                'descrizione_link_it',
                'descrizione_link_en',
                'link_it',
                'link_en',
            ).order_by('ordine')
            if len(links) > 0:
                q['CdsLink'] = links
            else:
                q['CdsLink'] = []

            sliders = SitoWebCdsSlider.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'ordine',
                'slider_it',
                'slider_en',
            ).order_by('ordine')
            if len(sliders) > 0:
                q['CdsSliders'] = sliders
            else:
                q['CdsSliders'] = []


        return query

    @staticmethod
    def getCdsWebsite(cds_cod):
        query = SitoWebCdsDatiBase.objects.filter(cds_cod__exact=cds_cod).values(
            "id",
            'cds_id',
            "cds_cod",
            'aa',
            "nome_corso_it",
            "nome_corso_en",
            "classe_laurea_it",
            "classe_laurea_en",
            "classe_laurea_interclasse_it",
            "classe_laurea_interclasse_en",
            "lingua_it",
            "lingua_en",
            "durata",
            "num_posti",
            "link_video_cds_it",
            "link_video_cds_en",
            "descrizione_corso_it",
            "descrizione_corso_en",
            "accesso_corso_it",
            "accesso_corso_en",
            "obiettivi_corso_it",
            "obiettivi_corso_en",
            "sbocchi_professionali_it",
            "sbocchi_professionali_en",
            "tasse_contributi_esoneri_it",
            "tasse_contributi_esoneri_en",
            "borse_studio_it",
            "borse_studio_en",
            "agevolazioni_it",
            "agevolazioni_en",
            "corso_in_pillole_it",
            "corso_in_pillole_en",
            "cosa_si_studia_it",
            "cosa_si_studia_en",
            "come_iscriversi_it",
            "come_iscriversi_en",
            "sito_web_it",
            "sito_web_en",
            "sito_web_cds_status",
            'id_didattica_regolamento'
        )

        query = list(query)
        for q in query:

            languages_it = q['lingua_it'].split(', ')
            languages_en = q['lingua_en'].split(', ')

            q['lingua_it'] = languages_it
            q['lingua_en'] = languages_en


            ex_studenti = SitoWebCdsExStudenti.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'nome',
                'ordine',
                'profilo_it',
                'profilo_en',
                'link_it',
                'link_en',
                'foto'
            ).order_by('ordine')
            if len(ex_studenti) > 0:
                q['ExStudents'] = ex_studenti
            else: # pragma: no cover
                q['ExStudents'] = []
            links = SitoWebCdsLink.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'ordine',
                'descrizione_link_it',
                'descrizione_link_en',
                'link_it',
                'link_en',
            ).order_by('ordine')
            if len(links) > 0:
                q['CdsLink'] = links
            else: # pragma: no cover
                q['CdsLink'] = []

            sliders = SitoWebCdsSlider.objects.filter(
                id_sito_web_cds_dati_base__exact=q['id']).values(
                'id',
                'ordine',
                'slider_it',
                'slider_en',
            ).order_by('ordine')
            if len(sliders) > 0:
                q['CdsSliders'] = sliders
            else:
                q['CdsSliders'] = []

        return query


    @staticmethod
    def getCdsWebsitesDegreeTypes():
        query = SitoWebCdsDatiBase.objects.values(
            "classe_laurea_it",
            "classe_laurea_en"
        ).distinct()

        return query


    @staticmethod
    def getCdsWebsitesTopics():

        query = SitoWebCdsTopic.objects.values(
            "id",
            "descr_topic_it",
            "descr_topic_en",
            'visibile'
        ).distinct()

        return query

    @staticmethod
    def getCdsWebsitesTopicArticles(cds_cod, topic_id):
        if cds_cod and topic_id:
            topic_id_list = topic_id.split(",")
            query_cdscod = Q(id_sito_web_cds_oggetti_portale__cds_id__cds_cod=cds_cod) | Q(id_sito_web_cds_articoli_regolamento__cds_id__cds_cod=cds_cod)
            query_topicid = Q(id_sito_web_cds_topic__id__in=topic_id_list)

            query = SitoWebCdsTopicArticoliReg.objects.filter(
                query_cdscod,
                query_topicid
            ).values(
                "id",
                'titolo_it',
                'titolo_en',
                "id_sito_web_cds_topic__id",
                'id_sito_web_cds_oggetti_portale',
                'id_sito_web_cds_articoli_regolamento',
                "id_sito_web_cds_topic__descr_topic_it",
                "id_sito_web_cds_topic__descr_topic_en",
                'visibile',
                'ordine'
            ).distinct().order_by('id_sito_web_cds_topic__id','ordine')

            query = list(query)

            for q in query:
                article = SitoWebCdsArticoliRegolamento.objects.filter(
                    id__exact=q['id_sito_web_cds_articoli_regolamento']).values(
                    'id',
                    'titolo_articolo_it',
                    'testo_it',
                    'titolo_articolo_en',
                    'titolo_articolo_en',
                    'testo_en',
                    'numero',
                    'visibile',
                    'aa_regdid_id',
                    'cds_id',
                    'cds_id__cds_cod',
                ).first()
                # .order_by('id_sito_web_cds_articoli_regolamento')
                q['Articles'] = article

                unicms_object = SitoWebCdsOggettiPortale.objects.filter(
                    id__exact=q['id_sito_web_cds_oggetti_portale']).values(
                    'id',
                    'cds_id',
                    'cds_id__cds_cod',
                    'aa_regdid_id',
                    'id_oggetto_portale',
                    'id_classe_oggetto_portale',
                    'testo_it',
                    'testo_en',
                    'visibile'
                ).first()

                q['CdsObjects'] = unicms_object

                other_data = SitoWebCdsTopicArticoliRegAltriDati.objects.filter(
                        id_sito_web_cds_topic_articoli_reg=q['id']
                    ).values(
                        'id',
                        'ordine',
                        'titolo_en',
                        'titolo_it',
                        'testo_it',
                        'testo_en',
                        'link',
                        'id_sito_web_cds_tipo_dato__pk',
                        'id_sito_web_cds_tipo_dato__descr_breve',
                        'visibile'
                    ).order_by('ordine')

                q['OtherData'] = other_data if other_data else []

            return query
        return {}

    @staticmethod
    def getCdsWebsitesStudyPlans(cds_cod, year, regdid):

        if cds_cod and year or regdid:
            query_cds = Q(regdid_id__cds_id__cds_cod__exact=cds_cod) if cds_cod else Q()
            query_year = Q(regdid_id__aa_reg_did__exact=year) if year else Q()
            query_regdid = Q(regdid_id__exact=regdid) if regdid else Q()

            query = DidatticaPianoRegolamento.objects.filter(
                query_cds,
                query_regdid,
                query_year,
                stato_cod='A'
               ).select_related('regdid__cds').values(
                   'regpiani_id',
                   'regdid_id',
                   'attinenza_cod',
                   'cod',
                   'aa_coorte_id',
                   'aa_regpiani_id',
                   'des',
                   'def_flg',
                   'stato_cod',
                   'stato_des',
                   'regpiani_pdr_id',
                   'regpiani_pdr_cod',
                   'regpiani_pdr_des',
                   'regpiani_pdr_aa_coorte_id',
                   'regpiani_pdr_aa_regpiani_id',
                   'flg_exp_seg_stu',
                   'regdid__cds__durata_anni'
               ).distinct().order_by('regpiani_id')

            for q in query:
                schede = DidatticaPianoSche.objects.filter(
                       regpiani_id__exact=q['regpiani_id']).values(
                    'sche_piano_id',
                    'sche_piano_des',
                    'sche_piano_cod',
                    'pds_cod',
                    'pds_des',
                    'comune_flg',

                   )

                q['PlanTabs'] = schede


                for s in schede:
                    obbl = DidatticaPianoSceltaSchePiano.objects.filter(
                            sche_piano_id__exact=s['sche_piano_id'],
                            tipo_sce_cod__exact='O'
                        ).values(
                            'sce_id',
                            'sce_des',
                            'anno_corso',
                            'apt_slot_ord_num',
                            'tipo_regsce_cod',
                            'tipo_sce_cod',
                            'tipo_sce_des',
                            'tipo_regsce_des',
                            'tipo_um_regsce_cod',
                            'min_unt',
                            'max_unt',
                            'opz_flg',
                            'vin_id',
                            'vin_sce_des',
                            'sce_id__opz_flg',
                            'sce_id__anno_corso_ant'
                            )


                    s['AfRequired'] = obbl


                    for af in obbl:

                        af_obblig = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=af['sce_id']
                        ).values(
                            'amb_id_af',
                            'anno_corso_af',
                            'ciclo_des',
                            'af_gen_des',
                            'af_id',
                            'af_gen_cod',
                            'tipo_af_des_af',
                            'ambito_des_af',
                            'sett_cod',
                            'peso',
                            'sce_id__sce_des',
                            'sce_id'
                        )


                        af['Required'] = af_obblig

                        for activity in af['Required']:
                            list_submodules = DidatticaAttivitaFormativa.objects.filter(
                                # ~Q(fat_part_stu_cod='GRP'),
                                part_stu_cod__isnull=True,
                                # af_radice_id=activity['af_id'],
                                af_pdr_id=activity['af_id'],
                                ).exclude(
                                af_id=activity['af_id']
                            ).values(
                                'af_id',
                                'af_gen_cod',
                                'des',
                                'peso',
                                'sett_cod',
                                'af_gen_des_eng',
                                'fat_part_stu_cod',
                                'lista_lin_did_af',
                                'part_stu_cod',
                                'part_stu_des',
                                'fat_part_stu_des',
                                'ciclo_des')

                            activity['MODULES'] = list_submodules


                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=af['sce_id']
                        ).values(
                            'sce_fil_and_id',
                            'sce_id',
                            'sce_fil_or_id',
                            'sce_fil_or_des',
                            'tipo_filtro_cod',
                            'tipo_filtro_des',
                            'tipo_corso_sce_fil_and_cod',
                            'cds_sce_fil_and_id',
                            'cds_sce_fil_and_cod',
                            'cds_sce_fil_and_nome',
                            'not_flg'
                        )

                        af['FilAnd'] = fil_and


                    # for obl in s['AfRequired']:
                    #
                    #     anno = DidatticaPianoSceltaSchePiano.objects.filter(
                    #         sce_id__exact=obl['sce_id'],
                    #         tipo_sce_cod__exact='O'
                    #     ).values(
                    #         'apt_slot_ord_num'
                    #     )
                    #
                    #     anno = anno[0]['apt_slot_ord_num']
                    #
                    #     obl['apt_slot_ord_num'] = anno



                    scelte = DidatticaPianoSceltaSchePiano.objects.filter(
                        ~Q(tipo_sce_cod__exact='O'),
                        sche_piano_id__exact=s['sche_piano_id'],
                    ).values(
                        'sce_id',
                        'sce_des',
                        'anno_corso',
                        'apt_slot_ord_num',
                        'tipo_regsce_cod',
                        'tipo_sce_cod',
                        'tipo_sce_des',
                        'tipo_regsce_des',
                        'tipo_um_regsce_cod',
                        'min_unt',
                        'max_unt',
                        'opz_flg',
                        'vin_id',
                        'vin_sce_des',
                        'sce_id__opz_flg',
                        'sce_id__anno_corso_ant'
                    )





                    verifica = Q(amb_id__isnull=False) | Q(amb_id_af_regsce__isnull=False) | Q(tipo_sce_cod='V')




                    s['AfChoices'] = scelte



                    for scelta in scelte:

                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=scelta['sce_id']
                        ).values(
                            'sce_fil_and_id',
                            'sce_id',
                            'sce_fil_or_id',
                            'sce_fil_or_des',
                            'tipo_filtro_cod',
                            'tipo_filtro_des',
                            'cds_sce_fil_and_id',
                            'cds_sce_fil_and_cod',
                            'cds_sce_fil_and_nome',
                            'tipo_corso_sce_fil_and_cod',
                            'not_flg'
                        )

                        scelta['FilAnd'] = fil_and


                        af_scelta = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=scelta['sce_id']
                        ).values(
                            'amb_id_af',
                            'anno_corso_af',
                            'ciclo_des',
                            'af_gen_des',
                            'af_gen_cod',
                            'af_id',
                            'tipo_af_des_af',
                            'ambito_des_af',
                            'sett_cod',
                            'peso',
                            'sce_id__sce_des',
                            'sce_id'
                        )

                        scelta['Choices'] = af_scelta

                        for activity in scelta['Choices']:
                            list_submodules = DidatticaAttivitaFormativa.objects.filter(
                                # ~Q(fat_part_stu_cod='GRP'),
                                part_stu_cod__isnull=True,
                                # af_radice_id=activity['af_id']
                                af_pdr_id=activity['af_id']
                            ).exclude(
                                af_id=activity['af_id']
                            ).values(
                                'af_id',
                                'af_gen_cod',
                                'des',
                                'af_gen_des_eng',
                                'peso',
                                'fat_part_stu_cod',
                                'lista_lin_did_af',
                                'part_stu_cod',
                                'part_stu_des',
                                'fat_part_stu_des',
                                'ciclo_des')

                            activity['MODULES'] = list_submodules



                        if af_scelta is None: # pragma: no cover

                            af_scelta = DidatticaPianoSceltaAf.objects.filter(
                                verifica,
                                sce_id__exact=scelta['sce_id']
                            ).values(
                                'amb_id_af',
                                'anno_corso_af',
                                'ciclo_des',
                                'af_gen_des',
                                'af_id',
                                'tipo_af_des_af',
                                'ambito_des_af',
                                'sett_cod',
                                'peso',
                                'sce_id__sce_des',
                                'sce_id'
                            )

                            scelta['Choices'] = af_scelta

                            for activity in scelta['Choices']:
                                list_submodules = DidatticaAttivitaFormativa.objects.filter(
                                    # ~Q(fat_part_stu_cod='GRP'),
                                    part_stu_cod__isnull=True,
                                    # af_radice_id=activity['af_id']
                                    af_pdr_id=activity['af_id']
                                ).exclude(
                                    af_id=activity['af_id']
                                ).values(
                                    'af_id',
                                    'af_gen_cod',
                                    'des',
                                    'peso',
                                    'af_gen_des_eng',
                                    'fat_part_stu_cod',
                                    'lista_lin_did_af',
                                    'part_stu_cod',
                                    'part_stu_des',
                                    'fat_part_stu_des',
                                    'ciclo_des')

                                activity['MODULES'] = list_submodules





                            # if a['amb_id'] is not None:
                            #
                            #
                            #     a['ElectiveCourses'] = DidatticaAttivitaFormativa.objects.filter(
                            #         query_cds,
                            #         query_regdid,
                            #         query_year,
                            #         Q(amb_id__exact=a['amb_id'])
                            #     ).values(
                            #         'af_gen_id',
                            #         'af_gen_cod',
                            #         'des',
                            #         'af_gen_des_eng',
                            #         'anno_corso',
                            #         'sett_cod',
                            #         'sett_des',
                            #         'peso'
                            #     )
                            #
                            #
                            #     a['ElectiveCourses'] = list(a['ElectiveCourses'])
                            #
                            #     # for el in a['ElectiveCourses']:
                            #     #     el['apt_slot_ord_num'] = a['apt_slot_ord_num']
                            #
                            # if a['amb_id_af_regsce'] is not None and a['amb_id'] is None:
                            #
                            #     a['ElectiveCourses'] = DidatticaPianoSceltaAf.objects.filter(
                            #         sce_id=a['sce_id']
                            #     ).values(
                            #         'sce_id',
                            #         'anno_corso_af',
                            #         'af_gen_des',
                            #         'ciclo_des',
                            #     )
                            #
                            #     a['ElectiveCourses'] = list(a['ElectiveCourses'])
                            #
                            #     # for el in a['ElectiveCourses']:
                            #     #     el['apt_slot_ord_num'] = a['apt_slot_ord_num']
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
                    'af_gen_cod',
                    'des',
                    'af_gen_des_eng',
                    'cds__cds_id',
                    'cds__cds_cod',
                    'regdid__regdid_id',
                    'regdid__aa_reg_did',
                    'anno_corso',
                    'ciclo_des',
                    'peso',
                    'sett_cod',
                    'sett_des',
                    'freq_obblig_flg',
                    'cds__nome_cds_it',
                    'cds__nome_cds_eng',
                    'tipo_af_des',
                    'tipo_af_cod',
                    'tipo_af_intercla_cod',
                    'tipo_af_intercla_des'
                )
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
                'af_gen_cod',
                'des',
                'af_gen_des_eng',
                'cds__cds_cod',
                'cds__cds_id',
                'regdid__regdid_id',
                'regdid__aa_reg_did',
                'anno_corso',
                'ciclo_des',
                'peso',
                'sett_cod',
                'sett_des',
                'freq_obblig_flg',
                'cds__nome_cds_it',
                'cds__nome_cds_eng',
                'tipo_af_des',
                'tipo_af_cod',
                'tipo_af_intercla_cod',
                'tipo_af_intercla_des'
            )

    @staticmethod
    def getAllActivities(language, department, cds, academic_year, period, ssd, teacher, teaching, course_year, cds_cod, teacher_code):

        query_department = Q()
        query_academic_year = Q()
        query_cds = Q()
        query_teacher = Q()
        query_teaching = Q()
        query_period = Q()
        query_ssd = Q()
        query_course_year = Q()
        query_cds_cod = Q()
        query_teacher_code = Q()


        if academic_year:
            query_academic_year = Q(aa_off_id=academic_year)
        if course_year:
            query_course_year = Q(anno_corso=course_year)
        if department:
            query_department = Q(cds_id__dip_id__dip_cod=department)
        if cds:
            if language == "it": # pragma: no cover
                query_cds = Q(cds_id__nome_cds_it__icontains=cds)
            else:
                query_cds = Q(cds_id__nome_cds_eng__icontains=cds)
        # serve un collegamento tra didatticaattivitàformativa e personale con il campo matricola_resp_did
        if teacher:
            query_teacher = Q(matricola_resp_did__cognome__istartswith=teacher)
        if teaching:
            if language == "it":
                query_teaching = Q(des__icontains=teaching)
            else:
                query_teaching = Q(af_gen_des_eng__icontains=teaching)
        if ssd:
            for k in ssd.split(" "):
                q_ssd = Q(sett_cod__icontains=k)
                query_ssd &= q_ssd
        if period:
            query_period = Q(ciclo_des=period)

        if cds_cod:
            query_cds_cod = Q(cds_id__cds_cod__exact=cds_cod)

        if teacher_code:
            query_teacher_code = Q(personale_id__matricola__exact=teacher_code)


        coperture = DidatticaCopertura.objects.filter(
            query_teacher_code
        ).values(
            'af_id'
        )

        query_coperture = Q(af_id__in=coperture) | Q(af_master_id__in=coperture)

        query = DidatticaAttivitaFormativa.objects.filter(query_department,
                                                          query_academic_year,
                                                          query_cds,
                                                          query_period,
                                                          query_ssd,
                                                          query_teaching,
                                                          query_course_year,
                                                          query_coperture,
                                                          query_teacher,
                                                          query_cds_cod
                                                          ).values(
            'af_id',
            'af_gen_cod',
            'des',
            'af_gen_des_eng',
            'sett_cod',
            'sett_des',
            'ciclo_des',
            'lista_lin_did_af',
            'aa_off_id',
            'regdid_id',
            'cds_id',
            'cds_id__cds_cod',
            'cds_id__nome_cds_it',
            'cds_id__nome_cds_eng',
            'cds_id__dip_id__dip_cod',
            'cds_id__dip_id__dip_des_it',
            'cds_id__dip_id__dip_des_eng',
            'fat_part_stu_cod',
            'fat_part_stu_des',
            'part_stu_cod',
            'part_stu_des',
            'anno_corso',
            'matricola_resp_did',
            'matricola_resp_did__nome',
            'matricola_resp_did__cognome',
            'matricola_resp_did__middle_name',
            'pds_des',
            'af_master_id',
            'af_radice_id',
        ).distinct().order_by('des')

        lista_padri = {}
        for i in query:
            lista_padri[i['af_id']] = i['des']

        for q in query:

            padre = lista_padri[q['af_id']]

            if padre:
                q['Father'] = padre
            else:
                q['Father'] = None


            if q['af_gen_cod'] == None: # pragma: no cover
                codice = None
                codice = DidatticaCopertura.objects.filter(af_id__exact=q['af_id']).values(
                    'af_gen_cod'
                )

                codice = list(codice)
                if len(codice)>0:
                    codice = codice[0]['af_gen_cod']

                if codice:
                    q['af_gen_cod'] = codice
                else:
                    q['af_gen_cod'] = None



            if q['anno_corso'] == None: # pragma: no cover
                anno = None
                anno = DidatticaCopertura.objects.filter(af_id__exact=q['af_id']).values(
                    'anno_corso'
                )

                anno = list(anno)

                if len(anno)>0:
                    anno = anno[0]['anno_corso']

                if anno:
                    q['anno_corso'] = anno
                else:
                    q['anno_corso'] = None


            if q['ciclo_des'] == None: # pragma: no cover
                semestre = None
                semestre = DidatticaCopertura.objects.filter(af_id__exact=q['af_id']).values(
                    'ciclo_des'
                )

                semestre = list(semestre)

                if len(semestre)>0:
                    semestre = semestre[0]['ciclo_des']

                if semestre:
                    q['ciclo_des'] = semestre
                else:
                    q['ciclo_des'] = None


        # for q in query:
        #     padre = DidatticaAttivitaFormativa.objects.filter(af_id__exact=q['af_radice_id']).values(
        #     'des'
        #     )
        #
        #     if padre:
        #         q['Father'] = padre
        #     else:
        #         q['Father'] = None

        # for q in query:
        #
        #     name = Personale.objects.filter(matricola=q['matricola_resp_did']).values(
        #         'nome',
        #         'cognome',
        #         'middle_name'
        #     )
        #     if(len(name) != 0):
        #         q['DirectorName'] = name
        #     else:
        #         q['DirectorName'] = None

        return query



    @staticmethod
    def getAttivitaFormativaWithSubModules(af_id, language):
        list_submodules = DidatticaAttivitaFormativa.objects.filter(
            Q(af_radice_id=af_id) | Q(af_pdr_id=af_id)).exclude(
            af_id=af_id
        ).values(
            'af_id',
            'af_gen_cod',
            'des',
            'af_gen_des_eng',
            'fat_part_stu_cod',
            'lista_lin_did_af',
            'part_stu_cod',
            'part_stu_des',
            'fat_part_stu_des',
            'ciclo_des',
            'matricola_resp_did')

        query = DidatticaAttivitaFormativa.objects.filter(
            af_id=af_id).order_by(
            'anno_corso',
            'ciclo_des') .values(
            'af_id',
            'af_gen_cod',
            'des',
            'af_gen_des_eng',
            'cds__cds_cod',
            'cds__cds_id',
            'lista_lin_did_af',
            'pds_cod',
            'pds_des',
            'regdid__regdid_id',
            'regdid__aa_reg_did',
            'anno_corso',
            'ciclo_des',
            'peso',
            'sett_cod',
            'sett_des',
            'freq_obblig_flg',
            'cds__nome_cds_it',
            'cds__nome_cds_eng',
            'tipo_af_des',
            'tipo_af_cod',
            'tipo_af_intercla_cod',
            'tipo_af_intercla_des',
            'matricola_resp_did',
            'mutuata_flg',
            'af_master_id',
            'af_radice_id',
            'af_pdr_id',
            'didatticacopertura__coper_peso',
            'part_stu_cod',
            'fat_part_stu_cod',
            'part_stu_des',
            'fat_part_stu_des'
        )

        lingue = DidatticaTestiAf.objects.filter(tipo_testo_af_cod='LINGUA_INS',
                                                af_id=af_id).values(
            'testo_af_ita',
            'testo_af_eng'
        )


        id_master = None
        mutuata_da = None
        if not query: raise Http404
        if query.first()['mutuata_flg'] == 1:
            id_master = query.first()['af_master_id']
            mutuata_da = DidatticaAttivitaFormativa.objects.filter(
                af_id=id_master).values(
                'af_id',
                'af_gen_cod',
                'des',
                'cds__cds_cod',
                'cds__cds_id',
                'cds__nome_cds_it',
                'cds__nome_cds_eng',
                'pds_cod',
                'pds_des',
                'af_gen_des_eng',
                'ciclo_des',
                'regdid__regdid_id',
                'regdid__aa_reg_did',
                'anno_corso',
                'didatticacopertura__coper_peso'
            ).first()


        attivita_mutuate_da_questa = DidatticaAttivitaFormativa.objects.filter(
            af_master_id=af_id, mutuata_flg=1) .exclude(
            af_id=af_id) .values(
            'af_id',
            'af_gen_cod',
            'des',
            'af_gen_des_eng',
            'ciclo_des',
            'regdid__regdid_id',
            'regdid__aa_reg_did',
            'anno_corso',
            'didatticacopertura__coper_peso',
            'cds__cds_cod',
            'cds__cds_id',
            'cds__nome_cds_it',
            'cds__nome_cds_eng',
            'pds_cod',
            'pds_des',
        )
        radice = query.first()
        id_radice_padre = radice['af_pdr_id']
        id_radice = radice['af_radice_id']


        activity_root = DidatticaAttivitaFormativa.objects.filter(
            af_id=id_radice).exclude(
            af_id=af_id).values(
            'af_id',
            'af_gen_cod',
            'des',
            'af_gen_des_eng',
            'ciclo_des',
            'regdid__regdid_id',
            'regdid__aa_reg_did',
            'anno_corso',
            'didatticacopertura__coper_peso',
            'cds__cds_cod',
            'cds__cds_id',
            'cds__nome_cds_it',
            'cds__nome_cds_eng',
            'pds_cod',
            'pds_des',
        )
        if len(activity_root) == 0:
            activity_root = None
        else:
            activity_root = activity_root.first()

        activity_father = None

        if id_radice_padre and id_radice_padre != id_radice: # pragma: no cover

            activity_father = DidatticaAttivitaFormativa.objects.filter(
                af_id=id_radice_padre).exclude(
                af_id=af_id).values(
                'af_id',
                'af_gen_cod',
                'des',
                'af_gen_des_eng',
                'ciclo_des',
                'regdid__regdid_id',
                'regdid__aa_reg_did',
                'anno_corso',
                'didatticacopertura__coper_peso',
                'cds__cds_cod',
                'cds__cds_id',
                'cds__nome_cds_it',
                'cds__nome_cds_eng',
                'pds_cod',
                'pds_des',
            )
            if len(activity_father) == 0:
                activity_father = None
            else:
                activity_father = activity_father.first()

        copertura = DidatticaCopertura.objects.filter(
            af_id=af_id).values(
            'personale__id',
            'personale__nome',
            'personale__cognome',
            'personale__middle_name',
            'personale__matricola',
            'fat_part_stu_cod',
            'fat_part_stu_des',
            'part_stu_cod',
            'part_stu_des',
        )
        query = list(query)

        filtered_hours = DidatticaCoperturaDettaglioOre.objects.filter(~Q(coper_id__stato_coper_cod='R'),coper_id__af_id=af_id).values(
            'tipo_att_did_cod',
            'ore',
            'coper_id__personale_id__matricola',
            'coper_id__personale_id__nome',
            'coper_id__personale_id__cognome',
            'coper_id__personale_id__middle_name',
            'coper_id__personale_id__flg_cessato',
            'coper_id'
        )
        filtered_hours = list(filtered_hours)


        for hour in filtered_hours:
            for hour2 in filtered_hours:
                if hour['tipo_att_did_cod'] == hour2['tipo_att_did_cod'] and hour['coper_id__personale_id__matricola'] == hour2['coper_id__personale_id__matricola'] and hour['coper_id'] != hour2['coper_id']: #pragma: no cover
                    hour['ore'] = hour['ore'] + hour2['ore']
                    filtered_hours.remove(hour2)



        query[0]['Hours'] = filtered_hours


        query[0]['Modalities'] = DidatticaAttivitaFormativaModalita.objects.filter(af_id=af_id).values(
            'mod_did_af_id',
            'mod_did_cod',
            'mod_did_des'
        )


        query[0]['LANGUAGEIT'] = None
        query[0]['LANGUAGEEN'] = None

        for l in lingue: # pragma: no cover
            query[0]['LANGUAGEIT'] = l['testo_af_ita']
            query[0]['LANGUAGEEN'] = l['testo_af_eng']


        query[0]['BorrowedFrom'] = mutuata_da
        query[0]['ActivitiesBorrowedFromThis'] = attivita_mutuate_da_questa

        query[0]['ActivityRoot'] = activity_root

        query[0]['ActivityFather'] = activity_father

        query[0]['StudyActivityTeacherID'] = None
        query[0]['StudyActivityTeacherName'] = None

        query[0]['PartitionCod'] = None
        query[0]['PartitionDescription'] = None
        query[0]['ExtendedPartitionCod'] = None
        query[0]['ExtendedPartitionDescription'] = None

        # for q in copertura:
        #     if q['personale__matricola'] == query[0]['matricola_resp_did']:
        #         query[0]['StudyActivityTeacherID'] = q['personale__matricola']
        #         if q['personale__cognome'] and q['personale__nome']:
        #             query[0]['StudyActivityTeacherName'] = f"{q['personale__cognome']} {q['personale__nome']}"
        #             if q['personale__middle_name']:
        #                 query[0]['StudyActivityTeacherName'] = f"{query[0]['StudyActivityTeacherName']} {q['personale__middle_name']}"
        #
        #         query[0]['PartitionCod'] = q['part_stu_cod']
        #         query[0]['PartitionDescription'] = q['part_stu_des']
        #         query[0]['ExtendedPartitionCod'] = q['fat_part_stu_cod']
        #         query[0]['ExtendedPartitionDescription'] = q['fat_part_stu_des']

        texts_af = DidatticaTestiAf.objects.filter(
            af_id=af_id).values(
            'tipo_testo_af_cod',
            'testo_af_ita',
            'testo_af_eng')

        query[0]['MODULES'] = list()
        allowed = []
        for i in range(len(list_submodules)):
            copertura = DidatticaCopertura.objects.filter(
                af_id=list_submodules[i]['af_id'],
                personale__matricola=list_submodules[i]['matricola_resp_did']).values(
                'fat_part_stu_cod',
                'fat_part_stu_des',
                'part_stu_cod',
                'part_stu_des',
            ).first()

            groups = DidatticaAttivitaFormativa.objects.filter(af_pdr_id=list_submodules[i]['af_id'],fat_part_stu_cod='GRP').values(
                'af_id',
                'af_gen_cod',
                'des',
                'fat_part_stu_cod',
                'fat_part_stu_des',
                'part_stu_cod',
                'part_stu_des',
                'af_gen_des_eng'
            )

            groups_serialize = []
            for j in range(len(groups)):

                groups_serialize.append({
                    'StudyActivityID': groups[j]['af_id'],
                    'StudyActivityCod': groups[j]['af_gen_cod'],
                    'StudyActivityName': groups[j]['des'] if language == 'it' or
                        groups[j]['af_gen_des_eng'] is None else groups[j]['af_gen_des_eng'],
                    'StudyActivityPartitionCod': groups[j]['part_stu_cod'],
                    'StudyActivityPartitionDescription': groups[j]['part_stu_des'],
                    'StudyActivityExtendedPartitionCod': groups[j]['fat_part_stu_cod'],
                    'StudyActivityExtendedPartitionDes': groups[j]['fat_part_stu_des'],
                })
            groups = groups.values('af_id')
            groups = list(groups)
            for g in groups:
                allowed.append(g['af_id'])

            if list_submodules[i]['af_id'] not in allowed:
                query[0]['MODULES'].append({
                        'StudyActivityID': list_submodules[i]['af_id'],
                        'StudyActivityCod': list_submodules[i]['af_gen_cod'],
                        'StudyActivityName': list_submodules[i]['des'] if language == 'it' or list_submodules[i]['af_gen_des_eng'] is None else list_submodules[i]['af_gen_des_eng'],
                        'StudyActivitySemester': list_submodules[i]['ciclo_des'],
                        'StudyActivityPartitionCod': list_submodules[i]['part_stu_cod'],
                        'StudyActivityPartitionDescription': list_submodules[i]['part_stu_des'],
                        'StudyActivityExtendedPartitionCod': list_submodules[i]['fat_part_stu_cod'],
                        'StudyActivityExtendedPartitionDes': list_submodules[i]['fat_part_stu_des'],
                        'StudyActivityGroups': groups_serialize

                })
            elif list_submodules[i]['af_id'] not in allowed and list_submodules[i]['fat_part_stu_cod'] == 'GRP': # pragma: no cover
                query[0]['MODULES'].append({
                    'StudyActivityID': list_submodules[i]['af_id'],
                    'StudyActivityCod': list_submodules[i]['af_gen_cod'],
                    'StudyActivityName': list_submodules[i]['des'] if language == 'it' or list_submodules[i][
                        'af_gen_des_eng'] is None else list_submodules[i]['af_gen_des_eng'],
                    'StudyActivitySemester': list_submodules[i]['ciclo_des'],
                    'StudyActivityPartitionCod': list_submodules[i]['part_stu_cod'],
                    'StudyActivityPartitionDescription': list_submodules[i]['part_stu_des'],
                    'StudyActivityExtendedPartitionCod': list_submodules[i]['fat_part_stu_cod'],
                    'StudyActivityExtendedPartitionDes': list_submodules[i]['fat_part_stu_des'],
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
        query[0]['StudyActivityDevelopmentGoal'] = None

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
            'OB_SVIL_SOS': 'StudyActivityDevelopmentGoal',
            'PROPEDE': None,
            'LINGUA_INS': None,
            'PAG_WEB_DOC': None,
            'ALTRO': None,
        }

        for text in texts_af:
            query[0][dict_activity[text['tipo_testo_af_cod']]
                     ] = text['testo_af_ita'] if language == 'it' or text['testo_af_eng'] is None else text['testo_af_eng']
        return query

    # @staticmethod
    # def getDocentiPerReg(regdid_id):
    #
    #     query = DidatticaAttivitaFormativa.objects.filter(
    #         didatticacopertura__personale__fl_docente=1,
    #         regdid__regdid_id=regdid_id,
    #         didatticacopertura__personale__isnull=False) .order_by(
    #         'didatticacopertura__personale__cd_ruolo',
    #         'didatticacopertura__personale__cognome',
    #         'didatticacopertura__personale__nome') .values(
    #         'didatticacopertura__personale__matricola',
    #         'didatticacopertura__personale__nome',
    #         'didatticacopertura__personale__cognome',
    #         'didatticacopertura__personale__middle_name',
    #         'didatticacopertura__personale__cd_ruolo',
    #         'didatticacopertura__personale__cd_ssd').distinct()
    #
    #     return query


class ServiceDocente:
    # @staticmethod
    # def getResearchGroups(teacher_id):
    #
    #     query = Personale.objects.filter(
    #         matricola__exact=teacher_id,
    #         fl_docente=1,
    #         ricercadocentegruppo__dt_fine__isnull=True) .order_by('ricercadocentegruppo__ricerca_gruppo__nome') .values(
    #         'ricercadocentegruppo__ricerca_gruppo__id',
    #         'ricercadocentegruppo__ricerca_gruppo__nome',
    #         'ricercadocentegruppo__ricerca_gruppo__descrizione').distinct()
    #
    #     return query

    @staticmethod
    def getAllResearchGroups(search, teacher, department, cod):

        query_search = Q()
        query_cod = Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(nome__icontains=k) | Q(descrizione__icontains=k) | Q(ricerca_erc1_id__descrizione__icontains=k) | Q(ricercadocentegruppo__personale_id__cognome__istartswith=k)
                query_search &= q_nome

        if cod:
            cod = cod.split(",")
            query_cod = Q(ricerca_erc1_id__cod_erc1__in=cod)

        query = RicercaGruppo.objects.filter(query_search, query_cod).order_by(
            'nome').values('id', 'nome', 'descrizione','ricerca_erc1_id__cod_erc1', 'ricerca_erc1_id__descrizione').distinct()

        if teacher is not None or department is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteGruppo.objects.filter(
                    ricerca_gruppo_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede')

                q['Teachers'] = None
                if department is None:
                    for t in teachers:
                        if t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers
                    if q['Teachers'] is not None:
                        res.append(q)
                if teacher is None:
                    for t in teachers:
                        if t['personale_id__sede'] == department:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if t['personale_id__sede'] == department and t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)
            # eliminazione duplicati di res
            res = [i for n, i in enumerate(res) if i not in res[n + 1:]]
            return res

        else:
            for q in query:
                teachers = RicercaDocenteGruppo.objects.filter(
                    ricerca_gruppo_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede')

                if len(teachers) == 0:
                    q['Teachers'] = []
                else:
                    q['Teachers'] = teachers

            return query

    @staticmethod
    def getResearchLines(teacher_id, only_active=True):
        query_is_active_app = Q(ricercadocentelineaapplicata__ricerca_linea_applicata__visibile=True) if only_active else Q()
        query_is_active_base = Q(ricercadocentelineabase__ricerca_linea_base__visibile=True) if only_active else Q()

        linea_applicata = Personale.objects.filter(
            query_is_active_app,
            matricola__exact=teacher_id,
            fl_docente=1,
            ricercadocentelineaapplicata__dt_fine__isnull=True) .order_by('ricercadocentelineaapplicata__ricerca_linea_applicata__id') .values(
            'ricercadocentelineaapplicata__ricerca_linea_applicata__id',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod',
            'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description').distinct()

        linea_base = Personale.objects.filter(
            query_is_active_base,
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

        for l in linea_base:
            if l['ricercadocentelineabase__ricerca_linea_base__id'] == None:
                linea_base.remove(l)

        for l in linea_applicata:
            if l['ricercadocentelineaapplicata__ricerca_linea_applicata__id'] == None:
                linea_applicata.remove(l)

        linea_applicata.extend(linea_base)

        return linea_applicata

    @staticmethod
    def getAllResearchLines(search, year, department, ercs, asters, exclude_base=False, exclude_applied=False, only_active=True):
        if exclude_applied and exclude_base:
            return []

        query_search = Q()
        query_year = Q()
        query_ercs = Q()
        query_asters = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year:
            query_year = Q(anno=year)
        if ercs:
            ercs = ercs.split(",")
            query_ercs = Q(ricerca_erc2_id__ricerca_erc1_id__cod_erc1__in=ercs)

        if asters:
            asters = asters.split(",")
            query_asters = Q(ricerca_aster2_id__ricerca_aster1_id__in=asters)

        linea_base = []
        linea_applicata = []

        if not exclude_base:
            linea_base = RicercaLineaBase.objects.filter(
                query_search,
                query_year,
                query_ercs,
                query_is_active
                ).order_by('descrizione').values(
                'id',
                'descrizione',
                'descr_pubblicaz_prog_brevetto',
                'anno',
                'ricerca_erc2_id__cod_erc2',
                'ricerca_erc2_id__descrizione',
                'ricerca_erc2_id__ricerca_erc1_id__cod_erc1',
                'ricerca_erc2_id__ricerca_erc1_id__descrizione',
                'ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__erc0_cod',
                'ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description',
                'ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en',
                'visibile'
            ).distinct()

        if not exclude_applied:
            linea_applicata = RicercaLineaApplicata.objects.filter(
                query_search,
                query_year,
                query_asters,
                query_is_active
            ).order_by('descrizione').values(
                'id',
                'descrizione',
                'descr_pubblicaz_prog_brevetto',
                'anno',
                'ricerca_aster2_id__ricerca_aster1_id',
                'ricerca_aster2_id__descrizione',
                'visibile'
            ).distinct()

        if ercs and asters:
            pass

        elif ercs:
            linea_applicata = []

        elif asters:
            linea_base = []

        for q in linea_base:
            teachers = RicercaDocenteLineaBase.objects.filter(
                ricerca_linea_base_id=q['id']
            ).values(
                'personale_id__matricola',
                'personale_id__nome',
                'personale_id__middle_name',
                'personale_id__cognome',
                'personale_id__ds_sede',
                'personale_id__sede',
                'personale_id__flg_cessato')

            if len(teachers) == 0:
                q['Teachers'] = []
            else:
                q['Teachers'] = teachers

        for q in linea_applicata:
            teachers = RicercaDocenteLineaApplicata.objects.filter(
                ricerca_linea_applicata_id=q['id']
            ).values(
                'personale_id__matricola',
                'personale_id__nome',
                'personale_id__middle_name',
                'personale_id__cognome',
                'personale_id__ds_sede',
                'personale_id__sede',
                'personale_id__flg_cessato')

            if len(teachers) == 0:
                q['Teachers'] = []
            else:
                q['Teachers'] = teachers

        linea_applicata = list(linea_applicata)
        for linea in linea_applicata:
            linea['Tipologia'] = 'applicata'


        linea_base = list(linea_base)
        for linea in linea_base:
            linea['Tipologia'] = 'base'

        if department is not None:
            res = []
            for q in linea_base:
                teachers = RicercaDocenteLineaBase.objects.filter(
                    ricerca_linea_base_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede',
                    'personale_id__flg_cessato')

                q['Teachers'] = None

                for t in teachers:
                    if t['personale_id__sede'] == department:
                        q['Teachers'] = teachers

                if q['Teachers'] is not None:
                    res.append(q)

            for q in linea_applicata:
                teachers = RicercaDocenteLineaApplicata.objects.filter(
                    ricerca_linea_applicata_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede',
                    'personale_id__flg_cessato')

                q['Teachers'] = None

                for t in teachers:
                    if t['personale_id__sede'] == department:
                        q['Teachers'] = teachers

                if q['Teachers'] is not None:
                        res.append(q)

            return res


        linea_applicata.extend(linea_base)

        linee = sorted(linea_applicata, key=lambda d: d['descrizione'])

        return linee

    @staticmethod
    def getBaseResearchLines(search, teacher, dip, year, only_active=True):

        query_search = Q()
        query_year = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year is not None:
            query_year = Q(anno=year)

        query = RicercaLineaBase.objects.filter(
            query_search,
            query_year,
            query_is_active).order_by('descrizione').values(
            'id',
            'descrizione',
            'descr_pubblicaz_prog_brevetto',
            'anno',
            'ricerca_erc2_id__cod_erc2',
            'ricerca_erc2_id__descrizione',
            'visibile'
        ).distinct()

        if teacher is not None or dip is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteLineaBase.objects.filter(
                    ricerca_linea_base_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede')

                q['Teachers'] = None
                if dip is None:
                    for t in teachers:
                        if t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)

                elif teacher is None:
                    for t in teachers:
                        if t['personale_id__sede'] == dip:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if t['personale_id__sede'] == dip and t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)

            return res

        for q in query:
            teachers = RicercaDocenteLineaBase.objects.filter(
                ricerca_linea_base_id=q['id']
            ).values(
                'personale_id__matricola',
                'personale_id__nome',
                'personale_id__middle_name',
                'personale_id__cognome',
                'personale_id__ds_sede',
                'personale_id__sede')

            if len(teachers) == 0:
                q['Teachers'] = []
            else:
                q['Teachers'] = teachers

        return query

    @staticmethod
    def getAppliedResearchLines(search, teacher, dip, year, only_active=True):
        query_search = Q()
        query_year = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year is not None:
            query_year = Q(anno=year)

        query = RicercaLineaApplicata.objects.filter(
            query_search,
            query_year,
            query_is_active).order_by('descrizione').values(
            'id',
            'descrizione',
            'descr_pubblicaz_prog_brevetto',
            'anno',
            'ricerca_aster2_id__ricerca_aster1_id',
            'ricerca_aster2_id__descrizione',
            'visibile'
        ).distinct()

        if teacher is not None or dip is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteLineaApplicata.objects.filter(
                    ricerca_linea_applicata_id=q['id']).values(
                    'personale_id__matricola',
                    'personale_id__nome',
                    'personale_id__middle_name',
                    'personale_id__cognome',
                    'personale_id__ds_sede',
                    'personale_id__sede')

                q['Teachers'] = None
                if dip is None:
                    for t in teachers:
                        if t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)

                elif teacher is None:
                    for t in teachers:
                        if t['personale_id__sede'] == dip:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if t['personale_id__sede'] == dip and t['personale_id__matricola'] == teacher:
                            q['Teachers'] = teachers

                    if q['Teachers'] is not None:
                        res.append(q)

            return res

        for q in query:
            teachers = RicercaDocenteLineaApplicata.objects.filter(
                ricerca_linea_applicata_id=q['id']
            ).values(
                'personale_id__matricola',
                'personale_id__nome',
                'personale_id__middle_name',
                'personale_id__cognome',
                'personale_id__ds_sede',
                'personale_id__sede')

            if len(teachers) == 0:
                q['Teachers'] = []
            else:
                q['Teachers'] = teachers

        return query

    @staticmethod
    def teachersList(search, regdid, dip, role, cds, year):

        query_search = Q()
        query_roles = Q()
        query_cds = Q()
        query_regdid = Q()
        query_year = Q()

        if search is not None:
            q_cognome = Q(cognome__istartswith=search)
            query_search &= q_cognome

        if regdid:
            query_regdid = Q(didatticacopertura__af__regdid__regdid_id=regdid)
        if role:
            roles = role.split(",")
            query_roles = Q(cd_ruolo__in=roles)
        if cds:
            query_cds = Q(didatticacopertura__cds_cod=cds)
        if year:
            query_year = Q(didatticacopertura__aa_off_id=year)

        # last_academic_year = ServiceDidatticaCds.getAcademicYears()[0]['aa_reg_did']

        query = Personale.objects.filter(Q(fl_docente=1) | Q(didatticacopertura__af__isnull=False),
                                         query_search,
                                         query_cds,
                                         query_regdid,
                                         query_roles,
                                         query_year) \
            .values("matricola",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "cd_uo_aff_org",
                    "ds_ssd",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve") \
            .order_by('cognome',
                      'nome',
                      'middle_name') \
            .distinct()

        # se visualizzo i docenti di un corso (anche passato)
        # mostro anche quelli che sono cessati
        # altrimenti solo quelli attivi
        if not regdid and not cds:
            query = query.filter(Q(fl_docente=1) |
                                 Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) |
                                 Q(didatticacopertura__aa_off_id=datetime.datetime.now().year-1),
                                 flg_cessato=0)

        if dip:
            department = DidatticaDipartimento.objects.filter(dip_cod=dip) .values(
                "dip_id", "dip_cod", "dip_des_it", "dip_des_eng").first()
            if not department:
                return None
            query = query.filter(cd_uo_aff_org=department["dip_cod"])
            query = list(query)
            for q in query:
                q["dip_id"] = department['dip_id']
                q["dip_cod"] = department['dip_cod']
                q["dip_des_it"] = department['dip_des_it']
                q["dip_des_eng"] = department["dip_des_eng"]

        else:
            dip_cods = query.values_list("cd_uo_aff_org", flat=True).distinct()
            dip_cods = list(dip_cods)

            departments = DidatticaDipartimento.objects.filter(
                dip_cod__in=dip_cods) .values(
                "dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

            for q in query:
                found = False
                for dep in departments:
                    if dep['dip_cod'] == q['cd_uo_aff_org']:
                        q["dip_id"] = dep['dip_id']
                        q["dip_cod"] = dep['dip_cod']
                        q["dip_des_it"] = dep['dip_des_it']
                        q["dip_des_eng"] = dep["dip_des_eng"]
                        found = True
                        break

                if not found:
                    q["dip_id"] = None
                    q["dip_cod"] = None
                    q["dip_des_it"] = None
                    q["dip_des_eng"] = None

        return query

    @staticmethod
    def teachingCoveragesList(search, regdid, dip, role, cds, year):

        query_search = Q()
        Q()
        query_roles = Q()
        query_cds = Q()
        query_regdid = Q()
        query_year = Q()

        if search is not None:
            for k in search.split(" "):
                q_cognome = Q(cognome__icontains=k)
                query_search &= q_cognome

        if regdid:
            query_regdid = Q(didatticacopertura__af__regdid__regdid_id=regdid)
        if role:
            roles = role.split(",")
            query_roles = Q(cd_ruolo__in=roles)
        if cds:
            query_cds = Q(didatticacopertura__cds_cod=cds)
        if year:
            query_year = Q(didatticacopertura__aa_off_id=year)

        query = Personale.objects.filter(query_search,
                                         query_cds,
                                         query_regdid,
                                         query_roles,
                                         query_year,
                                         didatticacopertura__af__isnull=False,
                                         flg_cessato=0) \
            .values("matricola",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "cd_uo_aff_org",
                    "ds_ssd",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve") \
            .order_by('cognome',
                      'nome',
                      'middle_name') \
            .distinct()

        if dip:
            department = DidatticaDipartimento.objects.filter(dip_cod=dip).values(
                "dip_id", "dip_cod", "dip_des_it", "dip_des_eng").first()
            if not department:
                return None
            query = query.filter(cd_uo_aff_org=department["dip_cod"])
            query = list(query)
            for q in query:
                q["dip_id"] = department['dip_id']
                q["dip_cod"] = department['dip_cod']
                q["dip_des_it"] = department['dip_des_it']
                q["dip_des_eng"] = department["dip_des_eng"]

        else:
            dip_cods = query.values_list("cd_uo_aff_org", flat=True).distinct()
            dip_cods = list(dip_cods)

            departments = DidatticaDipartimento.objects.filter(
                dip_cod__in=dip_cods).values(
                "dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

            for q in query:
                found = False
                for dep in departments:
                    if dep['dip_cod'] == q['cd_uo_aff_org']:
                        q["dip_id"] = dep['dip_id']
                        q["dip_cod"] = dep['dip_cod']
                        q["dip_des_it"] = dep['dip_des_it']
                        q["dip_des_eng"] = dep["dip_des_eng"]
                        found = True
                        break

                if not found:
                    q["dip_id"] = None
                    q["dip_cod"] = None
                    q["dip_des_it"] = None
                    q["dip_des_eng"] = None

        return query

    @staticmethod
    def getAttivitaFormativeByDocente(teacher, year, yearFrom, yearTo):

        if year:
            query = DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher,
                af__isnull=False,
                aa_off_id=year).select_related('personale', 'af')
        elif yearFrom and yearTo:
            query = DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher,
                af__isnull=False,
                aa_off_id__gte=yearFrom,
                aa_off_id__lte=yearTo).select_related('personale', 'af')
        elif yearFrom:
            query = DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher,
                af__isnull=False,
                aa_off_id__gte=yearFrom).select_related('personale', 'af')
        elif yearTo:
            query = DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher,
                af__isnull=False,
                aa_off_id__lte=yearTo).select_related('personale', 'af')
        else:
            query = DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher,
                af__isnull=False).select_related('personale', 'af')

        single_id = []
        to_exclude = []

        for cop in query:
            if cop.af_id not in single_id:
                single_id.append(cop.af_id)
            else:
                to_exclude.append(cop.coper_id)
        query = query.exclude(coper_id__in=to_exclude)

        return query.order_by(
            'aa_off_id',
            'anno_corso',
            'af_gen_des',
            'af_gen_des_eng'
            ).values(
            'af_id',
            'af_gen_cod',
            'af_gen_des',
            'af_gen_des_eng',
            'regdid_id',
            'anno_corso',
            'ciclo_des',
            'peso',
            'sett_des',
            'af__freq_obblig_flg',
            'cds_des',
            'af__cds__nome_cds_eng',
            'af__lista_lin_did_af',
            'aa_off_id',
            'cds_id',
            'cds_cod',
            'fat_part_stu_des',
            'fat_part_stu_cod',
            'part_stu_des',
            'part_stu_cod',
            'tipo_fat_stu_cod',
            'part_ini',
            'part_fine',
            'coper_peso',
            'ore'
        ).order_by('-aa_off_id')

    @staticmethod
    def getDocenteInfo(teacher):
        query = Personale.objects\
                         .filter(Q(fl_docente=1) |
                                 Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) |
                                 Q(didatticacopertura__aa_off_id=datetime.datetime.now().year-1),
                                 flg_cessato=0,
                                 matricola=teacher)\
                         .distinct()
                                 # didatticacopertura__af__isnull=False,
                         # .distinct()
        # query2 = Personale.objects.filter(fl_docente=1,
                                          # flg_cessato=0,
                                          # matricola=teacher)\
                                  # .distinct()

        # query = (query1 | query2).distinct()


        if not query.exists():
            raise Http404

        contacts = query.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=PERSON_CONTACTS_TO_TAKE
        ).values(
            "personalecontatti__cd_tipo_cont__descr_contatto",
            "personalecontatti__contatto")
        contacts = list(contacts)

        functions = UnitaOrganizzativaFunzioni.objects.filter(
            matricola=teacher,
            termine__gt=datetime.datetime.now(),
            decorrenza__lt=datetime.datetime.now()).values(
            "ds_funzione",
            "cd_csa__uo",
            "cd_csa__denominazione")

        docente_pta_altri_dati = DocentePtaAltriDati.objects.filter(matricola__exact=teacher).values(
            'path_foto',
            'path_cv_ita',
            'path_cv_en',
            'breve_bio',
            'breve_bio_en',
            'orario_ricevimento',
            'orario_ricevimento_en',
            'orcid'
        )

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
            "cd_uo_aff_org",
            "ds_aff_org",
            "telrif",
            "email",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng",
            'profilo',
            'ds_profilo',
            'ds_profilo_breve'

        )
        query = list(query)
        docente_pta_altri_dati = list(docente_pta_altri_dati)

        query[0]['ORCID'] = None
        query[0]['PHOTOPATH'] = None
        query[0]['PATHCVITA'] = None
        query[0]['PATHCVENG'] = None
        query[0]['BREVEBIO'] = None
        query[0]['BREVEBIOENG'] = None
        query[0]['ORARIORICEVIMENTO'] = None
        query[0]['ORARIORICEVIMENTOEN'] = None
        if len(docente_pta_altri_dati) > 0:
            query[0]['ORCID'] = docente_pta_altri_dati[0]['orcid']
            query[0]['PHOTOPATH'] = docente_pta_altri_dati[0]['path_foto']
            query[0]['PATHCVITA'] = docente_pta_altri_dati[0]['path_cv_ita']
            query[0]['PATHCVENG'] = docente_pta_altri_dati[0]['path_cv_en']
            query[0]['BREVEBIO'] = docente_pta_altri_dati[0]['breve_bio']
            query[0]['BREVEBIOENG'] = docente_pta_altri_dati[0]['breve_bio_en']
            query[0]['ORARIORICEVIMENTO'] = docente_pta_altri_dati[0]['orario_ricevimento']
            query[0]['ORARIORICEVIMENTOEN'] = docente_pta_altri_dati[0]['orario_ricevimento_en']


        for q in query:
            for c in PERSON_CONTACTS_TO_TAKE:
                q[c] = []
            for c in contacts:
                q[c['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    c['personalecontatti__contatto']
                )

            dep = DidatticaDipartimento.objects.filter(
                dip_cod=q["cd_uo_aff_org"]) .values(
                "dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
            if len(dep) == 0:
                q["dip_id"] = None
                q["dip_cod"] = None
                q["dip_des_it"] = None
                q["dip_des_eng"] = None
            else:
                dep = dep.first()
                q["dip_id"] = dep['dip_id']
                q["dip_cod"] = dep['dip_cod']
                q["dip_des_it"] = dep['dip_des_it']
                q["dip_des_eng"] = dep["dip_des_eng"]

            if len(functions) == 0:
                q["Functions"] = None
            else: # pragma: no cover
                q["Functions"] = functions


        return query

    @staticmethod
    def getDocenteMaterials(user, teacher, search=None):

        query_search = Q()
        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True)|Q(dt_inizio_validita__lte=datetime.datetime.now())
        query_is_end = Q(dt_fine_validita__isnull=True)|Q(dt_fine_validita__gt=datetime.datetime.now())

        if 'crud.teachers' in settings.INSTALLED_APPS: # pragma: no cover
            from crud.teachers.utils import can_manage_teacher
            if can_manage_teacher(user, teacher):
                query_is_active = Q()
                query_is_started = Q()
                query_is_end = Q()

        if search:
            for k in search.split(" "): # pragma: no cover
                query_search = Q(
                    titolo__icontains=k) | Q(
                    titolo_en__icontains=k)

        query = DocenteMaterialeDidattico.objects.filter(query_search,
                                                         query_is_active,
                                                         query_is_started,
                                                         query_is_end,
                                                         matricola__exact=teacher).values(
            'id',
            'titolo',
            'titolo_en',
            'testo',
            'testo_en',
            'url_testo',
            'url_testo_en',
            'ordine',
            'attivo',
            'dt_pubblicazione',
            'dt_inizio_validita',
            'dt_fine_validita',
        )
        for q in query:
            q['DocenteRiferimentoId'] = None
            q['DocenteRiferimentoId'] = teacher

        return query


    @staticmethod
    def getDocenteNews(user, teacher, search=None):

        query_search = Q()
        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True)|Q(dt_inizio_validita__lte=datetime.datetime.now())
        query_is_end = Q(dt_fine_validita__isnull=True)|Q(dt_fine_validita__gt=datetime.datetime.now())

        if 'crud.teachers' in settings.INSTALLED_APPS: # pragma: no cover
            from crud.teachers.utils import can_manage_teacher
            if can_manage_teacher(user, teacher):
                query_is_active = Q()
                query_is_started = Q()
                query_is_end = Q()

        if search:
            for k in search.split(" "): # pragma: no cover
                query_search = Q(
                    titolo__icontains=k) | Q(
                    titolo_en__icontains=k)


        query = DocentePtaBacheca.objects.filter(query_search,
                                                 query_is_active,
                                                 query_is_started,
                                                 query_is_end,
                                                 matricola__exact=teacher).values(
            'id',
            'tipo_testo',
            'tipo_testo_en',
            'titolo',
            'titolo_en',
            'testo',
            'testo_en',
            'url_testo',
            'url_testo_en',
            'ordine',
            'attivo',
            'dt_pubblicazione',
            'dt_inizio_validita',
            'dt_fine_validita',
        )

        return query


    @staticmethod
    def getRoles():
        query = Personale.objects.all().values("cd_ruolo",
                                               "ds_ruolo_locale").order_by('ds_ruolo_locale').distinct()

        return query

    @staticmethod
    def getPublicationsList(
            teacherid=None,
            search=None,
            year=None,
            type=None,
            structure=None
    ):
        query_search = Q()
        query_year = Q()
        query_type = Q()
        query_teacher = Q()
        query_structure = Q()

        if search is not None:
            for k in search.split(" "):
                query_search = Q(
                    title__icontains=k) | Q(
                    contributors__icontains=k)
        if year is not None:
            query_year = Q(date_issued_year=year)
        if type is not None:
            query_type = Q(collection_id__community_id__community_id=type)
        if teacherid:
            query_teacher = Q(pubblicazioneautori__id_ab__matricola=teacherid)
        if structure:
            query_structure = Q(
                pubblicazioneautori__id_ab__cd_uo_aff_org=structure)
        query = PubblicazioneDatiBase.objects.filter(
            query_search,
            query_year,
            query_type,
            query_teacher,
            query_structure).values(
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
            "collection_id__community_id__community_name",
            "title").distinct()

        for q in query:
            if q['date_issued_year'] == 9999:
                q['date_issued_year'] = 'in stampa'

        return query

    @staticmethod
    def getPublication(publicationid=None):

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
            if q['date_issued_year'] == 9999:
                q['date_issued_year'] = 'in stampa'

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

        return query

    @staticmethod
    def getPublicationsCommunityTypesList():
        query = PubblicazioneCommunity.objects.all().values(
            "community_id", "community_name").order_by("community_id").distinct()
        return query


class ServiceDottorato:
    @staticmethod
    def getPhd(query_params):

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
            'dip_cod__dip_id',
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

    @staticmethod
    def getPhdActivities(search=None, structure=None, phd=None, ssd=None, teacher=None, cycle=None):

        query_search = Q()
        query_structure = Q()
        query_phd = Q()
        query_ssd = Q()
        query_cycle = Q()


        if search is not None:
            query_search = Q(nome_af__icontains=search)
        if structure:
            query_structure = Q(struttura_proponente_origine__icontains=structure)
        if phd:
            query_phd = Q(rif_dottorato__icontains=phd)
        if ssd:
            query_ssd = Q(ssd__icontains=ssd)
        if cycle:
            query_cycle = Q(ciclo=cycle)

        query = DidatticaDottoratoAttivitaFormativa.objects.filter(
            query_search,
            query_structure,
            query_phd,
            query_ssd,
            query_cycle,
        ).values(
            "id",
            "nome_af",
            "ssd",
            "numero_ore",
            "cfu",
            "tipo_af",
            "rif_dottorato",
            "ciclo",
            "id_struttura_proponente",
            "struttura_proponente_origine",
            "contenuti_af",
            "prerequisiti",
            "num_min_studenti",
            "num_max_studenti",
            "verifica_finale",
            "modalita_verifica",
            "avvio",
            "fine",
            "orario_aule",
            "note",
            "visualizza_orario"
        )
        for q in query:
            main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
                id_didattica_dottorato_attivita_formativa=q['id']).values(
                'matricola',
                'cognome_nome_origine'
            )

            if len(main_teachers) == 0:
                q['MainTeachers'] = []
            else:
                q['MainTeachers'] = main_teachers

            other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
                id_didattica_dottorato_attivita_formativa=q['id']).values(
                'matricola',
                'cognome_nome_origine'
            )

            if len(other_teachers) == 0:
                q['OtherTeachers'] = []
            else:
                q['OtherTeachers'] = other_teachers

        if teacher:
            res = []
            for q in query:
                for i in q['MainTeachers']:
                    if i['cognome_nome_origine'] is not None and (i['cognome_nome_origine'].lower()).startswith(teacher.lower()) and q not in res:
                        res.append(q)
                        continue
                for t in q['OtherTeachers']:
                    if t['cognome_nome_origine'] is not None and (t['cognome_nome_origine'].lower()).startswith(teacher.lower()) and q not in res:
                        res.append(q)
            return res

        return query

    @staticmethod
    def getPhdActivity(activity_id):


        query = DidatticaDottoratoAttivitaFormativa.objects.filter(
            id=activity_id,
        ).values(
            "id",
            "nome_af",
            "ssd",
            "numero_ore",
            "cfu",
            "tipo_af",
            "rif_dottorato",
            "ciclo",
            "id_struttura_proponente",
            "struttura_proponente_origine",
            "contenuti_af",
            "prerequisiti",
            "num_min_studenti",
            "num_max_studenti",
            "verifica_finale",
            "modalita_verifica",
            "avvio",
            "fine",
            "orario_aule",
            "note",
            "visualizza_orario"
        )
        query_filter_teachers = ~Q(cognome_nome_origine='....DOCENTE NON IN ELENCO')
        for q in query:
            main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
                query_filter_teachers,
                id_didattica_dottorato_attivita_formativa=q['id']).values(
                'matricola',
                'cognome_nome_origine'
            )

            if len(main_teachers) == 0:
                q['MainTeachers'] = []
            else:
                q['MainTeachers'] = main_teachers

            other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
                id_didattica_dottorato_attivita_formativa=q['id'],
                cognome_nome_origine__isnull=False).values(
                'matricola',
                'cognome_nome_origine'
            )

            if len(other_teachers) == 0:
                q['OtherTeachers'] = []
            else:
                q['OtherTeachers'] = other_teachers

        return query


    @staticmethod
    def getRefPhd():
        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(rif_dottorato__isnull=False)\
                                                   .order_by('rif_dottorato')\
                                                   .values('rif_dottorato')\
                                                   .distinct()
        return list(query)

    @staticmethod
    def getPhdSsdList(): # pragma: no cover
        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(ssd__isnull=False)\
                                                   .order_by('ssd')\
                                                   .values('ssd')\
                                                   .distinct()
        return list(query)

    @staticmethod
    def getPhdActivityTypeList(): # pragma: no cover
        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(tipo_af__isnull=False)\
                                                   .order_by('tipo_af')\
                                                   .values('tipo_af')\
                                                   .distinct()
        return list(query)

    @staticmethod
    def getRefStructures(): # pragma:no cover
        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(struttura_proponente_origine__isnull=False)\
                                                   .order_by('struttura_proponente_origine')\
                                                   .values('struttura_proponente_origine')\
                                                   .distinct()
        return list(query)


class ServiceDipartimento:

    @staticmethod
    def getDepartmentsList(language):
        query = DidatticaDipartimento.objects.all()\
                                     .values("dip_id", "dip_cod",
                                             "dip_des_it", "dip_des_eng",
                                             "dip_nome_breve")

        query = query.order_by("dip_des_it") if language == 'it' \
                               else query.order_by("dip_des_eng")

        for q in query:
            url = DidatticaDipartimentoUrl.objects\
                                          .filter(dip_cod=q['dip_cod'])\
                                          .values_list('dip_url', flat=True)
            q['dip_url'] = url[0] if url else ''

        return query

    @staticmethod
    def getDepartment(departmentcod):
        query = DidatticaDipartimento.objects\
                                     .filter(dip_cod__exact=departmentcod)\
                                     .values("dip_id", "dip_cod",
                                             "dip_des_it", "dip_des_eng",
                                             "dip_nome_breve")
        if not query: raise Http404
        dip_cod = query.first()['dip_cod']
        url = DidatticaDipartimentoUrl.objects\
                                          .filter(dip_cod=dip_cod)\
                                          .values_list('dip_url', flat=True)
        for q in query:
            q['dip_url'] = url[0] if url else ''
        return query


class ServicePersonale:

    @staticmethod
    def getAddressbook(
            search=None,
            structureid=None,
            structuretypes=None,
            role=None,
            structuretree=None,
            phone=None):

        query_search = Q()
        role = role.split(',') if role else []

        if search is not None:
            query_search = Q(cognome__istartswith=search)

        query = Personale.objects.filter(
            query_search,
            flg_cessato=0,
            cd_uo_aff_org__isnull=False,
            dt_rap_fin__gte=datetime.datetime.today()).values(
            "nome",
            "middle_name",
            "cognome",
            # "cd_uo_aff_org",
            # 'cd_uo_aff_org__denominazione',
            # 'cd_uo_aff_org__cd_tipo_nodo',
            # 'cd_uo_aff_org__ds_tipo_nodo',
            "id_ab",
            "matricola",
            'personalecontatti__cd_tipo_cont__descr_contatto',
            'personalecontatti__contatto',
            'personalecontatti__prg_priorita',
            'fl_docente',
            'profilo',
            'ds_profilo',
            'ds_profilo_breve'
        ).order_by('cognome', 'nome')

        grouped = {}
        last_id = -1
        final_query = []

        ruoli = PersonaleAttivoTuttiRuoli.objects.values(
            'matricola',
            'cd_ruolo',
            'ds_ruolo',
            'cd_uo_aff_org',
            'ds_aff_org',
            'cd_uo_aff_org__cd_tipo_nodo'
        ).distinct()

        ruoli_dict = {}
        for r in ruoli:
            if not ruoli_dict.get(r['matricola']):
                ruoli_dict[r['matricola']] = []
            ruoli_dict[r['matricola']].append([r['cd_ruolo'],
                                               r['ds_ruolo'],
                                               r['cd_uo_aff_org'],
                                               r['ds_aff_org'],
                                               r['cd_uo_aff_org__cd_tipo_nodo']])

        priorita_tmp = PersonalePrioritaRuolo.objects.values(
            'cd_ruolo',
            'priorita'
        )

        priorita = {}

        for p in priorita_tmp:
            priorita.update({p['cd_ruolo']: p['priorita']})


        for q in query:
            if q['id_ab'] not in grouped:
                grouped[q['id_ab']] = {
                    'id_ab': q['id_ab'],
                    'nome': q['nome'],
                    'middle_name': q['middle_name'],
                    'cognome': q['cognome'],
                    # 'cd_uo_aff_org': q['cd_uo_aff_org'],
                    'matricola': q['matricola'],
                    # 'Struttura': q['cd_uo_aff_org__denominazione'],
                    # 'TipologiaStrutturaCod': q['cd_uo_aff_org__cd_tipo_nodo'],
                    # 'TipologiaStrutturaNome': q['cd_uo_aff_org__ds_tipo_nodo'],
                    # 'fl_docente': q['fl_docente'],
                    'profilo': q['profilo'],
                    'ds_profilo': q['ds_profilo'],
                    'ds_profilo_breve': q['ds_profilo_breve'],
                    'Roles': [],
                }
                for c in PERSON_CONTACTS_TO_TAKE:
                    grouped[q['id_ab']][c] = []

            if q['personalecontatti__cd_tipo_cont__descr_contatto'] in PERSON_CONTACTS_TO_TAKE:
                grouped[q['id_ab']][q['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    q['personalecontatti__contatto'])

            if last_id == -1 or last_id != q['id_ab']:
                last_id = q['id_ab']

                ruoli_dip = ruoli_dict.get(q['matricola']) or []
                roles = []
                for r in ruoli_dip:
                    roles.append({'matricola': q['matricola'],
                                  'cd_ruolo': r[0],
                                  'ds_ruolo': r[1],
                                  'priorita': priorita.get(r[0]) or 10,
                                  'cd_uo_aff_org': r[2],
                                  'ds_aff_org': r[3],
                                  'cd_tipo_nodo': r[4]
                                  })

                roles.sort(key=lambda x: x['priorita'])
                grouped[q['id_ab']]['Roles'] = roles
                final_query.append(grouped[q['id_ab']])

        filtered = []
        if phone:
            for item in final_query:
                numbers = item['Telefono Cellulare Ufficio'] + item['Telefono Ufficio']
                if any(phone in string for string in numbers):
                    filtered.append(item)
        else:
            filtered = final_query

        filtered2 = []

        if role:
            roles = []
            for k in role:
                roles.append(k)
            for item in filtered:
                final_roles = []
                for r in item['Roles']:
                    final_roles.append(r['cd_ruolo'])
                final_roles.append(item['profilo'])
                if (set(roles).intersection(set(final_roles))):
                    filtered2.append(item)
        else:
            filtered2 = filtered

        filtered3 = []

        if structuretypes:
            s = []
            for k in structuretypes.split(","):
                s.append(k)
            for item in filtered2:
                final_structures = []
                for r in item['Roles']:
                    if r['cd_ruolo'] in role or item['profilo'] in role or not role:
                        final_structures.append(r['cd_tipo_nodo'])
                if (set(s).intersection(set(final_structures))):
                    filtered3.append(item)
        else:
            filtered3 = filtered2

        filtered4 = []
        if structureid:

            for item in filtered3:
                for r in item['Roles']:
                    if r['cd_uo_aff_org'] == structureid:
                        if r['cd_ruolo'] in role or item['profilo'] in role or not role:
                            filtered4.append(item)
                            break
        else:
            filtered4 = filtered3

        filtered5 = []
        if structuretree:
            query_structuretree = ServiceStructure.getStructureChilds(structuretree)

            for item in filtered4:
                if item['Roles'] and len(item['Roles']) != 0:
                    for r in item['Roles']:
                        if r['cd_uo_aff_org'] in query_structuretree:
                            if r['cd_ruolo'] in role or item['profilo'] in role or not role:
                                filtered5.append(item)
                                break
        else:
            filtered5 = filtered4

        return filtered5

        # if phone or role or structuretypes:
        #     filtered = []
        #     if phone and role and structuretypes:
        #         filtered1 = []
        #         filtered2 = []
        #         filtered3 = []
        #
        #         roles = []
        #         for k in role.split(","):
        #             roles.append(k)
        #         s = []
        #         for k in structuretypes.split(","):
        #             s.append(k)
        #         for item in final_query:
        #             final_roles = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_roles.append(r['cd_ruolo'])
        #             final_roles.append(item['profilo'])
        #             if (set(roles).intersection(set(final_roles))):
        #                 filtered1.append(item)
        #
        #             numbers = item['Telefono Cellulare Ufficio'] + item['Telefono Ufficio']
        #             if any(phone in string for string in numbers):
        #                 filtered2.append(item)
        #
        #             final_structures = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_structures.append(r['cd_tipo_nodo'])
        #             if (set(s).intersection(set(final_structures))):
        #                 filtered3.append(item)
        #
        #
        #         filtered = [value for value in filtered1 if value in filtered2 and filtered3]
        #
        #         return filtered
        #
        #     if phone and role :
        #         filtered1 = []
        #         filtered2 = []
        #
        #         roles = []
        #         for k in role.split(","):
        #             roles.append(k)
        #
        #         for item in final_query:
        #             final_roles = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_roles.append(r['cd_ruolo'])
        #             final_roles.append(item['profilo'])
        #             if (set(roles).intersection(set(final_roles))):
        #                 filtered1.append(item)
        #
        #             numbers = item['Telefono Cellulare Ufficio'] + item['Telefono Ufficio']
        #             if any(phone in string for string in numbers):
        #                 filtered2.append(item)
        #
        #
        #         filtered = [value for value in filtered1 if value in filtered2]
        #
        #         return filtered
        #     if phone and structuretypes:
        #         filtered2 = []
        #         filtered3 = []
        #
        #
        #         s = []
        #         for k in structuretypes.split(","):
        #             s.append(k)
        #         for item in final_query:
        #
        #             numbers = item['Telefono Cellulare Ufficio'] + item['Telefono Ufficio']
        #             if any(phone in string for string in numbers):
        #                 filtered2.append(item)
        #
        #             final_structures = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_structures.append(r['cd_tipo_nodo'])
        #             if (set(s).intersection(set(final_structures))):
        #                 filtered3.append(item)
        #
        #         filtered = [value for value in filtered2 if value in filtered3]
        #
        #         return filtered
        #
        #     if role and structuretypes:
        #         filtered1 = []
        #         filtered3 = []
        #
        #         roles = []
        #         for k in role.split(","):
        #             roles.append(k)
        #         s = []
        #         for k in structuretypes.split(","):
        #             s.append(k)
        #         for item in final_query:
        #             final_roles = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_roles.append(r['cd_ruolo'])
        #             final_roles.append(item['profilo'])
        #             if (set(roles).intersection(set(final_roles))):
        #                 filtered1.append(item)
        #
        #             final_structures = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_structures.append(r['cd_tipo_nodo'])
        #             if (set(s).intersection(set(final_structures))):
        #                 filtered3.append(item)
        #
        #         filtered = [value for value in filtered1 if value in filtered3]
        #
        #         return filtered
        #
        #     if phone:
        #         for item in final_query:
        #             numbers = item['Telefono Cellulare Ufficio'] + item['Telefono Ufficio']
        #             if any(phone in string for string in numbers):
        #                 filtered.append(item)
        #         return filtered
        #
        #     if role:
        #         roles = []
        #         for k in role.split(","):
        #             roles.append(k)
        #         filtered = []
        #         for item in final_query:
        #             final_roles = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_roles.append(r['cd_ruolo'])
        #             final_roles.append(item['profilo'])
        #             if (set(roles).intersection(set(final_roles))):
        #                 filtered.append(item)
        #         return filtered
        #
        #     if structuretypes:
        #         s = []
        #         for k in structuretypes.split(","):
        #             s.append(k)
        #         filtered = []
        #         for item in final_query:
        #             final_structures = []
        #             if item['Roles'] and len(item['Roles']) != 0:
        #                 for r in item['Roles']:
        #                     final_structures.append(r['cd_tipo_nodo'])
        #             if (set(s).intersection(set(final_structures))):
        #                 filtered.append(item)
        #         return filtered


    @staticmethod
    def getStructuresList(search=None, father=None, type=None, depth=0):

        query_search = Q()
        query_father = Q()
        query_type = Q()

        if father == 'None':
            query_father = Q(uo_padre__isnull=True)
        elif father:
            query_father = Q(uo_padre=father)

        if search is not None:
            for k in search.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_search &= q_denominazione

        if type:
            for k in type.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type

        query = UnitaOrganizzativa.objects.filter(
            query_search,
            query_father,
            query_type,
            dt_fine_val__gte=datetime.datetime.today()).values(
            "uo",
            "denominazione",
            "ds_tipo_nodo",
            "cd_tipo_nodo").distinct().order_by('denominazione')

        for q in query:
            url = DidatticaDipartimentoUrl.objects\
                                          .filter(dip_cod=q['uo'])\
                                          .values_list('dip_url', flat=True)
            q['dip_url'] = url[0] if url else ''

            if depth == '1':
                q['childs'] = []
                sub_query = UnitaOrganizzativa.objects.filter(
                    query_search,
                    query_type,
                    uo_padre=q['uo'],
                    dt_fine_val__gte=datetime.datetime.today()).values(
                    "uo",
                    "denominazione",
                    "ds_tipo_nodo",
                    "cd_tipo_nodo").distinct().order_by('denominazione')
                for sq in sub_query:
                    q['childs'].append(StructuresSerializer.to_dict(sq))
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
    def getStructureFunctions():

        query = UnitaOrganizzativaTipoFunzioni.objects.values(
            "cd_tipo_nod",
            "funzione",
            "descr_funzione").distinct().order_by("cd_tipo_nod")

        return query

    @staticmethod
    def getPersonale(personale_id):
        query = Personale.objects.filter(matricola__exact=personale_id,
                                         flg_cessato=0)

        if not query:
            raise Http404

        if query.values('cd_uo_aff_org').first()['cd_uo_aff_org'] is None:
            query = query.annotate(
                        Struttura=Value(
                            None,
                            output_field=CharField()))\
                        .annotate(
                TipologiaStrutturaCod=Value(None, output_field=CharField())).annotate(
                TipologiaStrutturaNome=Value(None, output_field=CharField())).annotate(
                CodStruttura=Value(None, output_field=CharField()))
        else:
            query = query.extra(
                select={
                    'Struttura': 'UNITA_ORGANIZZATIVA.DENOMINAZIONE',
                    'CodStruttura': 'UNITA_ORGANIZZATIVA.UO',
                    'TipologiaStrutturaCod': 'UNITA_ORGANIZZATIVA.CD_TIPO_NODO',
                    'TipologiaStrutturaNome': 'UNITA_ORGANIZZATIVA.DS_TIPO_NODO'},
                tables=['UNITA_ORGANIZZATIVA'],
                where=[
                    'UNITA_ORGANIZZATIVA.UO=PERSONALE.CD_UO_AFF_ORG',
                ])

        contacts = query.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=PERSON_CONTACTS_TO_TAKE
        ).values(
            "personalecontatti__cd_tipo_cont__descr_contatto",
            "personalecontatti__contatto")
        contacts = list(contacts)

        functions = UnitaOrganizzativaFunzioni.objects.filter(
            matricola=personale_id,
            termine__gt=datetime.datetime.now(),
            decorrenza__lt=datetime.datetime.now()).values(
            "ds_funzione",
            "funzione",
            "cd_csa__uo",
            "cd_csa__denominazione",
        )

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
            "cd_uo_aff_org",
            "ds_aff_org",
            "telrif",
            "email",
            "Struttura",
            'CodStruttura',
            'TipologiaStrutturaCod',
            'TipologiaStrutturaNome',
            'unitaorganizzativafunzioni__ds_funzione',
            'unitaorganizzativafunzioni__termine',
            'fl_docente',
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng",
            'profilo',
            'ds_profilo',
            'ds_profilo_breve'
        )

        ruoli = PersonaleAttivoTuttiRuoli.objects.filter(matricola=personale_id).values_list(
            'matricola',
            'cd_ruolo',
            'ds_ruolo',
            'cd_uo_aff_org',
            'ds_aff_org',
            'cd_uo_aff_org__cd_tipo_nodo'
        ).distinct()

        priorita_tmp = PersonalePrioritaRuolo.objects.values(
            'cd_ruolo',
            'priorita'
        )

        priorita = {}

        for p in priorita_tmp:
            priorita.update({p['cd_ruolo']: p['priorita']})

        roles = []

        for r in ruoli:
            roles.append({'matricola': r[0],
                          'cd_ruolo': r[1],
                          'ds_ruolo': r[2],
                          'priorita': priorita.get(r[1]) or 10,
                          'cd_uo_aff_org': r[3],
                          'ds_aff_org': r[4],
                          'cd_tipo_nodo': r[5]
                          })
        roles.sort(key=lambda x: x['priorita'])



        for q in query:
            for c in PERSON_CONTACTS_TO_TAKE:
                q[c] = []
            for c in contacts:
                q[c['personalecontatti__cd_tipo_cont__descr_contatto']].append(
                    c['personalecontatti__contatto'])

            if len(functions) == 0:
                q["Functions"] = None
            else:
                q["Functions"] = functions

            if len(roles) == 0:
                q["Roles"] = []
            else:
                q["Roles"] = roles

            q["cop_teacher"] = False
            if not q["fl_docente"]:
                query_teacher = Personale.objects\
                                         .filter(Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) |
                                                 Q(didatticacopertura__aa_off_id=datetime.datetime.now().year-1),
                                                 didatticacopertura__af__isnull=False,
                                                 matricola__exact=personale_id)\
                                         .exists()
                if query_teacher:
                    q["cop_teacher"] = True

        if not query:
            raise Http404
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
            "ds_mission",
            "cd_csa",
        )
        for q in query:
            for c in contacts_to_take:
                q[c] = []
            for c in contacts:
                q[c['unitaorganizzativacontatti__cd_tipo_cont']].append(
                    c['unitaorganizzativacontatti__contatto'])
            funzioni_personale = UnitaOrganizzativaFunzioni.objects.filter(
                cd_csa=q['cd_csa'],
                termine__gt=datetime.datetime.now()).values(
                "ds_funzione",
                "funzione",
                "cod_fis__nome",
                "cod_fis__cognome",
                "cod_fis__middle_name",
                "cod_fis__matricola")
            if len(funzioni_personale) > 0:
                q['FunzioniPersonale'] = funzioni_personale
            else:
                q['FunzioniPersonale'] = None

            url = DidatticaDipartimentoUrl.objects\
                                          .filter(dip_cod=q['uo'])\
                                          .values_list('dip_url', flat=True)
            q['dip_url'] = url[0] if url else ''
        return query

    @staticmethod
    def getStructurePersonnelChild(structures_tree, structureid=None): # pragma: no cover
        child_structures = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid).values("uo")

        for child in child_structures:
            structures_tree |= Q(cd_uo_aff_org=child["uo"])
            structures_tree = ServicePersonale.getStructurePersonnelChild(
                structures_tree, child['uo'])
        return structures_tree

    @staticmethod
    def getAllStructuresList(search=None, father=None, type=None):

        query_search = Q()
        query_father = Q()
        query_type = Q()

        if father == 'None':
            query_father = Q(uo_padre__isnull=True)
        elif father:
            query_father = Q(uo_padre=father)

        if search is not None:
            for k in search.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_search &= q_denominazione

        if type:
            for k in type.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type

        query = UnitaOrganizzativa.objects.filter(query_search,
                                                  query_father,
                                                  query_type).extra(
            select={
                'matricola': 'PERSONALE.MATRICOLA',
                'cd_uo_aff_org': 'PERSONALE.CD_UO_AFF_ORG'},
            tables=['PERSONALE'],
            where=[
                'UNITA_ORGANIZZATIVA.UO=PERSONALE.CD_UO_AFF_ORG',
                'PERSONALE.FLG_CESSATO=0',
                'PERSONALE.CD_UO_AFF_ORG is not NULL']
        )

        query = query.values(
            'uo',
            'denominazione',
            'cd_tipo_nodo',
            'ds_tipo_nodo',
        ).distinct()

        return query


    @staticmethod
    def getPersonnelCfs(roles):

        query_roles = Q()

        if roles is not None:
            roles = roles.split(",")
            query_roles = Q(cd_ruolo__in=roles)

        query = Personale.objects.filter(
            query_roles,
            flg_cessato=0,
            dt_rap_fin__gte=datetime.datetime.today())

        query = query.values(
            "nome",
            "middle_name",
            "cognome",
            "cod_fis",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_uo_aff_org",
            "ds_aff_org",
            "matricola",
        ).order_by("cognome")

        return query


class ServiceLaboratorio:

    @staticmethod
    def getLaboratoriesList(
            language,
            search,
            ambito,
            dip,
            erc1,
            teacher,
            infrastructure,
            scope
    ):
        query_search = Q()
        query_ambito = Q()
        query_dip = Q()
        query_erc1 = Q()
        query_infrastructure = Q()

        if search:
            for k in search.split(" "):
                q_search = Q(nome_laboratorio__icontains=k)
                if language == "it":
                    q_search |= Q(finalita_ricerca_it__icontains=k) | Q(finalita_didattica_it__icontains=k) | Q(finalita_servizi_it__icontains=k)
                else:
                    q_search |= Q(finalita_ricerca_en__icontains=k) | Q(finalita_didattica_en__icontains=k) | Q(finalita_servizi_en__icontains=k)
                query_search &= q_search
        if ambito:
            query_ambito = Q(ambito__exact=ambito)
        if dip:
            query_dip = Q(id_dipartimento_riferimento__dip_cod__exact=dip)
            query_dip |= Q(laboratorioaltridipartimenti__id_dip__dip_cod=dip)
        if erc1:
            erc1_allowed = erc1.split(",")
            query_erc1 = Q(
                laboratoriodatierc1__id_ricerca_erc1__cod_erc1__in=erc1_allowed)
        if infrastructure:
            query_infrastructure = Q(
                id_infrastruttura_riferimento__id=infrastructure)

        query = LaboratorioDatiBase.objects.filter(
            query_search,
            query_ambito,
            query_dip,
            query_erc1,
            query_infrastructure
        ).values(
            'id',
            'nome_laboratorio',
            'ambito',
            'dipartimento_riferimento',
            'id_dipartimento_riferimento__dip_id',
            'id_dipartimento_riferimento__dip_cod',
            'sede_dimensione',
            'responsabile_scientifico',
            'matricola_responsabile_scientifico',
            'laboratorio_interdipartimentale',
            "finalita_servizi_it",
            "finalita_servizi_en",
            "finalita_ricerca_it",
            "finalita_ricerca_en",
            "finalita_didattica_en",
            "finalita_didattica_it",
            "id_infrastruttura_riferimento__id",
            "id_infrastruttura_riferimento__descrizione",
            "acronimo",
            "nome_file_logo",
        ).distinct()

        for q in query:
            if q['dipartimento_riferimento'] is not None:
                temp = q['dipartimento_riferimento'].rsplit(',',1)

                if len(temp)>1:
                    q['dipartimento_riferimento'] = temp[0] + ', ' + temp[1]
                else:
                    q['dipartimento_riferimento'] = temp[0]

        for q in query:
            personale_ricerca = LaboratorioPersonaleRicerca.objects.filter(
                id_laboratorio_dati__id=q['id']).values(
                "matricola_personale_ricerca__matricola",
                "matricola_personale_ricerca__nome",
                "matricola_personale_ricerca__cognome",
                "matricola_personale_ricerca__middle_name")
            personale_tecnico = LaboratorioPersonaleTecnico.objects.filter(
                id_laboratorio_dati__id=q['id']).values(
                "matricola_personale_tecnico__matricola",
                "matricola_personale_tecnico__nome",
                "matricola_personale_tecnico__cognome",
                "matricola_personale_tecnico__middle_name",
                "ruolo")
            finalita = LaboratorioAttivita.objects.filter(
                id_laboratorio_dati=q['id']).values(
                "id_tipologia_attivita__id",
                "id_tipologia_attivita__descrizione"
            ).distinct()


            personale_tecnico = list(personale_tecnico)
            personale_ricerca = list(personale_ricerca)

            for p in personale_tecnico: # pragma: no cover
                if q['matricola_responsabile_scientifico'] == p['matricola_personale_tecnico__matricola']:
                    personale_tecnico.remove(p)

            for p in personale_ricerca: # pragma: no cover
                if q['matricola_responsabile_scientifico'] == p['matricola_personale_ricerca__matricola']:
                    personale_ricerca.remove(p)

            q['TechPersonnel'] = personale_tecnico
            q['ResearchPersonnel'] = personale_ricerca
            q['Scopes'] = finalita

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

        if teacher and scope:
            res = []
            res1 = []
            if scope:
                for q in query:
                    for s in q['Scopes']:
                        if str(s['id_tipologia_attivita__id']) == scope:
                            res.append(q)
            if teacher:
                for q in query:
                    if teacher == q['matricola_responsabile_scientifico']:
                        res1.append(q)
                        continue
                    for i in q['TechPersonnel']:
                        if teacher == i['matricola_personale_tecnico__matricola']:
                            res1.append(q)
                            continue
                    for t in q['ResearchPersonnel']:
                        if teacher == t['matricola_personale_ricerca__matricola']:
                            res1.append(q)
            if len(res) > len(res1):
                res = [val for val in res if val in res1]
            else:
                res = [val for val in res1 if val in res]

            return res

        if scope or teacher:
            res = []

            if scope:
                for q in query:
                    for s in q['Scopes']:
                        if str(s['id_tipologia_attivita__id']) == scope:
                            res.append(q)
            if teacher:
                for q in query:
                    if teacher == q['matricola_responsabile_scientifico'] and q not in res:
                        res.append(q)
                        continue
                    for i in q['TechPersonnel']:
                        if teacher == i['matricola_personale_tecnico__matricola'] and q not in res:
                            res.append(q)
                            continue
                    for t in q['ResearchPersonnel']:
                        if teacher == t['matricola_personale_ricerca__matricola'] and q not in res:
                            res.append(q)
            return res
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
            "nome_file_logo",
            "id_dipartimento_riferimento__dip_id",
            "id_dipartimento_riferimento__dip_cod",
            "id_dipartimento_riferimento__dip_des_it",
            "id_dipartimento_riferimento__dip_des_eng",
            "id_infrastruttura_riferimento__id",
            "id_infrastruttura_riferimento__descrizione",
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
        finalita = LaboratorioAttivita.objects.filter(
            id_laboratorio_dati=laboratoryid).values(
            "id_tipologia_attivita__id",
            "id_tipologia_attivita__descrizione"
        ).distinct()


        erc1 = LaboratorioDatiErc1.objects.filter(
            id_laboratorio_dati=laboratoryid).values(
            'id_ricerca_erc1__ricerca_erc0_cod__erc0_cod',
            'id_ricerca_erc1__ricerca_erc0_cod__description',
            'id_ricerca_erc1__ricerca_erc0_cod__description_en').distinct()

        query = list(query)

        for q in erc1:
            q['Erc1'] = LaboratorioDatiErc1.objects.filter(
            id_laboratorio_dati=laboratoryid).filter(
                id_ricerca_erc1__ricerca_erc0_cod=q['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod']).values(
                'id_ricerca_erc1__id',
                'id_ricerca_erc1__cod_erc1',
                'id_ricerca_erc1__descrizione').distinct()

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
            q['Scopes'] = finalita
            q['LaboratoryErc1'] = erc1
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
    def getScopes():
        return LaboratorioTipologiaAttivita.objects.all().values(
            "id",
            "descrizione").distinct().order_by("id")

    @staticmethod
    def getInfrastructures():
        return LaboratorioInfrastruttura.objects.all().values(
            "id",
            "descrizione").distinct()

    @staticmethod
    def getErc1List():

        query = RicercaErc0.objects.values(
            'erc0_cod',
            'description',
            'description_en').distinct()

        query = list(query)

        for q in query:

            q['Erc1'] = RicercaErc1.objects.filter(
                ricerca_erc0_cod=q['erc0_cod']).values(
                'id',
                'cod_erc1',
                'descrizione').distinct()
        return query

    @staticmethod
    def getErc0List():

        query = RicercaErc0.objects.all().values(
            'erc0_cod',
            'description',
            'description_en').distinct()

        return query

    @staticmethod
    def getErc2List():
        query = ServiceLaboratorio.getErc1List()

        for q in query:
            for i in range(len(q['Erc1'])):
                q['Erc1'][i]['Erc2'] = RicercaErc2.objects.filter(
                    ricerca_erc1_id=q['Erc1'][i]['id']).values(
                    'cod_erc2', 'descrizione').distinct()
        return query


    @staticmethod
    def getAster1List():

        query = RicercaErc0.objects.values(
            'erc0_cod',
            'description',
            'description_en'
        )

        for q in query:

            q['Aster1'] = []

            q['Aster1'] = RicercaAster1.objects.filter(ricerca_erc0_cod=q['erc0_cod']).values(
                'id',
                'descrizione'
            ).distinct()

            query = list(query)

            if len(q['Aster1']) == 0:
                query.remove(q)

        return query

    @staticmethod
    def getAster2List():

        query = ServiceLaboratorio.getAster1List()

        for q in query:
            for i in range(len(q['Aster1'])):
                q['Aster1'][i]['Aster2'] = RicercaAster2.objects.filter(
                    ricerca_aster1_id=q['Aster1'][i]['id']).values(
                    'id', 'descrizione').distinct()

        return query

class ServiceBrevetto:

    @staticmethod
    def getPatents(search, techarea, structure, only_active=True):

        query_search = Q()
        query_techarea = Q()
        query_structure = Q()
        query_is_active = Q(is_active=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(titolo__icontains=k)
                query_search &= q_nome
        if techarea:
            query_techarea = Q(id_area_tecnologica=techarea)
        if structure:
            query_structure = Q(
                brevettoinventori__matricola_inventore__cd_uo_aff_org=structure)

        query = BrevettoDatiBase.objects.filter(
            query_search,
            query_techarea,
            query_structure,
            query_is_active).values(
            "id",
            "id_univoco",
            "titolo",
            "nome_file_logo",
            "breve_descrizione",
            "trl_iniziale",
            "trl_aggiornato",
            "valorizzazione",
            "url_knowledge_share",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_active"
        ).distinct()

        for q in query:
            inventori = BrevettoInventori.objects.filter(
                id_brevetto=q['id']).values(
                    "matricola_inventore",
                    "cognomenome_origine",
            ).distinct()

            if len(inventori) == 0:
                q['Inventori'] = []
            else:
                q['Inventori'] = inventori

        return query

    @staticmethod
    def getPatentDetail(patentid):

        query = BrevettoDatiBase.objects.filter(
            id=patentid,
            is_active=True).values(
            "id",
            "id_univoco",
            "titolo",
            "nome_file_logo",
            "breve_descrizione",
            "trl_iniziale",
            "trl_aggiornato",
            "valorizzazione",
            "url_knowledge_share",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_active"
        )

        for q in query:
            inventori = BrevettoInventori.objects.filter(
                id_brevetto=q['id']).values(
                    "matricola_inventore",
                    "cognomenome_origine",
            ).distinct()

            if len(inventori) == 0:
                q['Inventori'] = []
            else:
                q['Inventori'] = inventori

        return query


class ServiceCompany:

    @staticmethod
    def getCompanies(search, techarea, spinoff, startup, q_departments, only_active=True):

        query_search = Q()
        query_techarea = Q()
        query_spinoff = Q()
        query_startup = Q()
        query_is_active = Q(is_active=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(
                    descrizione_ita__icontains=k) | Q(
                    nome_azienda__icontains=k)
                query_search &= q_nome
        if techarea:
            query_techarea = Q(id_area_tecnologica=techarea)
        if spinoff:
            query_spinoff = Q(is_spinoff=spinoff)
        if startup:
            query_startup = Q(is_startup=startup)

        query = SpinoffStartupDatiBase.objects.filter(
            query_search,
            query_techarea,
            query_spinoff,
            query_startup,
            query_is_active
        ).values(
            "id",
            "piva",
            "nome_azienda",
            "nome_file_logo",
            "url_sito_web",
            "descrizione_ita",
            "descrizione_eng",
            "referente_unical",
            "matricola_referente_unical",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_startup",
            "is_spinoff",
            "is_active"
        ).distinct()

        for q in query:
            departments = SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base__exact=q['id']).values(
                'id_didattica_dipartimento__dip_cod',
                'id_didattica_dipartimento__dip_des_it',
                'id_didattica_dipartimento__dip_des_eng',
                'id_didattica_dipartimento__dip_nome_breve',
            )

            if len(departments) == 0:
                q['Departments'] = []
            else:
                q['Departments'] = departments

        if q_departments:
            dep = q_departments.split(',')
            final_query = []
            for q in query:
                for d in q['Departments']:
                    if d['id_didattica_dipartimento__dip_cod'] in dep:
                        final_query.append(q)
            return final_query


        return query

    @staticmethod
    def getCompanyDetail(companyid):

        query = SpinoffStartupDatiBase.objects.filter(
            id=companyid,
            is_active=True
        ).values(
            "id",
            "piva",
            "nome_azienda",
            "nome_file_logo",
            "url_sito_web",
            "descrizione_ita",
            "descrizione_eng",
            "referente_unical",
            "matricola_referente_unical",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_startup",
            "is_spinoff",
            "is_active"
        )
        for q in query:

            departments = SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base__exact=q['id']).values(
                'id_didattica_dipartimento__dip_cod',
                'id_didattica_dipartimento__dip_des_it',
                'id_didattica_dipartimento__dip_des_eng',
                'id_didattica_dipartimento__dip_nome_breve',
            )

            if len(departments) == 0:
                q['Departments'] = []
            else:
                q['Departments'] = departments

        return query

    @staticmethod
    def getTechAreas():

        query = TipologiaAreaTecnologica.objects.values(
            "id",
            "descr_area_ita",
            "descr_area_eng",
        ).distinct()

        return query


class ServiceProgetto:

    @staticmethod
    def getProjects(
            search,
            techarea,
            infrastructure,
            programtype,
            territorialscope,
            notprogramtype,
            year,
            only_active=True):

        query_search = Q()
        query_techarea = Q()
        query_infrastructure = Q()
        query_programtype = Q()
        query_territorialscope = Q()
        query_notprogramtype = Q()
        query_year = Q()
        query_is_active = Q(is_active=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(
                    titolo__icontains=k) | Q(
                    id_area_tecnologica__descr_area_ita__icontains=k) | Q(
                    uo__denominazione__icontains=k) | Q(
                    anno_avvio__icontains=k) | Q(
                    id_ambito_territoriale__ambito_territoriale__icontains=k)
                query_search &= q_nome
        if techarea:
            query_techarea = Q(id_area_tecnologica=techarea)
        if infrastructure:
            query_infrastructure = Q(uo=infrastructure)
        if programtype:
            programtype = programtype.split(",")
            query_programtype = Q(id_tipologia_programma__in=programtype)
        if territorialscope:
            query_territorialscope = Q(id_ambito_territoriale=territorialscope)
        if notprogramtype:
            notprogramtype = notprogramtype.split(",")
            query_notprogramtype= ~Q(id_tipologia_programma__in=notprogramtype)
        if year:
            query_year= Q(anno_avvio=year)

        query = ProgettoDatiBase.objects.filter(
            query_search,
            query_techarea,
            query_infrastructure,
            query_territorialscope,
            query_notprogramtype,
            query_programtype,
            query_year,
            query_is_active
        ).values(
            "id",
            "id_ambito_territoriale__id",
            "id_ambito_territoriale__ambito_territoriale",
            "id_tipologia_programma__id",
            "id_tipologia_programma__nome_programma",
            "titolo",
            "anno_avvio",
            "uo",
            "uo__denominazione",
            "descr_breve",
            "url_immagine",
            "abstract_ita",
            "abstract_eng",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_active"
        ).distinct().order_by(
            'ordinamento',
            '-anno_avvio',
            'id_ambito_territoriale__ambito_territoriale')

        for q in query:
            responsabili = ProgettoResponsabileScientifico.objects.filter(
                id_progetto=q['id']).values(
                "matricola",
                "nome_origine",
            )
            ricercatori = ProgettoRicercatore.objects.filter(
                id_progetto=q['id']).values(
                "matricola",
                "nome_origine",
            )
            if len(responsabili) == 0:
                q['Responsabili'] = []
            else:
                q['Responsabili'] = responsabili

            if len(ricercatori) == 0:
                q['Ricercatori'] = []
            else:
                q['Ricercatori'] = ricercatori

        return query

    @staticmethod
    def getProjectDetail(projectid):

        query = ProgettoDatiBase.objects.filter(
            id=projectid,
            is_active=True
        ).values(
            "id",
            "id_ambito_territoriale__id",
            "id_ambito_territoriale__ambito_territoriale",
            "id_tipologia_programma__id",
            "id_tipologia_programma__nome_programma",
            "titolo",
            "anno_avvio",
            "uo",
            "uo__denominazione",
            "descr_breve",
            "url_immagine",
            "abstract_ita",
            "abstract_eng",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_active"
        ).distinct()

        for q in query:
            responsabili = ProgettoResponsabileScientifico.objects.filter(
                id_progetto=q['id']).values(
                "matricola",
                "nome_origine",
            )
            ricercatori = ProgettoRicercatore.objects.filter(
                id_progetto=q['id']).values(
                "matricola",
                "nome_origine",
            )
            if len(responsabili) == 0:
                q['Responsabili'] = []
            else:
                q['Responsabili'] = responsabili

            if len(ricercatori) == 0:
                q['Ricercatori'] = []
            else:
                q['Ricercatori'] = ricercatori

        return query

    @staticmethod
    def getTerritorialScopes():

        query = ProgettoAmbitoTerritoriale.objects.values(
            "id",
            "ambito_territoriale"
        ).distinct()

        return query

    @staticmethod
    def getProgramTypes():

        query = ProgettoTipologiaProgramma.objects.values(
            "id",
            "nome_programma"
        ).distinct()

        return query

    @staticmethod
    def getProjectInfrastructures():

        query = ProgettoDatiBase.objects.values(
            "uo",
            "uo__denominazione",
        ).distinct()

        query = list(query)

        for q in query:
            if q['uo'] == None:
                query.remove(q)

        return query


class ServiceStructure:

    @staticmethod
    def getStructureChilds(structureid=None):

        child = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid).values_list("uo", flat=True)

        result = [structureid]


        for c in child:

            structures_tree = ServiceStructure.getStructureChilds(c)
            result.extend(structures_tree)

        result.extend(child)

        return result
