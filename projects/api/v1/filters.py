from generics.filters import GenericApiFilter


class ProjectsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by title, name, technological area's description, organizational structure's name, starting year or territorial scope.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "techarea",
            "description": "ID technological area.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
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
            "name": "year",
            "description": "Project year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "programtype",
            "description": "ID program type.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "territorialscope",
            "description": "ID territorial scope.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
