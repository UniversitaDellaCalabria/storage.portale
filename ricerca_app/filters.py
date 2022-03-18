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
            'name': 'cdscod',
            'description': 'Codice di un Corso di Studi',
            'required': False,
        },
        {
            'name': 'cdslanguage',
            'description': 'Lingua del corso di studi',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'area',
            'description': 'Area del Corso di Studio',
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
            'name': 'coderc1',
            'description': 'Lista di Codici di erc1',
            'required': False,
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
        {
            'name': 'year',
            'description': 'Anno Erogazione Attività',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            }
        },
    ]


class ApiBaseResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
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
            'name': 'year',
            'description': 'Anno',
            'required': False,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
    ]


class ApiAllResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'department',
            'description': 'Codice di un dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'year',
            'description': 'Anno',
            'required': False,
            'schema': {
                    'type': 'integer',
                    'format': 'int32',
            }
        },
        {
            'name': 'department',
            'description': 'Dipartimento',
            'required': False,
            'type': 'string',
        },
        {
            'name': 'ercs',
            'description': 'Lista di codici erc1',
            'required': False,
            'type': 'string',
        },
        {
            'name': 'asters',
            'description': 'Lista di codici aster1',
            'required': False,
            'type': 'string',
        },
        {
            'name': 'exclude_base',
            'description': 'Esclude le linee di ricerca di base',
            'required': False,
            'schema': {
                    'type': 'boolean',
            }
        },
        {
            'name': 'exclude_applied',
            'description': 'Esclude le linee di ricerca applicate',
            'required': False,
            'schema': {
                    'type': 'boolean',
            }
        },
    ]


class ApiAppliedResearchLinesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'teacher',
            'description': 'Matricola di un docente',
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
            'name': 'year',
            'description': 'Anno',
            'required': False,
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
            'name': 'phone',
            'description': 'Numero di telefono',
            'required': False,
            'type': 'string'
        },
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
        {
            'name': 'depth',
            'description': 'Livello di profondità sotto strutture (0 = nessuno, max 1)',
            'required': False,
            'schema': {
                  'type': 'integer',
                  'format': 'int32',
              }
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
                     {'name': 'infrastructure',
                      'description': 'Id Infrastruttura Riferimento',
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
            'required': False,
            'type': 'string'
        },

    ]


class ApiPatentsListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'techarea',
            'description': 'Area Tecnologica',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'structure',
            'description': 'Codice di una struttura',
            'required': False,
            'type': 'string'
        },
    ]


class ApiCompaniesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'techarea',
            'description': 'Area Tecnologica',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'spinoff',
            'description': 'Spinoff',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'startup',
            'description': 'Startup',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
    ]


class ApiProjectsListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'techarea',
            'description': 'Area Tecnologica',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'infrastructure',
            'description': 'Id Infrastruttura Riferimento',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'year',
            'description': 'Anno del progetto',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'programtype',
            'description': 'Id Tipologia Programma',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'territorialscope',
            'description': 'Id Ambito Territoriale',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
    ]


class ApiHighFormationMastersListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'coursetype',
            'description': 'Tipo Corso',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'erogation',
            'description': 'Erogazione',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'department',
            'description': 'Dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'director',
            'description': 'Direttore Scientifico',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'language',
            'description': 'Lingua Master',
            'required': False,
            'type': 'string'
        },
    ]


class ApiAllActivitiesListFilter(GenericApiFilter):
    search_params = [
        {
            'name': 'department',
            'description': 'Dipartimento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'cds',
            'description': 'CDS',
            'required': False,
            'schema': {
                'type': 'string',
            },
        },
        {
            'name': 'period',
            'description': 'Periodo',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'academic_year',
            'description': 'Anno Accademico',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
        {
            'name': 'ssd',
            'description': 'SSD',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'teaching',
            'description': 'Insegnamento',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'teacher',
            'description': 'Docente',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'course_year',
            'description': 'Anno Di Corso',
            'required': False,
            'schema': {
                'type': 'integer',
                'format': 'int32',
            },
        },
    ]
