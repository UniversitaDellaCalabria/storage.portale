from generics.filters import GenericApiFilter


class ApiResearchGroupsListFilter(GenericApiFilter):
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
            "name": "coderc1",
            "description": "Lista di Codici di erc1",
            "required": False,
            "type": "string",
        },
    ]
