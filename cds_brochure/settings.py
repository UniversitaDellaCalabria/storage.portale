from django.conf import settings

CDS_EX_STUDENTS_MEDIA_PATH_BASE = getattr(
    settings, "CDS_EX_STUDENTS_MEDIA_PATH_BASE", "portale/sito_web_cds/ex_studenti/"
)


def cds_brochure_exstudents_media_path(instance, filename):
    return f"{CDS_EX_STUDENTS_MEDIA_PATH_BASE}/{filename}"


OFFICE_CDS_BROCHURE = getattr(settings, "OFFICE_CDS_BROCHURE", "cds_brochure")
BROCHURES_CURRENT_YEAR = getattr(settings, "BROCHURES_CURRENT_YEAR", "")
BROCHURES_VISIBLE = getattr(settings, "BROCHURES_VISIBLE", False)
