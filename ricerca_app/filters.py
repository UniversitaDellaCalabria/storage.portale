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
        params.append(
            {
                'name': 'lang',
                'required': False,
                'in': 'query',
                'description': 'language (it or en)',
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
            'name': 'departmentcod',
            'description': 'Didattica dipartimento cod',
            'required': False,
            'type': 'string'
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
            'description': 'Lingua del corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'lang',
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
                      'type': 'int'},
                     ]


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


class ApiResearchGroupsListFilter(GenericApiFilter):
    search_params = [{'name': 'teacher',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'},
                     {'name': 'department',
                      'description': 'Codice di un dipartimento',
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
            'name': 'department',
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


class ApiBaseResearchLinesListFilter(GenericApiFilter):
    search_params = [{'name': 'teacher',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'},
                     {'name': 'department',
                      'description': 'Codice di un dipartimento',
                      'required': True,
                      'type': 'string'},
                     {'name': 'year',
                      'description': 'Anno',
                      'required': True,
                      'type': 'int'},
                     ]


class ApiApplicateResearchLinesListFilter(GenericApiFilter):
    search_params = [{'name': 'teacher',
                      'description': 'Matricola di un docente',
                      'required': True,
                      'type': 'string'},
                     {'name': 'department',
                      'description': 'Codice di un dipartimento',
                      'required': True,
                      'type': 'string'},
                     {'name': 'year',
                      'description': 'Anno',
                      'required': True,
                      'type': 'int'},
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
            'name': 'departmentcod',
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


class ApiAddressbookListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'structureid',
            'description': 'codice struttura',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'structuretypes',
            'description': 'tipologia struttura',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'roles',
            'description': 'ruoli personale',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'structuretree',
            'description': 'albero struttura',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'personaleid',
            'description': 'matricola personale',
            'required': False,
            'type': 'string'
        },
    ]


class ApiStructuresListFilter(GenericApiFilter):
    search_params = [{'name': 'father',
                      'description': 'codice struttura padre',
                      'required': False,
                      'type': 'string'},
                     {'name': 'type',
                      'description': 'codice tipologia struttura',
                      'required': False,
                      'type': 'string'},
                     {'name': 'structureid',
                      'description': 'codice struttura',
                      'required': False,
                      'type': 'string'},
                     ]


class ApiLaboratoriesListFilter(GenericApiFilter):
    search_params = [{'name': 'area',
                      'description': 'ambito laboratorio',
                      'required': False,
                      'type': 'string'},
                     {'name': 'department',
                      'description': 'codice dipartimento',
                      'required': False,
                      'type': 'string'},
                     {'name': 'erc1',
                      'description': 'codice ricerca erc1',
                      'required': False,
                      'type': 'string'},
                     {'name': 'teacher',
                      'description': 'matricola docente',
                      'required': False,
                      'type': 'string'},
                     ]


class ApiErc1ListFilter(GenericApiFilter):
    search_params = [{'name': 'laboratory',
                      'description': 'id laboratorio',
                      'required': False,
                      'type': 'string'},
                     ]


class ApiPublicationsListFilter(GenericApiFilter):
    search_params = [{'name': 'teacherid',
                      'description': 'matricola docente',
                      'required': False,
                      'type': 'string'},
                     {'name': 'year',
                      'description': 'anno',
                      'required': False,
                      'type': 'int'},
                     {'name': 'type',
                      'description': 'id tipologia di community',
                      'required': False,
                      'type': 'string'},
                     {'name': 'publicationid',
                      'description': 'id pubblicazione',
                      'required': False,
                      'type': 'string'},
                     ]
