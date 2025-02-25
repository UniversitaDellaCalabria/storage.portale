from rest_framework import serializers
from generics.api.serializers import ReadOnlyModelSerializer

from cds_brochure.models import CdsBrochure

class BrochuresListSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    cdsCod = serializers.CharField(source='cds.cds_cod')
    academicYear = serializers.IntegerField(source='aa')
    cdsName = serializers.CharField(source='cds.nome_cds_it')
    class Meta:
        model = CdsBrochure
        fields = [
            "id",
            "cdsCod",
            "academicYear",
            "cdsName",
            ]
        language_field_map = {
            "cdsName": {"it": "cds.nome_cds_it", "en": "cds.nome_cds_eng"}
        }
        
        
class BrochuresDetailSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    cdsCod = serializers.CharField(source='cds__cds_cod')
    academicYear = serializers.IntegerField(source='aa')
    cdsName = serializers.CharField(source='cds__nome_cds_it')
    courseClassName = serializers.CharField(source='course_class')
    courseInterClassDes = serializers.CharField(source='course_interclass')
    # languages = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    
    # interclassMiurCod = serializers.CharField(source='cds.intercla_miur_cod')
    # interclassMiurDes = serializers.CharField(source='cds.intercla_miur_des')
    # durationYears = serializers.IntegerField(source='cds.durata_anni')
    # numSeats = serializers.IntegerField(source='num_posti')
    # courseDescription = serializers.CharField(source='descrizione_corso_it')
    # courseAccess = serializers.CharField(source='accesso_corso_it')
    # courseGoals = serializers.CharField(source='obiettivi_corso_it')
    # professionalOutlets = serializers.CharField(source='sbocchi_professionali_it')
    
    
    # def get_languages(self, obj):
    #     languages = getattr(obj, 'languages', None)
    #     print(languages)
    #     return [lang.iso6392_cod for lang in languages]
    
    def get_video(self, obj):
        request = self.context.get("request", None)
        lang =  "en" if request and request.GET.get("lang") == "en" else "it"
        
        reg_did = getattr(obj, 'video_link', None)
        if reg_did:
            return reg_did[0].clob_txt_it if lang == "it" and reg_did[0].clob_txt_eng is None else reg_did[0].clob_txt_eng
            
    class Meta:
        model = CdsBrochure
        fields = [
            "id",
            "cdsCod",
            "academicYear",
            "cdsName",
            "courseClassName",
            "courseInterClassDes",
            # "languages",
            "video",
            
            ]
        language_field_map = {
            "cdsName": {"it": "cds__nome_cds_it", "en": "cds__nome_cds_eng"},
            # "courseDescription": {"it": "descrizione_corso_it", "en": "descrizione_corso_en"},
            # "courseAccess": {"it": "accesso_corso_it", "en": "accesso_corso_en"},
            # "courseGoals": {"it": "obiettivi_corso_it", "en": "obiettivi_corso_en"},
            # "professionalOutlets": {"it": "sbocchi_professionali_it", "en": "sbocchi_professionali_en"},
        }
    