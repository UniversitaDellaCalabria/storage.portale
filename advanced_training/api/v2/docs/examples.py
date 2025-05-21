from drf_spectacular.utils import OpenApiExample

HIGH_FORMATION_MASTER_EXAMPLES = [
    OpenApiExample(
        "High Formation Master Example",
        value={
            "masterTitle": "Master in Data Science",
            "typeId": 1,
            "typeDescription": "Master universitario di I livello",
            "erogationMode": 2,
            "erogationModeDescription": "In presenza",
            "hours": 1500,
            "months": 12,
            "language": "Italiano",
            "courseStructure": "Università degli Studi - Aula Magna",
            "minParticipants": 10,
            "maxParticipants": 30,
            "masterYear": 2024,
            "departmentId": 3,
            "departmentCod": "DIINF",
            "departmentName": "Dipartimento di Ingegneria dell'Informazione",
            "listenersAccepted": "Sì",
            "maxListeners": 5,
            "admissionRequirements": "Laurea triennale in ambito tecnico-scientifico.",
            "titleIssued": "Diploma di Master Universitario",
            "doubleTitle": False,
            "scientificDirectorId": "enc_id_001",
            "scientificDirectorName": "Mario Rossi",
            "subscriptionFee": 3500,
            "listenersFee": 500,
            "workFunction": "Analista di dati, consulente in AI",
            "formationObjectivesSummerSchool": "Approfondimento intensivo su tecnologie emergenti.",
            "skills": "Machine Learning, AI, Data Mining",
            "jobOpportunities": "Data Scientist, AI Engineer, Business Analyst",
            "courseObjectives": "Formare professionisti in grado di progettare soluzioni data-driven.",
            "finalTestMode": "Progetto finale con presentazione",
            "numModules": 6,
            "internship": "Presso aziende convenzionate",
            "internshipHours": 200,
            "internshipCFU": 8,
            "internshipMonths": 2,
            "typeCompaniesInternship": "Società ICT, Start-up, Centri di ricerca",
            "contentTimesCriteriaCFU": "Ogni modulo vale 5 CFU e richiede 125 ore.",
            "projectWork": "Sviluppo di un'applicazione AI per problemi reali",

            "partners": [
                {
                    "id": 1,
                    "denomination": "TechCompany S.p.A.",
                    "type": "Azienda privata",
                    "URL": "https://techcompany.example.com"
                }
            ],
            "selections": [
                {
                    "id": 1,
                    "type": "Colloquio motivazionale"
                }
            ],
            "internalScientificCouncil": [
                {
                    "id": "enc_id_002",
                    "name": "Giulia Bianchi"
                }
            ],
            "externalScientificCouncil": [
                {
                    "name": "Luca Verdi",
                    "role": "Esperto esterno",
                    "institution": "Consiglio Nazionale delle Ricerche"
                }
            ],
            "teachingPlan": [
                {
                    "module": "Fondamenti di AI",
                    "ssd": "INF/01",
                    "hours": 40,
                    "cfu": 5,
                    "finalTest": "Sì"
                }
            ],
            "teachingAssignments": [
                {
                    "module": "Machine Learning Avanzato",
                    "hours": 30,
                    "teacher": "Dott. Elisa Neri",
                    "qualification": "Professore Associato",
                    "institution": "Università degli Studi",
                    "type": "Interno"
                }
            ]
        },
        description="Example of a high formation master course with full structure and details",
        response_only=True,
    )
]

HIGH_FORMATION_COURSE_TYPES_EXAMPLES = [
    OpenApiExample(
        "Course Type - I livello",
        value={
            "id": 1,
            "description": "Master universitario di I livello"
        },
        description="Esempio di tipo corso di alta formazione di I livello",
        response_only=True,
    ),
    OpenApiExample(
        "Course Type - II livello",
        value={
            "id": 2,
            "description": "Master universitario di II livello"
        },
        description="Esempio di tipo corso di alta formazione di II livello",
        response_only=True,
    ),
]

EROGATION_MODES_EXAMPLES = [
    OpenApiExample(
        "In presenza",
        value={
            "id": 1,
            "description": "In presenza"
        },
        description="Modalità di erogazione del corso: in presenza",
        response_only=True,
    ),
    OpenApiExample(
        "Online",
        value={
            "id": 2,
            "description": "Online"
        },
        description="Modalità di erogazione del corso: completamente online",
        response_only=True,
    ),
    OpenApiExample(
        "Mista",
        value={
            "id": 3,
            "description": "Blended (presenza + online)"
        },
        description="Modalità di erogazione del corso: mista",
        response_only=True,
    ),
]