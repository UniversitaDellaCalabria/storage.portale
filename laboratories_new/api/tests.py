from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from laboratories_new.util_test import ApiLaboratoriesUnitTestMethods as U


def make_person(n, **kw):
    """Persona con id, id_ab, matricola e cod_fis univoci."""
    data = {
        "id": n,
        "id_ab": n,
        "matricola": f"11111{n}",
        "nome": f"Nome{n}",
        "cognome": f"Cognome{n}",
        "cod_fis": f"CF{n}",
    }
    data.update(kw)
    return U.create_personale(**data)


def make_dipartimenti():
    dip1 = U.create_didatticaDipartimento()
    dip2 = U.create_didatticaDipartimento(
        dip_id=2,
        dip_cod="2",
        dip_des_it="Lettere e filosofia",
        dip_des_eng="Philosophy",
    )
    return dip1, dip2


class LaboratoriesBaseTest(TestCase):
    def setUp(self):
        self.req = Client()

    def get_results(self, url, data=None):
        res = self.req.get(url, data=data or {})
        self.assertEqual(res.status_code, 200)
        return res.json()["results"]


class LaboratoriesListTest(LaboratoriesBaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("laboratories:apiv2:laboratories-list")

    def test_list_only_visible_for_anonymous(self):
        U.create_laboratorioDatiBase(nome_laboratorio="V1")
        U.create_laboratorioDatiBase(nome_laboratorio="V2")
        U.create_laboratorioDatiBase(nome_laboratorio="HIDDEN", visibile=False)
        results = self.get_results(self.url)
        self.assertEqual(len(results), 2)
        self.assertNotIn("HIDDEN", [r["name"] for r in results])

    def test_list_fields(self):
        dip1, dip2 = make_dipartimenti()
        director = make_person(1)
        researcher = make_person(2)
        tech = make_person(3)

        ambito = U.create_ambitoS3()
        infra = U.create_laboratorioInfrastruttura(
            descrizione_it="Infrastruttura 1", descrizione_en="Infra 1"
        )
        lab = U.create_laboratorioDatiBase(
            nome_laboratorio="Informatica",
            acronimo="INF",
            ambito_s3_prevalente=ambito,
            infrastruttura_riferimento=infra,
        )
        other_lab = U.create_laboratorioDatiBase(nome_laboratorio="Altro")

        U.create_laboratorioDipartimenti(
            laboratorio_dati_base=lab, didattica_dipartimento=dip1, principale=True
        )
        U.create_laboratorioDipartimenti(
            laboratorio_dati_base=lab, didattica_dipartimento=dip2, principale=False
        )
        U.create_laboratorioResponsabile(
            laboratorio_dati_base=lab, matricola_personale=director
        )
        U.create_laboratorioAffiliati(
            laboratorio_dati_base=lab,
            matricola_personale=researcher,
            laboratorio_ruolo=U.create_laboratorioRuolo(),
        )
        U.create_laboratorioAffiliati(
            laboratorio_dati_base=lab,
            matricola_personale=tech,
            laboratorio_ruolo=U.create_laboratorioRuoloTecnico(),
        )
        U.create_laboratorioUbicazione(
            laboratorio_dati_base=lab, edificio="A", piano="1", superficie_mq=100
        )
        U.create_laboratorioUbicazione(
            laboratorio_dati_base=lab, edificio="B", piano="2", superficie_mq=50
        )

        results = self.get_results(self.url)
        self.assertEqual(len(results), 2)
        r = next(x for x in results if x["id"] == lab.id)

        self.assertEqual(r["name"], "Informatica")
        self.assertEqual(r["acronym"], "INF")
        self.assertEqual(r["area"], "Tecnologico")
        self.assertEqual(r["departmentId"], dip1.dip_id)
        self.assertEqual(r["departmentCod"], dip1.dip_cod)
        self.assertEqual(r["departmentName"], dip1.dip_des_it)
        self.assertEqual(r["interdepartmental"], "SI")
        self.assertEqual([d["id"] for d in r["extraDepartments"]], ["2"])
        self.assertEqual(r["infrastructureId"], infra.id)
        self.assertEqual(r["infrastructureName"], "Infrastruttura 1")
        self.assertEqual(r["dimension"], "150")
        self.assertEqual(r["scientificDirector"], "Cognome1 Nome1")
        self.assertEqual(r["scientificDirectorId"], str(director.id_ab))
        self.assertEqual(len(r["researchPersonnel"]), 1)
        self.assertEqual(len(r["techPersonnel"]), 1)
        self.assertEqual(r["techPersonnel"][0]["ruolo"], "Tecnico")

        other = next(x for x in results if x["id"] == other_lab.id)
        self.assertEqual(other["interdepartmental"], "NO")
        self.assertIsNone(other["dimension"])
        self.assertIsNone(other["scientificDirector"])

    def test_director_expired_is_ignored(self):
        p = make_person(1)
        lab = U.create_laboratorioDatiBase()
        U.create_laboratorioResponsabile(
            laboratorio_dati_base=lab,
            matricola_personale=p,
            data_fine=date.today() - timedelta(days=1),
        )
        results = self.get_results(self.url)
        self.assertIsNone(results[0]["scientificDirector"])

    def test_director_excluded_from_personnel(self):
        p = make_person(1)
        lab = U.create_laboratorioDatiBase()
        U.create_laboratorioResponsabile(
            laboratorio_dati_base=lab, matricola_personale=p
        )
        U.create_laboratorioAffiliati(
            laboratorio_dati_base=lab,
            matricola_personale=p,
            laboratorio_ruolo=U.create_laboratorioRuolo(),
        )
        results = self.get_results(self.url)
        self.assertEqual(results[0]["researchPersonnel"], [])

    # TODO: filtri (department, teacher, scope, area, infrastructure, search, erc1)
    # Servono filters.py per ricostruirli.


class LaboratoryDetailTest(LaboratoriesBaseTest):
    def test_detail(self):
        dip1, dip2 = make_dipartimenti()
        director = make_person(1)
        researcher = make_person(2)
        tech = make_person(3)

        erc0 = U.create_ricercaErc0()
        erc1 = U.create_ricercaErc1(ricerca_erc0_cod=erc0)
        ambito = U.create_ambitoS3(
            codice="U",
            denominazione_it="Umanistico",
            denominazione_en="Humanistic",
        )
        lab = U.create_laboratorioDatiBase(
            nome_laboratorio="LAB1", ambito_s3_prevalente=ambito
        )

        U.create_laboratorioDipartimenti(
            laboratorio_dati_base=lab, didattica_dipartimento=dip1, principale=True
        )
        U.create_laboratorioDipartimenti(
            laboratorio_dati_base=lab, didattica_dipartimento=dip2, principale=False
        )
        U.create_laboratorioResponsabile(
            laboratorio_dati_base=lab, matricola_personale=director
        )
        U.create_laboratorioAffiliati(
            laboratorio_dati_base=lab,
            matricola_personale=researcher,
            laboratorio_ruolo=U.create_laboratorioRuolo(),
        )
        U.create_laboratorioAffiliati(
            laboratorio_dati_base=lab,
            matricola_personale=tech,
            laboratorio_ruolo=U.create_laboratorioRuoloTecnico(),
        )
        U.create_laboratorioDatiErc1(laboratorio_dati_base=lab, ricerca_erc1=erc1)
        U.create_laboratorioServizi(
            laboratorio_dati_base=lab,
            laboratorio_anagrafica_servizi=U.create_laboratorioAnagraficaServizi(),
        )
        U.create_laboratorioUbicazione(
            laboratorio_dati_base=lab, edificio="A", piano="1", note="nota"
        )

        url = reverse("laboratories:apiv2:laboratories-detail", args=[lab.id])
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertEqual(data["id"], lab.id)
        self.assertEqual(data["area"], "Umanistico")
        self.assertEqual(data["departmentReferentId"], dip1.dip_id)
        self.assertEqual(data["departmentReferentName"], dip1.dip_des_it)
        self.assertEqual(data["interdepartmental"], "SI")
        self.assertEqual(data["scientificDirectorName"], "Cognome1 Nome1")
        self.assertEqual(data["scientificDirectorId"], str(director.id_ab))
        self.assertEqual(len(data["researchPersonnel"]), 1)
        self.assertEqual(data["researchPersonnel"][0]["id"], str(researcher.id_ab))
        self.assertEqual(len(data["techPersonnel"]), 1)
        self.assertEqual(data["techPersonnel"][0]["ruolo"], "Tecnico")
        self.assertEqual(len(data["erc0"]), 1)
        self.assertEqual(data["erc0"][0]["idErc0"], erc0.erc0_cod)
        self.assertEqual(data["erc0"][0]["erc1List"][0]["idErc1"], erc1.cod_erc1)
        self.assertEqual(data["offeredServices"][0]["name"], "S1")
        self.assertEqual(
            data["offeredServices"][0]["description"], "Descrizione anagrafica"
        )
        self.assertEqual(
            data["location"], [{"building": "A", "floor": "1", "note": "nota"}]
        )
        # campi senza equivalente nel nuovo schema
        self.assertIsNone(data["equipment"])
        self.assertIsNone(data["URL"])
        self.assertIsNone(data["completionReferentId"])

    def test_detail_hidden_is_404_for_anonymous(self):
        lab = U.create_laboratorioDatiBase(visibile=False)
        url = reverse("laboratories:apiv2:laboratories-detail", args=[lab.id])
        self.assertEqual(self.req.get(url).status_code, 404)

    def test_detail_not_found(self):
        url = reverse("laboratories:apiv2:laboratories-detail", args=[999])
        self.assertEqual(self.req.get(url).status_code, 404)


class LookupApiTest(LaboratoriesBaseTest):
    def test_scopes_list(self):
        U.create_laboratorioTipologiaAttivita(
            descrizione_it="Ricerca", descrizione_en="Research"
        )
        url = reverse("laboratories:apiv2:laboratories-scopes-list")
        results = self.get_results(url)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["description"], "Ricerca")

    def test_infrastructures_list(self):
        U.create_laboratorioInfrastruttura(descrizione_it="Infrastruttura 1")
        url = reverse("laboratories:apiv2:infrastructures-list")
        results = self.get_results(url)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["description"], "Infrastruttura 1")

    def test_areas_list_only_used_areas(self):
        tec = U.create_ambitoS3(codice="T", denominazione_it="Tecnologico")
        sci = U.create_ambitoS3(codice="S", denominazione_it="Scientifico")
        U.create_ambitoS3(codice="X", denominazione_it="Non usato")
        U.create_laboratorioDatiBase(nome_laboratorio="LAB1", ambito_s3_prevalente=tec)
        U.create_laboratorioDatiBase(nome_laboratorio="LAB2", ambito_s3_prevalente=sci)
        U.create_laboratorioDatiBase(nome_laboratorio="LAB3", ambito_s3_prevalente=sci)

        url = reverse("laboratories:apiv2:laboratories-areas-list")
        results = self.get_results(url)
        self.assertEqual(len(results), 2)
        self.assertEqual(
            sorted(r["area"] for r in results), ["Scientifico", "Tecnologico"]
        )


