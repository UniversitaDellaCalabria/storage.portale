from django.db.models import Q
from projects.models import (
    ProgettoAmbitoTerritoriale,
    ProgettoDatiBase,
    ProgettoResponsabileScientifico,
    ProgettoRicercatore,
    ProgettoTipologiaProgramma,
)


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
        only_active=True,
    ):
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
                q_nome = (
                    Q(titolo__icontains=k)
                    | Q(area_tecnologica__descr_area_ita__icontains=k)
                    | Q(uo__denominazione__icontains=k)
                    | Q(anno_avvio__icontains=k)
                    | Q(ambito_territoriale__ambito_territoriale__icontains=k)
                )
                query_search &= q_nome
        if techarea:
            query_techarea = Q(area_tecnologica=techarea)
        if infrastructure:
            query_infrastructure = Q(uo=infrastructure)
        if programtype:
            programtype = programtype.split(",")
            query_programtype = Q(tipologia_programma__in=programtype)
        if territorialscope:
            query_territorialscope = Q(ambito_territoriale=territorialscope)
        if notprogramtype:
            notprogramtype = notprogramtype.split(",")
            query_notprogramtype = ~Q(tipologia_programma__in=notprogramtype)
        if year:
            query_year = Q(anno_avvio=year)

        query = (
            ProgettoDatiBase.objects.filter(
                query_search,
                query_techarea,
                query_infrastructure,
                query_territorialscope,
                query_notprogramtype,
                query_programtype,
                query_year,
                query_is_active,
            )
            .values(
                "id",
                "ambito_territoriale__id",
                "ambito_territoriale__ambito_territoriale",
                "tipologia_programma__id",
                "tipologia_programma__nome_programma",
                "titolo",
                "anno_avvio",
                "uo",
                "uo__denominazione",
                "descr_breve",
                "url_immagine",
                "url_sito_web",
                "abstract_ita",
                "abstract_eng",
                "area_tecnologica",
                "area_tecnologica__descr_area_ita",
                "area_tecnologica__descr_area_eng",
                "is_active",
            )
            .distinct()
            .order_by(
                "ordinamento",
                "-anno_avvio",
                "ambito_territoriale__ambito_territoriale",
            )
        )

        for q in query:
            responsabili = ProgettoResponsabileScientifico.objects.filter(
                progetto=q["id"]
            ).values(
                "matricola",
                "nome_origine",
            )
            ricercatori = ProgettoRicercatore.objects.filter(
                progetto=q["id"]
            ).values(
                "matricola",
                "nome_origine",
            )
            if len(responsabili) == 0:
                q["Responsabili"] = []
            else:
                q["Responsabili"] = responsabili

            if len(ricercatori) == 0:
                q["Ricercatori"] = []
            else:
                q["Ricercatori"] = ricercatori

        return query

    @staticmethod
    def getProjectDetail(projectid):
        query = (
            ProgettoDatiBase.objects.filter(id=projectid, is_active=True)
            .values(
                "id",
                "ambito_territoriale__id",
                "ambito_territoriale__ambito_territoriale",
                "tipologia_programma__id",
                "tipologia_programma__nome_programma",
                "titolo",
                "anno_avvio",
                "uo",
                "uo__denominazione",
                "descr_breve",
                "url_immagine",
                "url_sito_web",
                "abstract_ita",
                "abstract_eng",
                "area_tecnologica",
                "area_tecnologica__descr_area_ita",
                "area_tecnologica__descr_area_eng",
                "is_active",
            )
            .distinct()
        )

        for q in query:
            responsabili = ProgettoResponsabileScientifico.objects.filter(
                progetto=q["id"]
            ).values(
                "matricola",
                "nome_origine",
            )
            ricercatori = ProgettoRicercatore.objects.filter(
                progetto=q["id"]
            ).values(
                "matricola",
                "nome_origine",
            )
            if len(responsabili) == 0:
                q["Responsabili"] = []
            else:
                q["Responsabili"] = responsabili

            if len(ricercatori) == 0:
                q["Ricercatori"] = []
            else:
                q["Ricercatori"] = ricercatori

        return query

    @staticmethod
    def getTerritorialScopes():
        query = ProgettoAmbitoTerritoriale.objects.values(
            "id", "ambito_territoriale"
        ).distinct()

        return query

    @staticmethod
    def getProgramTypes():
        query = (
            ProgettoTipologiaProgramma.objects.values("id", "nome_programma")
            .order_by("nome_programma")
            .distinct()
        )

        return query

    @staticmethod
    def getProjectInfrastructures():
        query = (
            ProgettoDatiBase.objects.values(
                "uo",
                "uo__denominazione",
            )
            .distinct()
            .order_by("uo__denominazione")
        )
        query = list(query)
        for q in query:
            if q["uo"] is None:
                query.remove(q)
        return query
