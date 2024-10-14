from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaFilAnd,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSche,
)
from django.db.models import Case, CharField, F, Prefetch, Q, Value, When

from cds_websites.models import (
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliReg,
    SitoWebCdsTopicArticoliRegAltriDati,
)


class ServiceSitoWebCds:
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
