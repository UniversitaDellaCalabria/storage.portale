from cryptography.fernet import Fernet
from django.conf import settings


def encrypt(value):
    if not value:
        return None
    value = str(value)
    return Fernet(settings.ENCRYPTION_KEY).encrypt(value.encode()).decode()


def decrypt(value):
    if not value:
        return None
    value = str(value)
    return Fernet(settings.ENCRYPTION_KEY).decrypt(value.encode()).decode()


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

    if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
        label_mapping = settings.LABEL_MAPPING['it'] if language == "it" else settings.LABEL_MAPPING['en']
        for key in d.keys():
            labels[key] = label_mapping[key]
            if isinstance(d[key], dict):
                for k in d[key].keys():
                    if isinstance(d[key][k], dict):
                        labels[k] = {}
                        for k_temp, v_temp in d[key][k].items():
                            labels[k][k_temp] = label_mapping[k_temp]
                    elif isinstance(d[key][k], list):
                        for item in d[key][k]:
                            for k_temp, v_temp in item.items():
                                labels[k_temp] = label_mapping[k_temp]
                            break
                    else:
                        labels[k] = label_mapping[k]
            elif isinstance(d[key], list):
                for instance in d[key]:
                    if isinstance(instance, dict):
                        for k_temp, v_temp in instance.items():
                            labels[k_temp] = label_mapping[k_temp]
                        break

    return labels


# def encode_labels_detail(data, language):
#     labels = {}
#
#     if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
#         label_mapping = settings.LABEL_MAPPING['it'] if language == "it" else settings.LABEL_MAPPING['en']
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
