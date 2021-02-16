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
            'description': 'returns a list of cds filtered by academic year',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'departmentid',
            'description': 'returns a list of cds filtered by department id',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'departmentname',
            'description': 'returns a list of cds filtered by department name',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'coursetype',
            'description': 'returns a list of cds filtered by course type',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassid',
            'description': 'returns a list of cds filtered by course class id',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassname',
            'description': 'returns a list of cds filtered by course class name',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'jointdegree',
            'description': 'returns a list of cds filtered by joint degree',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'regdid_id',
            'description': 'returns a list of cds filtered by didattica regolamento id',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'cdslanguage',
            'description': '...',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'language',
            'description': 'returns a list of cds in italian or english ("it", "eng")',
            'required': False,
            'type': 'string'
        },
    ]


class ApiCdsInfoFilter(GenericApiFilter):
    search_params = [{'name': 'cdsid',
                      'description': 'returns one cds filtered on didattica regolamento id',
                      'required': False,
                      'type': 'int'}]


class ApiCdSStudyPlansFilter(GenericApiFilter):
    search_params = [{'name': 'cdsid',
                      'description': 'returns one cds filtered on didattica regolamento id',
                      'required': False,
                      'type': 'int'}]
