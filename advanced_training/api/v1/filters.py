from generics.filters import GenericApiFilter


class HighFormationMastersListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "coursetype",
            "description": "Course type.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "erogation",
            "description": "Erogation mode.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "department",
            "description": "Department ID.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "director",
            "description": "Scientific director ID.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "language",
            "description": "Master language.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "year",
            "description": "Year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
