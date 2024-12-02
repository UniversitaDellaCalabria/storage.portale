from django.utils.translation import gettext_lazy as _

REGDID_IMPORT_USE_CURR_STRUCTURE = '0'
REGDID_IMPORT_DEFINE_NEW_STRUCTURE = '1'

ACCEPTED_TIPO_CORSO_COD = ("L", "LM", "LM5", "LM6")

EXCEL_FIELDS_MAPPINGS = {
    "CDS_COD_PREC": "CDS_COD_PREC",
    "CDS_COD": "CDS_COD",
    "NOME_CDS_IT": "NOME_CDS_IT",
    "NOME_CDS_ENG": "NOME_CDS_ENG",
    "DIP_COD": "DIP_COD",
    "TIPO_CORSO_COD": "TIPO_CORSO_COD",
    "TIPO_CORSO_DES": "TIPO_CORSO_DES",
    "DURATA_ANNI": "DURATA_ANNI",
    "VALORE_MIN": "CFU",
    "CLA_MIUR_COD": "COD_CLASSE_LAUREA",
    "CLA_MIUR_DES": "DES_CLASSE_LAUREA",
    "INTERCLA_MIUR_COD": "COD_INTERCLASSE_LAUREA",
    "INTERCLA_MIUR_DES": "DES_INTERCLASSE_LAUREA",
    "MODALITA_EROGAZIONE": "MODALITA_EROGAZIONE",
    "LINGUE": "LINGUE",
    "NUMERO_POSTI": "NUMERO_POSTI",
}

CDS_IMPORT_FIELDS = [
    {
        "name": EXCEL_FIELDS_MAPPINGS["CDS_COD_PREC"],
        "required": False,
        "description": _(
            "Code of the CDS from the previous year if the course is in continuity (if available)"
        ),
        "example": "0754",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["CDS_COD"],
        "required": False,
        "description": _("Code of the CDS (if available)"),
        "example": "0707",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["NOME_CDS_IT"],
        "required": True,
        "description": _("Name of the CDS in Italian"),
        "example": "INGEGNERIA MECCANICA",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["NOME_CDS_ENG"],
        "required": False,
        "description": _("Name of the CDS in English"),
        "example": "MECHANICAL ENGINEERING",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["DIP_COD"],
        "required": True,
        "description": _("Code of the department"),
        "example": "002016",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["TIPO_CORSO_COD"],
        "required": True,
        "description": _(
            "Type of course (Bachelor's, Master's, etc.) in the form L, LM, LM5, etc."
        ),
        "example": "L",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["TIPO_CORSO_DES"],
        "required": True,
        "description": _(
            "Type of course (Bachelor's, Master's, etc.) in extended form"
        ),
        "example": "Bachelor's",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["DURATA_ANNI"],
        "required": True,
        "description": _("Duration of the course"),
        "example": "3",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["VALORE_MIN"],
        "required": True,
        "description": _("Number of credits of the course"),
        "example": "180",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["CLA_MIUR_COD"],
        "required": True,
        "description": _("Degree class code"),
        "example": "L-9",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["CLA_MIUR_DES"],
        "required": True,
        "description": _("Degree class description"),
        "example": "Class of degrees in Industrial Engineering",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["INTERCLA_MIUR_COD"],
        "required": False,
        "description": _("Interclass degree code"),
        "example": "L-40",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["INTERCLA_MIUR_DES"],
        "required": False,
        "description": _("Interclass degree description"),
        "example": "Class of degrees in Sociology",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["MODALITA_EROGAZIONE"],
        "required": True,
        "description": _("Course delivery mode"),
        "example": "Conventional",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["LINGUE"],
        "required": True,
        "description": _(
            'Languages of the course in the form "ita" or "eng" or "ita,eng"'
        ),
        "example": "ita,eng",
    },
    {
        "name": EXCEL_FIELDS_MAPPINGS["NUMERO_POSTI"],
        "required": False,
        "description": _("Number of available seats for the course"),
        "example": "70",
    },
]


REGDID_STRUCTURE_MAPPINGS = {
    "NUMERO": "NUMERO",
    "NUMERO_PREC": "NUMERO_PREC",
    "TITOLO_IT": "TITOLO_IT",
    "TITOLO_EN": "TITOLO_EN",
    "TIPO_CORSO_COD": "TIPO_CORSO_COD",
    "DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID": "ID_TITOLO",
}


REGDID_STRUCTURE_FIELDS = [
    {
        "name": REGDID_STRUCTURE_MAPPINGS["NUMERO"],
        "required": True,
        "description": _("Article number"),
        "example": "1",
    },
    {
        "name": REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"],
        "required": False,
        "description": _(
            "Corresponding article number from the previous year. Leave it blank to ignore this article when coping articles from the previous year"
        ),
        "example": "2",
    },
    {
        "name": REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"],
        "required": True,
        "description": _("Title of the article in italian"),
        "example": "Scopo del regolamento",
    },
    {
        "name": REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"],
        "required": False,
        "description": _("Title of the article in english"),
        "example": "Regulation purpose",
    },
    {
        "name": REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"],
        "required": True,
        "description": _("Course type cod") + f" in {ACCEPTED_TIPO_CORSO_COD}",
        "example": "1",
    },
    {
        "name": REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"],
        "required": True,
        "description": "DidatticaArticoliRegolamentoTitolo ID",
        "example": "1",
    },
]
