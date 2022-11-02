import magic

from django.conf import settings
from django.core.exceptions import ValidationError

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
    print(value.__dict__, mimetype)
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

