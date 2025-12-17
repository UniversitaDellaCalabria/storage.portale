from rest_framework import serializers
from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.utils import encrypt
from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneTipoCorso,
    AltaFormazioneStatusStorico,
)
from organizational_area.models import OrganizationalStructureOfficeEmployee
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING,
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
)


@extend_schema_serializer(examples=examples.HIGH_FORMATION_MASTER_EXAMPLES)
class AdvancedTrainingMastersSerializer(serializers.ModelSerializer):
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
    startDate = serializers.DateField(source="data_inizio")
    endDate = serializers.DateField(source="data_fine")
    financialPlanPath = serializers.CharField(source="path_piano_finanziario")
    deliberationDocPath = serializers.CharField(source="path_doc_delibera")
    proposerId = serializers.SerializerMethodField()
    proposerSurname = serializers.CharField(source="cognome_proponente")
    proposerName = serializers.CharField(source="nome_proponente")
    lastModified = serializers.DateTimeField(source="dt_mod")
    lastModifiedBy = serializers.IntegerField(source="user_mod_id")

    status = serializers.SerializerMethodField()
    statusDescription = serializers.SerializerMethodField()

    partners = serializers.SerializerMethodField()
    selections = serializers.SerializerMethodField()
    internalScientificCouncil = serializers.SerializerMethodField()
    externalScientificCouncil = serializers.SerializerMethodField()
    teachingPlan = serializers.SerializerMethodField()
    teachingAssignments = serializers.SerializerMethodField()
    trainingActivities = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_scientificDirectorId(self, obj):
        return encrypt(obj.matricola_direttore_scientifico)

    @extend_schema_field(serializers.CharField())
    def get_proposerId(self, obj):
        return encrypt(obj.matricola_proponente) if obj.matricola_proponente else None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_status(self, obj):
        """Ottiene il codice dello stato corrente del master"""
        status_storico = (
            AltaFormazioneStatusStorico.objects.filter(id_alta_formazione_dati_base=obj)
            .select_related("id_alta_formazione_status")
            .order_by("-data_status", "-dt_mod", "-id")
            .first()
        )

        if status_storico:
            return status_storico.id_alta_formazione_status.status_cod

        return None  # Bozza (nessuno stato registrato)

    @extend_schema_field(serializers.CharField())
    def get_statusDescription(self, obj):
        """Ottiene la descrizione dello stato corrente del master"""
        status_storico = (
            AltaFormazioneStatusStorico.objects.filter(id_alta_formazione_dati_base=obj)
            .select_related("id_alta_formazione_status")
            .order_by("-data_status", "-dt_mod", "-id")
            .first()
        )

        if status_storico:
            return status_storico.id_alta_formazione_status.status_desc

        return "Bozza"  # Default quando non c'è stato

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
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

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_selections(self, obj):
        return [
            {"id": s.id, "type": s.tipo_selezione} for s in getattr(obj, "selections")
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_internalScientificCouncil(self, obj):
        return [
            {"id": encrypt(c.matricola_cons), "name": c.nome_origine_cons}
            for c in getattr(obj, "internal_scientific_council")
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_externalScientificCouncil(self, obj):
        return [
            {"name": c.nome_cons, "role": c.ruolo_cons, "institution": c.ente_cons}
            for c in getattr(obj, "external_scientific_council")
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
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

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
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

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_trainingActivities(self, obj):
        return [
            {
                "id": t.id,
                "name": t.nome,
                "program": t.programma,
                "bibliography": t.bibliografia,
                "finalTestMode": t.modalita_verifica_finale,
                "parentActivityId": t.alta_formazione_attivita_formativa_padre_id,
            }
            for t in getattr(obj, "training_activities", [])
        ]


    def get_can_edit(self, obj):
        request = self.context.get("request")
        if not request or not request.user:
            return False

        # Superuser può sempre modificare
        if request.user.is_superuser:
            return True

        # Ottieni lo stato corrente
        status = obj.get_current_status()
        status_cod = status.id_alta_formazione_status.status_cod if status else None

        # Può modificare solo in stato 0 o 2
        if status_cod not in ["0", "2", None]:
            return False

        # Ottieni TUTTI gli uffici dell'utente
        user_all_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        # Ottieni i nomi di TUTTI gli uffici
        user_offices_names = list(user_all_offices.values_list("office__name", flat=True))

        user_is_validator = OFFICE_ADVANCED_TRAINING_VALIDATOR in user_offices_names

        # Se è validatore, può modificare usando solo il metodo del model
        if user_is_validator:
            return obj._check_edit_permission(user_offices_names)

        # Se NON è validatore, deve avere un ufficio master nello stesso dipartimento
        department_code = (
            obj.dipartimento_riferimento.dip_cod if obj.dipartimento_riferimento else None
        )

        if not department_code:
            return False

        # Verifica che abbia un ufficio master nello stesso dipartimento
        user_master_offices = user_all_offices.filter(office__name=OFFICE_ADVANCED_TRAINING)

        user_has_same_department = user_master_offices.filter(
            office__organizational_structure__unique_code=department_code
        ).exists()

        if not user_has_same_department:
            return False

        # Infine verifica i permessi generici
        return obj._check_edit_permission(user_offices_names)


    def get_can_delete(self, obj):
        request = self.context.get("request")
        if not request or not request.user:
            return False

        # Superuser può sempre eliminare
        if request.user.is_superuser:
            return True

        # Può eliminare solo in stato Bozza
        status = obj.get_current_status()
        status_cod = status.id_alta_formazione_status.status_cod if status else None

        if status_cod not in ["0", None]:
            return False

        # Ottieni TUTTI gli uffici dell'utente
        user_all_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        # Ottieni i nomi di TUTTI gli uffici
        user_offices_names = list(user_all_offices.values_list("office__name", flat=True))

        user_is_validator = OFFICE_ADVANCED_TRAINING_VALIDATOR in user_offices_names

        # Se è validatore, può eliminare
        if user_is_validator:
            return True

        # Se NON è validatore, deve avere un ufficio master nello stesso dipartimento
        department_code = (
            obj.dipartimento_riferimento.dip_cod if obj.dipartimento_riferimento else None
        )

        if not department_code:
            return False

        # Verifica che abbia un ufficio master nello stesso dipartimento
        user_master_offices = user_all_offices.filter(office__name=OFFICE_ADVANCED_TRAINING)

        user_has_same_department = user_master_offices.filter(
            office__organizational_structure__unique_code=department_code
        ).exists()

        return user_has_same_department

    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "id",
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
            "startDate",
            "endDate",
            "financialPlanPath",
            "deliberationDocPath",
            "proposerId",
            "proposerSurname",
            "proposerName",
            "lastModified",
            "lastModifiedBy",
            "status",
            "statusDescription",
            # LISTE
            "partners",
            "selections",
            "internalScientificCouncil",
            "externalScientificCouncil",
            "teachingPlan",
            "teachingAssignments",
            "trainingActivities",
            "can_edit",
            "can_delete",
        ]
        language_field_map = {
            "masterTitle": {"it": "titolo_it", "en": "titolo_en"},
            "departmentName": {
                "it": "dipartimento_riferimento.dip_des_it",
                "en": "dipartimento_riferimento.dip_des_eng",
            },
        }


@extend_schema_serializer(examples=examples.HIGH_FORMATION_COURSE_TYPES_EXAMPLES)
class AdvancedTrainingCourseTypesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="tipo_corso_descr")

    class Meta:
        model = AltaFormazioneTipoCorso
        fields = ["id", "description"]


@extend_schema_serializer(examples=examples.EROGATION_MODES_EXAMPLES)
class ErogationModesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="descrizione")

    class Meta:
        model = AltaFormazioneModalitaErogazione
        fields = ["id", "description"]
