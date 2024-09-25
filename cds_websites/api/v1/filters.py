from generics.filters import GenericApiFilter


class ApiCdsWebsitesTopicArticlesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "cds_cod",
            "description": "Codice di un cds",
            "required": False,
            "type": "string",
        },
        {
            "name": "topic_id",
            "description": "ID Topic",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
