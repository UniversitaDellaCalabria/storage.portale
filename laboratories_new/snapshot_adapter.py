from datetime import date
from types import SimpleNamespace

from django.utils.dateparse import parse_date


class Snap(SimpleNamespace):
    """Come SimpleNamespace, ma un campo mancante vale None invece di AttributeError."""

    def __getattr__(self, name):  # chiamato solo se l'attributo non esiste
        if name.startswith("__"):
            raise AttributeError(name)
        return None


def to_ns(value):
    if isinstance(value, dict):
        return Snap(**{k: to_ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [to_ns(v) for v in value]
    return value


def _parse_dates(items, *fields):
    for item in items:
        for f in fields:
            v = item.get(f)
            if isinstance(v, str):
                item[f] = parse_date(v[:10])
    return items


def _is_tech(a):
    ruolo = a.get("laboratorio_ruolo")
    descr = (ruolo.get("descr_ruolo_it") if isinstance(ruolo, dict) else "") or ""
    return "tecnic" in descr.lower()


def snapshot_to_obj(data: dict):
    data = dict(data)
    affiliati = data.get("laboratorioaffiliati_set", [])
    dipartimenti = data.get("laboratoriodipartimenti_set", [])
    responsabili = _parse_dates(
        data.get("laboratorioresponsabile_set", []), "data_inizio", "data_fine"
    )

    obj = to_ns(data)
    # stessi nomi dei Prefetch(to_attr=...) della view originale
    obj.erc0 = to_ns(data.get("laboratoriodatierc1_set", []))
    obj.ubicazione = to_ns(data.get("laboratorioubicazione_set", []))
    obj.servizi_offerti = to_ns(data.get("laboratorioservizi_set", []))
    obj.responsabili = to_ns(responsabili)
    obj.personale_tecnico = to_ns([a for a in affiliati if _is_tech(a)])
    obj.personale_ricerca = to_ns([a for a in affiliati if not _is_tech(a)])
    obj.dipartimento_principale = to_ns(
        [d for d in dipartimenti if d.get("principale")]
    )
    obj.other_dep = to_ns([d for d in dipartimenti if not d.get("principale")])
    return obj
