from generics.filters import GenericApiFilter


class ApiPatentsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "techarea",
            "description": "Area Tecnologica",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "structure",
            "description": "Codice di una struttura",
            "required": False,
            "type": "string",
        },
    ]
