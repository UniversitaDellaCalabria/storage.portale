from generics.filters import GenericApiFilter


class CdsWebsiteTimetableFilter(GenericApiFilter):
    search_params = [
        {
            "name": "academic_year",
            "description": "The academic year for the timetable.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
                "example": 2024,
            },
        },
        {
            "name": "lang",
            "description": "Language.",
            "required": False,
            "in": "query",
            "schema": {
                "example": "it",
                "type": "string",
            },
        },
        {
            "name": "year",
            "description": "The year of study.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
                "example": 1,
            },
        },
        {
            "name": "date_month",
            "description": "The month to filter timetables .",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "10",
            },
        },
        {
            "name": "date_year",
            "description": "The year to filter timetables.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "2024",
            },
        },
        {
            "name": "af_name",
            "description": "Educational activity name.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "af_cod",
            "description": "Educational activity code.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "search_teacher",
            "description": "Filter by teacher name.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "search_location",
            "description": "Location.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "show_past",
            "description": "Show past events.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "boolean",
                "default": True,
            },
        },
    ]
