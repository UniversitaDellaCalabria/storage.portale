import datetime

from addressbook.utils import append_email_addresses
from advanced_training.models import (
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneModalitaSelezione,
    AltaFormazionePartner,
    AltaFormazionePianoDidattico,
    AltaFormazioneTipoCorso,
)
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaAttivitaFormativaModalita,
    DidatticaCds,
    DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti,
    DidatticaCdsLingua,
    DidatticaCdsPeriodi,
    DidatticaCopertura,
    DidatticaCoperturaDettaglioOre,
    DidatticaPdsRegolamento,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaFilAnd,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSche,
    DidatticaRegolamento,
    DidatticaRegolamentoAltriDati,
    DidatticaTestiAf,
    DidatticaTestiRegolamento,
)
from cds_brochure.models import (
    SitoWebCdsDatiBase,
    SitoWebCdsExStudenti,
    SitoWebCdsLink,
    SitoWebCdsSlider,
)
from cds_websites.models import (
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliReg,
    SitoWebCdsTopicArticoliRegAltriDati,
)
from django.db.models import Case, CharField, F, Prefetch, Q, Value, When
from django.http import Http404
from generics.services import ServiceQueryBuilder
from structures.models import DidatticaDipartimentoUrl


class ServiceDidatticaCds:
    @staticmethod
    def cdslist(language, query_params):
        didatticacds_params_to_query_field = {
            "courseclasscod": "cla_miur_cod",
            "courseclassname": "cla_miur_des__icontains",
            "cdscod": "cds_cod",
            # 'courseclassgroup': ... unspecified atm
            "departmentid": "dip__dip_id",
            "departmentcod": "dip__dip_cod",
            "departmentname": f'dip__dip_des_{language == "it" and "it" or "eng"}__icontains',
            "area": "area_cds__icontains",
        }

        didatticaregolamento_params_to_query_field = {
            "academicyear": "didatticaregolamento__aa_reg_did__exact",
            "jointdegree": "didatticaregolamento__titolo_congiunto_cod",
            "regdid": "didatticaregolamento__regdid_id",
        }

        didatticacdslingua_params_to_query_field = {
            "cdslanguage": "didatticacdslingua__iso6392_cod",
        }

        search = query_params.get("search", None)
        if search is not None:
            search = search.split(" ")

        courses_allowed = query_params.get("coursetype", "")
        if courses_allowed != "":
            courses_allowed = courses_allowed.split(",")

        q1 = ServiceQueryBuilder.build_filter_chain(
            didatticacds_params_to_query_field, query_params
        )
        q2 = ServiceQueryBuilder.build_filter_chain(
            didatticaregolamento_params_to_query_field, query_params
        )
        q3 = ServiceQueryBuilder.build_filter_chain(
            didatticacdslingua_params_to_query_field, query_params
        )

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

        items = DidatticaCds.objects.filter(q4, q1, q2, q3)
        # didatticacdslingua__lin_did_ord_id__isnull=False

        if "academicyear" not in query_params:
            items = items.filter(didatticaregolamento__stato_regdid_cod__exact="A")

        if courses_allowed != "":
            items = items.filter(tipo_corso_cod__in=courses_allowed)

        items = items.values(
            "didatticaregolamento__regdid_id",
            "didatticaregolamento__aa_reg_did",
            "didatticaregolamento__frequenza_obbligatoria",
            "dip__dip_id",
            "dip__dip_cod",
            "dip__dip_des_it",
            "dip__dip_des_eng",
            "cds_id",
            "cds_cod",
            "cdsord_id",
            "nome_cds_it",
            "nome_cds_eng",
            "tipo_corso_cod",
            "tipo_corso_des",
            "cla_miur_cod",
            "cla_miur_des",
            "intercla_miur_cod",
            "intercla_miur_des",
            "durata_anni",
            "valore_min",
            "codicione",
            "didatticaregolamento__titolo_congiunto_cod",
            "didatticaregolamento__stato_regdid_cod",
            "area_cds",
            "area_cds_en",
        ).distinct()
        items = (
            items.order_by("nome_cds_it")
            if language == "it"
            else items.order_by(F("nome_cds_eng").asc(nulls_last=True))
        )
        for i in items:
            erogation_mode = DidatticaRegolamento.objects.filter(
                cds_id=i["cds_id"], stato_regdid_cod__exact="A"
            ).values("modalita_erogazione")
            if len(erogation_mode) != 0:
                i["ErogationMode"] = erogation_mode
            else:
                i["ErogationMode"] = None  # pragma: no cover

        items = list(items)
        for item in items:
            item["Languages"] = (
                DidatticaCdsLingua.objects.filter(cdsord_id=item["cdsord_id"])
                .values("lingua_des_it", "lingua_des_eng")
                .distinct()
            )

            item["OtherData"] = (
                DidatticaCdsAltriDati.objects.filter(
                    regdid_id=item["didatticaregolamento__regdid_id"]
                )
                .values(
                    # 'num_posti',
                    # 'modalita_iscrizione',
                    "manifesto_studi",
                    "regolamento_didattico",
                    "ordinamento_didattico",
                )
                .distinct()
            )

            # item['OfficesData'] = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=item['cds_id']).values(
            # 'ordine',
            # 'nome_ufficio',
            # 'matricola_riferimento',
            # 'nome_origine_riferimento',
            # 'telefono',
            # 'email',
            # 'edificio',
            # 'piano',
            # 'orari',
            # 'sportello_online'
            # ).distinct()

        return items

    @staticmethod
    def cds(language, cdsid_param, only_active=True):
        res = DidatticaCds.objects.filter(didatticaregolamento__regdid_id=cdsid_param)

        langs = res.prefetch_related("didatticacdslingua")

        res = res.values(
            "didatticaregolamento__regdid_id",
            "didatticaregolamento__aa_reg_did",
            "didatticaregolamento__frequenza_obbligatoria",
            "dip__dip_id",
            "dip__dip_cod",
            "dip__dip_des_it",
            "dip__dip_des_eng",
            "cds_id",
            "cds_cod",
            "cdsord_id",
            "nome_cds_it",
            "nome_cds_eng",
            "tipo_corso_cod",
            "tipo_corso_des",
            "cla_miur_cod",
            "cla_miur_des",
            "intercla_miur_cod",
            "intercla_miur_des",
            "durata_anni",
            "valore_min",
            "codicione",
            "didatticaregolamento__titolo_congiunto_cod",
            "didatticaregolamento__stato_regdid_cod",
            "area_cds",
            "area_cds_en",
        ).distinct()

        for r in res:
            erogation_mode = DidatticaRegolamento.objects.filter(
                cds_id=r["cds_id"], stato_regdid_cod__exact="A"
            ).values("modalita_erogazione")
            if len(erogation_mode) != 0:
                r["ErogationMode"] = erogation_mode
            else:
                r["ErogationMode"] = None

        res = list(res)

        if len(res) == 0:
            return None

        texts = DidatticaTestiRegolamento.objects.filter(regdid=cdsid_param).values(
            "regdid__regdid_id",
            "clob_txt_ita",
            "clob_txt_eng",
            "testo_regdid_url",
            "tipo_testo_regdid_cod",
            "profilo",
            "profilo_eng",
        )

        other_data = DidatticaRegolamentoAltriDati.objects.filter(
            regdid=cdsid_param
        ).values(
            "regdid__regdid_id", "clob_txt_ita", "clob_txt_eng", "tipo_testo_regdid_cod"
        )

        list_profiles = {}
        last_profile = ""

        res[0]["Languages"] = langs.values(
            "didatticacdslingua__lingua_des_it", "didatticacdslingua__lingua_des_eng"
        ).distinct()

        res[0]["URL_CDS_DOC"] = None
        res[0]["URL_CDS"] = None
        res[0]["INTRO_CDS_FMT"] = None
        res[0]["URL_CDS_VIDEO"] = None
        res[0]["DESC_COR_BRE"] = None
        res[0]["OBB_SPEC"] = None
        res[0]["REQ_ACC"] = None
        res[0]["REQ_ACC_2"] = None
        res[0]["PROFILO"] = None
        res[0]["PROVA_FINALE"] = None
        res[0]["PROVA_FINALE_2"] = None

        for text in texts:
            if (
                text["tipo_testo_regdid_cod"] != "FUNZIONI"
                and text["tipo_testo_regdid_cod"] != "COMPETENZE"
                and text["tipo_testo_regdid_cod"] != "SBOCCHI"
            ):
                if (
                    text["clob_txt_eng"] is None and language != "it"
                ) or language == "it":
                    res[0][text["tipo_testo_regdid_cod"]] = text["clob_txt_ita"]
                else:
                    res[0][text["tipo_testo_regdid_cod"]] = text["clob_txt_eng"]
            else:
                if (
                    language != "it" and text["profilo_eng"] is None
                ) or language == "it":
                    if text["profilo"] != last_profile:
                        last_profile = text["profilo"]
                        list_profiles[last_profile] = {}
                elif (
                    text[f'{ language == "it" and "profilo" or "profilo_eng" }']
                    != last_profile
                ):  # pragma: no cover
                    last_profile = text[
                        f'{language == "it" and "profilo" or "profilo_eng"}'
                    ]
                    list_profiles[last_profile] = {}

                if (
                    text["clob_txt_eng"] is None and language != "it"
                ) or language == "it":
                    list_profiles[last_profile][text["tipo_testo_regdid_cod"]] = text[
                        "clob_txt_ita"
                    ]
                else:
                    list_profiles[last_profile][text["tipo_testo_regdid_cod"]] = text[
                        "clob_txt_eng"
                    ]

        for od in other_data:
            if (od["clob_txt_eng"] is None and language != "it") or language == "it":
                res[0][od["tipo_testo_regdid_cod"]] = od["clob_txt_ita"]
            else:
                res[0][od["tipo_testo_regdid_cod"]] = od["clob_txt_eng"]

        res[0]["PROFILO"] = list_profiles

        res[0]["OtherData"] = (
            DidatticaCdsAltriDati.objects.filter(regdid_id=cdsid_param)
            .values(
                "matricola_coordinatore",
                "nome_origine_coordinatore",
                "matricola_vice_coordinatore",
                "nome_origine_vice_coordinatore",
                # 'num_posti',
                # 'modalita_iscrizione',
                "manifesto_studi",
                "regolamento_didattico",
                "ordinamento_didattico",
            )
            .distinct()
        )

        res[0]["OfficesData"] = (
            DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=res[0]["cds_id"])
            .values(
                "ordine",
                "nome_ufficio",
                "matricola_riferimento",
                "nome_origine_riferimento",
                "telefono",
                "email",
                "edificio",
                "piano",
                "orari",
                "sportello_online",
            )
            .distinct()
        )

        query_visibile = Q(visibile=True) if only_active else Q()
        res[0]["CdsGroups"] = (
            DidatticaCdsGruppi.objects.filter(
                query_visibile, id_didattica_cds=res[0]["cds_id"]
            )
            .values(
                "ordine",
                "id",
                "descr_breve_it",
                "descr_breve_en",
                "descr_lunga_it",
                "descr_lunga_en",
            )
            .distinct()
        )

        res[0]["CdsPeriods"] = DidatticaCdsPeriodi.objects.filter(
            cds_cod=res[0]["cds_cod"], aa_id=res[0]["didatticaregolamento__aa_reg_did"]
        ).values(
            "ciclo_des",
            "tipo_ciclo_des",
            "tipo_ciclo_des_eng",
            "data_inizio",
            "data_fine",
        )

        for group in res[0]["CdsGroups"]:
            members = (
                DidatticaCdsGruppiComponenti.objects.filter(
                    query_visibile, id_didattica_cds_gruppi=group["id"]
                )
                .values(
                    "ordine",
                    "id",
                    "matricola",
                    "cognome",
                    "nome",
                    "funzione_it",
                    "funzione_en",
                )
                .distinct()
            )
            group["members"] = members

        return res

    @staticmethod
    def getDegreeTypes():
        query = (
            DidatticaCds.objects.values("tipo_corso_cod", "tipo_corso_des")
            .order_by("tipo_corso_des")
            .distinct()
        )
        return query

    @staticmethod
    def getAcademicYears():
        query = (
            DidatticaRegolamento.objects.values("aa_reg_did")
            .order_by("-aa_reg_did")
            .distinct()
        )
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
            res.append(q["area_cds"])

        res = list(dict.fromkeys(res))
        temp = []
        for q in query:
            if (
                q["area_cds"] not in temp
                and q["area_cds"] in res
                and q["area_cds"] is not None
            ):
                temp.append(q)
                res.remove(q["area_cds"])

        return temp

    @staticmethod
    def getContacts(cdscod):
        last_year = datetime.date.today().year - 1
        current_year = datetime.date.today().year
        years = [last_year, current_year]
        query = (
            DidatticaCopertura.objects.filter(
                cds_cod=cdscod,
                aa_off_id__in=years,
                personale__flg_cessato=0,
                personale__fl_docente=1,
            )
            .values(
                "personale__nome",
                "personale__cognome",
                "personale__middle_name",
                "personale__matricola",
                "personale__cd_uo_aff_org",
                "personale__ds_aff_org",
            )
            .order_by("personale__cognome")
        )
        for q in query:
            q["DepartmentUrl"] = DidatticaDipartimentoUrl.objects.filter(
                dip_cod=q["personale__cd_uo_aff_org"]
            ).values("dip_url")
        return query

    @staticmethod
    def getHighFormationMasters(
        search, director, coursetype, erogation, department, language, year
    ):
        query_search = Q()
        query_director = Q()
        query_coursetype = Q()
        query_erogation = Q()
        query_department = Q()
        query_language = Q()
        query_year = Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(titolo_it__icontains=k) | Q(
                    matricola_direttore_scientifico__cognome__istartswith=k
                )
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

        query = (
            AltaFormazioneDatiBase.objects.filter(
                query_search,
                query_director,
                query_erogation,
                query_coursetype,
                query_department,
                query_language,
                query_year,
            )
            .values(
                "id",
                "titolo_it",
                "titolo_en",
                "id_alta_formazione_tipo_corso",
                "id_alta_formazione_tipo_corso__tipo_corso_descr",
                "id_alta_formazione_mod_erogazione",
                "id_alta_formazione_mod_erogazione__descrizione",
                "lingua",
                "ore",
                "mesi",
                "anno_rilevazione",
                "id_dipartiento_riferimento",
                "id_dipartiento_riferimento__dip_cod",
                "id_dipartiento_riferimento__dip_des_it",
                "id_dipartiento_riferimento__dip_des_eng",
                "sede_corso",
                "num_min_partecipanti",
                "num_max_partecipanti",
                "uditori_ammessi",
                "num_max_uditori",
                "requisiti_ammissione",
                "titolo_rilasciato",
                "doppio_titolo",
                "matricola_direttore_scientifico",
                "nome_origine_direttore_scientifico",
                "quota_iscrizione",
                "quota_uditori",
                "funzione_lavoro",
                "obiettivi_formativi_summer_school",
                "competenze",
                "sbocchi_occupazionali",
                "obiettivi_formativi_corso",
                "modalita_svolgimento_prova_finale",
                "numero_moduli",
                "stage_tirocinio",
                "ore_stage_tirocinio",
                "cfu_stage",
                "mesi_stage",
                "tipo_aziende_enti_tirocinio",
                "contenuti_tempi_criteri_cfu",
                "project_work",
            )
            .order_by("titolo_it", "id")
        )

        for q in query:
            partners = (
                AltaFormazionePartner.objects.filter(
                    id_alta_formazione_dati_base=q["id"]
                )
                .values("id", "denominazione", "tipologia", "sito_web")
                .distinct()
            )

            if len(partners) == 0:
                q["Partners"] = []
            else:
                q["Partners"] = partners

            selections = (
                AltaFormazioneModalitaSelezione.objects.filter(
                    id_alta_formazione_dati_base=q["id"]
                )
                .values(
                    "id",
                    "tipo_selezione",
                )
                .distinct()
            )

            if len(selections) == 0:
                q["Selections"] = []
            else:
                q["Selections"] = selections

            internal_scientific_council = (
                AltaFormazioneConsiglioScientificoInterno.objects.filter(
                    id_alta_formazione_dati_base=q["id"]
                ).values("matricola_cons", "nome_origine_cons")
            )

            if len(internal_scientific_council) == 0:
                q["InternalCouncil"] = []
            else:
                q["InternalCouncil"] = internal_scientific_council

            external_scientific_council = (
                AltaFormazioneConsiglioScientificoEsterno.objects.filter(
                    id_alta_formazione_dati_base=q["id"]
                ).values("nome_cons", "ruolo_cons", "ente_cons")
            )

            if len(external_scientific_council) == 0:
                q["ExternalCouncil"] = []
            else:
                q["ExternalCouncil"] = external_scientific_council

            teaching_plan = AltaFormazionePianoDidattico.objects.filter(
                id_alta_formazione_dati_base=q["id"]
            ).values("id", "modulo", "ssd", "num_ore", "cfu", "verifica_finale")

            if len(teaching_plan) == 0:
                q["TeachingPlan"] = []
            else:
                q["TeachingPlan"] = teaching_plan

            teaching_assignments = AltaFormazioneIncaricoDidattico.objects.filter(
                id_alta_formazione_dati_base=q["id"]
            ).values(
                "id", "modulo", "num_ore", "docente", "qualifica", "ente", "tipologia"
            )

            if len(teaching_assignments) == 0:
                q["TeachingAssignments"] = []
            else:
                q["TeachingAssignments"] = teaching_assignments

        return query

    @staticmethod
    def getHighFormationMaster(master_id):
        query = (
            AltaFormazioneDatiBase.objects.filter(id=master_id)
            .values(
                "id",
                "titolo_it",
                "titolo_en",
                "id_alta_formazione_tipo_corso",
                "id_alta_formazione_tipo_corso__tipo_corso_descr",
                "id_alta_formazione_mod_erogazione",
                "id_alta_formazione_mod_erogazione__descrizione",
                "ore",
                "mesi",
                "lingua",
                "anno_rilevazione",
                "id_dipartiento_riferimento",
                "id_dipartiento_riferimento__dip_cod",
                "id_dipartiento_riferimento__dip_des_it",
                "id_dipartiento_riferimento__dip_des_eng",
                "sede_corso",
                "num_min_partecipanti",
                "num_max_partecipanti",
                "uditori_ammessi",
                "num_max_uditori",
                "requisiti_ammissione",
                "titolo_rilasciato",
                "doppio_titolo",
                "matricola_direttore_scientifico",
                "nome_origine_direttore_scientifico",
                "quota_iscrizione",
                "quota_uditori",
                "funzione_lavoro",
                "obiettivi_formativi_summer_school",
                "competenze",
                "sbocchi_occupazionali",
                "obiettivi_formativi_corso",
                "modalita_svolgimento_prova_finale",
                "numero_moduli",
                "stage_tirocinio",
                "ore_stage_tirocinio",
                "cfu_stage",
                "mesi_stage",
                "tipo_aziende_enti_tirocinio",
                "contenuti_tempi_criteri_cfu",
                "project_work",
            )
            .order_by("titolo_it", "id")
        )

        query = list(query)
        query[0]["Partners"] = (
            AltaFormazionePartner.objects.filter(id_alta_formazione_dati_base=master_id)
            .values("id", "denominazione", "tipologia", "sito_web")
            .distinct()
        )

        query[0]["Selections"] = (
            AltaFormazioneModalitaSelezione.objects.filter(
                id_alta_formazione_dati_base=master_id
            )
            .values(
                "id",
                "tipo_selezione",
            )
            .distinct()
        )

        query[0]["InternalCouncil"] = (
            AltaFormazioneConsiglioScientificoInterno.objects.filter(
                id_alta_formazione_dati_base=master_id
            )
            .values("matricola_cons", "nome_origine_cons")
            .distinct()
        )

        query[0]["ExternalCouncil"] = (
            AltaFormazioneConsiglioScientificoEsterno.objects.filter(
                id_alta_formazione_dati_base=master_id
            )
            .values("nome_cons", "ruolo_cons", "ente_cons")
            .distinct()
        )

        query[0]["TeachingPlan"] = (
            AltaFormazionePianoDidattico.objects.filter(
                id_alta_formazione_dati_base=master_id
            )
            .values("id", "modulo", "ssd", "num_ore", "cfu", "verifica_finale")
            .distinct()
        )

        query[0]["TeachingAssignments"] = (
            AltaFormazioneIncaricoDidattico.objects.filter(
                id_alta_formazione_dati_base=master_id
            )
            .values(
                "id", "modulo", "num_ore", "docente", "qualifica", "ente", "tipologia"
            )
            .distinct()
        )

        return query

    @staticmethod
    def getErogationModes():
        query = AltaFormazioneModalitaErogazione.objects.values("id", "descrizione")

        return query

    @staticmethod
    def getHighFormationCourseTypes():
        query = AltaFormazioneTipoCorso.objects.values("id", "tipo_corso_descr")

        return query

    @staticmethod
    def getCdsWebsites(search):
        query_search = Q()

        if search:
            for k in search.split(" "):
                q_nome_corso_it = Q(cds__nome_cds_it__icontains=k)
                query_search &= q_nome_corso_it

        query = (
            SitoWebCdsDatiBase.objects.filter(query_search)
            .select_related("cds")
            .values(
                "id",
                # 'cds__cds_id',
                "cds__cds_cod",
                "aa",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
            )
        )
        return list(query)

    @staticmethod
    def getCdsWebsite(cds_cod):
        query = (
            SitoWebCdsDatiBase.objects.filter(cds__cds_cod=cds_cod)
            .select_related("cds")
            .values(
                "id",
                # "cds__cds_id",
                "cds__cds_cod",
                "aa",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "cds__cla_miur_cod",
                "cds__cla_miur_des",
                "cds__intercla_miur_cod",
                "cds__intercla_miur_des",
                # "classe_laurea_it",
                # "classe_laurea_en",
                # "classe_laurea_interclasse_it",
                # "classe_laurea_interclasse_en",
                # "lingua_it",
                # "lingua_en",
                "cds__durata_anni",
                "num_posti",
                # "link_video_cds_it",
                # "link_video_cds_en",
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
                # "sito_web_it",
                # "sito_web_en",
                # 'id_didattica_regolamento'
            )
        )

        query = list(query)
        for q in query:
            reg_did_video = DidatticaRegolamentoAltriDati.objects.filter(
                regdid__cds__cds_cod=q["cds__cds_cod"],
                regdid__aa_reg_did=q["aa"],
                tipo_testo_regdid_cod="URL_CDS_VIDEO",
            ).first()
            q["link_video_cds_it"] = None
            q["link_video_cds_en"] = None
            if reg_did_video:
                q["link_video_cds_it"] = reg_did_video.clob_txt_ita
                q["link_video_cds_en"] = reg_did_video.clob_txt_eng

            lingue = DidatticaCdsLingua.objects.filter(
                cdsord__cds_cod=q["cds__cds_cod"]
            )
            # lingua_it = []
            # lingua_en = []
            lingue_list = []
            for lingua in lingue:
                # if not lingua.lingua_des_it in lingua_it:
                # lingua_it.append(lingua.lingua_des_it)
                # if not lingua.lingua_des_eng in lingua_en:
                # lingua_en.append(lingua.lingua_des_eng)
                if lingua.iso6392_cod not in lingue_list:
                    lingue_list.append(lingua.iso6392_cod)
            # q['lingua_it'] = lingua_it
            # q['lingua_en'] = lingua_en
            q["lingue"] = lingue_list

            ex_studenti = (
                SitoWebCdsExStudenti.objects.filter(id_sito_web_cds_dati_base=q["id"])
                .values(
                    "id",
                    "nome",
                    "ordine",
                    "profilo_it",
                    "profilo_en",
                    "link_it",
                    "link_en",
                    "foto",
                )
                .order_by("ordine")
            )
            if len(ex_studenti) > 0:
                q["ExStudents"] = ex_studenti
            else:  # pragma: no cover
                q["ExStudents"] = []
            links = (
                SitoWebCdsLink.objects.filter(id_sito_web_cds_dati_base=q["id"])
                .values(
                    "id",
                    "ordine",
                    "descrizione_link_it",
                    "descrizione_link_en",
                    "link_it",
                    "link_en",
                )
                .order_by("ordine")
            )
            if len(links) > 0:
                q["CdsLink"] = links
            else:  # pragma: no cover
                q["CdsLink"] = []

            sliders = (
                SitoWebCdsSlider.objects.filter(id_sito_web_cds_dati_base=q["id"])
                .values(
                    "id",
                    "ordine",
                    "slider_it",
                    "slider_en",
                )
                .order_by("ordine")
            )
            if len(sliders) > 0:
                q["CdsSliders"] = sliders
            else:
                q["CdsSliders"] = []

        return query

    # @staticmethod
    # def getCdsWebsitesDegreeTypes():
    # query = SitoWebCdsDatiBase.objects.values(
    # "classe_laurea_it",
    # "classe_laurea_en"
    # ).distinct()

    # return query

    @staticmethod
    def getCdsWebsitesTopics():
        query = SitoWebCdsTopic.objects.values(
            "id", "descr_topic_it", "descr_topic_en", "visibile"
        ).distinct()

        return query

    @staticmethod
    def getCdsWebsitesTopicArticles(cds_cod, topic_id, only_active=True):
        result = []

        if not (cds_cod and topic_id):
            return result

        topic_id_list = topic_id.split(",")

        query_visibile = Q(visibile=True) if only_active else Q()
        query_topic_id = Q(id_sito_web_cds_topic__id__in=topic_id_list)
        query_cds_cod = Q(
            id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds__cds_cod=str(
                cds_cod
            )
        ) | Q(id_sito_web_cds_oggetti_portale__cds__cds_cod=str(cds_cod))

        articoli_reg_altri_dati_qs = (
            SitoWebCdsTopicArticoliRegAltriDati.objects.filter(query_visibile)
            .select_related("id_sito_web_cds_tipo_dato")
            .defer("dt_mod", "id_user_mod", "id_sito_web_cds_tipo_dato__descr_lunga")
            .annotate(
                type_id=F("id_sito_web_cds_tipo_dato__id"),
                type=F("id_sito_web_cds_tipo_dato__descr_breve"),
            )
        )

        sub_articoli_qs = SitoWebCdsSubArticoliRegolamento.objects.filter(
            query_visibile
        ).defer("dt_mod", "id_user_mod")

        records = (
            SitoWebCdsTopicArticoliReg.objects.prefetch_related(
                Prefetch(
                    "sitowebcdstopicarticoliregaltridati_set",
                    queryset=articoli_reg_altri_dati_qs,
                ),
                Prefetch(
                    "sitowebcdssubarticoliregolamento_set", queryset=sub_articoli_qs
                ),
            )
            .select_related(
                "id_sito_web_cds_oggetti_portale__cds",
                "id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds",
                "id_sito_web_cds_topic",
            )
            .filter(query_topic_id, query_cds_cod, query_visibile)
            .only(
                "id",
                "titolo_it",
                "titolo_en",
                "testo_it",
                "testo_en",
                "visibile",
                "ordine",
                "id_sito_web_cds_topic__id",
                "id_sito_web_cds_topic__descr_topic_it",
                "id_sito_web_cds_topic__descr_topic_en",
                "id_sito_web_cds_oggetti_portale__id",
                "id_sito_web_cds_oggetti_portale__id_classe_oggetto_portale",
                "id_sito_web_cds_oggetti_portale__id_oggetto_portale",
                "id_sito_web_cds_oggetti_portale__aa_regdid_id",
                "id_sito_web_cds_oggetti_portale__testo_it",
                "id_sito_web_cds_oggetti_portale__testo_en",
                "id_sito_web_cds_oggetti_portale__cds__cds_cod",
                "id_didattica_cds_articoli_regolamento__id",
                "id_didattica_cds_articoli_regolamento__id_didattica_cds_articoli_regolamento_testata__cds__cds_cod",
            )
            .annotate(
                tipo=Case(
                    When(
                        id_didattica_cds_articoli_regolamento__isnull=False,
                        then=Value("Article"),
                    ),
                    default=Value("Object"),
                    output_field=CharField(),
                )
            )
            .order_by("id_sito_web_cds_topic__id", "ordine")
        )

        for record in records:
            data = {
                "id": record.id,
                "tipo": record.tipo,
                "topic_id": record.id_sito_web_cds_topic_id,
                "descr_topic_it": record.id_sito_web_cds_topic.descr_topic_it,
                "descr_topic_en": record.id_sito_web_cds_topic.descr_topic_en,
                "titolo_it": record.titolo_it,
                "titolo_en": record.titolo_en,
                "testo_it": record.testo_it,
                "testo_en": record.testo_en,
                "visibile": record.visibile,
                "ordine": record.ordine,
                "altri_dati": [
                    {
                        "id": sito_cds_topic_articoli_reg_altri_dati.id,
                        "ordine": sito_cds_topic_articoli_reg_altri_dati.ordine,
                        "titolo_it": sito_cds_topic_articoli_reg_altri_dati.titolo_it,
                        "titolo_en": sito_cds_topic_articoli_reg_altri_dati.titolo_en,
                        "testo_it": sito_cds_topic_articoli_reg_altri_dati.testo_it,
                        "testo_en": sito_cds_topic_articoli_reg_altri_dati.testo_en,
                        "link": sito_cds_topic_articoli_reg_altri_dati.link,
                        "type_id": sito_cds_topic_articoli_reg_altri_dati.type_id,
                        "type": sito_cds_topic_articoli_reg_altri_dati.type,
                        "visibile": sito_cds_topic_articoli_reg_altri_dati.visibile,
                    }
                    for sito_cds_topic_articoli_reg_altri_dati in record.sitowebcdstopicarticoliregaltridati_set.all()
                ],
                "sotto_articoli": [
                    {
                        "id": sito_web_cds_sub_articoli_regolamento.id,
                        "ordine": sito_web_cds_sub_articoli_regolamento.ordine,
                        "titolo_it": sito_web_cds_sub_articoli_regolamento.titolo_it,
                        "titolo_en": sito_web_cds_sub_articoli_regolamento.titolo_en,
                        "testo_it": sito_web_cds_sub_articoli_regolamento.testo_it,
                        "testo_en": sito_web_cds_sub_articoli_regolamento.testo_en,
                        "visibile": sito_web_cds_sub_articoli_regolamento.visibile,
                    }
                    for sito_web_cds_sub_articoli_regolamento in record.sitowebcdssubarticoliregolamento_set.all()
                ],
            }

            if record.tipo == "Object":
                data["oggetto"] = {
                    "id": record.id_sito_web_cds_oggetti_portale.id,
                    "id_classe_oggetto_portale": record.id_sito_web_cds_oggetti_portale.id_classe_oggetto_portale,
                    "id_oggetto_portale": record.id_sito_web_cds_oggetti_portale.id_oggetto_portale,
                    "aa_regdid_id": record.id_sito_web_cds_oggetti_portale.aa_regdid_id,
                    "testo_it": record.id_sito_web_cds_oggetti_portale.testo_it,
                    "testo_en": record.id_sito_web_cds_oggetti_portale.testo_en,
                }

            result.append(data)

        return result

    @staticmethod
    def getCdsWebsitesStudyPlans(cds_cod, year):  # , regdid):
        if cds_cod and year:  # or regdid:
            query_cds = Q(regdid_id__cds_id__cds_cod__exact=cds_cod) if cds_cod else Q()
            query_year = Q(regdid_id__aa_reg_did__exact=year) if year else Q()
            # query_regdid = Q(regdid_id__exact=regdid) if regdid else Q()

            query = (
                DidatticaPianoRegolamento.objects.filter(
                    query_cds,
                    # query_regdid,
                    query_year,
                    stato_cod="A",
                )
                .select_related("regdid__cds")
                .values(
                    "regpiani_id",
                    "regdid_id",
                    "attinenza_cod",
                    "cod",
                    "aa_coorte_id",
                    "aa_regpiani_id",
                    "des",
                    "def_flg",
                    "stato_cod",
                    "stato_des",
                    "regpiani_pdr_id",
                    "regpiani_pdr_cod",
                    "regpiani_pdr_des",
                    "regpiani_pdr_aa_coorte_id",
                    "regpiani_pdr_aa_regpiani_id",
                    "flg_exp_seg_stu",
                    "regdid__cds__durata_anni",
                )
                .distinct()
                .order_by("regpiani_id")
            )

            for q in query:
                schede = DidatticaPianoSche.objects.filter(
                    regpiani_id__exact=q["regpiani_id"]
                ).values(
                    "sche_piano_id",
                    "sche_piano_des",
                    "sche_piano_cod",
                    "pds_cod",
                    "pds_des",
                    "comune_flg",
                    "apt_id",
                    "cla_m_id",
                    "cla_miur_cod",
                    "cla_miur_des",
                    "pds_cod",
                )

                for s in schede:
                    obbl = DidatticaPianoSceltaSchePiano.objects.filter(
                        sche_piano_id__exact=s["sche_piano_id"], tipo_sce_cod__exact="O"
                    ).values(
                        "sce_id",
                        "sce_des",
                        "anno_corso",
                        "apt_slot_ord_num",
                        "tipo_regsce_cod",
                        "tipo_sce_cod",
                        "tipo_sce_des",
                        "tipo_regsce_des",
                        "tipo_um_regsce_cod",
                        "min_unt",
                        "max_unt",
                        "opz_flg",
                        "vin_id",
                        "vin_sce_des",
                        "sce_id__opz_flg",
                        "sce_id__anno_corso_ant",
                        "sche_statutario_flg",
                    )
                    s["isStatutario"] = None
                    s["AfRequired"] = obbl

                    for af in obbl:
                        if s["isStatutario"] is None:
                            s["isStatutario"] = af["sche_statutario_flg"]

                        af_obblig = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=af["sce_id"]
                        ).values(
                            "amb_id_af",
                            "anno_corso_af",
                            "ciclo_des",
                            "af_gen_des",
                            "af_id",
                            "af_gen_cod",
                            "tipo_af_des_af",
                            "ambito_des_af",
                            "sett_cod",
                            "peso",
                            "sce_id__sce_des",
                            "sce_id",
                        )

                        af["Required"] = af_obblig

                        for activity in af["Required"]:
                            list_submodules = (
                                DidatticaAttivitaFormativa.objects.filter(
                                    # ~Q(fat_part_stu_cod='GRP'),
                                    part_stu_cod__isnull=True,
                                    # af_radice_id=activity['af_id'],
                                    af_pdr_id=activity["af_id"],
                                )
                                .exclude(af_id=activity["af_id"])
                                .values(
                                    "af_id",
                                    "af_gen_cod",
                                    "des",
                                    "peso",
                                    "sett_cod",
                                    "af_gen_des_eng",
                                    "fat_part_stu_cod",
                                    "lista_lin_did_af",
                                    "part_stu_cod",
                                    "part_stu_des",
                                    "fat_part_stu_des",
                                    "ciclo_des",
                                )
                            )

                            activity["MODULES"] = list_submodules

                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=af["sce_id"]
                        ).values(
                            "sce_fil_and_id",
                            "sce_id",
                            "sce_fil_or_id",
                            "sce_fil_or_des",
                            "tipo_filtro_cod",
                            "tipo_filtro_des",
                            "tipo_corso_sce_fil_and_cod",
                            "cds_sce_fil_and_id",
                            "cds_sce_fil_and_cod",
                            "cds_sce_fil_and_nome",
                            "not_flg",
                        )

                        af["FilAnd"] = fil_and

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
                        ~Q(tipo_sce_cod__exact="O"),
                        sche_piano_id__exact=s["sche_piano_id"],
                    ).values(
                        "sce_id",
                        "sce_des",
                        "anno_corso",
                        "apt_slot_ord_num",
                        "tipo_regsce_cod",
                        "tipo_sce_cod",
                        "tipo_sce_des",
                        "tipo_regsce_des",
                        "tipo_um_regsce_cod",
                        "min_unt",
                        "max_unt",
                        "opz_flg",
                        "vin_id",
                        "vin_sce_des",
                        "sce_id__opz_flg",
                        "sce_id__anno_corso_ant",
                    )

                    verifica = (
                        Q(amb_id__isnull=False)
                        | Q(amb_id_af_regsce__isnull=False)
                        | Q(tipo_sce_cod="V")
                    )

                    s["AfChoices"] = scelte

                    for scelta in scelte:
                        if s["isStatutario"] is None:
                            s["isStatutario"] = af["sche_statutario_flg"]

                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=scelta["sce_id"]
                        ).values(
                            "sce_fil_and_id",
                            "sce_id",
                            "sce_fil_or_id",
                            "sce_fil_or_des",
                            "tipo_filtro_cod",
                            "tipo_filtro_des",
                            "cds_sce_fil_and_id",
                            "cds_sce_fil_and_cod",
                            "cds_sce_fil_and_nome",
                            "tipo_corso_sce_fil_and_cod",
                            "not_flg",
                        )

                        scelta["FilAnd"] = fil_and

                        af_scelta = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=scelta["sce_id"]
                        ).values(
                            "amb_id_af",
                            "anno_corso_af",
                            "ciclo_des",
                            "af_gen_des",
                            "af_gen_cod",
                            "af_id",
                            "tipo_af_des_af",
                            "ambito_des_af",
                            "sett_cod",
                            "peso",
                            "sce_id__sce_des",
                            "sce_id",
                        )

                        scelta["Choices"] = af_scelta

                        for activity in scelta["Choices"]:
                            list_submodules = (
                                DidatticaAttivitaFormativa.objects.filter(
                                    # ~Q(fat_part_stu_cod='GRP'),
                                    part_stu_cod__isnull=True,
                                    # af_radice_id=activity['af_id']
                                    af_pdr_id=activity["af_id"],
                                )
                                .exclude(af_id=activity["af_id"])
                                .values(
                                    "af_id",
                                    "af_gen_cod",
                                    "des",
                                    "af_gen_des_eng",
                                    "peso",
                                    "fat_part_stu_cod",
                                    "lista_lin_did_af",
                                    "part_stu_cod",
                                    "part_stu_des",
                                    "fat_part_stu_des",
                                    "ciclo_des",
                                )
                            )

                            activity["MODULES"] = list_submodules

                        if af_scelta is None:  # pragma: no cover
                            af_scelta = DidatticaPianoSceltaAf.objects.filter(
                                verifica, sce_id__exact=scelta["sce_id"]
                            ).values(
                                "amb_id_af",
                                "anno_corso_af",
                                "ciclo_des",
                                "af_gen_des",
                                "af_id",
                                "tipo_af_des_af",
                                "ambito_des_af",
                                "sett_cod",
                                "peso",
                                "sce_id__sce_des",
                                "sce_id",
                            )

                            scelta["Choices"] = af_scelta

                            for activity in scelta["Choices"]:
                                list_submodules = (
                                    DidatticaAttivitaFormativa.objects.filter(
                                        # ~Q(fat_part_stu_cod='GRP'),
                                        part_stu_cod__isnull=True,
                                        # af_radice_id=activity['af_id']
                                        af_pdr_id=activity["af_id"],
                                    )
                                    .exclude(af_id=activity["af_id"])
                                    .values(
                                        "af_id",
                                        "af_gen_cod",
                                        "des",
                                        "peso",
                                        "af_gen_des_eng",
                                        "fat_part_stu_cod",
                                        "lista_lin_did_af",
                                        "part_stu_cod",
                                        "part_stu_des",
                                        "fat_part_stu_des",
                                        "ciclo_des",
                                    )
                                )

                                activity["MODULES"] = list_submodules

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

                schede = sorted(
                    list(schede),
                    key=lambda k: (
                        k["cla_m_id"] if k["cla_m_id"] else 0,
                        -k["isStatutario"],
                        k["apt_id"] if k["apt_id"] else 0,
                    ),
                )
                q["PlanTabs"] = schede
            return query


