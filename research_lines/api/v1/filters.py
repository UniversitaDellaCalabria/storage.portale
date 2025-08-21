from generics.api.filters import GenericApiFilter


class ResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by description.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "teacher",
            "description": "Teacher's encrypted matricola.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
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
            "name": "year",
            "description": "Year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class AllResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by description.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
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
            "name": "year",
            "description": "Year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
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
            "name": "asters",
            "description": "List of broad research sectors IDs (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "exclude_base",
            "description": "Excludes base research lines.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "boolean",
            },
        },
        {
            "name": "exclude_applied",
            "description": "Excludes applied research lines.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "boolean",
            },
        },
    ]
