from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import ReadOnlyModelSerializer
from laboratories.models import (
    LaboratorioDatiBase,
    LaboratorioTipologiaAttivita,
    LaboratorioInfrastruttura,
)
from research_lines.models import (
    RicercaErc0,
)
from generics.utils import build_media_path, encrypt

from addressbook.utils import add_email_addresses
from datetime import date


def _full_name(p):
    return " ".join(x for x in (p.cognome, p.nome, p.middle_name) if x)


def _tr(lang, it, en):
    """Testo nella lingua richiesta, con fallback sull'italiano."""
    return en if lang != "it" and en else it


class LaboratoryCommonMixin:
    def _lang(self):
        return self.context.get("language", "it")

    # --- helper interni ---
    def _director(self, obj):
        """Primo responsabile attivo (vedi nota sui ruoli)."""
        today = date.today()
        for r in getattr(obj, "responsabili", []):
            if r.matricola_personale and (r.data_fine is None or r.data_fine >= today):
                return r.matricola_personale
        return None

    def _main_department(self, obj):
        deps = getattr(obj, "dipartimento_principale", [])
        return deps[0].didattica_dipartimento if deps and deps[0].didattica_dipartimento else None

    def _scope(self, obj, keyword):
        lang = self._lang()
        for a in getattr(obj, "attivita", []):
            t = a.tipologia_attivita
            if t and keyword in (t.descrizione_it or "").lower():
                return _tr(lang, a.descr_finalita_it, a.descr_finalita_en)
        return None

    def _people(self, items, obj, tech):
        lang = self._lang()
        director = self._director(obj)
        out = []
        for p in items:
            pers = p.matricola_personale
            if not pers or (director and pers.matricola == director.matricola):
                continue
            if tech:
                ruolo = p.laboratorio_ruolo
                out.append({
                    "matricola": str(pers.id_ab),
                    "name": _full_name(pers),
                    "ruolo": _tr(lang, ruolo.descr_ruolo_it, ruolo.descr_ruolo_en) if ruolo else None,
                })
            else:
                out.append({
                    "id": str(pers.id_ab),
                    "name": _full_name(pers),
                    "email": add_email_addresses(pers.cod_fis),
                })
        return out

    @extend_schema_field(serializers.CharField())
    def get_logo(self, obj):
        return build_media_path(obj.nome_file_logo)

    @extend_schema_field(serializers.CharField())
    def get_scientificDirectorId(self, obj):
        d = self._director(obj)
        return str(d.id_ab) if d else None

    @extend_schema_field(serializers.CharField())
    def get_interdepartmental(self, obj):
        return "SI" if getattr(obj, "other_dep", None) else "NO"

    @extend_schema_field(serializers.CharField())
    def get_area(self, obj):
        a = obj.ambito_s3_prevalente
        return _tr(self._lang(), a.denominazione_it, a.denominazione_en) if a else None

    @extend_schema_field(serializers.IntegerField())
    def get_infrastructureId(self, obj):
        return obj.infrastruttura_riferimento.id if obj.infrastruttura_riferimento else None

    @extend_schema_field(serializers.CharField())
    def get_infrastructureName(self, obj):
        i = obj.infrastruttura_riferimento
        return _tr(self._lang(), i.descrizione_it, i.descrizione_en) if i else None

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_extraDepartments(self, obj):
        lang = self._lang()
        deps = [d.didattica_dipartimento for d in getattr(obj, "other_dep", []) if d.didattica_dipartimento]
        deps.sort(key=lambda d: (d.dip_des_it if lang == "it" else d.dip_des_eng) or "")
        return [
            {"id": d.dip_cod, "name": d.dip_des_it if lang == "it" else d.dip_des_eng}
            for d in deps
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_scopes(self, obj):
        lang = self._lang()
        return [
            {
                "id": s.tipologia_attivita.id,
                "description": _tr(lang, s.tipologia_attivita.descrizione_it,
                                   s.tipologia_attivita.descrizione_en),
            }
            for s in getattr(obj, "attivita", [])
            if s.tipologia_attivita
        ]

    @extend_schema_field(serializers.CharField())
    def get_servicesScope(self, obj):
        return self._scope(obj, "serviz")

    @extend_schema_field(serializers.CharField())
    def get_researchScope(self, obj):
        return self._scope(obj, "ricerc")

    @extend_schema_field(serializers.CharField())
    def get_teachingScope(self, obj):
        return self._scope(obj, "didatt")

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_researchPersonnel(self, obj):
        return self._people(getattr(obj, "personale_ricerca", []), obj, tech=False)

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_techPersonnel(self, obj):
        return self._people(getattr(obj, "personale_tecnico", []), obj, tech=True)


@extend_schema_serializer(examples=examples.LABORATORY_SERIALIZER_EXAMPLE)
class LaboratorySerializer(LaboratoryCommonMixin, serializers.ModelSerializer):
    id = serializers.IntegerField()
    completionReferentId = serializers.SerializerMethodField()
    completionReferentName = serializers.SerializerMethodField()
    scientificDirectorId = serializers.SerializerMethodField()
    scientificDirectorName = serializers.SerializerMethodField()
    scientificDirectorEmail = serializers.SerializerMethodField()
    name = serializers.CharField(source="nome_laboratorio")
    acronym = serializers.CharField(source="acronimo")
    logo = serializers.SerializerMethodField()
    equipment = serializers.SerializerMethodField()
    departmentReferentId = serializers.SerializerMethodField()
    departmentReferentCod = serializers.SerializerMethodField()
    departmentReferentName = serializers.SerializerMethodField()
    infrastructureId = serializers.SerializerMethodField()
    infrastructureName = serializers.SerializerMethodField()
    interdepartmental = serializers.SerializerMethodField()
    extraDepartments = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    servicesScope = serializers.SerializerMethodField()
    researchScope = serializers.SerializerMethodField()
    teachingScope = serializers.SerializerMethodField()
    scopes = serializers.SerializerMethodField()
    erc0 = serializers.SerializerMethodField()
    researchPersonnel = serializers.SerializerMethodField()
    techPersonnel = serializers.SerializerMethodField()
    offeredServices = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    URL = serializers.SerializerMethodField()
    visible = serializers.CharField(source="visibile")

    # campi senza equivalente nel nuovo schema
    def get_completionReferentId(self, obj):
        return None

    def get_completionReferentName(self, obj):
        return None

    def get_equipment(self, obj):
        return None

    def get_URL(self, obj):
        return None

    def get_scientificDirectorName(self, obj):
        d = self._director(obj)
        return _full_name(d) if d else None

    def get_scientificDirectorEmail(self, obj):
        d = self._director(obj)
        return add_email_addresses(d.cod_fis) if d else None

    def get_departmentReferentId(self, obj):
        d = self._main_department(obj)
        return d.dip_id if d else None

    def get_departmentReferentCod(self, obj):
        d = self._main_department(obj)
        return d.dip_cod if d else None

    def get_departmentReferentName(self, obj):
        d = self._main_department(obj)
        return _tr(self._lang(), d.dip_des_it, d.dip_des_eng) if d else None

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_erc0(self, obj):
        lang = self._lang()
        return [
            {
                "idErc0": e.ricerca_erc1.ricerca_erc0_cod.erc0_cod,
                "description": _tr(lang, e.ricerca_erc1.ricerca_erc0_cod.description,
                                   e.ricerca_erc1.ricerca_erc0_cod.description_en),
                "erc1List": [
                    {
                        "idErc1": e.ricerca_erc1.cod_erc1,
                        "description": e.ricerca_erc1.descrizione,
                    }
                ],
            }
            for e in getattr(obj, "erc0", [])
            if e.ricerca_erc1 and e.ricerca_erc1.ricerca_erc0_cod
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_offeredServices(self, obj):
        lang = self._lang()
        out = []
        for s in getattr(obj, "servizi_offerti", []):
            a = s.laboratorio_anagrafica_servizi
            if not a:
                continue
            out.append({
                "name": _tr(lang, a.nome_servizio_it, a.nome_servizio_en),
                "description": _tr(lang, s.descrizione_it or a.descrizione_servizio_it,
                                   s.descrizione_en or a.descrizione_servizio_en),
            })
        return out

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_location(self, obj):
        ubic = getattr(obj, "ubicazione", None)
        if not ubic:
            return None
        return [{"building": s.edificio, "floor": s.piano, "note": s.note} for s in ubic]

    class Meta:
        model = LaboratorioDatiBase
        fields = [
            "id", "completionReferentId", "completionReferentName",
            "scientificDirectorId", "scientificDirectorName", "scientificDirectorEmail",
            "name", "acronym", "logo", "equipment",
            "departmentReferentId", "departmentReferentCod", "departmentReferentName",
            "infrastructureId", "infrastructureName", "interdepartmental",
            "extraDepartments", "area", "servicesScope", "researchScope",
            "teachingScope", "scopes", "erc0", "researchPersonnel", "techPersonnel",
            "offeredServices", "location", "URL", "visible",
        ]


@extend_schema_serializer(examples=examples.LABORATORIES_SERIALIZER_EXAMPLE)
class LaboratoriesSerializer(LaboratoryCommonMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source="nome_laboratorio")
    acronym = serializers.CharField(source="acronimo")
    logo = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    departmentName = serializers.SerializerMethodField()
    departmentId = serializers.SerializerMethodField()
    departmentCod = serializers.SerializerMethodField()
    interdepartmental = serializers.SerializerMethodField()
    extraDepartments = serializers.SerializerMethodField()
    infrastructureId = serializers.SerializerMethodField()
    infrastructureName = serializers.SerializerMethodField()
    dimension = serializers.SerializerMethodField()
    scientificDirector = serializers.SerializerMethodField()
    scientificDirectorId = serializers.SerializerMethodField()
    researchPersonnel = serializers.SerializerMethodField()
    scopes = serializers.SerializerMethodField()
    techPersonnel = serializers.SerializerMethodField()
    servicesScope = serializers.SerializerMethodField()
    researchScope = serializers.SerializerMethodField()
    teachingScope = serializers.SerializerMethodField()
    visible = serializers.CharField(source="visibile")

    def get_departmentName(self, obj):
        d = self._main_department(obj)
        return _tr(self._lang(), d.dip_des_it, d.dip_des_eng) if d else None

    def get_departmentId(self, obj):
        d = self._main_department(obj)
        return d.dip_id if d else None

    def get_departmentCod(self, obj):
        d = self._main_department(obj)
        return d.dip_cod if d else None

    def get_scientificDirector(self, obj):
        d = self._director(obj)
        return _full_name(d) if d else None

    def get_dimension(self, obj):
        ubic = getattr(obj, "ubicazione", None)
        if not ubic:
            return None
        total = sum(u.superficie_mq or 0 for u in ubic)
        return str(total) if total else None

    class Meta:
        model = LaboratorioDatiBase
        fields = [
            "id", "name", "acronym", "logo", "area", "departmentName",
            "departmentId", "departmentCod", "interdepartmental", "extraDepartments",
            "infrastructureId", "infrastructureName", "dimension",
            "scientificDirector", "scientificDirectorId", "researchPersonnel",
            "scopes", "techPersonnel", "servicesScope", "researchScope",
            "teachingScope", "visible",
        ]

@extend_schema_serializer(examples=examples.LABORATORIES_AREA_SERIALIZER_EXAMPLE)
class LaboratoriesAreaSerializer(ReadOnlyModelSerializer):
    area = serializers.CharField(source="ambito")

    class Meta:
        model = LaboratorioDatiBase
        fields = ["area"]


@extend_schema_serializer(examples=examples.LABORATORIES_SCOPES_SERIALIZER_EXAMPLE)
class LaboratoriesScopesSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descrizione")

    class Meta:
        model = LaboratorioTipologiaAttivita
        fields = ["id", "description"]


@extend_schema_serializer(examples=examples.INFRASTRUCTURE_SERIALIZER_EXAMPLE)
class InfrastructuresSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descrizione")

    class Meta:
        model = LaboratorioInfrastruttura
        fields = ["id", "description"]


@extend_schema_serializer(examples=examples.ERC0_SERIALIZER_EXAMPLE)
class Erc0ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()

    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }


@extend_schema_serializer(examples=examples.ERC1_SERIALIZER_EXAMPLE)
class Erc1ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    erc1List = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_erc1List(self, obj):
        return [
            {
                "codErc1": erc1["cod_erc1"],
                "description": erc1["descrizione"],
            }
            for erc1 in obj["erc1_list"]
        ]

    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "erc1List"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }


