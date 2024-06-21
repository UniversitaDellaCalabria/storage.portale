import magic

from cryptography.fernet import Fernet

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.http import Http404

from PIL import Image

from . labels import LABEL_MAPPING as LOCAL_LABEL_MAPPING
from . import settings as app_settings


ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN = getattr(settings, 'ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN', app_settings.ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN)
ENCRYPTION_KEY = getattr(settings, 'ENCRYPTION_KEY', app_settings.ENCRYPTION_KEY)
FILETYPE_IMAGE = getattr(settings, 'FILETYPE_IMAGE', app_settings.FILETYPE_IMAGE)
SETTINGS_LABEL_MAPPING = getattr(settings, 'LABEL_MAPPING', None)
PERSON_CONTACTS_EXCLUDE_STRINGS = getattr(settings, 'PERSON_CONTACTS_EXCLUDE_STRINGS', app_settings.PERSON_CONTACTS_EXCLUDE_STRINGS)


def encrypt(value): # pragma: no cover
    if not value:
        return None
    value = str(value)
    # return Fernet(ENCRYPTION_KEY)._encrypt_from_parts(value.encode(), 0, ENCRYPTION_IV).decode()
    return Fernet(settings.ENCRYPTION_KEY).encrypt(value.encode()).decode()


def decrypt(value): # pragma: no cover
    if not value:
        return None
    value = str(value)
    try:
        return Fernet(settings.ENCRYPTION_KEY).decrypt(value.encode()).decode()
    except:
        raise Http404


def get_image_width_height(fopen): # pragma: no cover
    mime = magic.Magic(mime=True)
    fopen.seek(0)
    mimetype = mime.from_buffer(fopen.read())
    fopen.seek(0)
    if mimetype in FILETYPE_IMAGE:
        pil = Image.open(fopen)
        return pil.size


def encode_labels(data, language=None): # pragma: no cover
    labels = {}
    d = None
    if language is None:
        language = data['language']
        data = data['data']
        if len(data) > 0:
            d = data[0]
    else:
        d = data

    if len(data) > 0:
        loc_label_mapping = LOCAL_LABEL_MAPPING['it'] if language == "it" else LOCAL_LABEL_MAPPING['en']

        # labels from settings
        sett_label_mapping = {}
        if SETTINGS_LABEL_MAPPING:
            sett_label_mapping = SETTINGS_LABEL_MAPPING['it'] if language == "it" else SETTINGS_LABEL_MAPPING['en']

        for key in d:
            labels[key] = sett_label_mapping.get(key, loc_label_mapping.get(key, key))
            if isinstance(d[key], dict):
                for k in d[key]:
                    labels[k] = sett_label_mapping.get(k, loc_label_mapping.get(k, k))
            elif isinstance(d[key], list):
                for item in d[key]:
                    if isinstance(item, dict):
                        for k_temp in item:
                            labels[k_temp] = sett_label_mapping.get(k_temp, loc_label_mapping.get(k_temp, k_temp))

    return labels


def is_path(value): # pragma: no cover
    if not value: return False
    if type(value) is not str: return False
    if "/" not in value: return False
    return True


def build_media_path(filename, path=None): # pragma: no cover
    if not filename: return None
    try:
        if 'http' in filename or 'https' in filename: return filename
        if not path or is_path(filename):
            return f'//{settings.DEFAULT_HOST}{settings.MEDIA_URL}{filename}'
        return f'//{settings.DEFAULT_HOST}{path}/{filename}'
    except:
        return None


def get_personale_matricola(personale_id):
    if personale_id[len(personale_id) - 2:] == '==':
        return decrypt(personale_id)

    personale_model = apps.get_model('ricerca_app.Personale')
    personalecontatti_model = apps.get_model('ricerca_app.PersonaleContatti')

    contatto = personalecontatti_model.objects\
                                     .filter(contatto__istartswith=f'{personale_id}@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}')\
                                     .first()
    if not contatto: raise Http404
    personale = personale_model.objects.filter(id_ab=contatto.id_ab).values('matricola').first()
    if not personale: raise Http404
    return personale['matricola']


def append_email_addresses(addressbook_queryset, id_ab_key):
    personalecontatti_model = apps.get_model('ricerca_app.PersonaleContatti')
    cache_key = f"addressbook_email_list"
    if cache.get(cache_key) == None:
        contacts = personalecontatti_model.objects.filter(cd_tipo_cont__descr_contatto='Posta Elettronica')\
                                                          .order_by('prg_priorita')\
                                                          .values('contatto', 'id_ab')
        cache.set(cache_key, contacts)
    cached_contacts = cache.get(cache_key, [])
    for q in addressbook_queryset:
        emails = []
        uc = cached_contacts.filter(id_ab=q['id_ab'])
        for contact in uc:
            if any(x in contact['contatto'].lower() for x in PERSON_CONTACTS_EXCLUDE_STRINGS):
                continue
            if contact['contatto'] in emails:
                continue
            if contact['id_ab'] == q[id_ab_key]:
                emails.append(contact['contatto'])
        q['email'] = emails
