from drf_spectacular import openapi


class AutoSchema(openapi.AutoSchema):
    """
    Custom schema that avoids getting the queryset for v1 apis
    """

    def _resolve_path_parameters(self, variables):
        model = (
            None
            if "/ricerca/" in self.view.request._request.path
            or "/v1/" in self.view.request._request.path
            else openapi.get_view_model(self.view, emit_warnings=False)
        )

        parameters = []
        for variable in variables:
            schema = openapi.build_basic_type(openapi.OpenApiTypes.STR)
            description = ""

            resolved_parameter = openapi.resolve_django_path_parameter(
                self.path_regex,
                variable,
                self.map_renderers("format"),
            )
            if not resolved_parameter:
                resolved_parameter = openapi.resolve_regex_path_parameter(
                    self.path_regex, variable
                )

            if resolved_parameter:
                schema = resolved_parameter["schema"]
            elif model is None:
                openapi.warn(
                    f'could not derive type of path parameter "{variable}" because it '
                    f"is untyped and obtaining queryset from the viewset failed. "
                    f"Consider adding a type to the path (e.g. <int:{variable}>) or annotating "
                    f'the parameter type with @extend_schema. Defaulting to "string".'
                )
            else:
                try:
                    if getattr(self.view, "lookup_url_kwarg", None) == variable:
                        model_field_name = getattr(self.view, "lookup_field", variable)
                    elif variable.endswith("_pk"):
                        # Django naturally coins foreign keys *_id. improve chances to match a field
                        model_field_name = f"{variable[:-3]}_id"
                    else:
                        model_field_name = variable
                    model_field = openapi.follow_model_field_lookup(
                        model, model_field_name
                    )
                    schema = self._map_model_field(model_field, direction=None)
                    if "description" not in schema and model_field.primary_key:
                        description = openapi.get_pk_description(model, model_field)
                except openapi.django_exceptions.FieldError:
                    openapi.warn(
                        f'could not derive type of path parameter "{variable}" because model '
                        f'"{model.__module__}.{model.__name__}" contained no such field. Consider '
                        f'annotating parameter with @extend_schema. Defaulting to "string".'
                    )

            parameters.append(
                openapi.build_parameter_type(
                    name=variable,
                    location=openapi.OpenApiParameter.PATH,
                    description=description,
                    schema=schema,
                )
            )

        return parameters
