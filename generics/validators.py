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
        _msg = _("Can't detect file size")
        raise ValidationError(f'{_msg}: {value.__dict__}')
    if content_size > FILE_MAX_SIZE:
        _max_size_mb = (FILE_MAX_SIZE / 1024) / 1024
        _msg = _("File size exceed the maximum value")
        raise ValidationError(f'{_msg} {_max_size_mb} MB')


def _validate_generic_file_extension(value, allowed_filetypes): # pragma: no cover
    if not hasattr(value, 'file'): # pragma: no cover
        return
    mimetype = magic.Magic(mime=True).from_buffer(value.file.read())
    value.file.seek(0)
    if mimetype not in allowed_filetypes:
        _msg = _('Unsupported file extension')
        _msg2 = _('Allowed extensions')
        raise ValidationError(f'{_msg}: {mimetype}. {_msg2} {allowed_filetypes}')


def orcid_validator(value): # pragma: no cover
    regex = "^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9|X]$"
    if not re.match(regex, value):
        raise ValidationError(_('Invalid ORCID. Remember, ORCID is an https URI with a 16-digit number that is compatible as 0000-0001-2345-6789'))


def validate_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_ALLOWED)


def validate_pdf_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_PDF_ALLOWED)


def validate_image_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_IMAGE)


def validate_media_file_extension(value): # pragma: no cover
    _validate_generic_file_extension(value, FILETYPE_MEDIA)


def validate_image_size_ratio(value): # pragma: no cover
    # if not hasattr(value, 'content_type'): # pragma: no cover
        # return

    mimetype = magic.Magic(mime=True).from_buffer(value.file.read())
    value.file.seek(0)

    if mimetype in FILETYPE_IMAGE:
        w, y = get_image_width_height(value.file)
        ratio = y / w
        if ratio < FILETYPE_IMAGE_YX_RATIO_MIN or \
           ratio > FILETYPE_IMAGE_YX_RATIO_MAX:
            rratio = f'{ratio:.2f}'
            _msg = _('Image have invalid y / w ratio')
            raise ValidationError(f'{_msg}: {rratio} \
                                    (Min {FILETYPE_IMAGE_YX_RATIO_MIN} - \
                                    Max {FILETYPE_IMAGE_YX_RATIO_MAX})')


def validate_piva(value): # pragma: no cover
    if not value: 
        return False
    
    regex = "^((AT)?U[0-9]{8}|(BE)?0[0-9]{9}|(BG)?[0-9]{9,10}|(CY)?[0-9]{8}L|(CZ)?[0-9]{8,10}|(DE)?[0-9]{9}|(DK)?[0-9]{8}|(EE)?[0-9]{9}|(EL|GR)?[0-9]{9}|(ES)?[0-9A-Z][0-9]{7}[0-9A-Z]|(FI)?[0-9]{8}|(FR)?[0-9A-Z]{2}[0-9]{9}|(GB)?([0-9]{9}([0-9]{3})?|[A-Z]{2}[0-9]{3})|(HU)?[0-9]{8}|(IE)?[0-9]S[0-9]{5}L|(IT)?[0-9]{11}|(LT)?([0-9]{9}|[0-9]{12})|(LU)?[0-9]{8}|(LV)?[0-9]{11}|(MT)?[0-9]{8}|(NL)?[0-9]{9}B[0-9]{2}|(PL)?[0-9]{10}|(PT)?[0-9]{9}|(RO)?[0-9]{2,10}|(SE)?[0-9]{12}|(SI)?[0-9]{8}|(SK)?[0-9]{10})$"

    if not re.match(regex, value):
        raise ValidationError(_('Enter a valid VAT Number'))