@extend_schema_serializer(examples=examples.ERC2_SERIALIZER_EXAMPLE)
class Erc2ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    erc1List = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_erc1List(self, obj):
        return [
            {
                "codErc1": erc1["cod_erc1"],
                "description": erc1["descrizione"],
                "erc2List": [
                    {
                        "codErc2": erc2["cod_erc2"],
                        "description": erc2["descrizione"],
                    }
                    for erc2 in erc1.get("erc2_list")
                ],
            }
            for erc1 in obj.get("erc1_list")
        ]

    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "erc1List"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }


@extend_schema_serializer(examples=examples.ASTER1_SERIALIZER_EXAMPLE)
class Aster1ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    aster1_list = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_aster1_list(self, obj):
        return [
            {
                "idAster1": a["id"],
                "description": a["descrizione"],
            }
            for a in obj.get("aster1_list")
        ]

    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "aster1_list"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }


@extend_schema_serializer(examples=examples.ASTER2_SERIALIZER_EXAMPLE)
class Aster2ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    aster1_list = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_aster1_list(self, obj):
        return [
            {
                "idAster1": a["id"],
                "description": a["descrizione"],
                "aster2_list": [
                    {
                        "idAster2": a2["id"],
                        "description": a2["descrizione"],
                    }
                    for a2 in a.get("aster2_list")
                ],
            }
            for a in obj.get("aster1_list")
        ]

    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "aster1_list"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }
