from generics.serializers import CreateUpdateAbstract
from generics.utils import build_media_path, encrypt


class CompaniesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "SpinoffId": query["id"],
            "SpinoffPIva": query["piva"],
            "SpinoffAgencyName": query["nome_azienda"],
            "SpinoffAgencyUrl": query["url_sito_web"],
            "SpinoffImage": build_media_path(query["nome_file_logo"]),
            "SpinoffDescription": query["descrizione_ita"]
            if req_lang == "it" or query["descrizione_eng"] is None
            else query["descrizione_eng"],
            "SpinoffUnicalReferent": query["referente_unical"],
            "SpinoffUnicalReferentId": encrypt(query["matricola_referente_unical"]),
            "TechAreaId": query["id_area_tecnologica"],
            "TechAreaDescription": query["id_area_tecnologica__descr_area_ita"]
            if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None
            else query["id_area_tecnologica__descr_area_eng"],
            "IsSpinoff": query["is_spinoff"],
            "IsStartup": query["is_startup"],
            "IsActive": query["is_active"],
        }


class TechAreasSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "TechAreaId": query["id"],
            "TechAreaDescription": query["descr_area_ita"]
            if req_lang == "it" or query["descr_area_eng"] is None
            else query["descr_area_eng"],
        }
