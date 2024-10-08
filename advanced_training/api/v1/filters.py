from generics.filters import GenericApiFilter


class ApiHighFormationMastersListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "coursetype",
            "description": "Course type",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "erogation",
            "description": "Erogation mode",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "department",
            "description": "Department ID",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "director",
            "description": "Scientific director ID",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "language",
            "description": "Master language",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "year",
            "description": "Year of survey",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
