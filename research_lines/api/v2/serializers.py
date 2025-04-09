from rest_framework import serializers
from generics.utils import encrypt

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)

class BaseResearchLinesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="descrizione")
    results = serializers.CharField(source="descr_pubblicaz_prog_brevetto")
    year = serializers.IntegerField(source="anno")
    erc2Id = serializers.CharField(source="ricerca_erc2.cod_erc2", allow_null=True)
    erc2Name = serializers.CharField(source="ricerca_erc2.descrizione", allow_null=True)
    teachers = serializers.SerializerMethodField()
    visible = serializers.BooleanField(source="visibile")

    def get_teachers(self, obj):
        return [
            {
                "id": encrypt(docente.personale.matricola),
                "name": (
                    f"{docente.personale.cognome} {docente.personale.nome}"
                    + (f" {docente.personale.middle_name}" if docente.personale.middle_name else "")
                ),
                "departmentName": docente.personale.ds_sede,
                "departmentCod": docente.personale.sede,
            }
            for docente in obj.ricercadocentelineabase_set.all()
        ]
        
    
    class Meta:
        model = RicercaLineaBase
        fields = [
            "id",
            "description",
            "results",
            "year",
            "erc2Id",
            "erc2Name",
            "teachers",
            "visible"
        ]


class AppliedResearchLinessSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="descrizione")
    results = serializers.CharField(source="descr_pubblicaz_prog_brevetto")
    year = serializers.IntegerField(source="anno")
    aster2Id = serializers.CharField(source="ricerca_aster2_id.ricerca_aster1_id", allow_null=True)
    aster2Name = serializers.CharField(source="ricerca_aster2_id.descrizione", allow_null=True)
    teachers = serializers.SerializerMethodField()
    visible = serializers.BooleanField(source="visibile")

    def get_teachers(self, obj):
        return [
            {
                "id": encrypt(docente.personale.matricola),
                "name": (
                    f"{docente.personale.cognome} {docente.personale.nome}"
                    + (f" {docente.personale.middle_name}" if docente.personale.middle_name else "")
                ),
                "departmentName": docente.personale.ds_sede,
                "departmentCod": docente.personale.sede,
            }
            for docente in obj.ricercadocentelineaapplicata_set.all()
        ]
        
    
    class Meta:
        model = RicercaLineaApplicata
        fields = [
            "id",
            "description",
            "results",
            "year",
            "aster2Id",
            "aster2Name",
            "teachers",
            "visible"
        ]
