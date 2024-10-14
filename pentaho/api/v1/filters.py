from generics.filters import GenericApiFilter


class PentahoIsodidFilter(GenericApiFilter):
    search_params = [
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
