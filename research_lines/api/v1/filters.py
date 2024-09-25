from generics.filters import GenericApiFilter


class ApiBaseResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "teacher",
            "description": "Matricola di un docente",
            "required": False,
            "type": "string",
        },
        {
            "name": "department",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "year",
            "description": "Anno",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class ApiAllResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "department",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "year",
            "description": "Anno",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "department",
            "description": "Dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "ercs",
            "description": "Lista di codici erc1",
            "required": False,
            "type": "string",
        },
        {
            "name": "asters",
            "description": "Lista di codici aster1",
            "required": False,
            "type": "string",
        },
        {
            "name": "exclude_base",
            "description": "Esclude le linee di ricerca di base",
            "required": False,
            "schema": {
                "type": "boolean",
            },
        },
        {
            "name": "exclude_applied",
            "description": "Esclude le linee di ricerca applicate",
            "required": False,
            "schema": {
                "type": "boolean",
            },
        },
    ]


class ApiAppliedResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "teacher",
            "description": "Matricola di un docente",
            "required": False,
            "type": "string",
        },
        {
            "name": "department",
            "description": "Codice di un dipartimento",
            "required": False,
            "type": "string",
        },
        {
            "name": "year",
            "description": "Anno",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class ApiErc1ListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "laboratory",
            "description": "Id di un laboratorio",
            "required": False,
            "type": "string",
        },
    ]
