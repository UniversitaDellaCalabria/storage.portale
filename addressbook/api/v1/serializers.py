from addressbook.settings import ALLOWED_PROFILE_ID, PERSON_CONTACTS_TO_TAKE
from generics.serializers import CreateUpdateAbstract
from generics.utils import encrypt


class AddressbookSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en", full=False):
        full_name = (
            query["cognome"]
            + " "
            + query["nome"]
            + (" " + query["middle_name"] if query["middle_name"] is not None else "")
        )

        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(query["Roles"], full)

        return {
            "Name": full_name,
            "ID": encrypt(query["matricola"]),
            "Roles": roles,
            "OfficeReference": query["Riferimento Ufficio"]
            if "Riferimento Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Email": query["Posta Elettronica"]
            if "Posta Elettronica" in PERSON_CONTACTS_TO_TAKE
            else [],
            "PEC": query["POSTA ELETTRONICA CERTIFICATA"]
            if "POSTA ELETTRONICA CERTIFICATA" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelOffice": query["Telefono Ufficio"]
            if "Telefono Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelCelOffice": query["Telefono Cellulare Ufficio"]
            if "Telefono Cellulare Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Fax": query["Fax"] if "Fax" in PERSON_CONTACTS_TO_TAKE else [],
            "WebSite": query["URL Sito WEB"]
            if "URL Sito WEB" in PERSON_CONTACTS_TO_TAKE
            else [],
            "CV": query["URL Sito WEB Curriculum Vitae"]
            if "URL Sito WEB Curriculum Vitae" in PERSON_CONTACTS_TO_TAKE
            else [],
            # 'Teacher': query['fl_docente'],
            # ~ "ProfileId": query["profilo"],
            # ~ "ProfileDescription": query["ds_profilo"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
            # ~ "ProfileShortDescription": query["ds_profilo_breve"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
        }

    @staticmethod
    def to_dict_roles(query, full=False):
        roles = []
        for q in query:
            d_data = {
                "Role": q["cd_ruolo"],
                "RoleDescription": q["ds_ruolo"],
                "Priority": q["priorita"],
                "StructureCod": q["cd_uo_aff_org"],
                "Structure": q["ds_aff_org"],
                "StructureTypeCOD": q["cd_tipo_nodo"],
                "ProfileId": q["cd_profilo"] if q["cd_profilo"] in ALLOWED_PROFILE_ID else None,
                "ProfileDescription": q["ds_profilo"] if q["cd_profilo"] in ALLOWED_PROFILE_ID else None
            }
            if full:
                d_data["Start"] = q.get("dt_rap_ini")
            roles.append(d_data)
        return roles


class AddressbookFullSerializer(AddressbookSerializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower(), True))
        return data

    @staticmethod
    def to_dict(query, req_lang="en", full=False):
        full_name = query["nome"] + (
            " " + query["middle_name"] if query["middle_name"] is not None else ""
        )

        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(query["Roles"], full)

        return {
            "Name": full_name,
            "Surname": query["cognome"],
            "ID": query["matricola"],
            "Taxpayer_ID": query["cod_fis"],
            "Roles": roles,
            "OfficeReference": query["Riferimento Ufficio"]
            if "Riferimento Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Email": query["Posta Elettronica"]
            if "Posta Elettronica" in PERSON_CONTACTS_TO_TAKE
            else [],
            "PEC": query["POSTA ELETTRONICA CERTIFICATA"]
            if "POSTA ELETTRONICA CERTIFICATA" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelOffice": query["Telefono Ufficio"]
            if "Telefono Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelCelOffice": query["Telefono Cellulare Ufficio"]
            if "Telefono Cellulare Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Fax": query["Fax"] if "Fax" in PERSON_CONTACTS_TO_TAKE else [],
            "WebSite": query["URL Sito WEB"]
            if "URL Sito WEB" in PERSON_CONTACTS_TO_TAKE
            else [],
            "CV": query["URL Sito WEB Curriculum Vitae"]
            if "URL Sito WEB Curriculum Vitae" in PERSON_CONTACTS_TO_TAKE
            else [],
            # 'Teacher': query['fl_docente'],
            # ~ "ProfileId": query["profilo"],
            # ~ "ProfileDescription": query["ds_profilo"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
            # ~ "ProfileShortDescription": query["ds_profilo_breve"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
        }


class PersonaleSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en", full=False):
        middle_name = f" {query['middle_name']} " if query["middle_name"] else " "
        full_name = f"{query['nome']}{middle_name}{query['cognome']}"
        functions = None
        if query["Functions"] is not None:
            functions = PersonaleSerializer.to_dict_functions(query["Functions"])
        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(query["Roles"], full)

        return {
            "Name": full_name,
            "ID": encrypt(query["matricola"]),
            "Roles": roles,
            "OfficeReference": query["Riferimento Ufficio"]
            if "Riferimento Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Email": query["Posta Elettronica"]
            if "Posta Elettronica" in PERSON_CONTACTS_TO_TAKE
            else [],
            "PEC": query["POSTA ELETTRONICA CERTIFICATA"]
            if "POSTA ELETTRONICA CERTIFICATA" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelOffice": query["Telefono Ufficio"]
            if "Telefono Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TelCelOffice": query["Telefono Cellulare Ufficio"]
            if "Telefono Cellulare Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Fax": query["Fax"] if "Fax" in PERSON_CONTACTS_TO_TAKE else [],
            "WebSite": query["URL Sito WEB"]
            if "URL Sito WEB" in PERSON_CONTACTS_TO_TAKE
            else [],
            "CV": query["URL Sito WEB Curriculum Vitae"]
            if "URL Sito WEB Curriculum Vitae" in PERSON_CONTACTS_TO_TAKE
            else [],
            "Teacher": query["fl_docente"] or query["cop_teacher"],
            "PersonFunctions": functions,
            "TeacherCVFull": query["cv_full_it"]
            if req_lang == "it" or not query["cv_full_eng"]
            else query["cv_full_eng"],
            "TeacherCVShort": query["cv_short_it"]
            if req_lang == "it" or not query["cv_short_eng"]
            else query["cv_short_eng"],
            # ~ "ProfileId": query["profilo"],
            # ~ "ProfileDescription": query["ds_profilo"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
            # ~ "ProfileShortDescription": query["ds_profilo_breve"]
            # ~ if query["profilo"] in ALLOWED_PROFILE_ID
            # ~ else None,
        }

    @staticmethod
    def to_dict_functions(query):
        functions = []
        for q in query:
            functions.append(
                {
                    "TeacherRole": q["ds_funzione"],
                    "FunctionCod": q["funzione"],
                    "StructureCod": q["cd_csa__uo"],
                    "StructureName": q["cd_csa__denominazione"],
                }
            )
        return functions


class PersonaleFullSerializer(PersonaleSerializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower(), True))
        return data

    @staticmethod
    def to_dict(query, req_lang="en", full=False):
        middle_name = f" {query['middle_name']} " if query["middle_name"] else " "
        full_name = f"{query['nome']}{middle_name}"
        functions = None
        if query["Functions"] is not None:
            functions = PersonaleSerializer.to_dict_functions(query["Functions"])
        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(query["Roles"], full)

        return {
            "Name": full_name,
            "Surname": query["cognome"],
            "ID": query["matricola"],
            "Taxpayer_ID": query["cod_fis"],
            "Roles": roles,
            "OfficeReference": query["Riferimento Ufficio"] if "Riferimento Ufficio" in PERSON_CONTACTS_TO_TAKE else [],
            "Email": query["Posta Elettronica"] if "Posta Elettronica" in PERSON_CONTACTS_TO_TAKE else [],
            "PEC": query["POSTA ELETTRONICA CERTIFICATA"] if "POSTA ELETTRONICA CERTIFICATA" in PERSON_CONTACTS_TO_TAKE else [],
            "TelOffice": query["Telefono Ufficio"] if "Telefono Ufficio" in PERSON_CONTACTS_TO_TAKE else [],
            "TelCelOffice": query["Telefono Cellulare Ufficio"] if "Telefono Cellulare Ufficio" in PERSON_CONTACTS_TO_TAKE else [],
            "Fax": query["Fax"] if "Faxe" in PERSON_CONTACTS_TO_TAKE else [],
            "WebSite": query["URL Sito WEB"] if "URL Sito WEB" in PERSON_CONTACTS_TO_TAKE else [],
            "CV": query["URL Sito WEB Curriculum Vitae"] if "URL Sito WEB Curriculum Vitae" in PERSON_CONTACTS_TO_TAKE else [],
            "Teacher": query["fl_docente"] or query["cop_teacher"],
            "PersonFunctions": functions,
            "TeacherCVFull": query["cv_full_it"] if req_lang == "it" or not query["cv_full_eng"] else query["cv_full_eng"],
            "TeacherCVShort": query["cv_short_it"] if req_lang == "it" or not query["cv_short_eng"] else query["cv_short_eng"],
            # ~ "ProfileId": query["profilo"],
            # ~ "ProfileDescription": query["ds_profilo"] if query["profilo"] in ALLOWED_PROFILE_ID else None,
            # ~ "ProfileShortDescription": query["ds_profilo_breve"] if query["profilo"] in ALLOWED_PROFILE_ID else None,
            "Gender": query["cd_genere"]
        }


class AddressbookStructuresSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):  # pragma: no cover
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StructureCod": query["uo"],
            "StructureName": query["denominazione"],
            "StructureTypeName": query["cd_tipo_nodo"],
            "StructureTypeCOD": query["ds_tipo_nodo"],
        }


class RolesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "Role": query["cd_ruolo"],
            "RoleDescription": query["ds_ruolo_locale"],
        }


class PersonnelCfSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):  # pragma: no cover
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        full_name = (
            query["cognome"]
            + " "
            + query["nome"]
            + (" " + query["middle_name"] if query["middle_name"] is not None else "")
        )  # pragma: no cover
        return {
            "Name": full_name,
            "CF": query["cod_fis"],
            "ID": query["matricola"],
            "RoleDescription": query["ds_ruolo_locale"],
            "Role": query["cd_ruolo"],
            "InfrastructureId": query["cd_uo_aff_org"],
            "InfrastructureDescription": query["ds_aff_org"],
        }


class SortingContactsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        full_name = (
            query["personale__cognome"]
            + " "
            + query["personale__nome"]
            + (
                " " + query["personale__middle_name"]
                if query["personale__middle_name"] is not None
                else ""
            )
        )
        return {
            "Name": full_name,
            "ID": encrypt(query["personale__matricola"]),
            "TeacherDepartmentID": query["personale__cd_uo_aff_org"],
            "TeacherOffice": query["personale__ds_aff_org"],
            "DepartmentURL": query["DepartmentUrl"],
        }
