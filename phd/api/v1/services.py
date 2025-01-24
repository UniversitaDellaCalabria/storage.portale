import operator
from functools import reduce

from django.db.models import Q
from phd.models import (
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaAltriDocenti,
    DidatticaDottoratoAttivitaFormativaDocente,
    DidatticaDottoratoAttivitaFormativaTipologia,
    DidatticaDottoratoCds,
)


def build_filter_chain(params_dict, query_params, *args):
    return reduce(
        operator.and_,
        [
            Q(**{v: query_params.get(k)})
            for (k, v) in params_dict.items()
            if query_params.get(k)
        ]
        + list(args),
        Q(),
    )


class ServiceDottorato:
    @staticmethod
    def getPhd(query_params):
        params_to_query_field = {
            "year": "idesse3_ddr__aa_regdid_id__exact",
            "yearFrom": "idesse3_ddr__aa_regdid_id__gte",
            "yearTo": "idesse3_ddr__aa_regdid_id__lte",
            "regdid": "idesse3_ddr__regdid_id_esse3__exact",
            "departmentid": "dip_cod__dip_cod__exact",
            "cdscod": "cds_cod__exact",
            "pdscod": "idesse3_ddpds__pds_cod__exact",
            "cycle": "idesse3_ddr__num_ciclo",
        }

        query = DidatticaDottoratoCds.objects.filter(
            build_filter_chain(params_to_query_field, query_params)
        )

        return query.order_by(
            "idesse3_ddr__aa_regdid_id",
            "dip_cod__dip_cod",
            "cds_cod",
            "idesse3_ddpds__pds_cod",
        ).values(
            "dip_cod__dip_id",
            "dip_cod__dip_cod",
            "dip_cod__dip_des_it",
            "dip_cod__dip_des_eng",
            "cds_cod",
            "cdsord_des",
            "tipo_corso_cod",
            "tipo_corso_des",
            "durata_anni",
            "valore_min",
            "idesse3_ddr__aa_regdid_id",
            "idesse3_ddr__regdid_cod",
            "idesse3_ddr__frequenza_obbligatoria",
            "idesse3_ddr__num_ciclo",
            "idesse3_ddpds__pds_cod",
            "idesse3_ddpds__pds_des",
            "idesse3_ddr__regdid_id_esse3",
        )

    @staticmethod
    def getPhdActivities(
        search=None,
        structure=None,
        phd=None,
        ssd=None,
        teacher=None,
        cycle=None,
        typology=None,
    ):
        query_search = Q()
        query_structure = Q()
        query_phd = Q()
        query_ssd = Q()
        query_cycle = Q()
        query_typology = Q()

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
        if typology:
            query_typology = Q(tipologia=typology)

        query = DidatticaDottoratoAttivitaFormativa.objects.filter(
            query_search,
            query_structure,
            query_phd,
            query_ssd,
            query_cycle,
            query_typology,
        ).values(
            "id",
            "nome_af",
            "ssd",
            "numero_ore",
            "cfu",
            "tipo_af",
            "tipologia",
            "rif_dottorato",
            "ciclo",
            "struttura_proponente",
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
            "visualizza_orario",
        )
        for q in query:
            q["tipologia_obj"] = (
                DidatticaDottoratoAttivitaFormativaTipologia.objects.filter(
                    pk=q["tipologia"]
                ).first()
            )

            main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
                didattica_dottorato_attivita_formativa=q["id"]
            ).values("matricola", "cognome_nome_origine")

            if len(main_teachers) == 0:
                q["MainTeachers"] = []
            else:
                q["MainTeachers"] = main_teachers

            other_teachers = (
                DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
                    didattica_dottorato_attivita_formativa=q["id"]
                ).values("matricola", "cognome_nome_origine")
            )

            if len(other_teachers) == 0:
                q["OtherTeachers"] = []
            else:
                q["OtherTeachers"] = other_teachers

        if teacher:
            res = []
            for q in query:
                for i in q["MainTeachers"]:
                    if (
                        i["cognome_nome_origine"] is not None
                        and (i["cognome_nome_origine"].lower()).startswith(
                            teacher.lower()
                        )
                        and q not in res
                    ):
                        res.append(q)
                        continue
                for t in q["OtherTeachers"]:
                    if (
                        t["cognome_nome_origine"] is not None
                        and (t["cognome_nome_origine"].lower()).startswith(
                            teacher.lower()
                        )
                        and q not in res
                    ):
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
            "tipologia",
            "rif_dottorato",
            "ciclo",
            "struttura_proponente",
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
            "visualizza_orario",
        )
        query_filter_teachers = ~Q(cognome_nome_origine="....DOCENTE NON IN ELENCO")
        for q in query:
            q["tipologia_obj"] = (
                DidatticaDottoratoAttivitaFormativaTipologia.objects.filter(
                    pk=q["tipologia"]
                ).first()
            )

            main_teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
                query_filter_teachers, didattica_dottorato_attivita_formativa=q["id"]
            ).values("matricola", "cognome_nome_origine")

            if len(main_teachers) == 0:
                q["MainTeachers"] = []
            else:
                q["MainTeachers"] = main_teachers

            other_teachers = (
                DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
                    didattica_dottorato_attivita_formativa=q["id"],
                    cognome_nome_origine__isnull=False,
                ).values("matricola", "cognome_nome_origine")
            )

            if len(other_teachers) == 0:
                q["OtherTeachers"] = []
            else:
                q["OtherTeachers"] = other_teachers

        return query

    @staticmethod
    def getRefPhd():
        query = (
            DidatticaDottoratoAttivitaFormativa.objects.filter(
                rif_dottorato__isnull=False
            )
            .exclude(rif_dottorato__exact="")
            .order_by("rif_dottorato")
            .values("rif_dottorato")
            .distinct()
        )
        return list(query)

    @staticmethod
    def getPhdSsdList():  # pragma: no cover
        query = (
            DidatticaDottoratoAttivitaFormativa.objects.filter(ssd__isnull=False)
            .order_by("ssd")
            .values("ssd")
            .distinct()
        )
        return list(query)

    @staticmethod
    def getPhdActivityTypeList():  # pragma: no cover
        query = (
            DidatticaDottoratoAttivitaFormativa.objects.filter(tipo_af__isnull=False)
            .order_by("tipo_af")
            .values("tipo_af")
            .distinct()
        )
        return list(query)

    @staticmethod
    def getPhdActivityTypologies():  # pragma: no cover
        query = DidatticaDottoratoAttivitaFormativaTipologia.objects.all()
        return list(query)

    @staticmethod
    def getRefStructures():  # pragma:no cover
        query = (
            DidatticaDottoratoAttivitaFormativa.objects.filter(
                struttura_proponente_origine__isnull=False
            )
            .exclude(struttura_proponente_origine__exact="")
            .order_by("struttura_proponente_origine")
            .values("struttura_proponente_origine")
            .distinct()
        )
        return list(query)
