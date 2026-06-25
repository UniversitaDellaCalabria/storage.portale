from drf_spectacular.utils import OpenApiExample

CDS_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "CDS",
        value={
            "regDidId": 123,
            "status": "Active",
            "cdsId": 456,
            "cdsCod": "CDS123",
            "academicYear": 2023,
            "area": "Engineering",
            "name": "Computer Science",
            "departmentId": 789,
            "departmentCod": "ENG",
            "departmentName": "Engineering Department",
            "type": "Bachelor",
            "typeDescription": "Three-year degree",
            "courseClassCod": "L-31",
            "courseClassName": "Scienze e Tecnologie Informatiche",
            "courseInterClassCod": "L-8/L-31",
            "courseInterClassDes": "Ingegneria e Informatica",
            "erogationMode": "In presenza",
            "languages": ["ENG", "ITA"],
            "duration": 3,
            "ECTS": 180,
            "mandatoryAttendance": True,
            "profiles": {
                "Software Engineer": {
                    "FUNZIONI": "Sviluppo software e gestione di sistemi informatici",
                    "COMPETENZE": "Programmazione avanzata, gestione database",
                    "SBOCCHI": "Aziende IT, ricerca accademica, startup"
                }
            },
            "satisfactionSurvey": 4,
            "jointDegree": "Yes",
            "studyManifesto": "/media/path/manifesto.pdf",
            "didacticRegulation": "/media/path/regulation.pdf",
            "teachingSystem": "/media/path/ordinamento.pdf",
            "teachingSystemYear": 2020,
            "otherData": [
                {
                    "coordinatorId": 1001,
                    "coordinatorName": "Dr. John Doe",
                    "viceCoordinatorId": 1002,
                    "viceCoordinatorName": "Dr. Jane Smith",
                    "studyManifesto": "/media/path/manifesto.pdf",
                    "educationalRules": "/media/path/regulation.pdf",
                    "educationalSystem": "/media/path/ordinamento.pdf"
                }
            ],
            "officesData": [
                {
                    "ordine": 1,
                    "nome_ufficio": "Segreteria Didattica",
                    "matricola_riferimento": 2001,
                    "nome_origine_riferimento": "Mario Rossi",
                    "telefono": "+39 0123456789",
                    "email": "segreteria@university.it",
                    "edificio": "A",
                    "piano": "2",
                    "orari": "Lun-Ven 9:00-12:00",
                    "sportello_online": "https://university.it/sportello"
                }
            ],
            "groups": [
                {
                    "ordine": 1,
                    "id": 3001,
                    "descr_breve_it": "Docenti",
                    "descr_breve_en": "Faculty",
                    "descr_lunga_it": "Gruppo dei docenti del corso",
                    "descr_lunga_en": "Group of course professors",
                    "members": [
                        {
                            "ordine": 1,
                            "id": 4001,
                            "matricola": 5001,
                            "cognome": "Bianchi",
                            "nome": "Luca",
                            "funzione_it": "Professore Ordinario",
                            "funzione_en": "Full Professor"
                        }
                    ]
                }
            ],
            "periods": [
                {
                    "description": "Primo semestre",
                    "start": "2023-09-15",
                    "end": "2024-01-31"
                },
                {
                    "description": "Secondo semestre",
                    "start": "2024-02-15",
                    "end": "2024-06-30"
                }
            ],
            "currentPeriods": [
                {
                    "description": "Primo semestre",
                    "start": "2023-09-15",
                    "end": "2024-01-31"
                }
            ]
        },
        description="Detail of a CDS",
    )
]

CDS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "CDS",
        value={
            "regDidId": 123,
            "cdSId": 456,
            "cdSCod": "CDS123",
            "academicYear": 2023,
            "name": "Computer Science",
            "area": "Engineering",
            "departmentId": 789,
            "departmentCod": "ENG",
            "departmentName": "Engineering Department",
            "type": "Bachelor",
            "typeDescription": "Three-year degree",
            "courseClassCod": "L-31",
            "courseClassName": "Scienze e Tecnologie Informatiche",
            "courseInterClassCod": "L-8/L-31",
            "courseInterClassDes": "Ingegneria e Informatica",
            "erogationMode": "In presenza",
            "languages": ["ENG", "ITA"],
            "duration": 3,
            "ECTS": 180,
            "mandatoryAttendance": True,
            "status": "Active",
            "jointDegree": "Yes",
            "studyManifesto": "/media/path/manifesto.pdf",
            "didacticRegulation": "/media/path/regulation.pdf",
            "ordinamentoDidattico": "/media/path/ordinamento.pdf",
            "yearOrdinamentoDidattico": 2020,
        },
        description="Area of a CDS",
    )
]

