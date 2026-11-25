"""
Confronto tra la versione pubblicata (snapshot in corso) e le tabelle.

Serve alla pagina di gestione: chi modifica vede il valore che vedono tutti
(snapshot) accanto alla modifica in corso, non ancora approvata (tabelle).

Le righe delle tabelle figlie si abbinano a quelle dello snapshot per id:
- added:   id presente solo nelle tabelle (riga nuova, non ancora pubblicata)
- removed: id presente solo nello snapshot (riga tolta, ancora pubblicata)
- changed: id presente in entrambi ma con valori diversi
"""

import datetime
import json

from django.db import models

from .management.utils import ROLE_SAFETY_MANAGER, ROLE_SCIENTIFIC_DIRECTOR
from .models import (
    LaboratorioAffiliati,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioDipartimenti,
    LaboratorioResponsabile,
    LaboratorioServizi,
    LaboratorioUbicazione,
)
from .snapshot_exporter import _Encoder

# Campi tecnici: cambiano a ogni modifica/approvazione, non sono contenuto
IGNORED_FIELDS = {
    "id",
    "dt_mod",
    "dt_ins",
    "user_mod",
    "user_ins",
    "id_user_mod",
    "visibile",
    "laboratorio_dati_base",
}

# sezione -> (chiave nel JSON dello snapshot, modello della tabella)
SECTIONS = {
    "departments": ("laboratoriodipartimenti_set", LaboratorioDipartimenti),
    "researches_erc1": ("laboratoriodatierc1_set", LaboratorioDatiErc1),
    "locations": ("laboratorioubicazione_set", LaboratorioUbicazione),
    "services": ("laboratorioservizi_set", LaboratorioServizi),
    "affiliates": ("laboratorioaffiliati_set", LaboratorioAffiliati),
    "responsibles": ("laboratorioresponsabile_set", LaboratorioResponsabile),
}


# --------------------------------------------------------------------------
# normalizzazione dei valori (tabelle e snapshot nello stesso formato JSON)
# --------------------------------------------------------------------------


def _json_value(value):
    """Valore come finirebbe nello snapshot (date in ISO, Decimal in stringa...)."""
    return json.loads(json.dumps(value, cls=_Encoder))


def _snapshot_value(field, value):
    """Valore di un campo dello snapshot: per le FK espanse, la sola chiave."""
    if field.is_relation and isinstance(value, dict):
        return value.get(field.target_field.name)
    return value


def _current_value(obj, field):
    if field.is_relation:
        return _json_value(getattr(obj, field.attname))
    value = field.value_from_object(obj)
    if isinstance(field, models.FileField):
        return value.name if value else None
    return _json_value(value)


def _empty(value):
    return value in (None, "")


def _same(a, b):
    # None e "" valgono uguale (form e CKEditor salvano l'uno o l'altro)
    if _empty(a) and _empty(b):
        return True
    return a == b


def _changed_fields(model, obj, snap):
    """
    {campo: valore pubblicato da mostrare} per i campi con valore diverso tra
    l'oggetto e la sua riga di snapshot. I campi assenti nello snapshot
    (colonne mancanti al momento dell'export) non si confrontano.
    """
    changed = {}
    for f in model._meta.concrete_fields:
        if f.name in IGNORED_FIELDS or f.name not in snap:
            continue
        if not _same(_current_value(obj, f), _snapshot_value(f, snap[f.name])):
            changed[f.name] = _field_display(f, snap[f.name])
    return changed


# --------------------------------------------------------------------------
# etichette leggibili dei valori pubblicati
# --------------------------------------------------------------------------


def _get(data, *path):
    for key in path:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def _date(value):
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _person(row):
    p = row.get("matricola_personale")
    if isinstance(p, dict) and (p.get("cognome") or p.get("nome")):
        return " ".join(x for x in (p.get("cognome"), p.get("nome")) if x)
    return row.get("nome_cognome") or "-"


def _role(row):
    return _get(row, "laboratorio_ruolo", "descr_ruolo_it") or ""


