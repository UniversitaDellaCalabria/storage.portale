from django.conf import settings


def encode_labels_list(data):
    labels = {}
    language = data['language']
    data = data['data']

    label_mapping = settings.LABEL_MAPPING['it'] if language == "it" else settings.LABEL_MAPPING['en']
    if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
        d = data[0]
        for key in d.keys():
            labels[key] = label_mapping[key]

    return labels


def encode_labels_detail(data, language):
    labels = {}

    label_mapping = settings.LABEL_MAPPING['it'] if language == "it" else settings.LABEL_MAPPING['en']
    if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
        for key in data.keys():
            labels[key] = label_mapping[key]

    return labels