CDS_AREA_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "CDS Area", value={"areaCds": "Engineering"}, description="Area of a CDS"
    )
]

CDS_EXPIRED_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Expired CDS",
        value={"cdsCod": "CS101", "aaRegDid": "2024", "cdsDuration": "3"},
        description="Information about an expired CDS",
    )
]

DEGREE_TYPE_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Degree Type",
        value={
            "courseType": "LM",
            "courseTypeDescription": "Laurea Magistrale",
        },
        description="Information about the morphing of a CDS",
    )
]

ACADEMIC_YEARS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Academic Year",
        value={"aaRegDid": "2024/2025"},
        description="Academic year information",
    )
]

STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Esempio di DidatticaAttivitaFormativa",
        summary="Esempio completo di oggetto DidatticaAttivitaFormativa",
        value={
            "StudyActivityID": 10001,
            "StudyActivityCod": "INF001",
            "StudyActivityName": "Fondamenti di Informatica",
            "StudyActivityPartitionDes": None,
            "StudyActivityRoot": None,
            "StudyActivityCdSID": 456,
            "StudyActivityCdSCod": "CDS123",
            "StudyActivityRegDidId": 123,
            "StudyActivityStudyPlans": ["Percorso Generale"],
            "StudyActivityErogationYear": 2023,
            "StudyActivityECTS": 9,
            "StudyActivityLanguage": ["Italiano"],
            "StudyActivityModalities": [
                {
                    "ModalityActivityCod": "CONV",
                    "ModalityActivityDescription": "Convenzionale",
                }
            ],
            "StudyActivitySSDCod": "INF/01",
            "StudyActivitySSD": "Informatica",
            "StudyActivityCompulsory": "Si",
            "StudyActivityCdSName": "Ingegneria Informatica",
            "StudyActivityYear": 1,
            "StudyActivitySemester": "Primo Semestre",
            "StudyActivityTeacherID": "mrossi",
            "StudyActivityTeacherName": "Rossi Mario",
            "StudyActivityTeachingUnitTypeCod": "B",
            "StudyActivityTeachingUnitType": "Caratterizzanti",
            "StudyActivitiesModules": [],
            "StudyActivityPartitions": [],
            "StudyActivityHours": [
                {
                    "ActivityType": "LEZIONE",
                    "Hours": 60,
                    "StudyActivityTeacherID": "mrossi",
                    "StudyActivityTeacherName": "Rossi Mario",
                }
            ],
            "StudyActivityBorrows": [],
            "StudyActivityBorrowedFrom": None,
            "StudyActivityContents": [
                {
                    "StudyActivityContentCod": "OBIET",
                    "StudyActivityContentTitle": "Obiettivi formativi",
                    "StudyActivityContentDes": "<p>Il corso introduce i fondamenti dell'informatica...</p>",
                },
                {
                    "StudyActivityContentCod": "PROGR",
                    "StudyActivityContentTitle": "Programma",
                    "StudyActivityContentDes": "<p>Algoritmi, strutture dati, sistemi di numerazione...</p>",
                },
            ],
        },
        description="Dettaglio completo di un'attività formativa",
    )
]

STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Single",
        value=[
            {
                "StudyActivityID": 10001,
                "StudyActivityCdSID": 456,
                "StudyActivityCdSCod": "CDS123",
                "StudyActivityCdSName": "Ingegneria Informatica",
                "DepartmentName": "Dipartimento di Ingegneria Informatica",
                "DepartmentCod": "DIMES",
                "StudyActivityFathers": [],
                "StudyActivityRegDidId": 123,
                "StudyActivityCod": "INF001",
                "StudyActivityName": "Fondamenti di Informatica",
                "StudyActivityYear": 1,
                "StudyActivityAcademicYear": 2023,
                "StudyActivityLanguage": "Italiano",
                "StudyActivitySemester": "Primo Semestre",
                "StudyActivitySSDCod": "INF/01",
                "StudyActivitySSD": "Informatica",
                "StudyActivityTeacherName": "Rossi Mario",
                "StudyActivityTeacherID": "mrossi",
                "StudyActivityStudyPlans": ["Percorso Generale"],
                "StudyActivityPartitionCod": None,
                "StudyActivityPartitionDes": None,
                "StudyActivityExtendedPartitionCod": None,
                "StudyActivityExtendedPartitionDes": None,
            }
        ],
        description="Details of a single study activity",
    ),
    OpenApiExample(
        "Multiple",
        value=[
            {
                "StudyActivityID": 10001,
                "StudyActivityCdSID": 456,
                "StudyActivityCdSCod": "CDS123",
                "StudyActivityCdSName": "Ingegneria Informatica",
                "DepartmentName": "Dipartimento di Ingegneria Informatica",
                "DepartmentCod": "DIMES",
                "StudyActivityFathers": [],
                "StudyActivityRegDidId": 123,
                "StudyActivityCod": "INF001",
                "StudyActivityName": "Fondamenti di Informatica",
                "StudyActivityYear": 1,
                "StudyActivityAcademicYear": 2023,
                "StudyActivityLanguage": "Italiano",
                "StudyActivitySemester": "Primo Semestre",
                "StudyActivitySSDCod": "INF/01",
                "StudyActivitySSD": "Informatica",
                "StudyActivityTeacherName": "Rossi Mario",
                "StudyActivityTeacherID": "mrossi",
                "StudyActivityStudyPlans": ["Percorso Generale"],
                "StudyActivityPartitionCod": None,
                "StudyActivityPartitionDes": None,
                "StudyActivityExtendedPartitionCod": None,
                "StudyActivityExtendedPartitionDes": None,
            },
            {
                "StudyActivityID": 10002,
                "StudyActivityCdSID": 456,
                "StudyActivityCdSCod": "CDS123",
                "StudyActivityCdSName": "Ingegneria Informatica",
                "DepartmentName": "Dipartimento di Ingegneria Informatica",
                "DepartmentCod": "DIMES",
                "StudyActivityFathers": [
                    {
                        "FatherID": 9999,
                        "FatherName": "Laboratorio di Sistemi (Percorso A)",
                        "RegdidId": 123,
                    }
                ],
                "StudyActivityRegDidId": 123,
                "StudyActivityCod": "SIS002",
                "StudyActivityName": "Sistemi Operativi",
                "StudyActivityYear": 2,
                "StudyActivityAcademicYear": 2023,
                "StudyActivityLanguage": "Italiano",
                "StudyActivitySemester": "Secondo Semestre",
                "StudyActivitySSDCod": "INF/01",
                "StudyActivitySSD": "Informatica",
                "StudyActivityTeacherName": "Bianchi Anna",
                "StudyActivityTeacherID": "abianchi",
                "StudyActivityStudyPlans": ["Percorso A", "Percorso B"],
                "StudyActivityPartitionCod": "A",
                "StudyActivityPartitionDes": "Partizione A",
                "StudyActivityExtendedPartitionCod": "EXT-A",
                "StudyActivityExtendedPartitionDes": "Partizione Estesa A",
            },
        ],
        description="Details of multiple study activities",
    ),
]
STUDY_ACTIVITY_LITE_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Study Activity Lite",
        value={
            "id": 101,
            "name": "Analisi Matematica I",
            "year": 1,
            "cycle": "Primo Semestre",
            "etcs": 9,
            "type": "Attività formativa di base",
        },
        description="Vista semplificata di un'attività formativa",
    )
]
CDS_MORPH_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Single",
        value={"idCds": 101, "idCdsPrec": 100},
        description="Represents a single link between two cds, where `cds` is the current and `cds_prec` is the previous one.",
    ),
    OpenApiExample(
        "Multiple",
        value=[
            {"idCds": 201, "idCdsPrec": 200},
            {"idCds": 301, "idCdsPrec": 300},
        ],
        description="Represents multiple links between cds.",
    ),
]

ACADEMIC_PATHWAYS_LIST_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Single",
        value=[
            {
                "id": 1,
                "cod": "123",
                "name": "GENERIC",
                "duration": 2,
            }
        ],
        description="Single academic pathway",
    ),
    OpenApiExample(
        "Multiple",
        value=[
            {
                "id": 1,
                "cod": "123",
                "name": "GENERIC",
                "duration": 2,
            },
            {
                "id": 2,
                "cod": "321",
                "name": "OTHER",
                "duration": 3,
            },
        ],
        description="Multiple academic pathways",
    ),
]

ACADEMIC_PATHWAYS_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Example Academic Pathway",
        value={
            "id": 1,
            "cod": "PDS001",
            "name": "Example Academic Pathway",
            "activities": {
                1: [
                    {
                        "id": 101,
                        "name": "Analisi Matematica I",
                        "year": 1,
                        "cycle": "Primo Semestre",
                        "etcs": 9,
                        "type": "Attività formativa di base",
                    },
                    {
                        "id": 102,
                        "name": "Fisica I",
                        "year": 1,
                        "cycle": "Secondo Semestre",
                        "etcs": 9,
                        "type": "Attività formativa di base",
                    },
                ],
                2: [
                    {
                        "id": 201,
                        "name": "Algoritmi e Strutture Dati",
                        "year": 2,
                        "cycle": "Primo Semestre",
                        "etcs": 9,
                        "type": "Attività caratterizzante",
                    }
                ],
            },
        },
        description="An example representation of an academic pathway with its activities grouped by year.",
    )
]

