from rest_framework import filters


class GenericApiFilter(filters.SearchFilter):
    def get_schema_operation_parameters(self, view):
        params = super().get_schema_operation_parameters(view)
        for search_param in self.search_params:
            params.append(
                {
                    'name': search_param['name'],
                    'required': search_param.get('required', False),
                    'in': 'query',
                    'description': search_param['description'],
                    'schema': {
                        'type': search_param.get('type', 'string'),
                    },
                }
            )
        return params


# -------------------------------------- #

class ApiCdsListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'academicyear',
            'description': '...',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'departmentid',
            'description': '...',
            'required': False,
        },
        {
            'name': 'departmentname',
            'description': '...',
            'required': False,
        },

        # TODO: update descriptions & include left parameters
    ]


class ApiCdsInfoFilter(GenericApiFilter):
    ...
