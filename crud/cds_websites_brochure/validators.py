from django.utils.html import strip_tags
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

from re import sub

def _normalize_text(text):
    normalized_text = text
    normalized_text = sub(r"(\&[a-z0-9#]{2,8}\;)", " ", normalized_text)
    normalized_text = sub(r"(\r|\n)", "", normalized_text)
    normalized_text = normalized_text.strip()
    normalized_text = strip_tags(normalized_text)
    return normalized_text

class CKEditorWidgetMinLenghtValidator(MinLengthValidator):
    def clean(self, x):
        return len(_normalize_text(x))

class CKEditorWidgetMaxLenghtValidator(MaxLengthValidator):
    def clean(self, x):
        return len(_normalize_text(x))
