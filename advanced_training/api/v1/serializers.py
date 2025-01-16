from rest_framework import serializers
from generics.utils import encrypt


class HighFormationMastersSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        # full_name = query['personale__cognome'] + " " + query['personale__nome'] + \
        #             (" " + query['personale__middle_name']
        #              if query['personale__middle_name'] is not None else "")

        partners = None
        if query.get("Partners") is not None:
            partners = HighFormationMastersSerializer.to_dict_partners(
                query["Partners"]
            )

        selections = None
        if query.get("Selections") is not None:
            selections = HighFormationMastersSerializer.to_dict_selections(
                query["Selections"]
            )

        internal_council = None
        if query.get("InternalCouncil") is not None:
            internal_council = HighFormationMastersSerializer.to_dict_internal_council(
                query["InternalCouncil"]
            )

        external_council = None
        if query.get("ExternalCouncil") is not None:
            external_council = HighFormationMastersSerializer.to_dict_external_council(
                query["ExternalCouncil"]
            )

        teaching_plans = None
        if query.get("TeachingPlan") is not None:
            teaching_plans = HighFormationMastersSerializer.to_dict_teachings_plan(
                query["TeachingPlan"]
            )

        teaching_assignments = None
        if query.get("TeachingAssignments") is not None:
            teaching_assignments = (
                HighFormationMastersSerializer.to_dict_teaching_assignments(
                    query["TeachingAssignments"]
                )
            )
        return {
            "ID": query["id"],
            "MasterTitle": query["titolo_it"]
            if req_lang == "it" or query["titolo_en"] is None
            else query["titolo_en"],
            "HighFormationTypeId": query["alta_formazione_tipo_corso"],
            "HighFormationTypeDescription": query[
                "alta_formazione_tipo_corso__tipo_corso_descr"
            ],
            "HighFormationErogationMode": query["alta_formazione_mod_erogazione"],
            "HighFormationErogationModeDescription": query[
                "alta_formazione_mod_erogazione__descrizione"
            ],
            "HighFormationHours": query["ore"],
            "HighFormationMonths": query["mesi"],
            "HighFormationLanguage": query["lingua"],
            "HighFormationCourseStructure": query["sede_corso"],
            "HighFormationMinParticipants": query["num_min_partecipanti"],
            "HighFormationMaxParticipants": query["num_max_partecipanti"],
            "HighFormationMasterYear": query["anno_rilevazione"],
            "DepartmentId": query["dipartimento_riferimento"],
            "DepartmentCod": query["dipartimento_riferimento__dip_cod"],
            "DepartmentName": query["dipartimento_riferimento__dip_des_it"]
            if req_lang == "it"
            or query["dipartimento_riferimento__dip_des_eng"] is None
            else query["dipartimento_riferimento__dip_des_eng"],
            "ListenersAccepted": query["uditori_ammessi"],
            "MaxListeners": query["num_max_uditori"],
            "AdmissionRequirements": query["requisiti_ammissione"],
            "TitleIssued": query["titolo_rilasciato"],
            "DoubleTitle": query["doppio_titolo"],
            "ScientificDirectorId": encrypt(query["matricola_direttore_scientifico"]),
            "ScientificDirectorName": query["nome_origine_direttore_scientifico"],
            "SubscriptionFee": query["quota_iscrizione"],
            "ListenersFee": query["quota_uditori"],
            "WorkFunction": query["funzione_lavoro"],
            "FormationObjectivesSummerSchool": query[
                "obiettivi_formativi_summer_school"
            ],
            "Skills": query["competenze"],
            "JobOpportunities": query["sbocchi_occupazionali"],
            "CourseObjectives": query["obiettivi_formativi_corso"],
            "FinalTestMode": query["modalita_svolgimento_prova_finale"],
            "NumModules": query["numero_moduli"],
            "Internship": query["stage_tirocinio"],
            "InternshipHours": query["ore_stage_tirocinio"],
            "InternshipCFU": query["cfu_stage"],
            "InternshipMonths": query["mesi_stage"],
            "TypeCompaniesInternship": query["tipo_aziende_enti_tirocinio"],
            "ContentTimesCriteriaCFU": query["contenuti_tempi_criteri_cfu"],
            "ProjectWork": query["project_work"],
            "HighFormationMasterPartners": partners,
            "HighFormationMasterSelectionModes": selections,
            "HighFormationMasterInternalCouncil": internal_council,
            "HighFormationMasterExternalCouncil": external_council,
            "HighFormationMasterTeachingPlans": teaching_plans,
            "HighFormationMasterTeachingAssignments": teaching_assignments,
        }

    @staticmethod
    def to_dict_partners(query):
        result = []
        for q in query:
            result.append(
                {
                    "PartnerId": q["id"],
                    "PartnerDenomination": q["denominazione"],
                    "PartnerType": q["tipologia"],
                    "PartnerURL": q["sito_web"],
                }
            )
        return result

    @staticmethod
    def to_dict_selections(query):
        result = []
        for q in query:
            result.append(
                {"SelectionId": q["id"], "SelectionType": q["tipo_selezione"]}
            )
        return result

    @staticmethod
    def to_dict_internal_council(query):
        result = []
        for q in query:
            full_name = q["nome_origine_cons"]
            result.append(
                {
                    "PersonId": encrypt(q["matricola_cons"]),
                    "PersonName": full_name,
                }
            )
        return result

    @staticmethod
    def to_dict_external_council(query):
        result = []
        for q in query:
            full_name = q["nome_cons"]
            result.append(
                {
                    "PersonName": full_name,
                    "Role": q["ruolo_cons"],
                    "Institution": q["ente_cons"],
                }
            )
        return result

    @staticmethod
    def to_dict_teachings_plan(query):
        result = []
        for q in query:
            result.append(
                {
                    "TeachingPlanModule": q["modulo"],
                    "TeachingPlanSSD": q["ssd"],
                    "TeachingPlanHours": q["num_ore"],
                    "TeachingPlanCFU": q["cfu"],
                    "TeachingPlanFinalTest": q["verifica_finale"],
                }
            )
        return result

    @staticmethod
    def to_dict_teaching_assignments(query):
        result = []
        for q in query:
            result.append(
                {
                    "TeachingAssignmentsModule": q["modulo"],
                    "TeachingAssignmentsHours": q["num_ore"],
                    "TeachingAssignmentsTeachers": q["docente"],
                    "TeachingAssignmentsQualification": q["qualifica"],
                    "TeachingAssignmentsInstitution": q["ente"],
                    "TeachingAssignmentsType": q["tipologia"],
                }
            )
        return result


class HighFormationCourseTypesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {"ID": query["id"], "Description": query["tipo_corso_descr"]}


class ErogationModesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {"ID": query["id"], "Description": query["descrizione"]}
