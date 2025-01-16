from rest_framework import serializers
from generics.utils import encrypt
from phd.settings import PHD_CYCLES
from rest_framework import serializers


class PhdActivitiesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        cycle_des = ""
        for cycle in PHD_CYCLES:
            if cycle[0] == query["ciclo"]:
                cycle_des = cycle[1]
                break

        main_teachers = None
        if query.get("MainTeachers") is not None:
            main_teachers = PhdActivitiesSerializer.to_dict_teachers(
                query["MainTeachers"]
            )
        other_teachers = None
        if query.get("OtherTeachers") is not None:
            other_teachers = PhdActivitiesSerializer.to_dict_teachers(
                query["OtherTeachers"]
            )

        tipologia = None
        if query["tipologia_obj"]:
            tipologia = (
                query["tipologia_obj"].nome_it
                if req_lang == "it" or query["tipologia_obj"].nome_en is None
                else query["tipologia_obj"].nome_en
            )

        return {
            "ID": query["id"],
            "ActivityName": query["nome_af"],
            "SSD": query["ssd"],
            "Hours": query["numero_ore"],
            "CFU": query["cfu"],
            "ActivityType": query["tipo_af"],
            "ActivityTypology": tipologia,
            "ReferentPhd": query["rif_dottorato"],
            "Cycle": cycle_des,
            "ReferentStructureId": query["struttura_proponente"],
            "ReferentStructureName": query["struttura_proponente_origine"],
            "ActivityContents": query["contenuti_af"],
            "Prerequisities": query["prerequisiti"],
            "MinStudents": query["num_min_studenti"],
            "MaxStudents": query["num_max_studenti"],
            "FinalTest": query["verifica_finale"],
            "FinalTestMode": query["modalita_verifica"],
            "ActivityStart": query["avvio"],
            "ActivityEnd": query["fine"],
            "ClassroomsTimetable": query["orario_aule"],
            "ShowTimetable": query["visualizza_orario"],
            "Notes": query["note"],
            "MainTeachers": main_teachers,
            "OtherTeachers": other_teachers,
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q["cognome_nome_origine"]
            result.append(
                {
                    "PersonId": encrypt(q["matricola"]),
                    "PersonName": full_name,
                }
            )
        return result


class RefPhdSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ReferentPhd": query["rif_dottorato"],
        }


class RefStructuresSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ReferentStructureName": query["struttura_proponente_origine"],
        }


class PhdSsdListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "SSD": query["ssd"],
        }


class PhdActivityTypeSerializer(serializers.Serializer):  # pragma: no cover
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ActivityType": query["tipo_af"],
        }


class PhdActivityTypologySerializer(serializers.Serializer):  # pragma: no cover
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ID": query.id,
            "Name": query.nome_it
            if req_lang == "it" or query.nome_en is None
            else query.nome_en,
        }


class PhdSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "AcademicYear": query["idesse3_ddr__aa_regdid_id"],
            "DepartmentID": query["dip_cod__dip_id"],
            "DepartmentCod": query["dip_cod__dip_cod"],
            "DepartmentName": query["dip_cod__dip_des_it"]
            if req_lang == "it" or not query["dip_cod__dip_des_eng"]
            else query["dip_cod__dip_des_eng"],
            "PhdCdsCOD": query["cds_cod"],
            "PhdCdsName": query["cdsord_des"],
            "PhdRegID": query["idesse3_ddr__regdid_id_esse3"],
            "PhdRegCOD": query["idesse3_ddr__regdid_cod"],
            "PhdCdSDuration": query["durata_anni"],
            "PhdCdSECTS": query["valore_min"],
            "PhdCdSAttendance": query["idesse3_ddr__frequenza_obbligatoria"],
            "CourseType": query["tipo_corso_cod"],
            "CourseName": query["tipo_corso_des"],
            "CycleNumber": query["idesse3_ddr__num_ciclo"],
            "StudyPlanCOD": query["idesse3_ddpds__pds_cod"],
            "StudyPlanDes": query["idesse3_ddpds__pds_des"],
        }
