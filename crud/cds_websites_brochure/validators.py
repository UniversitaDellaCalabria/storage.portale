from django.utils.html import strip_tags
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

from re import sub, findall


class CKEditorWidgetMinLenghtValidator(MinLengthValidator):
    def clean(self, x):
        cleaned_string = x
        cleaned_string = strip_tags(cleaned_string)
        cleaned_string = sub(r"(\&[a-z0-9]{2,8}\;)", " ", cleaned_string)
        cleaned_string = cleaned_string.strip()
        return len(cleaned_string)
    
class CKEditorWidgetMaxLenghtValidator(MaxLengthValidator):
    def clean(self, x):
        cleaned_string = x
        cleaned_string = strip_tags(cleaned_string)
        cleaned_string = sub(r"(\&[a-z0-9]{2,8}\;)", " ", cleaned_string)
        cleaned_string = cleaned_string.strip()
        print('length', len(cleaned_string))
        return len(cleaned_string)
