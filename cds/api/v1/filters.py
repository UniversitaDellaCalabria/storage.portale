from generics.filters import GenericApiFilter


class ApiCdsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "academicyear",
            "description": "Cds erogati in uno specifico anno accademico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "departmentcod",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "departmentid",
            "description": "Id di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "departmentname",
            "description": "Nome di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "coursetype",
            "description": "Tipologia di corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "courseclassid",
            "description": "Id della classe di un corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "courseclassname",
            "description": "Nome delle classe di un corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "jointdegree",
            "description": "Titolo congiunto",
            "required": False,
            "schema": {
                "type": "array",
                "example": ["D", "N", "S"],
            },
        },
        {
            "name": "regdid",
            "description": "Id regolamento didattico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cdscod",
            "description": "Codice di un Corso di Studi",
            "required": False,
        },
        {
            "name": "cdslanguage",
            "description": "Lingua del corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "area",
            "description": "Area del Corso di Studio",
            "required": False,
            "type": "string",
        },
    ]


class ApiAllActivitiesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "department",
            "description": "Dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "cds",
            "description": "CDS",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "period",
            "description": "Periodo",
            "required": False,
            "type": "string",
        },
        {
            "name": "academic_year",
            "description": "Anno Accademico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {"name": "ssd", "description": "SSD", "required": False, "type": "string"},
        {
            "name": "teaching",
            "description": "Insegnamento",
            "required": False,
            "type": "string",
        },
        {
            "name": "teacher",
            "description": "Docente",
            "required": False,
            "type": "string",
        },
        {
            "name": "course_year",
            "description": "Anno Di Corso",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class ApiCdsWebsitesStudyPlansListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "year",
            "description": "Anno Accademico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cds_cod",
            "description": "Codice di un cds",
            "required": False,
            "type": "string",
        },
        {
            "name": "regdid",
            "description": "Id regolamento didattico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
