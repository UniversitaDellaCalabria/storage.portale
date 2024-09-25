from generics.filters import GenericApiFilter


class ApiHighFormationMastersListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "coursetype",
            "description": "Tipo Corso",
            "required": False,
            "type": "string",
        },
        {
            "name": "erogation",
            "description": "Erogazione",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "department",
            "description": "Dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "director",
            "description": "Direttore Scientifico",
            "required": False,
            "type": "string",
        },
        {
            "name": "language",
            "description": "Lingua Master",
            "required": False,
            "type": "string",
        },
        {
            "name": "year",
            "description": "Anno Rilevazione",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
