from django.db.models import Q
from patents.models import BrevettoDatiBase, BrevettoInventori


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
                brevettoinventori__matricola_inventore__cd_uo_aff_org=structure
            )

        query = (
            BrevettoDatiBase.objects.filter(
                query_search, query_techarea, query_structure, query_is_active
            )
            .values(
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
                "is_active",
            )
            .distinct()
        )

        for q in query:
            inventori = (
                BrevettoInventori.objects.filter(id_brevetto=q["id"])
                .values(
                    "matricola_inventore",
                    "cognomenome_origine",
                )
                .distinct()
            )

            if len(inventori) == 0:
                q["Inventori"] = []
            else:
                q["Inventori"] = inventori

        return query

    @staticmethod
    def getPatentDetail(patentid):
        query = BrevettoDatiBase.objects.filter(id=patentid, is_active=True).values(
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
            "is_active",
        )

        for q in query:
            inventori = (
                BrevettoInventori.objects.filter(id_brevetto=q["id"])
                .values(
                    "matricola_inventore",
                    "cognomenome_origine",
                )
                .distinct()
            )

            if len(inventori) == 0:
                q["Inventori"] = []
            else:
                q["Inventori"] = inventori

        return query
