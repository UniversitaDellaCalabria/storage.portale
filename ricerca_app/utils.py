import magic

from cryptography.fernet import Fernet

from django.conf import settings
from django.http import Http404

from . labels import LABEL_MAPPING as LOCAL_LABEL_MAPPING

SETTINGS_LABEL_MAPPING = getattr(settings, 'LABEL_MAPPING', None)


def encrypt(value):
    if not value:
        return None
    value = str(value)
    return Fernet(settings.ENCRYPTION_KEY).encrypt(value.encode()).decode()


def decrypt(value):
    if not value:
        return None
    value = str(value)
    try:
        return Fernet(settings.ENCRYPTION_KEY).decrypt(value.encode()).decode()
    except:
        raise Http404


def get_image_width_height(fopen):
    mime = magic.Magic(mime=True)
    fopen.seek(0)
    mimetype = mime.from_buffer(fopen.read())
    fopen.seek(0)
    if mimetype in FILETYPE_IMAGE:
        pil = Image.open(fopen)
        return pil.size


def encode_labels(data, language=None):
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

        for key in d.keys():
            labels[key] = sett_label_mapping.get(key, loc_label_mapping[key])
            if isinstance(d[key], dict):
                for k in d[key].keys():
                    if isinstance(d[key][k], dict):
                        labels[k] = {}
                        for k_temp, v_temp in d[key][k].items():
                            labels[k][k_temp] = sett_label_mapping.get(k_temp, loc_label_mapping[k_temp])
                    elif isinstance(d[key][k], list):
                        for item in d[key][k]:
                            for k_temp, v_temp in item.items():
                                labels[k_temp] = sett_label_mapping.get(k_temp, loc_label_mapping[k_temp])
                            break
                    else:
                        labels[k] = sett_label_mapping.get(k, loc_label_mapping[k])
            elif isinstance(d[key], list):
                for instance in d[key]:
                    if isinstance(instance, dict):
                        for k_temp, v_temp in instance.items():
                            labels[k_temp] = sett_label_mapping.get(k_temp, loc_label_mapping[k_temp])
                        break

    return labels


def is_path(value):
    if not value: return False
    if type(value) is not str: return False
    if "/" not in value: return False
    return True


def build_media_path(filename, path=None):
    if not filename: return ''
    if 'http' in filename or 'https' in filename: return filename
    if not path: return filename
    if is_path(filename): return f'//{settings.DEFAULT_HOST}{settings.MEDIA_URL}{filename}'
    return f'//{settings.DEFAULT_HOST}{path}/{filename}'

# def encode_labels_detail(data, language):
#     labels = {}
#
#     if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
#         label_mapping = LABEL_MAPPING['it'] if language == "it" else LABEL_MAPPING['en']
#         for key in data.keys():
#             labels[key] = label_mapping[key]
#             if isinstance(data[key], dict):
#                 for k in data[key].keys():
#                     labels[k] = {}
#                     for k_temp, v_temp in data[key][k].items():
#                         labels[k][k_temp] = label_mapping[k_temp]
#                 break
#             elif isinstance(data[key], list):
#                 for instance in data[key]:
#                     for k_temp, v_temp in instance.items():
#                         labels[k_temp] = label_mapping[k_temp]
#                     break
#
#     return labels
