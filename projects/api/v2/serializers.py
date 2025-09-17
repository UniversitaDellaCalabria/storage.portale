from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import ReadOnlyModelSerializer
from projects.models import (
    ProgettoAmbitoTerritoriale,
    ProgettoDatiBase,
    ProgettoTipologiaProgramma,
)
from generics.utils import encrypt


@extend_schema_serializer(examples=examples.PROJECTS_SERIALIZER_EXAMPLE)
class ProjectsSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    startingYear = serializers.IntegerField(source="anno_avvio")
    infrastructureId = serializers.CharField(source="uo")
    infrastructureDescription = serializers.CharField(source="uo.denominazione")
    territorialScopeId = serializers.IntegerField(source="ambito_territoriale.id")
    territorialScopeDescription = serializers.CharField(
        source="ambito_territoriale.ambito_territoriale"
    )
    typeProgramId = serializers.IntegerField(
        source="tipologia_programma.id", allow_null=True
    )
    typeProgramDescription = serializers.CharField(
        source="tipologia_programma.nome_programma", allow_null=True
    )
    title = serializers.CharField(source="titolo")
    description = serializers.CharField(source="descr_breve")
    abstract = serializers.CharField(source="abstract_ita")
    techAreaId = serializers.CharField(source="area_tecnologica")
    techAreaDescription = serializers.CharField(
        source="area_tecnologica.descr_area_ita"
    )
    projectImage = serializers.CharField(source="url_immagine")
    scientificDirectors = serializers.SerializerMethodField()
    researchers = serializers.SerializerMethodField()
    url_sito_web  = serializers.CharField(source="url_sito_web")
    isActive = serializers.BooleanField(source="is_active")

    @extend_schema_field(serializers.ListField())
    def get_scientificDirectors(self, obj):
        return [
            {"id": encrypt(r.matricola), "name": r.nome_origine}
            for r in obj.responsabili
        ]

    @extend_schema_field(serializers.ListField())
    def get_researchers(self, obj):
        return [
            {"id": encrypt(r.matricola), "name": r.nome_origine}
            for r in obj.ricercatori
        ]

    class Meta:
        model = ProgettoDatiBase
        fields = [
            "id",
            "startingYear",
            "infrastructureId",
            "infrastructureDescription",
            "territorialScopeId",
            "territorialScopeDescription",
            "typeProgramId",
            "typeProgramDescription",
            "title",
            "description",
            "abstract",
            "techAreaId",
            "techAreaDescription",
            "projectImage",
            "scientificDirectors",
            "researchers",
            "url_sito_web",
            "isActive",
        ]
        language_field_map = {
            "abstract": {"it": "abstract_ita", "en": "abstract_eng"},
            "techAreaDescription": {
                "it": "area_tecnologica.descr_area_ita",
                "en": "area_tecnologica.descr_area_eng",
            },
        }


@extend_schema_serializer(examples=examples.TERRITORIAL_SCOPES_SERIALIZER_EXAMPLE)
class TerritorialScopesSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="ambito_territoriale")

    class Meta:
        model = ProgettoAmbitoTerritoriale
        fields = [
            "id",
            "description",
        ]


@extend_schema_serializer(examples=examples.PROGRAM_TYPES_SERIALIZER_EXAMPLE)
class ProgramTypesSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="nome_programma")

    class Meta:
        model = ProgettoTipologiaProgramma
        fields = [
            "id",
            "description",
        ]


@extend_schema_serializer(examples=examples.INFRASTRUCTURES_SERIALIZER_EXAMPLE)
class InfrastructuresSerializer(ReadOnlyModelSerializer):
    id = serializers.CharField(source="uo")
    description = serializers.CharField(source="uo__denominazione")

    class Meta:
        model = ProgettoDatiBase
        fields = [
            "id",
            "description",
        ]
