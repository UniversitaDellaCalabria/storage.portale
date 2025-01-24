from generics.api.filters import GenericApiFilter


class CompaniesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "techarea",
            "description": "ID technoly area.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "spinoff",
            "description": "Whether or not the company is a spinoff.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "boolean",
            },
        },
        {
            "name": "startup",
            "description": "Whether or not the company is a startup.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "boolean",
            },
        },
        {
            "name": "departments",
            "description": "List of departments codes (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "search",
            "description": "Search for company name or description.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]
