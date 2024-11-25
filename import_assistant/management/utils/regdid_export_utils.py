import json
from django.conf import settings
from django.db.models import F
from import_assistant.settings import REGDID_STRUCTURE_MAPPINGS
from regdid.models import DidatticaArticoliRegolamentoStruttura


def gen_json_regdid_structures_for_export():
    """
    Returns a json representation of the expected input for regdid structures import,
    populated with data for settings.CURRENT_YEAR
    """
    articles_structures = (
        DidatticaArticoliRegolamentoStruttura.objects.filter(aa=settings.CURRENT_YEAR)
        .annotate(
            **{
                REGDID_STRUCTURE_MAPPINGS["NUMERO"]: F("numero"),
                REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"]: F("numero"),
                REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"]: F("titolo_it"),
                REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"]: F("titolo_en"),
                REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"]: F(
                    "didattica_cds_tipo_corso__tipo_corso_cod"
                ),
                REGDID_STRUCTURE_MAPPINGS[
                    "DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"
                ]: F("didattica_articoli_regolamento_titolo__id"),
            }
        )
        .order_by("didattica_cds_tipo_corso", "numero")
        .values(*REGDID_STRUCTURE_MAPPINGS.values())
    )
    return json.dumps(list(articles_structures), ensure_ascii=False, indent=4)
