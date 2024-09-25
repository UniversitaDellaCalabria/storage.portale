from cds.api.v1.util_tests import (
    DidatticaCdsLinguaUnitTest,
    DidatticaCdsUnitTest,
    DidatticaRegolamentoUnitTest,
    DidatticaTestiRegolamentoUnitTest,
)
from django.test import Client, TestCase
from django.urls import reverse
from structures.api.v1.util_tests import (
    ComuniAllUnitTest,
    DidatticaDipartimentoUnitTest,
    TerritorioItUnitTest,
)

from .serializers import CreateUpdateAbstract


class OpenApiSchemaUnitTest(TestCase):
    def test_openapi(self):
        req = Client()
        url = reverse("openapi-schema")
        res = req.get(url)
        assert res.status_code == 200

        url = reverse("openapi-schema-json")
        res = req.get(url)
        assert res.status_code == 200


class SerializersUnitTest(TestCase):
    def test_createUpdateAbstract(self):
        ser = CreateUpdateAbstract()
        ser.create(None)
        ser.update(None, None)


class ModelsToStringUnitTest(TestCase):
    def test_modelstostring(self):
        comuni_all = ComuniAllUnitTest.create_comuniAll(**{"id_comune": 1})
        assert isinstance(comuni_all.__str__(), str)

        territorio_it = TerritorioItUnitTest.create_territorioIt(
            **{"cd_catasto": comuni_all}
        )
        assert isinstance(territorio_it.__str__(), str)

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        assert isinstance(dip.__str__(), str)

        didattica_cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
            }
        )
        assert isinstance(didattica_cds.__str__(), str)

        didattica_lingua = DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(
            **{
                "cdsord": didattica_cds,
            }
        )
        assert isinstance(didattica_lingua.__str__(), str)

        didattica_regolamento = (
            DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
                **{
                    "regdid_id": 1,
                }
            )
        )
        assert isinstance(didattica_regolamento.__str__(), str)

        didattica_testi_regolamento = (
            DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
                **{
                    "regdid": didattica_regolamento,
                }
            )
        )
        assert isinstance(didattica_testi_regolamento.__str__(), str)