class ErcApiTest(LaboratoriesBaseTest):
    def setUp(self):
        super().setUp()
        self.erc0 = U.create_ricercaErc0()
        self.erc01 = U.create_ricercaErc0(
            erc0_cod="112", description="ITA", description_en="ITA"
        )
        self.erc1 = U.create_ricercaErc1(ricerca_erc0_cod=self.erc0)
        U.create_ricercaErc2(ricerca_erc1=self.erc1)

    def test_erc0(self):
        url = reverse("laboratories:apiv2:erclist-list", args=["0"])
        results = self.get_results(url)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["idErc0"], "111")
        self.assertNotIn("erc1List", results[0])

    def test_erc1(self):
        url = reverse("laboratories:apiv2:erclist-list", args=["1"])
        results = self.get_results(url)
        self.assertEqual(len(results), 2)
        first = next(r for r in results if r["idErc0"] == self.erc0.erc0_cod)
        self.assertEqual(len(first["erc1List"]), 1)
        self.assertEqual(first["erc1List"][0]["codErc1"], self.erc1.cod_erc1)
        self.assertNotIn("erc2List", first["erc1List"][0])
        empty = next(r for r in results if r["idErc0"] == "112")
        self.assertEqual(empty["erc1List"], [])

    def test_erc2(self):
        url = reverse("laboratories:apiv2:erclist-list", args=["2"])
        results = self.get_results(url)
        first = next(r for r in results if r["idErc0"] == self.erc0.erc0_cod)
        erc2_list = first["erc1List"][0]["erc2List"]
        self.assertEqual(len(erc2_list), 1)
        self.assertIn("codErc2", erc2_list[0])

    def test_erc_queries_do_not_scale(self):
        # il livello 2 deve usare un numero fisso di query
        U.create_ricercaErc0(erc0_cod="113", description="X", description_en="X")
        url = reverse("laboratories:apiv2:erclist-list", args=["2"])
        with self.assertNumQueries(3):
            self.req.get(url)


class AsterApiTest(LaboratoriesBaseTest):
    def setUp(self):
        super().setUp()
        self.erc0 = U.create_ricercaErc0()
        self.a1 = U.create_ricercaAster1(ricerca_erc0_cod=self.erc0)
        self.a2 = U.create_ricercaAster2(ricerca_aster1=self.a1)

    def test_aster1(self):
        url = reverse("laboratories:apiv2:asterlist-list", args=["1"])
        results = self.get_results(url)
        self.assertEqual(results[0]["idErc0"], self.erc0.erc0_cod)
        self.assertEqual(results[0]["aster1_list"][0]["idAster1"], self.a1.id)
        self.assertNotIn("aster2_list", results[0]["aster1_list"][0])

    def test_aster2(self):
        url = reverse("laboratories:apiv2:asterlist-list", args=["2"])
        results = self.get_results(url)
        aster2 = results[0]["aster1_list"][0]["aster2_list"]
        self.assertEqual(len(aster2), 1)
        self.assertEqual(aster2[0]["idAster2"], self.a2.id)
