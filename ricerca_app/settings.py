from django.conf import settings


ALLOWED_PROFILE_ID = []

# file validation
FILETYPE_PDF = ('application/pdf',)
FILETYPE_DATA = ('text/csv', 'application/json',
                 'application/vnd.ms-excel',
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                 'application/vnd.oasis.opendocument.spreadsheet',
                 'application/wps-office.xls',
                 )
FILETYPE_TEXT = ('text/plain',
                 'application/vnd.oasis.opendocument.text',
                 'application/msword',
                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )
FILETYPE_IMAGE = ('image/webp', 'image/jpeg', 'image/png',
                  'image/gif', 'image/x-ms-bmp')
FILETYPE_VIDEO = ('video/mp4',)
FILETYPE_P7M = ('application/pkcs7-mime',)
FILETYPE_SIGNED = FILETYPE_PDF + FILETYPE_P7M
FILETYPE_MEDIA = FILETYPE_IMAGE + FILETYPE_VIDEO
FILETYPE_ALLOWED = FILETYPE_TEXT + FILETYPE_DATA + FILETYPE_MEDIA + FILETYPE_SIGNED

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

LABORATORIES_MEDIA_PATH = f'{settings.MEDIA_URL}laboratori/loghi'
COMPANIES_MEDIA_PATH = f'{settings.MEDIA_URL}spinoff-startup/loghi'
PATENTS_MEDIA_PATH = f'{settings.MEDIA_URL}brevetti/loghi'
CDS_BROCHURE_MEDIA_PATH = f'{settings.MEDIA_URL}cds_media_brochure'
TEACHER_PHOTO_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/foto'
TEACHER_CV_EN_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/cv_en'
TEACHER_CV_ITA_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/cv_ita'
