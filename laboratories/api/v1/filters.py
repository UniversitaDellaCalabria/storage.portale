from generics.filters import GenericApiFilter


class ApiLaboratoriesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "area",
            "description": "Ambito di un laboratorio",
            "required": False,
            "schema": {
                "type": "string",
                "example": "Informatico/Multimediale",
            },
        },
        {
            "name": "department",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "erc1",
            "description": "Codice di ricerca erc1",
            "required": False,
            "type": "string",
        },
        {
            "name": "teacher",
            "description": "Matricola di un docente",
            "required": False,
            "type": "string",
        },
        {
            "name": "scope",
            "description": "Scopo di un laboratorio",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "infrastructure",
            "description": "Id Infrastruttura Riferimento",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
