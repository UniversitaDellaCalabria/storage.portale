from rest_framework import serializers
from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.utils import build_media_path
from generics.api.serializers import ReadOnlyModelSerializer
from cds.models import DidatticaRegolamentoAltriDati
from cds_brochure.models import CdsBrochure
from cds.models import DidatticaCdsLingua


@extend_schema_serializer(examples=examples.BROCHURE_LIST_SERIALIZER_EXAMPLE)
class BrochuresListSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    cdsCod = serializers.CharField(source="cds.cds_cod")
    academicYear = serializers.IntegerField(source="aa")
    cdsName = serializers.CharField(source="cds.nome_cds_it")

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


@extend_schema_serializer(examples=examples.BROCHURE_DETAIL_SERIALIZER_EXAMPLE)
class BrochuresDetailSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    cdsCod = serializers.CharField(source="cds.cds_cod")
    academicYear = serializers.IntegerField(source="aa")
    cdsName = serializers.CharField(source="cds.nome_cds_it")
    courseClassName = serializers.CharField(source="course_class")
    courseInterClassDes = serializers.CharField(source="course_interclass")
    languages = serializers.SerializerMethodField()
    durationYears = serializers.IntegerField(source="cds.durata_anni")
    seatsNumber = serializers.IntegerField(source="num_posti")
    video = serializers.SerializerMethodField()
    intro = serializers.CharField(source="descrizione_corso_it")
    admission = serializers.CharField(source="accesso_corso_it")
    goals = serializers.CharField(source="obiettivi_corso_it")
    jobOpportunities = serializers.CharField(source="sbocchi_professionali_it")
    taxes = serializers.CharField(source="tasse_contributi_esoneri_it")
    scholarships = serializers.CharField(source="borse_studio_it")
    concessions = serializers.CharField(source="agevolazioni_it")
    shortDescription = serializers.CharField(source="corso_in_pillole_it")
    studyPlan = serializers.CharField(source="cosa_si_studia_it")
    enrollmentMode = serializers.CharField(source="come_iscriversi_it")
    exStudents = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    sliders = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_links(self, obj):
        lang = self.get_requestLang()

        links = getattr(obj, "links", [])

        return [
            {
                "id": links.id,
                "order": links.ordine,
                "description": links.descrizione_link_it
                if lang == "it" or links.descrizione_link_en is None
                else links.descrizione_link_en,
                "link": links.link_it
                if lang == "it" or links.link_en is None
                else links.link_en,
            }
            for links in links
        ]

    @extend_schema_field(serializers.ListField())
    def get_sliders(self, obj):
        lang = self.get_requestLang()

        sliders = getattr(obj, "sliders", [])

        return [
            {
                "id": s.id,
                "order": s.ordine,
                "description": s.slider_it
                if lang == "it" or s.slider_en is None
                else s.slider_it,
            }
            for s in sliders
        ]

    @extend_schema_field(serializers.ListField())
    def get_exStudents(self, obj):
        request = self.context.get("request", None)
        lang = "en" if request and request.GET.get("lang") == "en" else "it"

        exStudensts = getattr(obj, "exStudenti", [])
        return [
            {
                "id": e.id,
                "name": e.nome,
                "order": e.ordine,
                "profile": e.profilo_it
                if lang == "it" or e.profilo_en is None
                else e.profilo_en,
                "link": e.link_it if lang == "it" or e.link_en is None else e.link_en,
                "photo": build_media_path(e.foto) if e.foto else None,
            }
            for e in exStudensts
        ]

    @extend_schema_field(serializers.ListField())
    def get_languages(self, obj):
        lingua = DidatticaCdsLingua.objects.filter(
            cdsord__cds_cod=obj.cds.cds_cod
        ).only("iso6392_cod")

        for lingua in lingua:
            return [lingua.iso6392_cod] if lingua else []

    @extend_schema_field(serializers.ListField())
    def get_video(self, obj):
        lang = self.get_requestLang()

        reg_did = (
            DidatticaRegolamentoAltriDati.objects.filter(
                regdid__cds__cds_cod=obj.cds.cds_cod,
                regdid__aa_reg_did=obj.aa,
                tipo_testo_regdid_cod="URL_CDS_VIDEO",
            )
            .only("clob_txt_ita", "clob_txt_eng")
            .first()
        )

        if reg_did:
            return (
                reg_did.clob_txt_ita
                if lang == "it" and reg_did.clob_txt_eng is None
                else reg_did.clob_txt_eng
            )

    class Meta:
        model = CdsBrochure
        fields = [
            "id",
            "cdsCod",
            "academicYear",
            "cdsName",
            "courseClassName",
            "courseInterClassDes",
            "languages",
            "durationYears",
            "seatsNumber",
            "video",
            "intro",
            "admission",
            "goals",
            "jobOpportunities",
            "taxes",
            "scholarships",
            "concessions",
            "shortDescription",
            "studyPlan",
            "enrollmentMode",
            "exStudents",
            "links",
            "sliders",
        ]
        language_field_map = {
            "cdsName": {"it": "cds.nome_cds_it", "en": "cds.nome_cds_eng"},
            "intro": {"it": "descrizione_corso_it", "en": "descrizione_corso_en"},
            "admission": {"it": "accesso_corso_it", "en": "accesso_corso_en"},
            "goals": {"it": "obiettivi_corso_it", "en": "obiettivi_corso_en"},
            "jobOpportunities": {
                "it": "sbocchi_professionali_it",
                "en": "sbocchi_professionali_en",
            },
            "taxes": {
                "it": "tasse_contributi_esoneri_it",
                "en": "tasse_contributi_esoneri_en",
            },
            "scholarships": {"it": "borse_studio_it", "en": "borse_studio_en"},
            "concessions": {"it": "agevolazioni_it", "en": "agevolazioni_en"},
            "shortDescription": {
                "it": "corso_in_pillole_it",
                "en": "corso_in_pillole_en",
            },
            "studyPlan": {"it": "cosa_si_studia_it", "en": "cosa_si_studia_en"},
            "enrollmentMode": {"it": "come_iscriversi_it", "en": "come_iscriversi_en"},
        }
