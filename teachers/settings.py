from django.conf import settings

# Path to teacher's photos
TEACHER_PHOTO_MEDIA_PATH_BASE = getattr(settings, "TEACHER_PHOTO_MEDIA_PATH_BASE", "portale/docenti_pta/foto/")


def teacher_photo_media_path(instance, filename):
    return f'{TEACHER_PHOTO_MEDIA_PATH_BASE}{filename}'


# Path to teacher's en CV
TEACHER_CV_EN_MEDIA_PATH_BASE = getattr(settings, "TEACHER_CV_EN_MEDIA_PATH_BASE", "portale/docenti_pta/cv_en/")


def teacher_cv_en_media_path(instance, filename):
    return f'{TEACHER_CV_EN_MEDIA_PATH_BASE}{filename}'


# Path to teacher's ita CV
TEACHER_CV_ITA_MEDIA_PATH_BASE = getattr(settings, "TEACHER_CV_ITA_MEDIA_PATH_BASE", "portale/docenti_pta/cv_ita/")


def teacher_cv_ita_media_path(instance, filename):
    return f'{TEACHER_CV_ITA_MEDIA_PATH_BASE}{filename}'


OFFICE_TEACHERS = getattr(settings, 'OFFICE_TEACHERS', 'teachers')
