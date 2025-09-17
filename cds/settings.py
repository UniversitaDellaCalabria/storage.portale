from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Path to cds manifests
CDS_MANIFESTO_MEDIA_PATH_BASE = getattr(
    settings, "CDS_MANIFESTO_MEDIA_PATH_BASE", "portale/cds/manifesti"
)


def cds_manifesto_media_path(instance, filename):
    return f"{CDS_MANIFESTO_MEDIA_PATH_BASE}/{instance.regdid.aa_reg_did}/{filename}"


# Path to cds regulations
CDS_REGOLAMENTO_MEDIA_PATH_BASE = getattr(
    settings, "CDS_REGOLAMENTO_MEDIA_PATH_BASE", "portale/cds/regolamenti"
)


def cds_regolamento_media_path(instance, filename):
    return (
        f"{CDS_REGOLAMENTO_MEDIA_PATH_BASE}/{instance.regdid.aa_reg_did}/{filename}"
    )


# Path to cds educational order
CDS_ORDINAMENTO_MEDIA_PATH_BASE = getattr(
    settings, "CDS_ORDINAMENTO_MEDIA_PATH_BASE", "portale/cds/ordinamenti"
)


def cds_ordinamento_media_path(instance, filename):
    return (
        f"{CDS_ORDINAMENTO_MEDIA_PATH_BASE}/{instance.regdid.aa_reg_did}/{filename}"
    )


# Path to cds multimedia
CDS_MULTIMEDIA_MEDIA_PATH_BASE = getattr(
    settings, "CDS_MULTIMEDIA_MEDIA_PATH_BASE", "portale/cds_media_brochure"
)


def cds_multimedia_media_path(instance, filename):
    return f"{CDS_MULTIMEDIA_MEDIA_PATH_BASE}/{filename}"


CDS_BROCHURE_IS_VISIBLE = getattr(settings, "CDS_BROCHURE_IS_VISIBLE", True)

CDS_BROCHURE_MEDIA_PATH = getattr(
    settings, "CDS_BROCHURE_MEDIA_PATH", "portale/cds_media_brochure"
)

OFFICE_CDS = getattr(settings, "OFFICE_CDS", "cds")
OFFICE_CDS_DOCUMENTS = getattr(settings, "OFFICE_CDS_DOCUMENTS", "cds_documents")
OFFICE_CDS_TEACHING_SYSTEM = getattr(
    settings, "OFFICE_CDS_TEACHING_SYSTEM", "cds_teaching_system"
)

ALLOWED_CDS_LANGUAGES = ["ita", "eng"]
ALLOWED_CDS_JOINT_DEGREES = [
    {"COD": "N", "name": _("No")},
    {"COD": "S", "name": _("Joint title")},
    {"COD": "D", "name": _("Double title")},
]

REGDID_OTHER_DATA_TYPES_MAPPINGS = getattr(
    settings,
    "REGDID_OTHER_DATA_TYPES_MAPPINGS",
    {
        "INTRO_CDS_FMT": ["HTML"],
        "URL_CDS_DOC": ["PDF"],
        "URL_CDS_VIDEO": ["URL", "PDF"],
    },
)
