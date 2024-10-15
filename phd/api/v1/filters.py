from generics.filters import GenericApiFilter


class PhdActivitiesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by educational activity name.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "structure",
            "description": "Proposing structure name.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "phd",
            "description": "PhD's name.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "ssd",
            "description": "SSD (Scientific Disciplinary Sector).",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "teacher",
            "description": "Teacher's last name (starts with).",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "cycle",
            "description": "Cycle of an educational activity.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "typology",
            "description": "Typology of an educational activity.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]


class PhdListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "year",
            "description": "Specific year of erogation.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearFrom",
            "description": "First year of erogation.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "yearTo",
            "description": "Last year of erogation.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "regdid",
            "description": "ID didactic regulation.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "departmentid",
            "description": "ID of a department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cdscod",
            "description": "Code of a course of study.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "pdscod",
            "description": "Code of a study plan.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "cycle",
            "description": "Cycle of an educational activity.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