def _department_label(row):
    return (
        row.get("descr_dip_lab")
        or _get(row, "didattica_dipartimento", "dip_des_it")
        or "-"
    )


def _location_label(row):
    parts = [row.get("edificio"), row.get("piano")]
    return " - ".join(p for p in parts if p) or "-"


def _service_label(row):
    return _get(row, "laboratorio_anagrafica_servizi", "nome_servizio_it") or "-"


def _published_row(section, row):
    """Dati di una riga pubblicata, con gli stessi nomi usati nel template."""
    if section == "departments":
        return {"label": _department_label(row), "principale": row.get("principale")}
    if section == "researches_erc1":
        return {"label": _get(row, "ricerca_erc1", "descrizione") or "-"}
    if section == "locations":
        detail = [row.get("note")]
        if row.get("sede_principale"):
            detail.append(f"sede principale: {row['sede_principale']}")
        return {
            "label": _location_label(row),
            "detail": ", ".join(d for d in detail if d),
            "edificio": row.get("edificio"),
            "piano": row.get("piano"),
            "sede_principale": row.get("sede_principale"),
            "note": row.get("note"),
        }
    if section == "services":
        start, end = _date(row.get("data_inizio")), _date(row.get("data_fine"))
        detail = [_get(row, "traiettoria_s3", "denominazione_it")]
        if start or end:
            fmt = lambda d: d.strftime("%d/%m/%Y") if d else "-"  # noqa: E731
            detail.append(f"{fmt(start)} - {fmt(end)}")
        return {
            "label": _service_label(row),
            "detail": ", ".join(d for d in detail if d),
            "traiettoria": _get(row, "traiettoria_s3", "denominazione_it"),
            "data_inizio": _date(row.get("data_inizio")),
            "data_fine": _date(row.get("data_fine")),
        }
    # personale
    return {
        "label": row.get("nome_cognome") or _person(row),
        "ruolo": _role(row),
        "external": not row.get("matricola_personale"),
    }


# chiavi (in ordine di preferenza) per l'etichetta di una FK espansa nello snapshot
_FK_LABEL_KEYS = (
    "denominazione_it",
    "descrizione_it",
    "nome_servizio_it",
    "descr_ruolo_it",
    "dip_des_it",
    "descrizione",
    "nome",
)


def _fk_label(field, value):
    if "matricola" in value and (value.get("cognome") or value.get("nome")):  # Personale
        return " ".join(x for x in (value.get("cognome"), value.get("nome")) if x)
    if value.get("edificio"):  # anagrafica ubicazioni
        return " - ".join(x for x in (value.get("edificio"), value.get("piano")) if x)
    for key in _FK_LABEL_KEYS:
        if value.get(key):
            return value[key]
    return value.get(field.target_field.name)


def _field_display(field, value):
    """Valore pubblicato di un campo, da mostrare (None se vuoto)."""
    if _empty(value):
        return None
    if field.is_relation and isinstance(value, dict):
        return _fk_label(field, value)
    if isinstance(field, models.BooleanField):
        return bool(value)
    if isinstance(field, models.DateField):
        return _date(value) or value
    return value


# --------------------------------------------------------------------------
# titolari dei ruoli (responsabile scientifico, preposto alla sicurezza)
# --------------------------------------------------------------------------


def _row_still_valid(row, today):
    start, end = _date(row.get("data_inizio")), _date(row.get("data_fine"))
    return (end is None or end > today) and (start is None or start <= today)


def published_role_holder(data, role_descr, today=None):
    """
    Titolare in corso di un ruolo secondo lo snapshot, con la stessa logica di
    _current_role_holder (prima l'interno, poi l'esterno; il piu' recente).
    """
    today = today or datetime.date.today()

    def _latest(rows):
        rows = [
            r
            for r in rows
            if _role(r) == role_descr and _row_still_valid(r, today)
        ]
        rows.sort(
            key=lambda r: (_date(r.get("data_inizio")) or datetime.date.min, r["id"]),
            reverse=True,
        )
        return rows[0] if rows else None

    internal = _latest(data.get("laboratorioresponsabile_set") or [])
    if internal and isinstance(internal.get("matricola_personale"), dict):
        return {"label": _person(internal), "external": False}
    external = _latest(data.get("laboratorioaffiliati_set") or [])
    if external:
        return {"label": external.get("nome_cognome"), "external": True}
    return None


