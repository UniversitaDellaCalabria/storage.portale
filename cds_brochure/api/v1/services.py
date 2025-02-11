from cds.models import DidatticaCdsLingua, DidatticaRegolamentoAltriDati
from django.db.models import Prefetch, Q

from cds.models import DidatticaCdsLingua
from cds_brochure.models import (
    CdsBrochure,
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider,
)


class ServiceCdsBrochure:
    @staticmethod
    def getCdsBrochures(query_params):
        search = query_params.get("search", "")
        coursetype = query_params.get("coursetype", "")
        cdslanguage = query_params.get("cdslanguage", "")

        query_search = Q()

        if search:
            for k in search.split(" "):
                query_search &= Q(cds__nome_cds_it__icontains=k)
        if coursetype:
            query_search &= Q(cds__tipo_corso_cod__in=coursetype.split(","))
        if cdslanguage:
            query_search &= Q(cds__didatticacdslingua__iso6392_cod=cdslanguage)

        query = (
            CdsBrochure.objects.filter(query_search)
            .select_related("cds")
            .prefetch_related(
                Prefetch(
                    "cds__didatticacdslingua",
                    queryset=DidatticaCdsLingua.objects.only("iso6392_cod"),
                    to_attr="languages"
                )
            )
        )
        return query

    @staticmethod
    def getCdsBrochure(cds_cod):
        query = (
            CdsBrochure.objects.filter(cds__cds_cod=cds_cod)
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
                CdsBrochureExStudenti.objects.filter(cds_brochure=q["id"])
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
                CdsBrochureLink.objects.filter(cds_brochure=q["id"])
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
                CdsBrochureSlider.objects.filter(cds_brochure=q["id"])
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
