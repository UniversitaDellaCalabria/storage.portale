from django.conf import settings
from django_ckeditor_5.widgets import CKEditor5Widget

CMS_STORAGE_ROOT_API = getattr(
    settings, "CMS_STORAGE_ROOT_API", "https://pp.storage.unical.it"
)
UNICMS_AUTH_TOKEN = getattr(settings, "UNICMS_AUTH_TOKEN", "")

STRUCTURES_FATHER = getattr(settings, "STRUCTURES_FATHER", "")
ALLOWED_STRUCTURE_TYPES = getattr(settings, "ALLOWED_STRUCTURE_TYPES", [])

CURRENT_YEAR = getattr(settings, "CURRENT_YEAR", "")

ENCRYPTION_KEY = getattr(settings, "ENCRYPTION_KEY", b"key")

# file validation
FILETYPE_PDF = ("application/pdf",)
FILETYPE_XLSX = (
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',       # .xlsx Excel Workbook
)
FILETYPE_DATA = (
    "text/csv",
    "application/json",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/wps-office.xls",
)
FILETYPE_TEXT = (
    "text/plain",
    "application/vnd.oasis.opendocument.text",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)
FILETYPE_IMAGE = (
    "image/webp",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/x-ms-bmp",
)
FILETYPE_VIDEO = ("video/mp4",)
FILETYPE_P7M = ("application/pkcs7-mime",)
FILETYPE_SIGNED = FILETYPE_PDF + FILETYPE_P7M
FILETYPE_MEDIA = FILETYPE_IMAGE + FILETYPE_VIDEO
FILETYPE_ALLOWED = FILETYPE_TEXT + FILETYPE_DATA + FILETYPE_MEDIA + FILETYPE_SIGNED

SETTINGS_LABEL_MAPPING = getattr(settings, "SETTINGS_LABEL_MAPPING", None)

# maximum permitted filename lengh in attachments, uploads
FILE_NAME_MAX_LEN = 128

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
FILE_MAX_SIZE = 5242880

FILETYPE_IMAGE_YX_RATIO_MIN = 0.9
FILETYPE_IMAGE_YX_RATIO_MAX = 1.1

# CKEDITOR 5 overrides
"""
    ckeditor js and css removed to avoid duplicates
    added one single import inside generics/templates/storage_crud_base.html

    (default) js = ['django_ckeditor_5/dist/bundle.js' ]
    (default) css = {
                        'all': [
                            'django_ckeditor_5/dist/styles.css',
                        ],
                    }
"""
CKEDITOR_WIDGET_OVERRIDES = getattr(
    settings, "CKEDITOR_WIDGET_OVERRIDES", {"css": {"all": []}, "js": []}
)

CKEditor5Widget.Media.css = CKEDITOR_WIDGET_OVERRIDES["css"]
CKEditor5Widget.Media.js = CKEDITOR_WIDGET_OVERRIDES["js"]

RICERCA_API_URL = getattr(settings, 'RICERCA_API_URL', 'api/ricerca/')


# First ID that doesn't get overridden by etl procedures
FIRST_DUMMY_ID = 99999001
