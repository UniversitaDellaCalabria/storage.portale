from rest_framework import serializers
from generics.utils import encrypt
from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneTipoCorso,
)


class HighFormationMastersSerializer(serializers.ModelSerializer):
    masterTitle = serializers.CharField(source="titolo_it")
    typeId = serializers.IntegerField(source="alta_formazione_tipo_corso.id")
    typeDescription = serializers.CharField(
        source="alta_formazione_tipo_corso.tipo_corso_descr"
    )
    erogationMode = serializers.IntegerField(source="alta_formazione_mod_erogazione.id")
    erogationModeDescription = serializers.CharField(
        source="alta_formazione_mod_erogazione.descrizione"
    )
    hours = serializers.IntegerField(source="ore")
    months = serializers.IntegerField(source="mesi")
    language = serializers.CharField(source="lingua")
    courseStructure = serializers.CharField(source="sede_corso")
    minParticipants = serializers.IntegerField(source="num_min_partecipanti")
    maxParticipants = serializers.IntegerField(source="num_max_partecipanti")
    masterYear = serializers.IntegerField(source="anno_rilevazione")
    departmentId = serializers.IntegerField(source="dipartimento_riferimento.dip_id")
    departmentCod = serializers.CharField(source="dipartimento_riferimento.dip_cod")
    departmentName = serializers.CharField(source="dipartimento_riferimento.dip_des_it")
    listenersAccepted = serializers.CharField(source="uditori_ammessi")
    maxListeners = serializers.IntegerField(source="num_max_uditori")
    admissionRequirements = serializers.CharField(source="requisiti_ammissione")
    titleIssued = serializers.CharField(source="titolo_rilasciato")
    doubleTitle = serializers.BooleanField(source="doppio_titolo")
    scientificDirectorId = serializers.SerializerMethodField()
    scientificDirectorName = serializers.CharField(
        source="nome_origine_direttore_scientifico"
    )
    subscriptionFee = serializers.IntegerField(source="quota_iscrizione")
    listenersFee = serializers.IntegerField(source="quota_uditori")
    workFunction = serializers.CharField(source="funzione_lavoro")
    formationObjectivesSummerSchool = serializers.CharField(
        source="obiettivi_formativi_summer_school"
    )
    skills = serializers.CharField(source="competenze")
    jobOpportunities = serializers.CharField(source="sbocchi_occupazionali")
    courseObjectives = serializers.CharField(source="obiettivi_formativi_corso")
    finalTestMode = serializers.CharField(source="modalita_svolgimento_prova_finale")
    numModules = serializers.IntegerField(source="numero_moduli")
    internship = serializers.CharField(source="stage_tirocinio")
    internshipHours = serializers.IntegerField(source="ore_stage_tirocinio")
    internshipCFU = serializers.IntegerField(source="cfu_stage")
    internshipMonths = serializers.IntegerField(source="mesi_stage")
    typeCompaniesInternship = serializers.CharField(
        source="tipo_aziende_enti_tirocinio"
    )
    contentTimesCriteriaCFU = serializers.CharField(
        source="contenuti_tempi_criteri_cfu"
    )
    projectWork = serializers.CharField(source="project_work")

    partners = serializers.SerializerMethodField()
    selections = serializers.SerializerMethodField()
    internalScientificCouncil = serializers.SerializerMethodField()
    externalScientificCouncil = serializers.SerializerMethodField()
    teachingPlan = serializers.SerializerMethodField()
    teachingAssignments = serializers.SerializerMethodField()

    def get_scientificDirectorId(self, obj):
        return encrypt(obj.matricola_direttore_scientifico)

    def get_partners(self, obj):
        return [
            {
                "id": p.id,
                "denomination": p.denominazione,
                "type": p.tipologia,
                "URL": p.sito_web,
            }
            for p in getattr(obj, "partners")
        ]

    def get_selections(self, obj):
        return [
            {"id": s.id, "type": s.tipo_selezione} for s in getattr(obj, "selections")
        ]

    def get_internalScientificCouncil(self, obj):
        return [
            {"id": encrypt(c.matricola_cons), 
             "name": c.nome_origine_cons}
            for c in getattr(obj, "internal_scientific_council")
        ]

    def get_externalScientificCouncil(self, obj):
        return [
            {"name": c.nome_cons, "role": c.ruolo_cons, "institution": c.ente_cons}
            for c in getattr(obj, "external_scientific_council")
        ]

    def get_teachingPlan(self, obj):
        return [
            {
                "module": p.modulo,
                "ssd": p.ssd,
                "hours": p.num_ore,
                "cfu": p.cfu,
                "finalTest": p.verifica_finale,
            }
            for p in getattr(obj, "teaching_plan")
        ]

    def get_teachingAssignments(self, obj):
        return [
            {
                "module": a.modulo,
                "hours": a.num_ore,
                "teacher": a.docente,
                "qualification": a.qualifica,
                "institution": a.ente,
                "type": a.tipologia,
            }
            for a in getattr(obj, "teaching_assignments")
        ]

    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "masterTitle",
            "typeId",
            "typeDescription",
            "erogationMode",
            "erogationModeDescription",
            "hours",
            "months",
            "language",
            "courseStructure",
            "minParticipants",
            "maxParticipants",
            "masterYear",
            "departmentId",
            "departmentCod",
            "departmentName",
            "listenersAccepted",
            "maxListeners",
            "admissionRequirements",
            "titleIssued",
            "doubleTitle",
            "scientificDirectorId",
            "scientificDirectorName",
            "subscriptionFee",
            "listenersFee",
            "workFunction",
            "formationObjectivesSummerSchool",
            "skills",
            "jobOpportunities",
            "courseObjectives",
            "finalTestMode",
            "numModules",
            "internship",
            "internshipHours",
            "internshipCFU",
            "internshipMonths",
            "typeCompaniesInternship",
            "contentTimesCriteriaCFU",
            "projectWork",
            "partners",
            "selections",
            "internalScientificCouncil",
            "externalScientificCouncil",
            "teachingPlan",
            "teachingAssignments",
        ]
        language_field_map = {
            "masterTitle": {"it": "titolo_it", "en": "titolo_en"},
            "departmentName": {
                "it": "dipartimento_riferimento.dip_des_it",
                "en": "dipartimento_riferimento.dip_des_eng",
            },
        }


class HighFormationCourseTypesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="tipo_corso_descr")

    class Meta:
        model = AltaFormazioneTipoCorso
        fields = ["id", "description"]


class ErogationModesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="descrizione")

    class Meta:
        model = AltaFormazioneModalitaErogazione
        fields = ["id", "description"]
