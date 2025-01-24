from generics.api.filters import GenericApiFilter


class StructureTypesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "father",
            "description": "ID of the parent structure (if applicable). Must be a valid ID of an existing organizational unit.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "example": 1234,
                "format": "int32",
            },
        },
    ]


class StructuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by the name of the organizational structure.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "Department of Mathematics",
            },
        },
        {
            "name": "father",
            "description": "ID of the parent structure (if applicable). Must be a valid ID of an existing organizational unit.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "example": 1234,
                "format": "int32",
            },
        },
        {
            "name": "type",
            "description": "List of types of organizational structures (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "DPT,FAC",
            },
        },
        {
            "name": "depth",
            "description": "Sub structures' depth (min: 0, max: 1).",
            "required": False,
            "in": "query",
            "schema": {
                "default": 0,
                "type": "integer",
                "format": "int32",
            },
        },
    ]
