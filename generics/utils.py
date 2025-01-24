import logging

import magic
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from PIL import Image
from django.db import transaction

from generics.api.labels import LABEL_MAPPING as LOCAL_LABEL_MAPPING

from .settings import (
    ENCRYPTION_KEY,
    FILETYPE_IMAGE,
    SETTINGS_LABEL_MAPPING,
    FIRST_DUMMY_ID,
)

logger = logging.getLogger(__name__)


def log_action(user, obj, flag, msg):
    logger.info(f"[{timezone.now()}] {user} - {obj.__str__()} . {msg}")

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=obj.__str__(),
        action_flag=flag,
        change_message=msg,
    )


def log_action_on_commit(user, obj, flag, msg):
    """
    Wraps log_action to be used with transaction.on_commit
    """

    def log():
        log_action(user, obj, flag, msg)

    transaction.on_commit(log)


def base_context(context):
    context["base_template"] = getattr(settings, "DEFAULT_BASE_TEMPLATE", "")
    return context


def custom_message(request, message="", status=None):
    """ """
    return render(
        request,
        "custom_message.html",
        base_context({"avviso": message}),
        status=status,
    )


def encrypt(value):  # pragma: no cover
    if not value:
        return None
    value = str(value)
    # return Fernet(ENCRYPTION_KEY)._encrypt_from_parts(value.encode(), 0, ENCRYPTION_IV).decode()
    return Fernet(ENCRYPTION_KEY).encrypt(value.encode()).decode()


def decrypt(value):  # pragma: no cover
    if not value:
        return None
    value = str(value)
    try:
        return Fernet(ENCRYPTION_KEY).decrypt(value.encode()).decode()
    except Exception:
        raise Http404


def get_image_width_height(fopen):  # pragma: no cover
    mime = magic.Magic(mime=True)
    fopen.seek(0)
    mimetype = mime.from_buffer(fopen.read())
    fopen.seek(0)
    if mimetype in FILETYPE_IMAGE:
        pil = Image.open(fopen)
        return pil.size


def encode_labels(data, language=None):  # pragma: no cover
    labels = {}
    d = None
    if language is None:
        language = data["language"]
        data = data["data"]
        if len(data) > 0:
            d = data[0]
    else:
        d = data

    if len(data) > 0:
        loc_label_mapping = (
            LOCAL_LABEL_MAPPING["it"] if language == "it" else LOCAL_LABEL_MAPPING["en"]
        )

        # labels from settings
        sett_label_mapping = {}
        if SETTINGS_LABEL_MAPPING:
            sett_label_mapping = (
                SETTINGS_LABEL_MAPPING["it"]
                if language == "it"
                else SETTINGS_LABEL_MAPPING["en"]
            )

        for key in d:
            labels[key] = sett_label_mapping.get(key, loc_label_mapping.get(key, key))
            if isinstance(d[key], dict):
                for k in d[key]:
                    labels[k] = sett_label_mapping.get(k, loc_label_mapping.get(k, k))
            elif isinstance(d[key], list):
                for item in d[key]:
                    if isinstance(item, dict):
                        for k_temp in item:
                            labels[k_temp] = sett_label_mapping.get(
                                k_temp, loc_label_mapping.get(k_temp, k_temp)
                            )

    return labels


def is_path(value):  # pragma: no cover
    if not value:
        return False
    if type(value) is not str:
        return False
    if "/" not in value:
        return False
    return True


def build_media_path(filename, path=None):  # pragma: no cover
    if not filename:
        return None
    try:
        if "http" in filename or "https" in filename:
            return filename
        if not path or is_path(filename):
            return f"//{settings.DEFAULT_HOST}{settings.MEDIA_URL}{filename}"
        return f"//{settings.DEFAULT_HOST}{path}/{filename}"
    except Exception:
        return None


def get_latest_available_dummy_id(model, id_field_name, threshold=FIRST_DUMMY_ID - 1):
    """Retrieves the latest available ID and increments it, ensuring it's above the threshold"""
    instance = (
        model.objects.filter(**{id_field_name + "__isnull": False})
        .order_by(f"-{id_field_name}")
        .first()
    )
    latest_id = getattr(instance, id_field_name)
    return max(threshold, latest_id) + 1
