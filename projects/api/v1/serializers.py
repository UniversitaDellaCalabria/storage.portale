from generics.serializers import CreateUpdateAbstract
from generics.utils import encrypt


class ProjectSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        responsabili = None
        ricercatori = None
        if query.get("Responsabili") is not None:
            responsabili = ProjectSerializer.to_dict_directors(query["Responsabili"])
        if query.get("Ricercatori") is not None:
            ricercatori = ProjectSerializer.to_dict_researchers(query["Ricercatori"])
        return {
            "ProjectId": query["id"],
            "ProjectYear": query["anno_avvio"],
            "InfrastructureId": query["uo"],
            "InfrastructureDescription": query["uo__denominazione"],
            "TerritorialScopeId": query["ambito_territoriale__id"],
            "TerritorialScopeDescription": query[
                "ambito_territoriale__ambito_territoriale"
            ],
            "TypeProgramId": query["tipologia_programma__id"],
            "TypeProgramDescription": query["tipologia_programma__nome_programma"],
            "ProjectTitle": query["titolo"],
            "ProjectDescription": query["descr_breve"],
            "ProjectAbstract": query["abstract_ita"]
            if req_lang == "it" or query["abstract_eng"] is None
            else query["abstract_eng"],
            "TechAreaId": query["area_tecnologica"],
            "TechAreaDescription": query["area_tecnologica__descr_area_ita"]
            if req_lang == "it" or query["area_tecnologica__descr_area_eng"] is None
            else query["area_tecnologica__descr_area_eng"],
            "ProjectImage": query["url_immagine"],
            "ScientificDirectors": responsabili,
            "Researchers": ricercatori,
            "WebSite": query["url_sito_web"],
            "IsActive": query["is_active"],
        }

    @staticmethod
    def to_dict_directors(query):
        result = []
        for q in query:
            full_name = q["nome_origine"]
            result.append(
                {
                    "ScientificDirectorId": encrypt(q["matricola"]),
                    "ScientificDirectorName": full_name,
                }
            )
        return result

    @staticmethod
    def to_dict_researchers(query):
        result = []
        for q in query:
            full_name = q["nome_origine"]
            result.append(
                {
                    "ResearcherId": encrypt(q["matricola"]),
                    "ResearcherName": full_name,
                }
            )
        return result


class ProjectInfrastructuresSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "InfrastructureId": query["uo"],
            "InfrastructureDescription": query["uo__denominazione"],
        }
