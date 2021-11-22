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
                    'schema': search_param.get('schema', {'type': 'string'}),
                }
            )
        params.append(
            {
                'name': 'lang',
                'required': False,
                'in': 'query',
                'description': 'language',
                'schema': {
                    'type': 'string',
                    "example": "en",
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
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
        {
            'name': 'departmentcod',
            'description': 'Codice di un dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'departmentid',
            'description': 'Id di un dipartimento',
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
            'description': 'Tipologia di corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassid',
            'description': 'Id della classe di un corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'courseclassname',
            'description': 'Nome delle classe di un corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'jointdegree',
            'description': 'Titolo congiunto',
            'required': False,
            'schema': {
                    'type': 'array',
                    "example": ["D", "N", "S"],
            },
        },
        {
            'name': 'regdid',
            'description': 'Id regolamento didattico',
            'required': False,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
        {
            'name': 'cdslanguage',
            'description': 'Lingua del corso di studi',
            'required': False,
            'type': 'string'
        },
    ]


# not used!
# class ApiCdSMainTeachersFilter(GenericApiFilter):
    # search_params = [
    # {
    # 'name': 'regdid',
    # 'description': 'ID regolamento didattico',
    # 'required': True,
    # 'type': 'int'
    # }
    # ]


class ApiResearchGroupsListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'department',
            'description': 'Codice di un dipartimento',
            'required': True,
            'type': 'string'
        }
    ]


class ApiTeachersListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'regdid',
            'description': 'Id regolamento didattico',
            'required': False,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
        {
            'name': 'cds',
            'description': 'Codice del corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'department',
            'description': 'Codice di un dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'role',
            'description': 'Ruolo di un docente',
            'required': False,
            'type': 'string'
        },
    ]


class ApiBaseResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'department',
            'description': 'Codice di un dipartimento',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'year',
            'description': 'Anno',
            'required': True,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
    ]


class ApiAppliedResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'department',
            'description': 'Codice di un dipartimento',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'year',
            'description': 'Anno',
            'required': True,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
    ]


class ApiTeacherStudyActivitiesFilter(GenericApiFilter):
    search_params = [{'name': 'year',
                      'description': 'Attività formative erogate in uno specifico anno',
                      'required': False,
                      'schema': {
                          'type': 'integer',
                          'format': 'int32',
                      }
                      },
                     {'name': 'yearFrom',
                      'description': 'Attività formative erogate in un anno maggiore uguale a yearFrom',
                      'required': False,
                      'schema': {
                          'type': 'integer',
                          'format': 'int32',
                      }
                      },
                     {'name': 'yearTo',
                      'description': 'Attività formative erogate in un anno minore uguale a yearTo',
                      'required': False,
                      'schema': {
                          'type': 'integer',
                          'format': 'int32',
                      }
                      },
                     ]


class ApiDoctoratesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'regdid',
            'description': 'Id regolamento didattico dottorato',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
        {
            'name': 'year',
            'description': 'Regolamento didattico dottorato di uno specifico anno accademico',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
        {
            'name': 'yearFrom',
            'description': 'Regolamento didattico dottorato di uno specifico anno accademico maggiore uguale a yearTo',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
        {
            'name': 'yearTo',
            'description': 'Regolamento didattico dottorato di uno specifico anno accademico minore uguale a yearTo',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
        {
            'name': 'departmentcod',
            'description': 'Codice di un dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'cdscod',
            'description': 'Codice di un corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'pdscod',
            'description': 'Codice del piano di studi del dottorato',
            'required': False,
            'schema': {
                'type': 'string',
                "example": "GEN",
            },
        },
        {
            'name': 'cycle',
            'description': 'Numero ciclo del dottorato',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
    ]


class ApiAddressbookListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'structure',
            'description': 'Codice di una struttura',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'structuretypes',
            'description': 'Codice della tipologia di struttura',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'role',
            'description': 'Ruolo personale',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'structuretree',
            'description': 'Albero struttura',
            'required': False,
            'type': 'string'
        },
        # {
        # 'name': 'personaleid',
        # 'description': 'matricola personale',
        # 'required': False,
        # 'type': 'string'
        # },
    ]


class ApiStructuresListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'father',
            'description': 'Codice della struttura padre',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'type',
            'description': 'Codice della tipologia di struttura',
            'required': False,
            'type': 'string'
        },
    ]


class ApiLaboratoriesListFilter(GenericApiFilter):
    search_params = [{'name': 'area',
                      'description': 'Ambito di un laboratorio',
                      'required': False,
                      'schema': {'type': 'string',
                                 "example": "Informatico/Multimediale",
                                 },
                      },
                     {'name': 'department',
                      'description': 'Codice di un dipartimento',
                      'required': False,
                      'type': 'string'},
                     {'name': 'erc1',
                      'description': 'Codice di ricerca erc1',
                      'required': False,
                      'type': 'string'},
                     {'name': 'teacher',
                      'description': 'Matricola di un docente',
                      'required': False,
                      'type': 'string'},
                     {'name': 'scope',
                      'description': 'Scopo di un laboratorio',
                      'required': False,
                      'schema': {
                          'type': 'integer',
                          'format': 'int32',
                      }
                      },
                     ]


class ApiErc1ListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'laboratory',
            'description': 'Id di un laboratorio',
            'required': False,
            'type': 'string'
        },
    ]


class ApiPublicationsListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'year',
            'description': 'Anno',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'type',
            'description': 'Id di una tipologia di community',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'structure',
            'description': 'Struttura di un docente',
            'required': True,
            'type': 'string'
        },

    ]
