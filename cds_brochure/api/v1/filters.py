from generics.filters import GenericApiFilter

class ApiCdsWebsitesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "academic_year",
            "description": "Anno Accademico",
            "required": False,
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "language",
            "description": "Lingua Master",
            "required": False,
            "type": "string",
        },
        {
            "name": "course_class",
            "description": "Classe di laurea",
            "required": False,
            "type": "string",
        },
    ]