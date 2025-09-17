from generics.api.filters import GenericApiFilter


class CdsBrochuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by the name of the course of study.",
            "required": False,
            "in": "query",
            "type": "string",
        },
        {
            "name": "coursetype",
            "description": "Search by course type.",
            "required": False,
            "in": "query",
            "type": "string",
        },
        {
            "name": "cdslanguage",
            "description": "Search by course language.",
            "required": False,
            "in": "query",
            "type": "string",
        },
    ]
