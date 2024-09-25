from generics.serializers import CreateUpdateAbstract
from generics.utils import encrypt


class DepartmentSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "DepartmentID": query["dip_id"],
            "DepartmentCod": query["dip_cod"],
            "DepartmentName": query["dip_des_it"]
            if req_lang == "it" or query["dip_des_eng"] is None
            else query["dip_des_eng"],
            "DepartmentNameShort": query["dip_nome_breve"],
            "DepartmentURL": query["dip_url"],
        }


class StructuresSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        d = {
            "StructureCod": query["uo"],
            "StructureName": query["denominazione"],
            "StructureTypeName": query["ds_tipo_nodo"],
            "StructureTypeCOD": query["cd_tipo_nodo"],
        }
        if "dip_url" in query:
            d["StructureURL"] = query["dip_url"]
        if "childs" in query:
            d["StructureChilds"] = query.get("childs", [])
        return d


class StructureTypesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StructureTypeName": query["ds_tipo_nodo"],
            "StructureTypeCOD": query["cd_tipo_nodo"],
        }


class StructureDetailSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        personnel_functions = None
        if query["FunzioniPersonale"] is not None:
            personnel_functions = StructureDetailSerializer.to_dict_personnel_functions(
                query["FunzioniPersonale"]
            )
        return {
            "StructureCod": query["uo"],
            "StructureName": query["denominazione"],
            "StructureTypeName": query["ds_tipo_nodo"],
            "StructureTypeCOD": query["cd_tipo_nodo"],
            "StructureFatherId": query["uo_padre"],
            "StructureFatherName": query["denominazione_padre"],
            "StructureEmail": query["EMAIL"],
            "StructurePec": query["PEC"],
            "StructureTfr": query["TFR"],
            "StructurePersonnelFunctions": personnel_functions,
            "StructureMission": query["ds_mission"],
            "StructureURL": query["dip_url"],
        }

    @staticmethod
    def to_dict_personnel_functions(query):
        result = []
        for q in query:
            if q["cod_fis__matricola"] is None:
                full_name = None
            else:
                full_name = (
                    q["cod_fis__cognome"]
                    + " "
                    + q["cod_fis__nome"]
                    + (
                        " " + q["cod_fis__middle_name"]
                        if q["cod_fis__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "ID": encrypt(q["cod_fis__matricola"]),
                    "Name": full_name,
                    "Function": q["ds_funzione"],
                    "FunctionCod": q["funzione"],
                }
            )
        return result


class InfrastructuresSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "InfrastructureId": query["id"],
            "InfrastructureDescription": query["descrizione"],
        }


class StructureFunctionsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StructureTypeCOD": query["cd_tipo_nod"],
            "Function": query["funzione"],
            "FunctionDescription": query["descr_funzione"],
        }


class TerritorialScopesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "TerritorialScopeId": query["id"],
            "TerritorialScopeDescription": query["ambito_territoriale"],
        }
