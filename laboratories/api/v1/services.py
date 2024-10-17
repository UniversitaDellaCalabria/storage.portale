from django.db.models import Q
from addressbook.utils import append_email_addresses, get_personale_matricola
from laboratories.models import (
    LaboratorioAltriDipartimenti,
    LaboratorioAttivita,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioInfrastruttura,
    LaboratorioPersonaleRicerca,
    LaboratorioPersonaleTecnico,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)


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
        scope,
        is_active=True,
    ):
        if teacher:
            teacher = get_personale_matricola(teacher)

        query_search = Q()
        query_ambito = Q()
        query_dip = Q()
        query_erc1 = Q()
        query_infrastructure = Q()
        query_is_active = Q(visibile=True) if is_active else Q()

        if search:
            for k in search.split(" "):
                q_search = Q(nome_laboratorio__icontains=k)
                if language == "it":
                    q_search |= (
                        Q(finalita_ricerca_it__icontains=k)
                        | Q(finalita_didattica_it__icontains=k)
                        | Q(finalita_servizi_it__icontains=k)
                    )
                else:
                    q_search |= (
                        Q(finalita_ricerca_en__icontains=k)
                        | Q(finalita_didattica_en__icontains=k)
                        | Q(finalita_servizi_en__icontains=k)
                    )
                query_search &= q_search
        if ambito:
            query_ambito = Q(ambito__exact=ambito)
        if dip:
            query_dip = Q(dipartimento_riferimento__dip_cod__exact=dip)
            query_dip |= Q(laboratorioaltridipartimenti__didattica_dipartimento__dip_cod=dip)
        if erc1:
            erc1_allowed = erc1.split(",")
            query_erc1 = Q(
                laboratoriodatierc1__ricerca_erc1__cod_erc1__in=erc1_allowed
            )
        if infrastructure:
            query_infrastructure = Q(infrastruttura_riferimento__id=infrastructure)

        query = (
            LaboratorioDatiBase.objects.filter(
                query_search,
                query_ambito,
                query_dip,
                query_erc1,
                query_infrastructure,
                query_is_active,
            )
            .values(
                "id",
                "nome_laboratorio",
                "ambito",
                "dipartimento_riferimento_nome",
                "dipartimento_riferimento__dip_id",
                "dipartimento_riferimento__dip_cod",
                "sede_dimensione",
                "responsabile_scientifico",
                "matricola_responsabile_scientifico",
                "laboratorio_interdipartimentale",
                "finalita_servizi_it",
                "finalita_servizi_en",
                "finalita_ricerca_it",
                "finalita_ricerca_en",
                "finalita_didattica_en",
                "finalita_didattica_it",
                "infrastruttura_riferimento__id",
                "infrastruttura_riferimento__descrizione",
                "acronimo",
                "nome_file_logo",
                "visibile",
            )
            .distinct()
        )

        for q in query:
            if q["dipartimento_riferimento_nome"] is not None:
                temp = q["dipartimento_riferimento_nome"].rsplit(",", 1)

                if len(temp) > 1:
                    q["dipartimento_riferimento_nome"] = temp[0] + ", " + temp[1]
                else:
                    q["dipartimento_riferimento_nome"] = temp[0]

        for q in query:
            personale_ricerca = LaboratorioPersonaleRicerca.objects.filter(
                laboratorio_dati_base__id=q["id"]
            ).values(
                "matricola_personale_ricerca__matricola",
                "matricola_personale_ricerca__nome",
                "matricola_personale_ricerca__cognome",
                "matricola_personale_ricerca__middle_name",
            )
            personale_tecnico = LaboratorioPersonaleTecnico.objects.filter(
                laboratorio_dati_base__id=q["id"]
            ).values(
                "matricola_personale_tecnico__matricola",
                "matricola_personale_tecnico__nome",
                "matricola_personale_tecnico__cognome",
                "matricola_personale_tecnico__middle_name",
                "ruolo",
            )
            finalita = (
                LaboratorioAttivita.objects.filter(laboratorio_dati_base=q["id"])
                .values(
                    "tipologia_attivita__id", "tipologia_attivita__descrizione"
                )
                .distinct()
            )

            personale_tecnico = list(personale_tecnico)
            personale_ricerca = list(personale_ricerca)

            for p in personale_tecnico:  # pragma: no cover
                if (
                    q["matricola_responsabile_scientifico"]
                    == p["matricola_personale_tecnico__matricola"]
                ):
                    personale_tecnico.remove(p)

            for p in personale_ricerca:  # pragma: no cover
                if (
                    q["matricola_responsabile_scientifico"]
                    == p["matricola_personale_ricerca__matricola"]
                ):
                    personale_ricerca.remove(p)

            q["TechPersonnel"] = personale_tecnico
            q["ResearchPersonnel"] = personale_ricerca
            q["Scopes"] = finalita

            if q["laboratorio_interdipartimentale"] == "SI":
                other_dep = (
                    LaboratorioAltriDipartimenti.objects.filter(
                        laboratorio_dati_base=q["id"]
                    )
                    .values(
                        "didattica_dipartimento__dip_cod", "didattica_dipartimento__dip_des_it", "didattica_dipartimento__dip_des_eng"
                    )
                    .distinct()
                )
                q["ExtraDepartments"] = (
                    other_dep.order_by("didattica_dipartimento__dip_des_it")
                    if language == "it"
                    else other_dep.order_by("didattica_dipartimento__dip_des_eng")
                )
            else:
                q["ExtraDepartments"] = []

        if teacher and scope:
            res = []
            res1 = []
            if scope:
                for q in query:
                    for s in q["Scopes"]:
                        if str(s["tipologia_attivita__id"]) == scope:
                            res.append(q)
            if teacher:
                for q in query:
                    if teacher == q["matricola_responsabile_scientifico"]:
                        res1.append(q)
                        continue
                    for i in q["TechPersonnel"]:
                        if teacher == i["matricola_personale_tecnico__matricola"]:
                            res1.append(q)
                            continue
                    for t in q["ResearchPersonnel"]:
                        if teacher == t["matricola_personale_ricerca__matricola"]:
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
                    for s in q["Scopes"]:
                        if str(s["tipologia_attivita__id"]) == scope:
                            res.append(q)
            if teacher:
                for q in query:
                    if (
                        teacher == q["matricola_responsabile_scientifico"]
                        and q not in res
                    ):
                        res.append(q)
                        continue
                    for i in q["TechPersonnel"]:
                        if (
                            teacher == i["matricola_personale_tecnico__matricola"]
                            and q not in res
                        ):
                            res.append(q)
                            continue
                    for t in q["ResearchPersonnel"]:
                        if (
                            teacher == t["matricola_personale_ricerca__matricola"]
                            and q not in res
                        ):
                            res.append(q)
            return res
        return query

    @staticmethod
    def getLaboratory(language, laboratoryid, is_active=True):
        query_is_active = Q(visibile=True) if is_active else Q()
        query = LaboratorioDatiBase.objects.filter(
            Q(id__exact=laboratoryid), query_is_active
        ).values(
            "id",
            "referente_compilazione",
            "matricola_referente_compilazione",
            "nome_laboratorio",
            "acronimo",
            "nome_file_logo",
            "dipartimento_riferimento__dip_id",
            "dipartimento_riferimento__dip_cod",
            "dipartimento_riferimento__dip_des_it",
            "dipartimento_riferimento__dip_des_eng",
            "infrastruttura_riferimento__id",
            "infrastruttura_riferimento__descrizione",
            "ambito",
            "finalita_servizi_it",
            "finalita_servizi_en",
            "finalita_ricerca_it",
            "finalita_ricerca_en",
            "finalita_didattica_en",
            "finalita_didattica_it",
            "responsabile_scientifico",
            "matricola_responsabile_scientifico",
            "matricola_responsabile_scientifico__id_ab",
            "laboratorio_interdipartimentale",
            "sito_web",
            "strumentazione_descrizione",
            "visibile",
        )
        append_email_addresses(query, "matricola_responsabile_scientifico__id_ab")

        finalita = (
            LaboratorioAttivita.objects.filter(laboratorio_dati_base=laboratoryid)
            .values("tipologia_attivita__id", "tipologia_attivita__descrizione")
            .distinct()
        )

        erc1 = (
            LaboratorioDatiErc1.objects.filter(laboratorio_dati_base=laboratoryid)
            .values(
                "ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                "ricerca_erc1__ricerca_erc0_cod__description",
                "ricerca_erc1__ricerca_erc0_cod__description_en",
            )
            .distinct()
        )

        query = list(query)

        for q in erc1:
            q["Erc1"] = (
                LaboratorioDatiErc1.objects.filter(laboratorio_dati_base=laboratoryid)
                .filter(
                    ricerca_erc1__ricerca_erc0_cod=q[
                        "ricerca_erc1__ricerca_erc0_cod__erc0_cod"
                    ]
                )
                .values(
                    "ricerca_erc1__id",
                    "ricerca_erc1__cod_erc1",
                    "ricerca_erc1__descrizione",
                )
                .distinct()
            )

        personale_ricerca = LaboratorioPersonaleRicerca.objects.filter(
            laboratorio_dati_base__id=laboratoryid
        ).values(
            "matricola_personale_ricerca__id_ab",
            "matricola_personale_ricerca__matricola",
            "matricola_personale_ricerca__nome",
            "matricola_personale_ricerca__cognome",
            "matricola_personale_ricerca__middle_name",
        )
        append_email_addresses(personale_ricerca, "matricola_personale_ricerca__id_ab")

        personale_tecnico = LaboratorioPersonaleTecnico.objects.filter(
            laboratorio_dati_base__id=laboratoryid
        ).values(
            "matricola_personale_tecnico__id_ab",
            "matricola_personale_tecnico__matricola",
            "matricola_personale_tecnico__nome",
            "matricola_personale_tecnico__cognome",
            "matricola_personale_tecnico__middle_name",
            "ruolo",
        )
        append_email_addresses(personale_tecnico, "matricola_personale_tecnico__id_ab")

        servizi_offerti = LaboratorioServiziOfferti.objects.filter(
            laboratorio_dati_base__id=laboratoryid
        ).values("nome_servizio", "descrizione_servizio")
        ubicazione = LaboratorioUbicazione.objects.filter(
            laboratorio_dati_base__id=laboratoryid
        ).values("edificio", "piano", "note")

        other_dep = (
            LaboratorioAltriDipartimenti.objects.filter(
                laboratorio_dati_base=laboratoryid
            )
            .values("didattica_dipartimento__dip_cod", "didattica_dipartimento__dip_des_it", "didattica_dipartimento__dip_des_eng")
            .distinct()
        )
        query = list(query)
        for q in query:
            q["Scopes"] = finalita
            q["LaboratoryErc1"] = erc1
            q["ResearchPersonnel"] = personale_ricerca
            q["TechPersonnel"] = personale_tecnico
            q["OfferedServices"] = servizi_offerti
            if len(ubicazione) > 0:
                q["Location"] = ubicazione.first()
            else:
                q["Location"] = None

            if q["laboratorio_interdipartimentale"] == "SI":
                q["ExtraDepartments"] = (
                    other_dep.order_by("didattica_dipartimento__dip_des_it")
                    if language == "it"
                    else other_dep.order_by("didattica_dipartimento__dip_des_eng")
                )
            else:
                q["ExtraDepartments"] = []
        return query

    @staticmethod
    def getLaboratoriesAreasList():
        return (
            LaboratorioDatiBase.objects.all()
            .values("ambito")
            .distinct()
            .order_by("ambito")
        )

    @staticmethod
    def getScopes():
        return (
            LaboratorioTipologiaAttivita.objects.all()
            .values("id", "descrizione")
            .distinct()
            .order_by("id")
        )

    @staticmethod
    def getInfrastructures():
        return (
            LaboratorioInfrastruttura.objects.all()
            .values("id", "descrizione")
            .distinct()
        )

    @staticmethod
    def getErc1List():
        query = RicercaErc0.objects.values(
            "erc0_cod", "description", "description_en"
        ).distinct()

        query = list(query)

        for q in query:
            q["Erc1"] = (
                RicercaErc1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                .values("id", "cod_erc1", "descrizione")
                .distinct()
            )
        return query

    @staticmethod
    def getErc0List():
        query = (
            RicercaErc0.objects.all()
            .values("erc0_cod", "description", "description_en")
            .distinct()
        )

        return query

    @staticmethod
    def getErc2List():
        query = ServiceLaboratorio.getErc1List()

        for q in query:
            for i in range(len(q["Erc1"])):
                q["Erc1"][i]["Erc2"] = (
                    RicercaErc2.objects.filter(ricerca_erc1_id=q["Erc1"][i]["id"])
                    .values("cod_erc2", "descrizione")
                    .distinct()
                )
        return query

    @staticmethod
    def getAster1List():
        query = RicercaErc0.objects.values("erc0_cod", "description", "description_en")

        for q in query:
            q["Aster1"] = []

            q["Aster1"] = (
                RicercaAster1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                .values("id", "descrizione")
                .distinct()
            )

            query = list(query)

            if len(q["Aster1"]) == 0:
                query.remove(q)

        return query

    @staticmethod
    def getAster2List():
        query = ServiceLaboratorio.getAster1List()

        for q in query:
            for i in range(len(q["Aster1"])):
                q["Aster1"][i]["Aster2"] = (
                    RicercaAster2.objects.filter(ricerca_aster1_id=q["Aster1"][i]["id"])
                    .values("id", "descrizione")
                    .distinct()
                )

        return query
