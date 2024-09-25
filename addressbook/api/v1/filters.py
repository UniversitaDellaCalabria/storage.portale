from generics.filters import GenericApiFilter


class ApiAddressbookListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "phone",
            "description": "Numero di telefono",
            "required": False,
            "type": "string",
        },
        {
            "name": "structure",
            "description": "Codice di una struttura",
            "required": False,
            "type": "string",
        },
        {
            "name": "structuretypes",
            "description": "Codice della tipologia di struttura",
            "required": False,
            "type": "string",
        },
        {
            "name": "role",
            "description": "Ruolo personale",
            "required": False,
            "type": "string",
        },
        {
            "name": "structuretree",
            "description": "Albero struttura",
            "required": False,
            "type": "string",
        },
    ]
