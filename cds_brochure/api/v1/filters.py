from generics.filters import GenericApiFilter


class CdsBrochuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by the name of the course of study.",
            "required": False,
            "in": "query",
            "type": "string",
        },
    ]
