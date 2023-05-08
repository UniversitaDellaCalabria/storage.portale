import magic
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . utils import get_image_width_height
from . import settings as app_settings


FILETYPE_IMAGE = getattr(settings, 'FILETYPE_IMAGE',
                         app_settings.FILETYPE_IMAGE)
FILETYPE_MEDIA = getattr(settings, 'FILETYPE_MEDIA',
                         app_settings.FILETYPE_MEDIA)
FILETYPE_ALLOWED = getattr(settings, 'FILETYPE_ALLOWED',
                           app_settings.FILETYPE_ALLOWED)
FILETYPE_PDF_ALLOWED = getattr(settings, 'FILETYPE_PDF',
                           app_settings.FILETYPE_PDF)
FILE_MAX_SIZE = getattr(settings, 'FILE_MAX_SIZE',
                        app_settings.FILE_MAX_SIZE)
FILETYPE_IMAGE_YX_RATIO_MIN = getattr(settings, 'FILETYPE_IMAGE_YX_RATIO_MIN',
                                      app_settings.FILETYPE_IMAGE_YX_RATIO_MIN)
FILETYPE_IMAGE_YX_RATIO_MAX = getattr(settings, 'FILETYPE_IMAGE_YX_RATIO_MAX',
                                      app_settings.FILETYPE_IMAGE_YX_RATIO_MAX)


def validate_file_size(value): # pragma: no cover
    if not hasattr(value, 'size'): # pragma: no cover
        return
    content_size = None
    try:
        content_size = int(value.size)
    except ValueError: # pragma: no cover
        _msg = "Can't detect file size: {}"
        raise ValidationError(_msg.format(value.__dict__))
    if content_size > FILE_MAX_SIZE:
        _max_size_mb = (FILE_MAX_SIZE / 1024) / 1024
        _msg = f'File size exceed the maximum value ({_max_size_mb} MB)'
        raise ValidationError(_msg)


def _validate_generic_file_extension(value, allowed_filetypes): # pragma: no cover
    if not hasattr(value, 'file'): # pragma: no cover
        return
    mimetype = magic.Magic(mime=True).from_buffer(value.file.read())
    value.file.seek(0)
    if mimetype not in allowed_filetypes:
        raise ValidationError(f'Unsupported file extension {mimetype}')



def orcid_validator(value): # pragma: no cover
    if len(value) != 19:
        raise ValidationError('Unsupported ORCID. Remember, ORCID is an https URI with a 16-digit number that is compatible as 0000-0001-2345-6789')
    cont = 0
    for v in value:
        if not v.isdigit() and v!='X' and v!='-':
            raise ValidationError('Unsupported ORCID. Remember, ORCID is an https URI with a 16-digit number that is compatible as 0000-0001-2345-6789')
        if v == '-':
            cont+=1
    if cont != 3:
        raise ValidationError('Unsupported ORCID. Remember, ORCID is an https URI with a 16-digit number that is compatible as 0000-0001-2345-6789')



def validate_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_ALLOWED)


def validate_pdf_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_PDF_ALLOWED)


def validate_image_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_IMAGE)


def validate_media_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_MEDIA)


def validate_image_size_ratio(value): # pragma: no cover
    if not hasattr(value, 'content_type'): # pragma: no cover
        return

    mimetype = magic.Magic(mime=True).from_buffer(value.file.read())
    value.file.seek(0)

    if mimetype in FILETYPE_IMAGE:
        w, y = get_image_width_height(value.file)
        ratio = y / w
        if ratio < FILETYPE_IMAGE_YX_RATIO_MIN or \
           ratio > FILETYPE_IMAGE_YX_RATIO_MAX:
            rratio = f'{ratio:.2f}'
            raise ValidationError(f'Image have invalid y / w ratio {rratio}. \
                                    Min {FILETYPE_IMAGE_YX_RATIO_MIN} - \
                                    Max {FILETYPE_IMAGE_YX_RATIO_MAX}')


def validate_piva(value):
    if not value: return False
    if not re.match(r"^[0-9]{11}$", value):
        raise ValidationError(_('Enter a valid VAT Number'))
