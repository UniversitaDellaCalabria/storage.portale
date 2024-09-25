from generics.filters import GenericApiFilter


class ApiProjectsListFilter(GenericApiFilter):
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
            "name": "infrastructure",
            "description": "Id Infrastruttura Riferimento",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "year",
            "description": "Anno del progetto",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "programtype",
            "description": "Id Tipologia Programma",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "territorialscope",
            "description": "Id Ambito Territoriale",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
