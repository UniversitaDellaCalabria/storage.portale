from generics.filters import GenericApiFilter


class CdsWebsitesTopicArticlesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "cds_cod",
            "description": "Code of a course of study.",
            "required": True,
            "in": "query",
            "type": "string",
        },
        {
            "name": "topic_id",
            "description": "ID of the topic.",
            "required": True,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]


class CdsWebsitesStudyPlansListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "year",
            "description": "Anno Accademico.",
            "required": True,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cds_cod",
            "description": "Code of a course of study.",
            "required": True,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]