class ServiceDidatticaAttivitaFormativa:
    @staticmethod
    def getStudyPlans(regdid_id=None):
        query = DidatticaAttivitaFormativa.objects.filter(regdid=regdid_id)
        query = (
            query.order_by("pds_regdid_id__pds_des_it")
            .values(
                "regdid_id",
                "pds_regdid_id",
                "pds_cod",
                "pds_regdid_id__pds_des_it",
                "pds_regdid_id__pds_des_eng",
            )
            .distinct()
        )
        query = list(query)
        for q in query:
            activities = (
                ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                    q["pds_regdid_id"], group=True
                )
            )
            q["StudyActivities"] = activities  # list(activities)
        return query

    @staticmethod
    def getStudyPlan(studyplanid=None):
        query = DidatticaPdsRegolamento.objects.filter(pds_regdid_id=studyplanid)
        query = query.order_by("pds_des_it").values(
            "regdid__regdid_id", "pds_regdid_id", "pds_cod", "pds_des_it", "pds_des_eng"
        )
        query = list(query)
        for q in query:
            activities = (
                ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                    q["pds_regdid_id"], group=True
                )
            )
            q["StudyActivities"] = activities  # list(activities)
        return query

    @staticmethod
    def getAttivitaFormativaByStudyPlan(studyplanid, group=False):
        if group:
            total_years = (
                DidatticaPdsRegolamento.objects.filter(pds_regdid_id=studyplanid)
                .values("regdid__cds__durata_anni")
                .first()["regdid__cds__durata_anni"]
            )
            final_query = {}
            for i in range(total_years):
                query = DidatticaAttivitaFormativa.objects.filter(
                    pds_regdid__pds_regdid_id=studyplanid,
                    af_id__isnull=False,
                    anno_corso=(i + 1),
                )
                new_query = DidatticaAttivitaFormativa.objects.none()
                for q in query:
                    if q.checkIfMainCourse():
                        new_query = (
                            new_query
                            | DidatticaAttivitaFormativa.objects.filter(af_id=q.af_id)
                        )
                final_query[i + 1] = new_query.order_by("ciclo_des").values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "af_gen_des_eng",
                    "cds__cds_id",
                    "cds__cds_cod",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "ciclo_des",
                    "peso",
                    "sett_cod",
                    "sett_des",
                    "freq_obblig_flg",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "tipo_af_des",
                    "tipo_af_cod",
                    "tipo_af_intercla_cod",
                    "tipo_af_intercla_des",
                )
            return final_query
        else:
            query = DidatticaAttivitaFormativa.objects.filter(
                pds_regdid__pds_regdid_id=studyplanid, af_id__isnull=False
            )
            new_query = DidatticaAttivitaFormativa.objects.none()
            for q in query:
                if q.checkIfMainCourse():
                    new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                        af_id=q.af_id
                    )

            return new_query.order_by("anno_corso", "ciclo_des").values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "cds__cds_cod",
                "cds__cds_id",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_cod",
                "sett_des",
                "freq_obblig_flg",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "tipo_af_des",
                "tipo_af_cod",
                "tipo_af_intercla_cod",
                "tipo_af_intercla_des",
            )

    @staticmethod
    def getAllActivities(
        language,
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
    ):
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
            if language == "it":  # pragma: no cover
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

        coperture = DidatticaCopertura.objects.filter(query_teacher_code).values(
            "af_id"
        )

        query_coperture = Q(af_id__in=coperture) | Q(af_master_id__in=coperture)

        query = (
            DidatticaAttivitaFormativa.objects.filter(
                query_department,
                query_academic_year,
                query_cds,
                query_period,
                query_ssd,
                query_teaching,
                query_course_year,
                query_coperture,
                query_teacher,
                query_cds_cod,
            )
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "sett_cod",
                "sett_des",
                "ciclo_des",
                "lista_lin_did_af",
                "aa_off_id",
                "regdid_id",
                "cds_id",
                "cds_id__cds_cod",
                "cds_id__nome_cds_it",
                "cds_id__nome_cds_eng",
                "cds_id__dip_id__dip_cod",
                "cds_id__dip_id__dip_des_it",
                "cds_id__dip_id__dip_des_eng",
                "fat_part_stu_cod",
                "fat_part_stu_des",
                "part_stu_cod",
                "part_stu_des",
                "anno_corso",
                "matricola_resp_did",
                "matricola_resp_did__nome",
                "matricola_resp_did__cognome",
                "matricola_resp_did__middle_name",
                "pds_des",
                "af_master_id",
                "af_radice_id",
            )
            .distinct()
            .order_by("des")
        )

        lista_padri = {}
        for i in query:
            lista_padri[i["af_id"]] = i["des"]

        for q in query:
            padre = lista_padri[q["af_id"]]

            if padre:
                q["Father"] = padre
            else:
                q["Father"] = None

            if q["af_gen_cod"] is None:  # pragma: no cover
                codice = None
                codice = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("af_gen_cod")

                codice = list(codice)
                if len(codice) > 0:
                    codice = codice[0]["af_gen_cod"]

                if codice:
                    q["af_gen_cod"] = codice
                else:
                    q["af_gen_cod"] = None

            if q["anno_corso"] is None:  # pragma: no cover
                anno = None
                anno = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("anno_corso")

                anno = list(anno)

                if len(anno) > 0:
                    anno = anno[0]["anno_corso"]

                if anno:
                    q["anno_corso"] = anno
                else:
                    q["anno_corso"] = None

            if q["ciclo_des"] is None:  # pragma: no cover
                semestre = None
                semestre = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("ciclo_des")

                semestre = list(semestre)

                if len(semestre) > 0:
                    semestre = semestre[0]["ciclo_des"]

                if semestre:
                    q["ciclo_des"] = semestre
                else:
                    q["ciclo_des"] = None

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
        list_submodules = (
            DidatticaAttivitaFormativa.objects.filter(
                Q(af_radice_id=af_id) | Q(af_pdr_id=af_id)
            )
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "fat_part_stu_cod",
                "lista_lin_did_af",
                "part_stu_cod",
                "part_stu_des",
                "fat_part_stu_des",
                "ciclo_des",
                "matricola_resp_did",
            )
        )

        query = (
            DidatticaAttivitaFormativa.objects.filter(af_id=af_id)
            .order_by("anno_corso", "ciclo_des")
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "cds__cds_cod",
                "cds__cds_id",
                "lista_lin_did_af",
                "pds_cod",
                "pds_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_cod",
                "sett_des",
                "freq_obblig_flg",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "tipo_af_des",
                "tipo_af_cod",
                "tipo_af_intercla_cod",
                "tipo_af_intercla_des",
                "matricola_resp_did",
                "mutuata_flg",
                "af_master_id",
                "af_radice_id",
                "af_pdr_id",
                "didatticacopertura__coper_peso",
                "part_stu_cod",
                "fat_part_stu_cod",
                "part_stu_des",
                "fat_part_stu_des",
            )
        )

        lingue = DidatticaTestiAf.objects.filter(
            tipo_testo_af_cod="LINGUA_INS", af_id=af_id
        ).values("testo_af_ita", "testo_af_eng")

        id_master = None
        mutuata_da = None
        if not query:
            raise Http404
        if query.first()["mutuata_flg"] == 1:
            id_master = query.first()["af_master_id"]
            mutuata_da = (
                DidatticaAttivitaFormativa.objects.filter(af_id=id_master)
                .values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "cds__cds_cod",
                    "cds__cds_id",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "pds_cod",
                    "pds_des",
                    "af_gen_des_eng",
                    "ciclo_des",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "didatticacopertura__coper_peso",
                )
                .first()
            )

        attivita_mutuate_da_questa = (
            DidatticaAttivitaFormativa.objects.filter(af_master_id=af_id, mutuata_flg=1)
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "ciclo_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "didatticacopertura__coper_peso",
                "cds__cds_cod",
                "cds__cds_id",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "pds_cod",
                "pds_des",
            )
        )
        radice = query.first()
        id_radice_padre = radice["af_pdr_id"]
        id_radice = radice["af_radice_id"]

        activity_root = (
            DidatticaAttivitaFormativa.objects.filter(af_id=id_radice)
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "ciclo_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "didatticacopertura__coper_peso",
                "cds__cds_cod",
                "cds__cds_id",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "pds_cod",
                "pds_des",
            )
        )
        if len(activity_root) == 0:
            activity_root = None
        else:
            activity_root = activity_root.first()

        activity_father = None

        if id_radice_padre and id_radice_padre != id_radice:  # pragma: no cover
            activity_father = (
                DidatticaAttivitaFormativa.objects.filter(af_id=id_radice_padre)
                .exclude(af_id=af_id)
                .values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "af_gen_des_eng",
                    "ciclo_des",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "didatticacopertura__coper_peso",
                    "cds__cds_cod",
                    "cds__cds_id",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "pds_cod",
                    "pds_des",
                )
            )
            if len(activity_father) == 0:
                activity_father = None
            else:
                activity_father = activity_father.first()

        copertura = DidatticaCopertura.objects.filter(af_id=af_id).values(
            "personale__id",
            "personale__id_ab",
            "personale__nome",
            "personale__cognome",
            "personale__middle_name",
            "personale__matricola",
            "fat_part_stu_cod",
            "fat_part_stu_des",
            "part_stu_cod",
            "part_stu_des",
        )

        query = list(query)

        filtered_hours = DidatticaCoperturaDettaglioOre.objects.filter(
            ~Q(coper_id__stato_coper_cod="R"), coper_id__af_id=af_id
        ).values(
            "tipo_att_did_cod",
            "ore",
            "coper_id__personale_id__id_ab",
            "coper_id__personale_id__matricola",
            "coper_id__personale_id__nome",
            "coper_id__personale_id__cognome",
            "coper_id__personale_id__middle_name",
            "coper_id__personale_id__flg_cessato",
            "coper_id",
        )

        append_email_addresses(filtered_hours, "coper_id__personale_id__id_ab")
        filtered_hours = list(filtered_hours)

        for hour in filtered_hours:
            for hour2 in filtered_hours:
                if (
                    hour["tipo_att_did_cod"] == hour2["tipo_att_did_cod"]
                    and hour["coper_id__personale_id__matricola"]
                    == hour2["coper_id__personale_id__matricola"]
                    and hour["coper_id"] != hour2["coper_id"]
                ):  # pragma: no cover
                    hour["ore"] = hour["ore"] + hour2["ore"]
                    filtered_hours.remove(hour2)

        query[0]["Hours"] = filtered_hours

        query[0]["Modalities"] = DidatticaAttivitaFormativaModalita.objects.filter(
            af_id=af_id
        ).values("mod_did_af_id", "mod_did_cod", "mod_did_des")

        query[0]["LANGUAGEIT"] = None
        query[0]["LANGUAGEEN"] = None

        for lingua in lingue:  # pragma: no cover
            query[0]["LANGUAGEIT"] = lingua["testo_af_ita"]
            query[0]["LANGUAGEEN"] = lingua["testo_af_eng"]

        query[0]["BorrowedFrom"] = mutuata_da
        query[0]["ActivitiesBorrowedFromThis"] = attivita_mutuate_da_questa

        query[0]["ActivityRoot"] = activity_root

        query[0]["ActivityFather"] = activity_father

        query[0]["StudyActivityTeacherID"] = None
        query[0]["StudyActivityTeacherName"] = None

        query[0]["PartitionCod"] = None
        query[0]["PartitionDescription"] = None
        query[0]["ExtendedPartitionCod"] = None
        query[0]["ExtendedPartitionDescription"] = None

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

        texts_af = DidatticaTestiAf.objects.filter(af_id=af_id).values(
            "tipo_testo_af_cod", "testo_af_ita", "testo_af_eng"
        )

        query[0]["MODULES"] = list()
        allowed = []
        for i in range(len(list_submodules)):
            copertura = (
                DidatticaCopertura.objects.filter(
                    af_id=list_submodules[i]["af_id"],
                    personale__matricola=list_submodules[i]["matricola_resp_did"],
                )
                .values(
                    "fat_part_stu_cod",
                    "fat_part_stu_des",
                    "part_stu_cod",
                    "part_stu_des",
                )
                .first()
            )

            groups = DidatticaAttivitaFormativa.objects.filter(
                af_pdr_id=list_submodules[i]["af_id"], fat_part_stu_cod="GRP"
            ).values(
                "af_id",
                "af_gen_cod",
                "des",
                "fat_part_stu_cod",
                "fat_part_stu_des",
                "part_stu_cod",
                "part_stu_des",
                "af_gen_des_eng",
            )

            groups_serialize = []
            for j in range(len(groups)):
                groups_serialize.append(
                    {
                        "StudyActivityID": groups[j]["af_id"],
                        "StudyActivityCod": groups[j]["af_gen_cod"],
                        "StudyActivityName": groups[j]["des"]
                        if language == "it" or groups[j]["af_gen_des_eng"] is None
                        else groups[j]["af_gen_des_eng"],
                        "StudyActivityPartitionCod": groups[j]["part_stu_cod"],
                        "StudyActivityPartitionDescription": groups[j]["part_stu_des"],
                        "StudyActivityExtendedPartitionCod": groups[j][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": groups[j][
                            "fat_part_stu_des"
                        ],
                    }
                )
            groups = groups.values("af_id")
            groups = list(groups)
            for g in groups:
                allowed.append(g["af_id"])

            if list_submodules[i]["af_id"] not in allowed:
                query[0]["MODULES"].append(
                    {
                        "StudyActivityID": list_submodules[i]["af_id"],
                        "StudyActivityCod": list_submodules[i]["af_gen_cod"],
                        "StudyActivityName": list_submodules[i]["des"]
                        if language == "it"
                        or list_submodules[i]["af_gen_des_eng"] is None
                        else list_submodules[i]["af_gen_des_eng"],
                        "StudyActivitySemester": list_submodules[i]["ciclo_des"],
                        "StudyActivityPartitionCod": list_submodules[i]["part_stu_cod"],
                        "StudyActivityPartitionDescription": list_submodules[i][
                            "part_stu_des"
                        ],
                        "StudyActivityExtendedPartitionCod": list_submodules[i][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": list_submodules[i][
                            "fat_part_stu_des"
                        ],
                        "StudyActivityGroups": groups_serialize,
                    }
                )
            elif (
                list_submodules[i]["af_id"] not in allowed
                and list_submodules[i]["fat_part_stu_cod"] == "GRP"
            ):  # pragma: no cover
                query[0]["MODULES"].append(
                    {
                        "StudyActivityID": list_submodules[i]["af_id"],
                        "StudyActivityCod": list_submodules[i]["af_gen_cod"],
                        "StudyActivityName": list_submodules[i]["des"]
                        if language == "it"
                        or list_submodules[i]["af_gen_des_eng"] is None
                        else list_submodules[i]["af_gen_des_eng"],
                        "StudyActivitySemester": list_submodules[i]["ciclo_des"],
                        "StudyActivityPartitionCod": list_submodules[i]["part_stu_cod"],
                        "StudyActivityPartitionDescription": list_submodules[i][
                            "part_stu_des"
                        ],
                        "StudyActivityExtendedPartitionCod": list_submodules[i][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": list_submodules[i][
                            "fat_part_stu_des"
                        ],
                    }
                )

        query[0]["StudyActivityContent"] = None
        query[0]["StudyActivityProgram"] = None
        query[0]["StudyActivityLearningOutcomes"] = None
        query[0]["StudyActivityMethodology"] = None
        query[0]["StudyActivityEvaluation"] = None
        query[0]["StudyActivityTextbooks"] = None
        query[0]["StudyActivityWorkload"] = None
        query[0]["StudyActivityElearningLink"] = None
        query[0]["StudyActivityElearningInfo"] = None
        query[0]["StudyActivityPrerequisites"] = None
        query[0]["StudyActivityDevelopmentGoal"] = None

        dict_activity = {
            "CONTENUTI": "StudyActivityContent",
            "PROGR_EST": "StudyActivityProgram",
            "OBIETT_FORM": "StudyActivityLearningOutcomes",
            "METODI_DID": "StudyActivityMethodology",
            "MOD_VER_APPR": "StudyActivityEvaluation",
            "TESTI_RIF": "StudyActivityTextbooks",
            "STIMA_CAR_LAV": "StudyActivityWorkload",
            "PREREQ": "StudyActivityPrerequisites",
            "LINK_TEAMS": "StudyActivityElearningLink",
            "CODICE_TEAMS": "StudyActivityElearningInfo",
            "OB_SVIL_SOS": "StudyActivityDevelopmentGoal",
            "PROPEDE": None,
            "LINGUA_INS": None,
            "PAG_WEB_DOC": None,
            "ALTRO": None,
        }

        for text in texts_af:
            query[0][dict_activity[text["tipo_testo_af_cod"]]] = (
                text["testo_af_ita"]
                if language == "it" or text["testo_af_eng"] is None
                else text["testo_af_eng"]
            )
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
