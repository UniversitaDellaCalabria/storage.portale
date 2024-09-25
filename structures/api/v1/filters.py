from generics.filters import GenericApiFilter


class ApiStructuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "father",
            "description": "Codice della struttura padre",
            "required": False,
            "type": "string",
        },
        {
            "name": "type",
            "description": "Codice della tipologia di struttura",
            "required": False,
            "type": "string",
        },
        {
            "name": "depth",
            "description": "Livello di profondità sotto strutture (0 = nessuno, max 1)",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