# --------------------------------------------------------------------------
# confronto
# --------------------------------------------------------------------------


def diff_rows(section, model, current_objs, snapshot_rows):
    """{added: set(id), removed: [riga pubblicata], changed: {id: riga pubblicata}}."""
    snap_by_id = {r.get("id"): r for r in snapshot_rows or [] if isinstance(r, dict)}
    current_ids = set()
    added, changed = set(), {}
    for obj in current_objs:
        current_ids.add(obj.pk)
        snap = snap_by_id.get(obj.pk)
        if snap is None:
            added.add(obj.pk)
        else:
            fields = _changed_fields(model, obj, snap)
            if fields:
                changed[obj.pk] = dict(_published_row(section, snap), fields=fields)
    removed = [
        _published_row(section, row)
        for row_id, row in snap_by_id.items()
        if row_id not in current_ids
    ]
    return {"added": added, "removed": removed, "changed": changed}


def diff_laboratory_fields(laboratory, data):
    """{nome campo: valore pubblicato} per i campi del laboratorio modificati."""
    out = {}
    for f in LaboratorioDatiBase._meta.concrete_fields:
        if f.name in IGNORED_FIELDS or f.name not in data:
            continue
        published = _snapshot_value(f, data[f.name])
        if not _same(_current_value(laboratory, f), published):
            out[f.name] = {"published": _field_display(f, data[f.name])}
    return out


def row_pending_change(data, section, obj):
    """
    Stato di una riga di una sezione rispetto allo snapshot `data`:
    - None:                                  pubblicata cosi' com'e'
    - {"state": "added"}:                    non ancora pubblicata
    - {"state": "changed", "fields": {...}}: {campo: valore pubblicato}
    """
    key, model = SECTIONS[section]
    snap = next(
        (r for r in data.get(key) or [] if isinstance(r, dict) and r.get("id") == obj.pk),
        None,
    )
    if snap is None:
        return {"state": "added"}
    fields = _changed_fields(model, obj, snap)
    if not fields:
        return None
    return {"state": "changed", "fields": fields}


def published_section_labels(data, section):
    """Etichette delle righe pubblicate di una sezione (es. la classificazione ERC)."""
    key, _model = SECTIONS[section]
    return [
        _published_row(section, r)["label"]
        for r in data.get(key) or []
        if isinstance(r, dict)
    ]


def laboratory_pending_changes(laboratory, data, current_rows, today=None):
    """
    Differenze tra le tabelle e lo snapshot `data` (dict JSON).

    current_rows: {sezione: oggetti attuali} per le sezioni di SECTIONS.
    Ritorna un dict con:
      fields:   {campo: {"published": valore}}
      <sezione>: vedi diff_rows
      scientific_director / safety_manager: titolare pubblicato
      has_changes: True se c'e' almeno una differenza
    """
    out = {"fields": diff_laboratory_fields(laboratory, data)}
    has_changes = bool(out["fields"])
    for section, (key, model) in SECTIONS.items():
        rows = current_rows.get(section)
        if rows is None:
            rows = model.objects.filter(laboratorio_dati_base=laboratory)
        d = diff_rows(section, model, rows, data.get(key))
        out[section] = d
        has_changes = has_changes or bool(d["added"] or d["removed"] or d["changed"])

    out["scientific_director"] = published_role_holder(
        data, ROLE_SCIENTIFIC_DIRECTOR[0], today
    )
    out["safety_manager"] = published_role_holder(data, ROLE_SAFETY_MANAGER[0], today)
    out["has_changes"] = has_changes
    return out
