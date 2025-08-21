from rest_framework import serializers
from generics.utils import encrypt


class BaseResearchLinesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        teachers = None
        if query["Teachers"] is not None:
            teachers = BaseResearchLinesSerializer.to_dict_teachers(query["Teachers"])
        return {
            "RLineID": query["id"],
            "RLineDescription": query["descrizione"],
            "RLineResults": query["descr_pubblicaz_prog_brevetto"],
            "RYear": query["anno"],
            "RLineErc2ID": query["ricerca_erc2_id__cod_erc2"],
            "RLineErc2Name": query["ricerca_erc2_id__descrizione"],
            "Teachers": teachers,
            "RLineVisibile": query["visibile"],
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = (
                q["personale_id__cognome"]
                + " "
                + q["personale_id__nome"]
                + (
                    " " + q["personale_id__middle_name"]
                    if q["personale_id__middle_name"] is not None
                    else ""
                )
            )
            result.append(
                {
                    "TeacherID": encrypt(q["personale_id__matricola"]),
                    "TeacherName": full_name,
                    "DepartmentName": q["personale_id__ds_sede"],
                    "DepartmentCod": q["personale_id__sede"],
                }
            )
        return result


class AppliedResearchLinesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        teachers = None
        if query["Teachers"] is not None:
            teachers = AppliedResearchLinesSerializer.to_dict_teachers(
                query["Teachers"]
            )
        return {
            "RLineID": query["id"],
            "RLineDescription": query["descrizione"],
            "RLineResults": query["descr_pubblicaz_prog_brevetto"],
            "RYear": query["anno"],
            "RLineAster2Id": query["ricerca_aster2_id__ricerca_aster1_id"],
            "RLineAster2Name": query["ricerca_aster2_id__descrizione"],
            "Teachers": teachers,
            "RLineVisibile": query["visibile"],
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = (
                q["personale_id__cognome"]
                + " "
                + q["personale_id__nome"]
                + (
                    " " + q["personale_id__middle_name"]
                    if q["personale_id__middle_name"] is not None
                    else ""
                )
            )
            result.append(
                {
                    "TeacherID": encrypt(q["personale_id__matricola"]),
                    "TeacherName": full_name,
                    "DepartmentName": q["personale_id__ds_sede"],
                    "DepartmentCod": q["personale_id__sede"],
                }
            )
        return result


class AllResearchLinesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        teachers = None
        if query["Teachers"] is not None:
            teachers = AllResearchLinesSerializer.to_dict_teachers(query["Teachers"])
        if query["Tipologia"] == "base":
            return {
                "RLineID": query["id"],
                "RLineDescription": query["descrizione"],
                "RLineResults": query["descr_pubblicaz_prog_brevetto"],
                "RYear": query["anno"],
                "RLineERC0Id": query[
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__erc0_cod"
                ],
                "RLineERC0Name": query[
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description"
                ]
                if req_lang == "it"
                or query[
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en"
                ]
                is None
                else query[
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en"
                ],
                "RLineERC1Id": query["ricerca_erc2_id__ricerca_erc1_id__cod_erc1"],
                "RLineERC1Name": query["ricerca_erc2_id__ricerca_erc1_id__descrizione"],
                "RLineErc2ID": query["ricerca_erc2_id__cod_erc2"],
                "RLineErc2Name": query["ricerca_erc2_id__descrizione"],
                "Teachers": teachers,
                "RLineVisibile": query["visibile"],
            }
        else:
            return {
                "RLineID": query["id"],
                "RLineDescription": query["descrizione"],
                "RLineResults": query["descr_pubblicaz_prog_brevetto"],
                "RYear": query["anno"],
                "RLineAster2Id": query["ricerca_aster2_id__ricerca_aster1_id"],
                "RLineAster2Name": query["ricerca_aster2_id__descrizione"],
                "Teachers": teachers,
                "RLineVisibile": query["visibile"],
            }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = (
                q["personale_id__cognome"]
                + " "
                + q["personale_id__nome"]
                + (
                    " " + q["personale_id__middle_name"]
                    if q["personale_id__middle_name"] is not None
                    else ""
                )
            )
            result.append(
                {
                    "TeacherID": encrypt(q["personale_id__matricola"])
                    if not q["personale_id__flg_cessato"]
                    else None,
                    "TeacherName": full_name,
                    "DepartmentName": q["personale_id__ds_sede"],
                    "DepartmentCod": q["personale_id__sede"],
                }
            )
        return result


class Erc1Serializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        erc1 = Erc1Serializer.to_dict_erc1_list(query["Erc1"], req_lang)

        return {
            "IdErc0": query["erc0_cod"],
            "Description": query["description"]
            if req_lang == "it" or query["description_en"] is None
            else query["description_en"],
            "Erc1List": erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):
        result = []

        for q in query:
            result.append(
                {
                    "IdErc1": q["cod_erc1"],
                    "Description": q["descrizione"],
                }
            )

        return result


class Erc0Serializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "IdErc0": query["erc0_cod"],
            "Description": query["description"]
            if req_lang == "it" or query["description_en"] is None
            else query["description_en"],
        }


class Erc2Serializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        erc1 = Erc2Serializer.to_dict_erc1_list(query["Erc1"], req_lang)

        return {
            "IdErc0": query["erc0_cod"],
            "Description": query["description"]
            if req_lang == "it" or query["description_en"] is None
            else query["description_en"],
            "Erc1List": erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "IdErc1": q["cod_erc1"],
                    "Description": q["descrizione"],
                    "Erc2List": Erc2Serializer.to_dict_erc2_list(q["Erc2"], req_lang),
                }
            )
        return result

    @staticmethod
    def to_dict_erc2_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "CodErc2": q["cod_erc2"],
                    "Description": q["descrizione"],
                }
            )
        return result


class Asters1Serializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        aster1 = Asters1Serializer.to_dict_aster1_list(query["Aster1"], req_lang)

        return {
            "IdErc0": query["erc0_cod"],
            "Description": query["description"]
            if req_lang == "it" or query["description_en"] is None
            else query["description_en"],
            "Aster1List": aster1,
        }

    @staticmethod
    def to_dict_aster1_list(query, req_lang="en"):
        result = []

        for q in query:
            result.append(
                {
                    "IdAster1": q["id"],
                    "Description": q["descrizione"],
                }
            )

        return result


class Asters2Serializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        aster1 = Asters2Serializer.to_dict_aster1_list(query["Aster1"], req_lang)

        return {
            "IdErc0": query["erc0_cod"],
            "Description": query["description"]
            if req_lang == "it" or query["description_en"] is None
            else query["description_en"],
            "Aster1List": aster1,
        }

    @staticmethod
    def to_dict_aster1_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "IdAster1": q["id"],
                    "Description": q["descrizione"],
                    "Aster2List": Asters2Serializer.to_dict_aster2_list(
                        q["Aster2"], req_lang
                    ),
                }
            )
        return result

    @staticmethod
    def to_dict_aster2_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append(
                {
                    "IdAster2": q["id"],
                    "Description": q["descrizione"],
                }
            )
        return result
