from generics.filters import GenericApiFilter


class ResearchGroupsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by name, description, ERC's description, teacher's last name (starts with).",
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
            "description": "ID department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            }
        },
        {
            "name": "coderc1",
            "description": "List of ERC (European Research Council) codes (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "example": "LS1,PE4",
                "type": "string",
            },
        },
    ]
