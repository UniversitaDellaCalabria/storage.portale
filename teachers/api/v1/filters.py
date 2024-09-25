from generics.filters import GenericApiFilter


class ApiTeachersListFilter(GenericApiFilter):
    search_params = [
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
            "name": "cds",
            "description": "Codice del corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "department",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "role",
            "description": "Ruolo di un docente",
            "required": False,
            "type": "string",
        },
        {
            "name": "year",
            "description": "Anno Erogazione Attività",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class ApiTeacherStudyActivitiesFilter(GenericApiFilter):
    search_params = [
        {
            "name": "year",
            "description": "Attività formative erogate in uno specifico anno",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearFrom",
            "description": "Attività formative erogate in un anno maggiore uguale a yearFrom",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearTo",
            "description": "Attività formative erogate in un anno minore uguale a yearTo",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class ApiPublicationsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "year",
            "description": "Anno",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "type",
            "description": "Id di una tipologia di community",
            "required": False,
            "type": "string",
        },
        {
            "name": "structure",
            "description": "Struttura di un docente",
            "required": False,
            "type": "string",
        },
    ]
