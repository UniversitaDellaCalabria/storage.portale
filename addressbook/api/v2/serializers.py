from rest_framework import serializers

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from addressbook.models import Personale
from structures.models import UnitaOrganizzativa
from generics.utils import encrypt
from addressbook.settings import (
    ALLOWED_PROFILE_ID,
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)


class AddressbookSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    officeReference = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    pec = serializers.SerializerMethodField()
    telOffice = serializers.SerializerMethodField()
    telCelOffice = serializers.SerializerMethodField()
    fax = serializers.SerializerMethodField()
    webSite = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()
    profileId = serializers.CharField(source="profilo")
    profileDescription = serializers.SerializerMethodField()
    profileShortDescription = serializers.SerializerMethodField()

    def get_name(self, obj):
        return (
            obj.cognome + " " + obj.nome
            if obj.middle_name is None
            else obj.cognome + " " + obj.nome + " " + obj.middle_name
        )

    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    def get_id(self, obj):
        return encrypt(obj.matricola)

    def get_contacts(self, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    def get_officeReference(self, obj):
        return self.get_contacts(obj, "Riferimento Ufficio")

    def get_email(self, obj):
        return self.get_contacts(obj, "Posta Elettronica")

    def get_pec(self, obj):
        return self.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    def get_telOffice(self, obj):
        return self.get_contacts(obj, "Telefono Ufficio")

    def get_telCelOffice(self, obj):
        return self.get_contacts(obj, "Telefono Cellulare Ufficio")

    def get_fax(self, obj):
        return self.get_contacts(obj, "Fax")

    def get_webSite(self, obj):
        return self.get_contacts(obj, "URL Sito WEB")

    def get_cv(self, obj):
        return self.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    def get_roles(self, obj):
        for role in obj.pers_attivo_tutti_ruoli:
            struct = role.cd_uo_aff_org
            return [
                {
                    "role": role.cd_ruolo,
                    "description": role.ds_ruolo,
                    "priorita": role.priorita,
                    "structureCod": struct.pk,
                    "structure": role.ds_aff_org,
                    "structureTypeCOD": struct.cd_tipo_nodo,
                }
            ]

    class Meta:
        model = Personale
        fields = [
            "name",
            "id",
            "roles",
            "officeReference",
            "email",
            "pec",
            "telOffice",
            "telCelOffice",
            "fax",
            "webSite",
            "cv",
            "profileId",
            "profileDescription",
            "profileShortDescription",
        ]


class AddressbookFullSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    surname = serializers.CharField(source="cognome")
    id = serializers.CharField(source="matricola")
    taxpayer_ID = serializers.CharField(source="cod_fis")
    roles = serializers.SerializerMethodField()
    officeReference = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    pec = serializers.SerializerMethodField()
    telOffice = serializers.SerializerMethodField()
    telCelOffice = serializers.SerializerMethodField()
    fax = serializers.SerializerMethodField()
    webSite = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()
    profileId = serializers.CharField(source="profilo")
    profileDescription = serializers.SerializerMethodField()
    profileShortDescription = serializers.SerializerMethodField()

    def get_name(self, obj):
        return (
            obj.cognome + " " + obj.nome
            if obj.middle_name is None
            else obj.cognome + " " + obj.nome + " " + obj.middle_name
        )

    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    def get_id(self, obj):
        return encrypt(obj.matricola)

    def get_contacts(self, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    def get_officeReference(self, obj):
        return self.get_contacts(obj, "Riferimento Ufficio")

    def get_email(self, obj):
        return self.get_contacts(obj, "Posta Elettronica")

    def get_pec(self, obj):
        return self.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    def get_telOffice(self, obj):
        return self.get_contacts(obj, "Telefono Ufficio")

    def get_telCelOffice(self, obj):
        return self.get_contacts(obj, "Telefono Cellulare Ufficio")

    def get_fax(self, obj):
        return self.get_contacts(obj, "Fax")

    def get_webSite(self, obj):
        return self.get_contacts(obj, "URL Sito WEB")

    def get_cv(self, obj):
        return self.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    def get_roles(self, obj):
        for role in obj.pers_attivo_tutti_ruoli:
            struct = role.cd_uo_aff_org
            return [
                {
                    "role": role.cd_ruolo,
                    "description": role.ds_ruolo,
                    "priorita": role.priorita,
                    "structureCod": struct.pk,
                    "structure": role.ds_aff_org,
                    "structureTypeCOD": struct.cd_tipo_nodo,
                    "dateRapIni": role.dt_rap_ini
                }
            ]

    class Meta:
        model = Personale
        fields = [
            "name",
            "surname",
            "id",
            "taxpayer_ID",
            "roles",
            "officeReference",
            "email",
            "pec",
            "telOffice",
            "telCelOffice",
            "fax",
            "webSite",
            "cv",
            "profileId",
            "profileDescription",
            "profileShortDescription",
        ]


class AddressbookDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    officeReference = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    pec = serializers.SerializerMethodField()
    telOffice = serializers.SerializerMethodField()
    telCelOffice = serializers.SerializerMethodField()
    fax = serializers.SerializerMethodField()
    webSite = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    teacherCVFull = serializers.CharField(source="cv_full_it")
    teacherCVShort = serializers.CharField(source="cv_short_it")
    personFunctions = serializers.SerializerMethodField()
    profileId = serializers.CharField(source="profilo")
    profileDescription = serializers.SerializerMethodField()
    profileShortDescription = serializers.SerializerMethodField()
    
    def get_personFunctions(self, obj):
            return [
                {
                    "teacherRole": f.ds_funzione,
                    "tunctionCod": f.funzione,
                    "structureCod": f.cd_csa.uo,
                    "structureName": f.cd_csadenominazione,
                }
                for f in obj.functions
            ]
    
    def get_teacher(self, obj):
        return obj.fl_docente or obj.cop_teacher

    def get_name(self, obj):
        return (
            obj.cognome + " " + obj.nome
            if obj.middle_name is None
            else obj.cognome + " " + obj.nome + " " + obj.middle_name
        )

    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    def get_id(self, obj):
        return encrypt(obj.matricola)

    def get_contacts(self, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    def get_officeReference(self, obj):
        return self.get_contacts(obj, "Riferimento Ufficio")

    def get_email(self, obj):
        return self.get_contacts(obj, "Posta Elettronica")

    def get_pec(self, obj):
        return self.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    def get_telOffice(self, obj):
        return self.get_contacts(obj, "Telefono Ufficio")

    def get_telCelOffice(self, obj):
        return self.get_contacts(obj, "Telefono Cellulare Ufficio")

    def get_fax(self, obj):
        return self.get_contacts(obj, "Fax")

    def get_webSite(self, obj):
        return self.get_contacts(obj, "URL Sito WEB")

    def get_cv(self, obj):
        return self.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    def get_roles(self, obj):
        for role in obj.pers_attivo_tutti_ruoli:
            struct = role.cd_uo_aff_org
            return [
                {
                    "role": role.cd_ruolo,
                    "description": role.ds_ruolo,
                    "priorita": role.priorita,
                    "structureCod": struct.pk,
                    "structure": role.ds_aff_org,
                    "structureTypeCOD": struct.cd_tipo_nodo,
                }
            ]

    class Meta:
        model = Personale
        fields = [
            "name",
            "id",
            "roles",
            "officeReference",
            "email",
            "pec",
            "telOffice",
            "telCelOffice",
            "fax",
            "webSite",
            "cv",
            "teacher",
            "teacherCVFull",
            "teacherCVShort",
            "personFunctions",
            "profileId",
            "profileDescription",
            "profileShortDescription",
        ]
        language_field_map = {
            "teacherCVFull": {"it": "cv_full_it", "en": "cv_full_eng"},
            "teacherCVShort": {"it": "cv_short_it", "en": "cv_short_eng"}
        }




class PersonnelCfSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    Cf = serializers.CharField(source="cod_fis")
    ID = serializers.CharField(source="matricola")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    role = serializers.CharField(source="cd_ruolo")
    infrastructureId = serializers.CharField(source="cd_uo_aff_org")
    infrastructureDescription = serializers.CharField(source="ds_aff_org")

    def get_name(self, obj):
        full_name = obj.cognome + " " + obj.nome
        if obj.middle_name:
            full_name += " " + obj.middle_name
        return full_name

    class Meta:
        model = Personale
        fields = [
            "name",
            "Cf",
            "ID",
            "roleDescription",
            "role",
            "infrastructureId",
            "infrastructureDescription",
        ]


class AddressbookStructuresSerializer(serializers.ModelSerializer):
    cod = serializers.CharField(source="uo")
    name = serializers.CharField(source="denominazione")
    typeName = serializers.CharField(source="cd_tipo_nodo")
    typeCOD = serializers.CharField(source="ds_tipo_nodo")

    class Meta:
        model = UnitaOrganizzativa
        fields = [
            "cod",
            "name",
            "typeName",
            "typeCOD",
        ]


class RolesSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")

    class Meta:
        model = Personale
        fields = ["role", "roleDescription"]
