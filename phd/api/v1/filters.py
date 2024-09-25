from generics.filters import GenericApiFilter


class ApiPhdListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "regdid",
            "description": "Id regolamento didattico dottorato",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "year",
            "description": "Regolamento didattico dottorato di uno specifico anno accademico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearFrom",
            "description": "Regolamento didattico dottorato di uno specifico anno accademico maggiore uguale a yearTo",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearTo",
            "description": "Regolamento didattico dottorato di uno specifico anno accademico minore uguale a yearTo",
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
            "name": "cdscod",
            "description": "Codice di un corso di studi",
            "required": False,
            "type": "string",
        },
        {
            "name": "pdscod",
            "description": "Codice del piano di studi del dottorato",
            "required": False,
            "schema": {
                "type": "string",
                "example": "GEN",
            },
        },
        {
            "name": "cycle",
            "description": "Numero ciclo del dottorato",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
