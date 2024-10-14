from generics.filters import GenericApiFilter


class LaboratoriesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search for laboratories by name, description or purpose.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "area",
            "description": "Scientific area (exact match required).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "Scientifico/Tecnologico",
            },
        },
        {
            "name": "department",
            "description": "Department code.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "erc1",
            "description": "List of ERC (European Research Council) codes (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "example": "LS1,PE4",
                "type": "string",
            },
        },
        {
            "name": "teacher",
            "description": "Teacher's encrpyted matricola.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "infrastructure",
            "description": "ID infrastructure.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "scope",
            "description": "Scope of the laboratory.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]
