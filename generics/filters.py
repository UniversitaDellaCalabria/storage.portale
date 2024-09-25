from rest_framework import filters


class GenericApiFilter(filters.SearchFilter):
    def get_schema_operation_parameters(self, view):
        params = super().get_schema_operation_parameters(view)
        for search_param in self.search_params:
            params.append(
                {
                    "name": search_param["name"],
                    "required": search_param.get("required", False),
                    "in": "query",
                    "description": search_param["description"],
                    "schema": search_param.get("schema", {"type": "string"}),
                }
            )
        params.append(
            {
                "name": "lang",
                "required": False,
                "in": "query",
                "description": "language",
                "schema": {
                    "type": "string",
                    "example": "en",
                },
            }
        )
        return params
