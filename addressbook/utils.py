from django.core.cache import cache
from django.http import Http404
from generics.utils import decrypt
from django.apps import apps

from .models import (
    Personale, PersonaleContatti
)
from .settings import (
    ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN,
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)


def get_roles(obj):
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
                "profileId": role.cd_profilo,
                "profileDescription": role.ds_profilo,
            }
        ]


def get_roles_with_start(cls, obj):
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
                "profileId": role.cd_profilo,
                "profileDescription": role.ds_profilo,
            }
        ]


def get_contacts(obj, contactDescr):
    if contactDescr not in PERSON_CONTACTS_TO_TAKE:
        return []
    if not getattr(obj, 'contatti', None):
        return []
    result = []
    for contact in obj.contatti:
        tipo = contact.cd_tipo_cont
        if tipo.descr_contatto in PERSON_CONTACTS_EXCLUDE_STRINGS:
            continue
        descr = tipo.descr_contatto
        if descr == contactDescr:
            result.append(contact.contatto)
    return result

# def get_contacts(obj, contactDescr):
#     if getattr(obj, 'contatti', None):
#         contacts = obj.contatti
#     elif obj.email is not None:
#         contacts = obj.email
#     else:
#         return []
#     results = []
#     if contactDescr in PERSON_CONTACTS_TO_TAKE:
#         for contact in contacts:
#             print(contact)
#             descr = contact["cd_tipo_cont__descr_contatto"]
#             if descr != contactDescr:
#                 continue
#             if descr not in PERSON_CONTACTS_EXCLUDE_STRINGS:
#                 results.append(contact["contatto"])
                  
#     return results


def get_personale_matricola(personale_id):
    try:
        id_ab= int(personale_id)
    except ValueError:
        c = PersonaleContatti.objects.filter(
            contatto__istartswith=f"{personale_id}@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"
        ).first()
        if not c: raise Http404
        id_ab = c.id_ab
    personale = (
        Personale.objects.filter(id_ab=id_ab).values("matricola").first()
    )
    if not personale:
        raise Http404
    return personale["matricola"]


def add_email_addresses(cod_fis):
    contatti = (
        PersonaleContatti
        .objects.filter(cod_fis=cod_fis, cd_tipo_cont="EMAIL")
        .order_by("prg_priorita")
        .only("contatto")
    )

    return [
        c.contatto
        for c in contatti
        if c.contatto
        and not any(x in c.contatto.lower() for x in PERSON_CONTACTS_EXCLUDE_STRINGS)
    ]


def append_email_addresses(addressbook_queryset, id_ab_key):
    cache_key = "addressbook_email_list"
    if cache.get(cache_key) is None:
        cached_contacts = {}
        contacts = (
            PersonaleContatti.objects.filter(
                cd_tipo_cont__descr_contatto="Posta Elettronica"
            )
            .order_by("prg_priorita")
            .values("contatto", "id_ab")
        )
        for cc in contacts:
            if cc["id_ab"] not in cached_contacts:
                cached_contacts[cc["id_ab"]] = []
            cached_contacts[cc["id_ab"]].append(cc["contatto"])

        cache.set(cache_key, cached_contacts)
    cached_contacts = cache.get(cache_key, {})

    for q in addressbook_queryset:
        good_emails = []
        if cached_contacts:
            emails = cached_contacts.get(q[id_ab_key], [])
            for email in emails:
                if any(x in email.lower() for x in PERSON_CONTACTS_EXCLUDE_STRINGS):
                    continue
                good_emails.append(email)
        q["email"] = good_emails
