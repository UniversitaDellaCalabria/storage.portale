from generics.serializers import CreateUpdateAbstract
from generics.utils import build_media_path, encrypt


class LaboratoryDetailSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        erc0 = LaboratoryDetailSerializer.to_dict_erc0(
            query["LaboratoryErc1"], req_lang
        )
        research_personnel = LaboratoryDetailSerializer.to_dict_research_personnel(
            query["ResearchPersonnel"]
        )
        tech_personnel = LaboratoryDetailSerializer.to_dict_tech_personnel(
            query["TechPersonnel"]
        )
        offered_services = LaboratoryDetailSerializer.to_dict_offered_services(
            query["OfferedServices"]
        )
        scopes = LaboratoryDetailSerializer.to_dict_scopes(query["Scopes"])
        if query["Location"] is None:
            location = None
        else:
            location = LaboratoryDetailSerializer.to_dict_location(query["Location"])
        extra_departments = LaboratoriesSerializer.to_dict_extra_departments(
            query["ExtraDepartments"], req_lang
        )

        return {
            "LaboratoryId": query["id"],
            "CompletionReferentId": encrypt(query["matricola_referente_compilazione"]),
            "CompletionReferentName": query["referente_compilazione"],
            "ScientificDirectorId": encrypt(
                query["matricola_responsabile_scientifico"]
            ),
            "ScientificDirectorName": query["responsabile_scientifico"],
            "ScientificDirectorEmail": query["email"],
            "LaboratoryName": query["nome_laboratorio"],
            "LaboratoryAcronym": query["acronimo"],
            "LaboratoryLogo": build_media_path(query["nome_file_logo"]),
            "LaboratoryEquipment": query["strumentazione_descrizione"],
            "DepartmentReferentId": query["id_dipartimento_riferimento__dip_id"],
            "DepartmentReferentCod": query["id_dipartimento_riferimento__dip_cod"],
            "DepartmentReferentName": query["id_dipartimento_riferimento__dip_des_it"]
            if req_lang == "it"
            or query["id_dipartimento_riferimento__dip_des_eng"] is None
            else query["id_dipartimento_riferimento__dip_des_eng"],
            "InfrastructureId": query["id_infrastruttura_riferimento__id"],
            "InfrastructureName": query["id_infrastruttura_riferimento__descrizione"],
            "Interdepartmental": query["laboratorio_interdipartimentale"],
            "ExtraDepartments": extra_departments,
            "LaboratoryScope": query["ambito"],
            "LaboratoryServicesScope": query["finalita_servizi_it"]
            if req_lang == "it" or query["finalita_servizi_en"] is None
            else query["finalita_servizi_en"],
            "LaboratoryResearchScope": query["finalita_ricerca_it"]
            if req_lang == "it" or query["finalita_ricerca_en"] is None
            else query["finalita_ricerca_en"],
            "LaboratoryTeachingScope": query["finalita_didattica_it"]
            if req_lang == "it" or query["finalita_didattica_en"] is None
            else query["finalita_didattica_en"],
            "LaboratoryScopes": scopes,
            "LaboratoryErc1": erc0,
            "LaboratoryResearchPersonnel": research_personnel,
            "LaboratoryTechPersonnel": tech_personnel,
            "LaboratoryOfferedServices": offered_services,
            "LaboratoryLocation": location,
            "LaboratoryURL": query["sito_web"],
            "Visible": query["visibile"],
        }

    @staticmethod
    def to_dict_scopes(query, lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "ScopeID": q["id_tipologia_attivita__id"],
                    "ScopeDescription": q["id_tipologia_attivita__descrizione"],
                }
            )
        return result

    @staticmethod
    def to_dict_erc0(query, req_lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "IdErc0": q["id_ricerca_erc1__ricerca_erc0_cod__erc0_cod"],
                    "Description": q["id_ricerca_erc1__ricerca_erc0_cod__description"]
                    if req_lang == "it"
                    or q["id_ricerca_erc1__ricerca_erc0_cod__description_en"] is None
                    else q["id_ricerca_erc1__ricerca_erc0_cod__description_en"],
                    "Erc1List": LaboratoryDetailSerializer.to_dict_erc1_list(
                        q["Erc1"], req_lang
                    ),
                }
            )
        return result

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):
        result = []

        for q in query:
            result.append(
                {
                    "IdErc1": q["id_ricerca_erc1__cod_erc1"],
                    "Description": q["id_ricerca_erc1__descrizione"],
                }
            )
        return result

    @staticmethod
    def to_dict_research_personnel(query):
        result = []
        for q in query:
            if q["matricola_personale_ricerca__matricola"] is None:
                full_name = None
            else:
                full_name = (
                    q["matricola_personale_ricerca__cognome"]
                    + " "
                    + q["matricola_personale_ricerca__nome"]
                    + (
                        " " + q["matricola_personale_ricerca__middle_name"]
                        if q["matricola_personale_ricerca__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "ResearchPersonnelID": encrypt(
                        q["matricola_personale_ricerca__matricola"]
                    ),
                    "ResearchPersonnelName": full_name,
                    "ResearchPersonnelEmail": q["email"],
                }
            )
        return result

    @staticmethod
    def to_dict_tech_personnel(query):
        result = []
        for q in query:
            if q["matricola_personale_tecnico__matricola"] is None:
                full_name = None
            else:
                full_name = (
                    q["matricola_personale_tecnico__cognome"]
                    + " "
                    + q["matricola_personale_tecnico__nome"]
                    + (
                        " " + q["matricola_personale_tecnico__middle_name"]
                        if q["matricola_personale_tecnico__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "TechPersonnelID": encrypt(
                        q["matricola_personale_tecnico__matricola"]
                    ),
                    "TechPersonnelName": full_name,
                    "TechPersonnelRole": q["ruolo"],
                    "TechPersonnelEmail": q["email"],
                }
            )
        return result

    @staticmethod
    def to_dict_offered_services(query):
        result = []
        for q in query:
            result.append(
                {
                    "ServiceName": q["nome_servizio"],
                    "ServiceDescription": q["descrizione_servizio"],
                }
            )
        return result

    @staticmethod
    def to_dict_location(query):
        result = {
            "LocationBuilding": query["edificio"],
            "LocationFloor": query["piano"],
            "LocationNotes": query["note"],
        }
        return result


class LaboratoriesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        extra_departments = LaboratoriesSerializer.to_dict_extra_departments(
            query["ExtraDepartments"], req_lang
        )
        research_personnel = LaboratoriesSerializer.to_dict_research_personnel(
            query["ResearchPersonnel"]
        )
        tech_personnel = LaboratoriesSerializer.to_dict_tech_personnel(
            query["TechPersonnel"]
        )
        scopes = LaboratoriesSerializer.to_dict_scopes(query["Scopes"])

        return {
            "LaboratoryId": query["id"],
            "LaboratoryName": query["nome_laboratorio"],
            "LaboratoryAcronym": query["acronimo"],
            "LaboratoryLogo": build_media_path(query["nome_file_logo"]),
            "Area": query["ambito"],
            "DepartmentName": query["dipartimento_riferimento"],
            "DepartmentReferentId": query["id_dipartimento_riferimento__dip_id"],
            "DepartmentReferentCod": query["id_dipartimento_riferimento__dip_cod"],
            "Interdepartmental": query["laboratorio_interdipartimentale"],
            "ExtraDepartments": extra_departments,
            "InfrastructureId": query["id_infrastruttura_riferimento__id"],
            "InfrastructureName": query["id_infrastruttura_riferimento__descrizione"],
            "Dimension": query["sede_dimensione"],
            "ScientificDirector": query["responsabile_scientifico"],
            "ScientificDirectorId": encrypt(
                query["matricola_responsabile_scientifico"]
            ),
            "LaboratoryResearchPersonnel": research_personnel,
            "LaboratoryScopes": scopes,
            "LaboratoryTechPersonnel": tech_personnel,
            "LaboratoryServicesScope": query["finalita_servizi_it"]
            if req_lang == "it" or query["finalita_servizi_en"] is None
            else query["finalita_servizi_en"],
            "LaboratoryResearchScope": query["finalita_ricerca_it"]
            if req_lang == "it" or query["finalita_ricerca_en"] is None
            else query["finalita_ricerca_en"],
            "LaboratoryTeachingScope": query["finalita_didattica_it"]
            if req_lang == "it" or query["finalita_didattica_en"] is None
            else query["finalita_didattica_en"],
            "Visible": query["visibile"],
        }

    @staticmethod
    def to_dict_extra_departments(query, lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "DepartmentID": q["id_dip__dip_cod"],
                    "DepartmentName": q["id_dip__dip_des_it"]
                    if lang == "it" or q["id_dip__dip_des_eng"] is None
                    else q["id_dip__dip_des_eng"],
                }
            )
        return result

    @staticmethod
    def to_dict_scopes(query, lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "ScopeID": q["id_tipologia_attivita__id"],
                    "ScopeDescription": q["id_tipologia_attivita__descrizione"],
                }
            )
        return result

    @staticmethod
    def to_dict_research_personnel(query):
        result = []
        for q in query:
            if q["matricola_personale_ricerca__matricola"] is None:
                full_name = None
            else:
                full_name = (
                    q["matricola_personale_ricerca__cognome"]
                    + " "
                    + q["matricola_personale_ricerca__nome"]
                    + (
                        " " + q["matricola_personale_ricerca__middle_name"]
                        if q["matricola_personale_ricerca__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "ResearchPersonnelID": encrypt(
                        q["matricola_personale_ricerca__matricola"]
                    ),
                    "ResearchPersonnelName": full_name,
                }
            )
        return result

    @staticmethod
    def to_dict_tech_personnel(query):
        result = []
        for q in query:
            if q["matricola_personale_tecnico__matricola"] is None:
                full_name = None
            else:
                full_name = (
                    q["matricola_personale_tecnico__cognome"]
                    + " "
                    + q["matricola_personale_tecnico__nome"]
                    + (
                        " " + q["matricola_personale_tecnico__middle_name"]
                        if q["matricola_personale_tecnico__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "TechPersonnelID": encrypt(
                        q["matricola_personale_tecnico__matricola"]
                    ),
                    "TechPersonnelName": full_name,
                    "TechPersonnelRole": q["ruolo"],
                }
            )
        return result


class LaboratoriesAreasSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "Area": query["ambito"],
        }


class LaboratoriesScopesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ScopeID": query["id"],
            "ScopeDescription": query["descrizione"],
        }
