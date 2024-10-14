from generics.filters import GenericApiFilter


class PatentsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by name or title.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "techarea",
            "description": "ID technology area.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "structure",
            "description": "Organizational unit code.",
            "required": False,
            "in": "query",
            "type": "string",
        },
    ]