STUDY_PLANS_SERIALIZER_FULL_EXAMPLE = [
    OpenApiExample(
        "Study Plan",
        value={
            "RegPlanId": 1001,
            "RegDidId": 123,
            "YearCoorteId": 2023,
            "StatusCod": "A",
            "StatusDes": "Approvato",
            "CdSDuration": 3,
            "PlanTabs": [
                {
                    "PlanTabId": 201,
                    "PlanTabDes": "Percorso Comune",
                    "PlanTabCod": "COM",
                    "PdsDes": "Percorso Generico",
                    "ClaMiurCod": "L-31",
                    "ClaMiurDes": "Scienze e Tecnologie Informatiche",
                    "CommonFlg": 1,
                    "Rules": [
                        {
                            "SceId": 301,
                            "SceDes": "Attività obbligatorie anno 1",
                            "Year": 1,
                            "RegSceCodType": "OBB",
                            "UmRegSceCodType": "CFU",
                            "MinUnt": 60,
                            "MaxUnt": 60,
                            "NotePre": None,
                            "NotePost": None,
                            "Filters": None,
                            "Required": [
                                {
                                    "AfId": 10001,
                                    "AfCod": "INF001",
                                    "AfDescription": "Fondamenti di Informatica",
                                    "CycleDes": ["Primo Semestre"],
                                    "CreditValue": 9,
                                    "SettCod": ["INF/01"],
                                    "AfType": "Fondamentali",
                                    "AfScope": "B",
                                    "AfSubModules": [],
                                },
                                {
                                    "AfId": 10002,
                                    "AfCod": "MAT001",
                                    "AfDescription": "Analisi Matematica I",
                                    "CycleDes": ["Primo Semestre"],
                                    "CreditValue": 9,
                                    "SettCod": ["MAT/05"],
                                    "AfType": "Fondamentali",
                                    "AfScope": "A",
                                    "AfSubModules": [],
                                },
                            ],
                            "AfChoices": [
                                [
                                    {
                                        "AfId": 10010,
                                        "AfCod": "LIN001",
                                        "AfDescription": "Lingua Inglese",
                                        "StudyActivitySemester": "Secondo Semestre",
                                        "CreditValue": 3,
                                        "SettCod": "L-LIN/12",
                                        "CycleDes": ["Secondo Semestre"],
                                        "AfType": None,
                                        "AfScope": "E",
                                        "AfSubModules": [],
                                    }
                                ]
                            ],
                        }
                    ],
                }
            ],
        },
        description="Esempio di un piano di studi con le relative materie obbligatorie e opzionali.",
    ),
]
SORTING_CONTACTS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Sorting Contact",
        value={
            "fullName": "Rossi, Mario",
            "id": "mrossi",
            "teacherDepartmentID": "DIMES",
            "teacherOffice": "Dipartimento di Ingegneria Informatica",
            "departmentURL": "https://www.unical.it/dimes",
        },
        description="Contatto docente con dati di ordinamento per la rubrica",
    )
]
 
STUDY_PLANS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Study Plan Activities",
        value={
            "RegPlanId": 1001,
            "RegDidId": 123,
            "YearCoorteId": 2023,
            "CdSDuration": 3,
            "PlanTabs": [
                {
                    "StudyPlanID": 201,
                    "StudyPlanCOD": "COM",
                    "StudyPlanName": "Percorso Comune",
                    "StudyActivities": {
                        1: [
                            {
                                "StudyActivityID": 10001,
                                "StudyActivityCod": "INF001",
                                "StudyActivityName": "Fondamenti di Informatica",
                                "StudyActivityECTS": 9,
                                "StudyActivityCompulsory": True,
                                "StudyActivitySSD": ["INF/01"],
                                "StudyActivitySemester": ["Primo Semestre"],
                                "StudyActivityTeachingUnitType": "Caratterizzanti",
                            }
                        ],
                        2: [
                            {
                                "StudyActivityID": 10002,
                                "StudyActivityCod": "SIS001",
                                "StudyActivityName": "Sistemi Operativi",
                                "StudyActivityECTS": 9,
                                "StudyActivityCompulsory": True,
                                "StudyActivitySSD": ["INF/01"],
                                "StudyActivitySemester": ["Primo Semestre"],
                                "StudyActivityTeachingUnitType": "Caratterizzanti",
                            }
                        ],
                    },
                }
            ],
        },
        description="Piano di studi con attività raggruppate per anno di corso",
    )
]
 