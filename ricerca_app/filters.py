from rest_framework import filters
import django_filters

from ricerca_app.models import DidatticaCds


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
            'description': 'Cds erogati in uno specifico anno accademico',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'departmentid',
            'description': 'Didattica dipartimento id',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'departmentname',
            'description': 'Nome di un dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'coursetype',
            'description': 'Didattica cds course type',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassid',
            'description': 'Didattica cds course class id',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassname',
            'description': 'Didattica cds course class name',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'jointdegree',
            'description': 'didattica cds joint degree',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'regdid_id',
            'description': 'didattica regolamento id',
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
            'description': 'lingua dei risultati in output',
            'required': False,
            'type': 'string'
        },
    ]


class ApiCdsInfoFilter(GenericApiFilter):
    search_params = [{'name': 'cdsid',
                      'description': 'didattica regolamento id',
                      'required': True,
                      'type': 'int'}]


class ApiCdSStudyPlansFilter(GenericApiFilter):
    search_params = [{'name': 'cdsid',
                      'description': 'didattica regolamento id',
                      'required': True,
                      'type': 'int'}]


class ApiStudyPlanDetailFilter(GenericApiFilter):
    search_params = [{'name': 'studyplanid',
                      'description': 'id di un piano di studio',
                      'required': True,
                      'type': 'int'}]


class ApiStudyActivityInfoFilter(GenericApiFilter):
    search_params = [{'name': 'studyactivityid',
                      'description': 'id di un\'attività formativa',
                      'required': True,
                      'type': 'int'}]


class ApiCdSMainTeachersFilter(GenericApiFilter):
    search_params = [{'name': 'cdsid',
                      'description': 'didattica regolamento id',
                      'required': True,
                      'type': 'int'}]


class ApiTeacherResearchGroupsFilter(GenericApiFilter):
    search_params = [{'name': 'teacherid',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'}]


class ApiTeacherResearchLinesFilter(GenericApiFilter):
    search_params = [{'name': 'teacherid',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'}]


class ApiTeachersListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'cdsid',
            'description': 'didattica regolamento id',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'departmentid',
            'description': 'didattica dipartimento cod',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'role',
            'description': 'Ruolo docente',
            'required': False,
            'type': 'string'
        },
    ]


class ApiTeacherStudyActivitiesFilter(GenericApiFilter):
    search_params = [{'name': 'teacherid',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'},
                     {'name': 'year',
                      'description': 'Attività formative erogate in uno specifico anno',
                      'required': False,
                      'type': 'int'},
                     {'name': 'yearFrom',
                      'description': 'Attività formative erogate in un anno maggiore uguale a yearFrom',
                      'required': False,
                      'type': 'int'},
                     {'name': 'yearTo',
                      'description': 'Attività formative erogate in un anno minore uguale a yearTo',
                      'required': False,
                      'type': 'int'},
                     ]


class ApiTeacherInfoFilter(GenericApiFilter):
    search_params = [{'name': 'teacherid',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'}]


class ApiDoctoratesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'regdid',
            'description': 'didattica dottorato regolamento id',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'year',
            'description': 'didattica dottorato regolamento di uno specifico anno accademico',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'yearFrom',
            'description': 'didattica dottorato regolamento con anno accademico maggiore uguale a yearTo',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'yearTo',
            'description': 'didattica dottorato regolamento con anno accademico minore uguale a yearTo',
            'required': False,
            'type': 'int'
        },
        {
            'name': 'departmentid',
            'description': 'didattica dipartimento cod',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'cdscod',
            'description': 'didattica dottorato cds cod',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'pdscod',
            'description': 'codice del piano di studi del cds dottorato',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'cycle',
            'description': 'numero ciclo del dottorato',
            'required': False,
            'type': 'int'
        },
    ]

# class ApiStructuresListFilter(GenericApiFilter):
#     search_params = [{'name': 'uo',
#                       'description': 'codice struttura',
#                       'required': True,
#                       'type': 'string'}]
