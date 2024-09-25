from generics.filters import GenericApiFilter


class ApiCompaniesListFilter(GenericApiFilter):
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
            "name": "spinoff",
            "description": "Spinoff",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "startup",
            "description": "Startup",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "departments",
            "description": "Lista di codici di dipartimento",
            "required": False,
            "type": "string",
        },
    ]
