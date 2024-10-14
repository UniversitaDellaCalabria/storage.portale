from generics.filters import GenericApiFilter


class TeachersListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by teacher's last name.",
            "required": False,
            "in": "query",
            "type": "string",
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
            "name": "cds",
            "description": "Code of a course of study.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            }
        },
        {
            "name": "department",
            "description": "Code of a department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            }
        },
        {
            "name": "role",
            "description": "List of roles codes (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            }
        },
        {
            "name": "year",
            "description": "Coverage year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class TeacherStudyActivitiesFilter(GenericApiFilter):
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
    ]


class TeacherMaterialsAndNewsFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by title.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            }
        }
    ]


class PublicationsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by title.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            }
        },
        {
            "name": "year",
            "description": "Year.",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "type",
            "description": "ID community type.",
            "required": False,
            "schema": {
                "type": "string",
            }
        },
        {
            "name": "structure",
            "description": "Code of a structure.",
            "required": False,
            "type": "string",
        },
    ]
