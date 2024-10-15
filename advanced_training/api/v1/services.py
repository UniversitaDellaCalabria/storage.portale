from django.db.models import Q

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


class ServiceAltaFormazione:
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
            query_department = Q(id_dipartimento_riferimento__dip_cod=department)
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
                "id_dipartimento_riferimento",
                "id_dipartimento_riferimento__dip_cod",
                "id_dipartimento_riferimento__dip_des_it",
                "id_dipartimento_riferimento__dip_des_eng",
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
                "id_dipartimento_riferimento",
                "id_dipartimento_riferimento__dip_cod",
                "id_dipartimento_riferimento__dip_des_it",
                "id_dipartimento_riferimento__dip_des_eng",
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
