from drf_spectacular.utils import OpenApiExample

TEACHERS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Teacher Basic",
        value={
            "id": "encrypted_id_001",
            "name": "Rossi Mario",
            "role": "PA",
            "roleDescription": "Professore Associato",
            "SSDCod": "INF/01",
            "SSDDescription": "Informatica",
            "CVFull": "Testo completo del CV in italiano",
            "CVShort": "Sintesi del CV in italiano",
            "profileId": 3,
            "profileDescription": "Professore di ruolo",
            "profileShortDescription": "Prof. ruolo",
            "email": ["mario.rossi@univ.it"],
        },
        description="Example of a basic teacher profile.",
    )
]
TEACHER_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Teacher Full",
        value={
            "id": "encrypted_id_002",
            "name": "Verdi Anna",
            "departmentInfo": [
                {
                    "departmentId": 12,
                    "departmentCod": "DMATH",
                    "departmentName": "Dipartimento di Matematica"
                }
            ],
            "role": "PO",
            "roleDescription": "Professore Ordinario",
            "SSDCod": "MAT/05",
            "SSDDescription": "Analisi Matematica",
            "office": "Edificio 1, stanza 23",
            "moreInfo": [
                {
                    "ORCID": "0000-0002-1825-0097",
                    "PHOTOPATH": "/media/photos/verdi_anna.jpg",
                    "PATHCV": "/media/cv/verdi_cv.pdf",
                    "BREVEBIO": "Professoressa ordinaria in analisi matematica...",
                    "ORARIORICEVIMENTO": "Lunedì 10:00 - 12:00"
                }
            ],
            "officeReference": ["Segreteria Matematica"],
            "email": ["anna.verdi@univ.it"],
            "pec": ["anna.verdi@pec.univ.it"],
            "telOffice": ["051-2094000"],
            "telCelOffice": ["320-1234567"],
            "fax": ["051-2094001"],
            "webSite": ["https://verdi.univ.it"],
            "cv": ["https://verdi.univ.it/cv"],
            "functions": [
                {
                    "functionCod": "DIR",
                    "structureCod": "DMATH",
                    "structureName": "Dipartimento di Matematica"
                }
            ],
            "CVFull": "CV completo in italiano...",
            "CVShort": "CV breve in italiano...",
            "profileId": 2,
            "profileDescription": "Professore Ordinario",
            "profileShortDescription": "Prof. ord."
        },
        description="Detailed teacher profile with contact info and functions.",
    )
]
PUBLICATIONS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Publication Example",
        value={
            "id": 101,
            "title": "Deep Learning for Computer Vision",
            "abstract": "Questo lavoro presenta un'analisi approfondita dei modelli CNN...",
            "collection": "Artificial Intelligence",
            "community": "Computer Science",
            "publication": "Conference Paper",
            "label": "Proc. of ICML 2023",
            "year": 2023,
            "url": "https://repository.univ.it/handle/123456789/101"
        },
        description="Example of a research publication entry.",
    )
]
PUBLICATION_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Publication Example",
        value={
            "id": 123,
            "title": "Deep Learning in Medical Imaging",
            "abstract": "This paper explores the application of deep learning in diagnosing diseases.",
            "collection": "Machine Learning Publications",
            "community": "Computer Science",
            "publication": "IEEE Transactions on Medical Imaging",
            "label": "IEEE TMI, Vol. 40, No. 1",
            "contributors": [],
            "authors": [
                {
                    "id": "encrypted_matricola_001",
                    "name": "Bianchi Luca",
                    "email": ["l.bianchi@university.it"]
                },
                {
                    "id": "encrypted_matricola_002",
                    "name": "Neri Giulia Maria",
                    "email": ["g.neri@university.it"]
                }
            ],
            "year": 2024,
            "url": "https://example.com/publications/123"
        },
        description="An example of a scientific publication with metadata and authors.",
    )
]
TEACHERS_BASE_RESEARCH_LINES_EXAMPLE = [
    OpenApiExample(
        "Teacher Base Research Line Example",
        value={
            "id": 101,
            "description": "Machine learning methods for big data analysis",
            "results": "5 journal articles and 2 conference papers published",
            "ERC0Id": "PE6",
            "ERC0Name": "Computer science and informatics"
        },
        description="An example of a teacher's base research line, with related ERC classification.",
    )
]
TEACHERS_APPLIED_RESEARCH_LINES_EXAMPLE = [
    OpenApiExample(
        "Teacher Applied Research Line Example",
        value={
            "id": 202,
            "description": "Application of AI to smart manufacturing systems",
            "results": "2 patents filed and 1 industrial project completed",
            "ERC0Id": "PE8",
            "ERC0Name": "Products and processes engineering"
        },
        description="An example of a teacher's applied research line, including practical outcomes.",
    )
]
TEACHERS_STUDY_ACTIVITIES_EXAMPLE = [
    OpenApiExample(
        "Study Activity",
        value={
            "id": 101,
            "cod": "INF1234",
            "name": "Fondamenti di Informatica",
            "cdsId": 45,
            "cdsCod": "LM-32",
            "regDidId": 99,
            "cdsName": "Ingegneria Informatica",
            "aa": 2023,
            "year": 1,
            "semester": "Primo Semestre",
            "etcs": "6",
            "language": "Italiano",
            "ssd": "INF/01",
            "compulsory": True,
            "partitionCod": 1,
            "partitionDescription": "Lezione",
            "partitionType": "LEZ",
            "partitionStart": "2023-10-01",
            "partitionEnd": "2024-01-15"
        },
        description="Example of a study activity taught by a teacher",
    )
]
TEACHERS_MATERIALS_EXAMPLE = [
    OpenApiExample(
        "Teaching Material",
        value={
            "id": 501,
            "title": "Dispensa di Fondamenti",
            "text": "Materiale introduttivo al corso",
            "textUrl": "https://example.com/materiale/dispensa.pdf",
            "order": 1,
            "active": True,
            "publicationDate": "2023-11-01"
        },
        description="Example of teaching material uploaded by a teacher",
    )
]
PUBLICATIONS_COMMUNITY_TYPES_EXAMPLE = [
    OpenApiExample(
        "Publication Community",
        value={
            "id": 12,
            "name": "Computer Science Department"
        },
        description="Example of a publication community type",
    )
]
TEACHERS_NEWS_EXAMPLE = [
    OpenApiExample(
        "Teacher News",
        value={
            "id": 301,
            "title": "Conferenza Internazionale su AI",
            "textType": "Abstract",
            "text": "Presentazione alla conferenza AI 2024",
            "textUrl": "https://example.com/news/conferenza_ai",
            "order": "1",
            "active": "true",
            "publicationDate": "2024-04-15"
        },
        description="Example of a news item published by a teacher",
    )
]
