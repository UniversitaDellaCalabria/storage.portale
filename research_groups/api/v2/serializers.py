from rest_framework import serializers
from generics.utils import encrypt

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from research_groups.models import RicercaGruppo

class ResearchGroupsSerializer(serializers.ModelSerializer):
    codErc1 = serializers.CharField(source="ricerca_erc1.cod_erc1", allow_null=True)
    descrizioneErc1 = serializers.CharField(source="ricerca_erc1.descrizione", allow_null=True)
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = RicercaGruppo
        fields = [
            "id",
            "name",
            "description",
            "codErc1",
            "descrizioneErc1",
            "teachers"
        ]

    name = serializers.CharField(source="nome")
    description = serializers.CharField(source="descrizione")

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
            for docente in obj.ricercadocentegruppo_set.all()
        ]
