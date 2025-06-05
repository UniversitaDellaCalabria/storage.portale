from django.core.cache import cache
from django.http import Http404
from generics.utils import decrypt
from django.apps import apps

from .settings import (
    ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN,
    PERSON_CONTACTS_EXCLUDE_STRINGS,
)


def get_personale_matricola(personale_id):
    if personale_id[len(personale_id) - 2:] == "==":
        return decrypt(personale_id)

    personale_model = apps.get_model("addressbook.Personale")
    personalecontatti_model = apps.get_model("addressbook.PersonaleContatti")

    contatto = personalecontatti_model.objects.filter(
        contatto__istartswith=f"{personale_id}@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"
    ).first()
    if not contatto:
        raise Http404
    personale = (
        personale_model.objects.filter(id_ab=contatto.id_ab).values("matricola").first()
    )
    if not personale:
        raise Http404
    return personale["matricola"]


def add_email_addresses(cod_fis):
    return apps.get_model("addressbook.PersonaleContatti").objects.filter(
            cod_fis=cod_fis, cd_tipo_cont="EMAIL"
        ).only("contatto")

def append_email_addresses(addressbook_queryset, id_ab_key):
    personalecontatti_model = apps.get_model("addressbook.PersonaleContatti")
    cache_key = "addressbook_email_list"
    if cache.get(cache_key) is None:
        cached_contacts = {}
        contacts = (
            personalecontatti_model.objects.filter(
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
