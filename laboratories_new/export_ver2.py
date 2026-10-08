import json
import logging
from functools import lru_cache

from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection, models

from laboratories_new.models import LaboratorioDatiBase

logger = logging.getLogger(__name__)

# Campi da non esportare mai (dati personali sensibili)
EXCLUDED_FIELDS = {"cod_fis", "taxpayer_id"}
MAX_DEPTH = 2  # profondità di espansione delle FK in avanti


@lru_cache(maxsize=None)
def _missing_fields(model):
    """Nomi dei campi del modello la cui colonna non esiste nel DB."""
    try:
        with connection.cursor() as cursor:
            desc = connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        existing = {c.name.lower() for c in desc}
    except Exception:  # pragma: no cover
        return ()
    if not existing:
        return ()
    missing = tuple(
        f.name for f in model._meta.concrete_fields if f.column.lower() not in existing
    )
    if missing:
        logger.warning(
            "Colonne mancanti nel DB per %s: %s", model.__name__, ", ".join(missing)
        )
    return missing


def _manager(model):
    """Queryset che non seleziona le colonne inesistenti."""
    return model._default_manager.defer(*_missing_fields(model))


def _serialize(obj, depth=MAX_DEPTH):
    """Dizionario con i campi concreti; le FK vengono espanse fino a `depth`."""
    data = {}
    missing = set(_missing_fields(type(obj)))
    for f in obj._meta.concrete_fields:
        if f.name in EXCLUDED_FIELDS or f.name in missing:
            continue
        if f.is_relation:
            raw = getattr(obj, f.attname)
            if raw is None:
                data[f.name] = None
            elif depth > 0 and f.related_model is not LaboratorioDatiBase:
                related = (
                    _manager(f.related_model)
                    .filter(**{f.target_field.name: raw})
                    .first()
                )
                data[f.name] = _serialize(related, depth - 1) if related else raw
            else:
                data[f.name] = raw  # solo id (anche per FK verso il laboratorio)
        elif isinstance(f, models.FileField):
            value = f.value_from_object(obj)
            data[f.name] = value.name if value else None  # percorso salvato nel DB
        else:
            data[f.name] = f.value_from_object(obj)

    for f in obj._meta.many_to_many:
        data[f.name] = list(getattr(obj, f.name).values_list("pk", flat=True))
    return data


def laboratory_full_dict(lab_id):
    lab = _manager(LaboratorioDatiBase).get(pk=lab_id)
    data = _serialize(lab)

    # relazioni inverse (tabelle figlie che puntano al laboratorio)
    for rel in lab._meta.related_objects:
        accessor = rel.get_accessor_name()
        qs = _manager(rel.related_model).filter(**{rel.field.name: lab})
        if rel.one_to_many:
            data[accessor] = [_serialize(o) for o in qs]
        elif rel.one_to_one:
            o = qs.first()
            data[accessor] = _serialize(o) if o else None
    return data


class _Encoder(DjangoJSONEncoder):
    """DjangoJSONEncoder + fallback per tipi non standard (file, bytes, ecc.)."""

    def default(self, o):
        if hasattr(o, "name") and hasattr(o, "storage"):  # FieldFile
            return o.name or None
        if isinstance(o, (bytes, bytearray, memoryview)):
            return bytes(o).decode("utf-8", errors="replace")
        try:
            return super().default(o)
        except TypeError:
            return str(o)


def laboratory_full_json(lab_id, indent=2):
    return json.dumps(
        laboratory_full_dict(lab_id),
        cls=_Encoder,  # date, datetime, Decimal, file, bytes
        indent=indent,
        ensure_ascii=False,
    )
