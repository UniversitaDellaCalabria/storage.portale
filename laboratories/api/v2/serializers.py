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


@extend_schema_serializer(examples=examples.LABORATORY_SERIALIZER_EXAMPLE)
class LaboratorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    completionReferentId = serializers.SerializerMethodField()
    completionReferentName = serializers.CharField(source="referente_compilazione")
    scientificDirectorId = serializers.SerializerMethodField()
    scientificDirectorName = serializers.CharField(source="responsabile_scientifico")
    scientificDirectorEmail = serializers.SerializerMethodField()
    name = serializers.CharField(source="nome_laboratorio")
    acronym = serializers.CharField(source="acronimo")
    logo = serializers.SerializerMethodField()
    equipment = serializers.CharField(source="strumentazione_descrizione")
    departmentReferentId = serializers.IntegerField(
        source="dipartimento_riferimento.dip_id"
    )
    departmentReferentCod = serializers.CharField(
        source="dipartimento_riferimento.dip_cod"
    )
    departmentReferentName = serializers.CharField(
        source="dipartimento_riferimento.dip_des_it"
    )
    infrastructureId = serializers.IntegerField(
        source="infrastruttura_riferimento.id", allow_null=True
    )
    infrastructureName = serializers.CharField(
        source="infrastruttura_riferimento.descrizione", allow_null=True
    )
    interdepartmental = serializers.CharField(source="laboratorio_interdipartimentale")
    extraDepartments = serializers.SerializerMethodField()
    area = serializers.CharField(source="ambito")
    servicesScope = serializers.CharField(source="finalita_servizi_it")
    researchScope = serializers.CharField(source="finalita_ricerca_it")
    teachingScope = serializers.CharField(source="finalita_didattica_it")
    scopes = serializers.SerializerMethodField()
    erc0 = serializers.SerializerMethodField()
    researchPersonnel = serializers.SerializerMethodField()
    techPersonnel = serializers.SerializerMethodField()
    offeredServices = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    URL = serializers.CharField(source="sito_web")
    visible = serializers.CharField(source="visibile")

    def get_scientificDirectorEmail(self, obj):
        return add_email_addresses(obj.matricola_responsabile_scientifico.cod_fis)

    @extend_schema_field(serializers.CharField())
    def get_completionReferentId(self, obj):
        return encrypt(obj.matricola_referente_compilazione)

    @extend_schema_field(serializers.CharField())
    def get_logo(self, obj):
        return build_media_path(obj.nome_file_logo)

    @extend_schema_field(serializers.IntegerField())
    def get_scientificDirectorId(self, obj):
        return encrypt(obj.matricola_responsabile_scientifico)

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_extraDepartments(self, obj):
        if not obj.other_dep:
            return []
        language = self.context.get("language", "it")

        if obj.laboratorio_interdipartimentale == "SI":
            # obj.order_by(
            #     "didattica_dipartimento.dip_des_it"
            # ) if language == "it" else obj.order_by(
            #     "didattica_dipartimento.dip_des_eng"
            # )
            def key(d):
                if language == "it":
                    return d.didattica_dipartimento.dip_des_it
                else:
                    return d.didattica_dipartimento.dip_des_eng

            other_deps_sorted = sorted(obj.other_dep, key=key)

            return [
                {
                    "id": d.didattica_dipartimento.dip_cod,
                    "name": d.didattica_dipartimento.dip_des_it
                    if language == "it"
                    else d.didattica_dipartimento.dip_des_eng,
                }
                for d in other_deps_sorted
            ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_scopes(self, obj):
        return [
            {
                "id": s.tipologia_attivita.id,
                "description": s.tipologia_attivita.descrizione,
            }
            for s in obj.attivita
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_researchPersonnel(self, obj):
        for p in obj.personale_ricerca:
            if (
                p.matricola_personale_ricerca
                and p.matricola_personale_ricerca.matricola
                != obj.matricola_responsabile_scientifico
            ):
                full_name = (
                    p.matricola_personale_ricerca.cognome
                    + " "
                    + p.matricola_personale_ricerca.nome
                    + " "
                )
                if p.matricola_personale_ricerca.middle_name:
                    full_name += p.matricola_personale_ricerca.middle_name

                return [
                    {
                        "id": encrypt(p.matricola_personale_ricerca.matricola),
                        "name": full_name,
                        "email": add_email_addresses(
                            p.matricola_personale_ricerca.cod_fis
                        ),
                    }
                ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_techPersonnel(self, obj):
        return [
            {
                "matricola": encrypt(p.matricola_personale_tecnico.matricola),
                "name": p.matricola_personale_tecnico.cognome
                + " "
                + p.matricola_personale_tecnico.nome
                + " "
                if not p.matricola_personale_tecnico.middle_name
                else p.matricola_personale_tecnico.cognome
                + " "
                + p.matricola_personale_tecnico.nome
                + " "
                + p.matricola_personale_tecnico.middle_name,
                "ruolo": p.ruolo,
            }
            for p in obj.personale_tecnico
            if p.matricola_personale_tecnico
            and p.matricola_personale_tecnico.matricola
            != obj.matricola_responsabile_scientifico
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_erc0(self, obj):
        language = self.context.get("language", "it")
        return [
            {
                "idErc0": erc0.ricerca_erc1.ricerca_erc0_cod.erc0_cod,
                "description": erc0.ricerca_erc1.ricerca_erc0_cod.description
                if language == "it"
                else erc0.ricerca_erc1.ricerca_erc0_cod.description_en,
                "erc1List": [
                    {
                        "idErc1": erc0.ricerca_erc1.cod_erc1,
                        "description": erc0.ricerca_erc1.descrizione,
                    }
                ],
            }
            for erc0 in obj.erc0
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_offeredServices(self, obj):
        return [
            {
                "name": s.nome_servizio,
                "description": s.descrizione_servizio,
            }
            for s in obj.servizi_offerti
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_location(self, obj):
        if not obj.ubicazione:
            return None
        return [
            {
                "building": s.edificio,
                "floor": s.piano,
                "note": s.note,
            }
            for s in obj.ubicazione
        ]

    class Meta:
        model = LaboratorioDatiBase
        fields = [
            "id",
            "completionReferentId",
            "completionReferentName",
            "scientificDirectorId",
            "scientificDirectorName",
            "scientificDirectorEmail",
            "name",
            "acronym",
            "logo",
            "equipment",
            "departmentReferentId",
            "departmentReferentCod",
            "departmentReferentName",
            "infrastructureId",
            "infrastructureName",
            "interdepartmental",
            "extraDepartments",
            "area",
            "servicesScope",
            "researchScope",
            "teachingScope",
            "scopes",
            "erc0",
            "researchPersonnel",
            "techPersonnel",
            "offeredServices",
            "location",
            "URL",
            "visible",
        ]
        language_field_map = {
            "departmentReferentName": {
                "it": "dipartimento_riferimento.dip_des_it",
                "en": "dipartimento_riferimento.dip_des_eng",
            },
            "servicesScope": {"it": "finalita_servizi_it", "en": "finalita_servizi_en"},
            "researchScope": {"it": "finalita_ricerca_it", "en": "finalita_ricerca_en"},
            "teachingScope": {
                "it": "finalita_didattica_it",
                "en": "finalita_didattica_en",
            },
        }


@extend_schema_serializer(examples=examples.LABORATORIES_SERIALIZER_EXAMPLE)
class LaboratoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source="nome_laboratorio")
    acronym = serializers.CharField(source="acronimo")
    logo = serializers.SerializerMethodField()
    area = serializers.CharField(source="ambito")
    departmentName = serializers.SerializerMethodField()
    departmentId = serializers.IntegerField(source="dipartimento_riferimento.dip_id")
    departmentCod = serializers.CharField(source="dipartimento_riferimento.dip_cod")
    interdepartmental = serializers.CharField(source="laboratorio_interdipartimentale")
    extraDepartments = serializers.SerializerMethodField()
    infrastructureId = serializers.IntegerField(
        source="infrastruttura_riferimento.id", allow_null=True
    )
    infrastructureName = serializers.CharField(
        source="infrastruttura_riferimento.descrizione", allow_null=True
    )
    dimension = serializers.CharField(source="sede_dimensione")
    scientificDirector = serializers.CharField(source="responsabile_scientifico")
    scientificDirectorId = serializers.SerializerMethodField()
    researchPersonnel = serializers.SerializerMethodField()
    scopes = serializers.SerializerMethodField()
    techPersonnel = serializers.SerializerMethodField()
    servicesScope = serializers.CharField(source="finalita_servizi_it")
    researchScope = serializers.CharField(source="finalita_ricerca_it")
    teachingScope = serializers.CharField(source="finalita_didattica_it")
    visible = serializers.CharField(source="visibile")

    @extend_schema_field(serializers.CharField())
    def get_logo(self, obj):
        return build_media_path(obj.nome_file_logo)

    @extend_schema_field(serializers.IntegerField())
    def get_scientificDirectorId(self, obj):
        return encrypt(obj.matricola_responsabile_scientifico)

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_extraDepartments(self, obj):
        if not obj.other_dep:
            return []
        language = self.context.get("language", "it")
        if obj.laboratorio_interdipartimentale == "SI":
            # obj.order_by(
            #     "didattica_dipartimento.dip_des_it"
            # ) if language == "it" else obj.order_by(
            #     "didattica_dipartimento.dip_des_eng"
            # )
            def key(d):
                if language == "it":
                    return d.didattica_dipartimento.dip_des_it
                else:
                    return d.didattica_dipartimento.dip_des_eng

            other_deps_sorted = sorted(obj.other_dep, key=key)

            return [
                {
                    "id": d.didattica_dipartimento.dip_cod,
                    "name": d.didattica_dipartimento.dip_des_it
                    if language == "it"
                    else d.didattica_dipartimento.dip_des_eng,
                }
                for d in other_deps_sorted
            ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_scopes(self, obj):
        return [
            {
                "id": s.tipologia_attivita.id,
                "description": s.tipologia_attivita.descrizione,
            }
            for s in obj.attivita
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_researchPersonnel(self, obj):
        # append_email_addresses(obj.personale_ricerca, obj.personale_ricerca.matricola_personale_ricerca.id_ab)
        for p in obj.personale_ricerca:
            if (
                p.matricola_personale_ricerca
                and p.matricola_personale_ricerca.matricola
                != obj.matricola_responsabile_scientifico
            ):
                full_name = (
                    p.matricola_personale_ricerca.cognome
                    + " "
                    + p.matricola_personale_ricerca.nome
                    + " "
                )
                if p.matricola_personale_ricerca.middle_name:
                    full_name += p.matricola_personale_ricerca.middle_name

                return [
                    {
                        "id": encrypt(p.matricola_personale_ricerca.matricola),
                        "name": full_name,
                        "email": add_email_addresses(
                            p.matricola_personale_ricerca.cod_fis
                        ),
                    }
                ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_techPersonnel(self, obj):
        # append_email_addresses(obj.personale_tecnico, obj.personale_tecnico.matricola_personale_tecnico.id_ab)

        return [
            {
                "matricola": encrypt(p.matricola_personale_tecnico.matricola),
                "name": p.matricola_personale_tecnico.cognome
                + " "
                + p.matricola_personale_tecnico.nome
                + " "
                if not p.matricola_personale_tecnico.middle_name
                else p.matricola_personale_tecnico.cognome
                + " "
                + p.matricola_personale_tecnico.nome
                + " "
                + p.matricola_personale_tecnico.middle_name,
                "ruolo": p.ruolo,
            }
            for p in obj.personale_tecnico
            if p.matricola_personale_tecnico
            and p.matricola_personale_tecnico.matricola
            != obj.matricola_responsabile_scientifico
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_departmentName(self, obj):
        nome = obj.dipartimento_riferimento_nome
        if nome:
            temp = nome.rsplit(",", 1)
            return temp[0] + ", " + temp[1].strip() if len(temp) > 1 else temp[0]

    class Meta:
        model = LaboratorioDatiBase
        fields = [
            "id",
            "name",
            "acronym",
            "logo",
            "area",
            "departmentName",
            "departmentId",
            "departmentCod",
            "interdepartmental",
            "extraDepartments",
            "infrastructureId",
            "infrastructureName",
            "dimension",
            "scientificDirector",
            "scientificDirectorId",
            "researchPersonnel",
            "scopes",
            "techPersonnel",
            "servicesScope",
            "researchScope",
            "teachingScope",
            "visible",
        ]
        language_field_map = {
            "servicesScope": {"it": "finalita_servizi_it", "en": "finalita_servizi_en"},
            "researchScope": {"it": "finalita_ricerca_it", "en": "finalita_ricerca_en"},
            "teachingScope": {
                "it": "finalita_didattica_it",
                "en": "finalita_didattica_en",
            },
        }


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
