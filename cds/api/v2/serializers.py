from rest_framework import serializers
from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class CdsSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCds
        fields = "__all__"


class DegreeTypeSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = ["tipo_corso_cod", "tipo_corso_des"]


class DidatticaAttivitaFormativaSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = "__all__"
        

class StudyActivitiesSerializer(ReadOnlyModelSerializer):   

    full_name = serializers.CharField()
    cds_cod = serializers.CharField(source="cds.cds_cod")
    dip_des_it = serializers.CharField(source="cds.dip.dip_des_it")
    dip_des_eng = serializers.CharField(source="cds.dip.dip_des_eng")
    dip_cod = serializers.CharField(source="cds.dip.dip_cod")
    
    nome_cds_it = serializers.CharField(source="cds.nome_cds_it")
    nome_cds_eng = serializers.CharField(source="cds.nome_cds_eng")
    
    

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = [
            "af_id",
            "af_gen_cod",
            "des",
            "af_gen_des_eng",
            "cds_id",
            "cds_cod",
            "lista_lin_did_af",
            "af_radice_id",
            #Father
            "regdid_id",
            "dip_des_it",
            "dip_des_eng",
            "dip_cod",
            "anno_corso",
            "aa_off_id",
            "ciclo_des",
            "sett_cod",
            "sett_des",
            "part_stu_cod",
            "part_stu_des",
            "fat_part_stu_cod",
            "fat_part_stu_des",
            "nome_cds_it",
            "nome_cds_eng",
            "matricola_resp_did",
            "full_name",
            "pds_des",
            ]