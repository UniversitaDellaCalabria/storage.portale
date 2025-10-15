from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from addressbook.models import Personale
from structures.models import UnitaOrganizzativa
from generics.utils import encrypt
from addressbook.settings import (
    ALLOWED_PROFILE_ID,
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
    ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN,
)


@extend_schema_serializer(examples=examples.ADDRESSBOOK_SERIALIZER_EXAMPLE)
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

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
    def get_name(self, obj):
        return (
            obj.cognome + " " + obj.nome
            if obj.middle_name is None
            else obj.cognome + " " + obj.nome + " " + obj.middle_name
        )

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        return encrypt(obj.matricola)

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
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

    @classmethod
    def get_contacts(cls, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto != contactDescr:
                    continue
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_officeReference(self, obj):
        return self.get_contacts(obj, "Riferimento Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_email(self, obj):
        return self.get_contacts(obj, "Posta Elettronica")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_pec(self, obj):
        return self.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telOffice(self, obj):
        return self.get_contacts(obj, "Telefono Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telCelOffice(self, obj):
        return self.get_contacts(obj, "Telefono Cellulare Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_fax(self, obj):
        return self.get_contacts(obj, "Fax")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_webSite(self, obj):
        return self.get_contacts(obj, "URL Sito WEB")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_cv(self, obj):
        return self.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

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


@extend_schema_serializer(examples=examples.ADDRESSBOOK_FULL_SERIALIZER_EXAMPLE)
class AddressbookFullSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    surname = serializers.CharField(source="cognome")
    # id = serializers.CharField(source="matricola")
    id = serializers.SerializerMethodField()
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

    def getId(self, obj):
        posta = self.get_contacts(obj, "Posta Elettronica")
        if not posta:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in posta
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )

        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_name(self, obj):
        return (
            obj.cognome + " " + obj.nome
            if obj.middle_name is None
            else obj.cognome + " " + obj.nome + " " + obj.middle_name
        )

    @extend_schema_field(serializers.CharField())
    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    @extend_schema_field(serializers.CharField())
    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        return encrypt(obj.matricola)

    # ~ def get_contacts(self, obj, contactDescr):
    # ~ if contactDescr in PERSON_CONTACTS_TO_TAKE:
    # ~ for contact in obj.contatti:
    # ~ tipo = contact.cd_tipo_cont
    # ~ if tipo.descr_contatto != contactDescr: continue
    # ~ if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
    # ~ return contact.contatto
    # ~ return []

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_officeReference(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Riferimento Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_email(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Posta Elettronica")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_pec(self, obj):
        return AddressbookSerializer.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telCelOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Cellulare Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_fax(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Fax")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_webSite(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_cv(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
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
                    "start": role.dt_rap_ini,
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


@extend_schema_serializer(examples=examples.ADDRESSBOOK_DETAIL_SERIALIZER_EXAMPLE)
class AddressbookDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    surname = serializers.CharField(source="cognome")
    id = serializers.SerializerMethodField()
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
    teacher = serializers.SerializerMethodField()
    personFunctions = serializers.SerializerMethodField()
    teacherCVFull = serializers.CharField(source="cv_full_it")
    teacherCVShort = serializers.CharField(source="cv_short_it")
    profileId = serializers.CharField(source="profilo")
    profileDescription = serializers.SerializerMethodField()
    profileShortDescription = serializers.SerializerMethodField()
    gender = serializers.CharField(source="cd_genere")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_personFunctions(self, obj):
        return [
            {
                "teacherRole": f.ds_funzione,
                "tunctionCod": f.funzione,
                "structureCod": f.cd_csa.uo,
                "structureName": f.cd_csa.denominazione,
            }
            for f in obj.functions
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_teacher(self, obj):
        return obj.fl_docente or obj.cop_teacher

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return obj.nome if obj.middle_name is None else obj.nome + " " + obj.middle_name

    @extend_schema_field(serializers.CharField())
    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    @extend_schema_field(serializers.CharField())
    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        # return encrypt(obj.matricola)
        posta = self.get_contacts(obj, "Posta Elettronica")
        if not posta:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in posta
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )

        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    # ~ def get_contacts(self, obj, contactDescr):
    # ~ if contactDescr in PERSON_CONTACTS_TO_TAKE:
    # ~ for contact in obj.contatti:
    # ~ tipo = contact.cd_tipo_cont
    # ~ if tipo.descr_contatto != contactDescr: continue
    # ~ if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
    # ~ return contact.contatto
    # ~ return []
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_officeReference(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Riferimento Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_email(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Posta Elettronica")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_pec(self, obj):
        return AddressbookSerializer.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telCelOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Cellulare Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_fax(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Fax")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_webSite(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_cv(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
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
            "teacher",
            "personFunctions",
            "teacherCVFull",
            "teacherCVShort",
            "profileId",
            "profileDescription",
            "profileShortDescription",
            "gender",
        ]
        language_field_map = {
            "teacherCVFull": {"it": "cv_full_it", "en": "cv_full_eng"},
            "teacherCVShort": {"it": "cv_short_it", "en": "cv_short_eng"},
        }


@extend_schema_serializer(examples=examples.ADDRESSBOOK_FULL_DETAIL_SERIALIZER_EXAMPLE)
class AddressbookFullDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    surname = serializers.CharField(source="cognome")
    id = serializers.SerializerMethodField()
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
    teacher = serializers.SerializerMethodField()
    personFunctions = serializers.SerializerMethodField()
    teacherCVFull = serializers.CharField(source="cv_full_it")
    teacherCVShort = serializers.CharField(source="cv_short_it")
    profileId = serializers.CharField(source="profilo")
    profileDescription = serializers.SerializerMethodField()
    profileShortDescription = serializers.SerializerMethodField()
    gender = serializers.CharField(source="cd_genere")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
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

    @extend_schema_field(serializers.BooleanField())
    def get_teacher(self, obj):
        return obj.fl_docente or obj.cop_teacher

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return obj.nome if obj.middle_name is None else obj.nome + " " + obj.middle_name

    @extend_schema_field(serializers.CharField())
    def get_profileDescription(self, obj):
        return obj.ds_profilo if obj.ds_profilo in ALLOWED_PROFILE_ID else None

    @extend_schema_field(serializers.CharField())
    def get_profileShortDescription(self, obj):
        return (
            obj.ds_profilo_breve if obj.ds_profilo_breve in ALLOWED_PROFILE_ID else None
        )

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        # return encrypt(obj.matricola)
        posta = self.get_contacts(obj, "Posta Elettronica")
        if not posta:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in posta
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )

        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    # ~ def get_contacts(self, obj, contactDescr):
    # ~ if contactDescr in PERSON_CONTACTS_TO_TAKE:
    # ~ for contact in obj.contatti:
    # ~ tipo = contact.cd_tipo_cont
    # ~ if tipo.descr_contatto != contactDescr: continue
    # ~ if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
    # ~ return contact.contatto
    # ~ return []

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_officeReference(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Riferimento Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_email(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Posta Elettronica")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_pec(self, obj):
        return AddressbookSerializer.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telCelOffice(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Telefono Cellulare Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_fax(self, obj):
        return AddressbookSerializer.get_contacts(obj, "Fax")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_webSite(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_cv(self, obj):
        return AddressbookSerializer.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
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
                    "start": role.dt_rap_ini,
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
            "teacher",
            "personFunctions",
            "teacherCVFull",
            "teacherCVShort",
            "profileId",
            "profileDescription",
            "profileShortDescription",
            "gender",
        ]
        language_field_map = {
            "teacherCVFull": {"it": "cv_full_it", "en": "cv_full_eng"},
            "teacherCVShort": {"it": "cv_short_it", "en": "cv_short_eng"},
        }


@extend_schema_serializer(examples=examples.PERSONNEL_CF_SERIALIZER_EXAMPLE)
class PersonnelCfSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    Cf = serializers.CharField(source="cod_fis")
    ID = serializers.CharField(source="matricola")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    role = serializers.CharField(source="cd_ruolo")
    infrastructureId = serializers.CharField(source="cd_uo_aff_org")
    infrastructureDescription = serializers.CharField(source="ds_aff_org")

    @extend_schema_field(serializers.CharField())
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


@extend_schema_serializer(examples=examples.ADDRESSBOOK_STRUCTURES_SERIALIZER_EXAMPLE)
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


@extend_schema_serializer(examples=examples.ROLES_SERIALIZER_EXAMPLE)
class RolesSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")

    class Meta:
        model = Personale
        fields = ["role", "roleDescription"]
