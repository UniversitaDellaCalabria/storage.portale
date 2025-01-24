from django_filters import rest_framework as df_filters
from rest_framework import filters


class GenericApiFilter(filters.BaseFilterBackend):
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
                "description": "Language.",
                "schema": {
                    "type": "string",
                    "example": "en",
                },
            }
        )
        return params


class InCharFilter(df_filters.BaseInFilter, df_filters.CharFilter):
    """
    A reusable filter for filtering fields using multiple values.
    """

    pass
