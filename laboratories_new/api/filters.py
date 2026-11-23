from datetime import date

from django_filters import rest_framework as filters
from django.db.models import Q
from laboratories_new.models import LaboratorioDatiBase


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class LaboratoriesFilters(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Cerca nel nome del laboratorio",
    )
    ambito = filters.CharFilter(
        field_name="ambito_s3_prevalente__id",
        lookup_expr="exact",
        label="Ambito",
    )
    dip = filters.CharFilter(method="filter_dip", label="Dipartimento")
    erc1 = CharInFilter(
        field_name="laboratoriodatierc1__ricerca_erc1__cod_erc1",
        lookup_expr="in",
        label="Ricerca Erc1",
    )
    infrastructure = filters.CharFilter(
        field_name="infrastruttura_riferimento__id",
        lookup_expr="exact",
        label="Infrastruttura",
    )
    teacher = filters.CharFilter(
        method="filter_teacher",
        label="Docente",
        help_text="Filtra per id_ab del personale coinvolto",
    )
    scope = filters.CharFilter(method="filter_scope", label="Traiettoria S3")

    def filter_scope(self, queryset, name, value):
        return queryset.filter(laboratorioservizi__traiettoria_s3__id=value).distinct()

    def filter_teacher(self, queryset, name, value):
        today = date.today()
        active_resp = Q(laboratorioresponsabile__data_fine__isnull=True) | Q(
            laboratorioresponsabile__data_fine__gt=today
        )
        active_aff = Q(laboratorioaffiliati__data_fine__isnull=True) | Q(
            laboratorioaffiliati__data_fine__gt=today
        )
        return queryset.filter(
            (Q(laboratorioresponsabile__matricola_personale__id_ab=value) & active_resp)
            | (Q(laboratorioaffiliati__matricola_personale__id_ab=value) & active_aff)
        ).distinct()

    def filter_erc1(self, queryset, name, value):
        return queryset.filter(
            laboratoriodatierc1__ricerca_erc1__cod_erc1__in=value.split(",")
        ).distinct()

    def filter_dip(self, queryset, name, value):
        return queryset.filter(
            laboratoriodipartimenti__didattica_dipartimento__dip_cod=value
        ).distinct()

    def filter_search(self, queryset, name, value):
        for k in value.split():
            queryset = queryset.filter(nome_laboratorio__icontains=k)
        return queryset

    class Meta:
        model = LaboratorioDatiBase
        fields = []


# ---------------------------------------------------------------------------
# Stessi filtri applicati ai dati di uno snapshot (dict JSON).
#
# Per un laboratorio con modifiche in attesa di approvazione le tabelle
# contengono i dati NON approvati, mentre l'API mostra lo snapshot: filtrare
# sulle tabelle farebbe trovare il laboratorio cercando dati non ancora
# pubblici. Per questi laboratori i filtri si valutano qui, sullo snapshot.
# Va tenuto allineato con i metodi di LaboratoriesFilters.
# ---------------------------------------------------------------------------


def _ref(value, key):
    """Campo di una FK serializzata: dict espanso o id/valore grezzo."""
    if isinstance(value, dict):
        return value.get(key)
    return value if key == "id" else None


def _same(a, b):
    return a is not None and str(a) == str(b)


def _not_ended(record, today):
    data_fine = record.get("data_fine")
    return not data_fine or str(data_fine)[:10] > today.isoformat()


def _snap_search(data, value):
    name = (data.get("nome_laboratorio") or "").casefold()
    return all(k.casefold() in name for k in value.split())


def _snap_ambito(data, value):
    return _same(_ref(data.get("ambito_s3_prevalente"), "id"), value)


def _snap_infrastructure(data, value):
    return _same(_ref(data.get("infrastruttura_riferimento"), "id"), value)


def _snap_dip(data, value):
    return any(
        _same(_ref(d.get("didattica_dipartimento"), "dip_cod"), value)
        for d in data.get("laboratoriodipartimenti_set") or []
    )


def _snap_erc1(data, values):
    values = {str(v) for v in values}
    return any(
        str(_ref(e.get("ricerca_erc1"), "cod_erc1")) in values
        for e in data.get("laboratoriodatierc1_set") or []
        if _ref(e.get("ricerca_erc1"), "cod_erc1") is not None
    )


def _snap_teacher(data, value):
    today = date.today()
    people = (data.get("laboratorioresponsabile_set") or []) + (
        data.get("laboratorioaffiliati_set") or []
    )
    return any(
        _same(_ref(p.get("matricola_personale"), "id_ab"), value)
        and _not_ended(p, today)
        for p in people
    )


def _snap_scope(data, value):
    return any(
        _same(_ref(s.get("traiettoria_s3"), "id"), value)
        for s in data.get("laboratorioservizi_set") or []
    )


SNAPSHOT_FILTERS = {
    "search": _snap_search,
    "ambito": _snap_ambito,
    "dip": _snap_dip,
    "erc1": _snap_erc1,
    "infrastructure": _snap_infrastructure,
    "teacher": _snap_teacher,
    "scope": _snap_scope,
}


def snapshot_matches(data, params):
    """True se i dati dello snapshot soddisfano tutti i filtri valorizzati.
    params: cleaned_data del form di LaboratoriesFilters."""
    for name, check in SNAPSHOT_FILTERS.items():
        value = params.get(name)
        if value in (None, "", []):
            continue
        if not check(data, value):
            return False
    return True
