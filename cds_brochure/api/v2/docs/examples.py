from drf_spectacular.utils import OpenApiExample

BROCHURE_LIST_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Brochures List",
        value=[
            {
                "id": 1,
                "cdsCod": "CDS123",
                "academicYear": 2023,
                "cdsName": "Ingegneria Informatica"
            },
            {
                "id": 2,
                "cdsCod": "CDS456",
                "academicYear": 2024,
                "cdsName": "Scienze dell'Informazione"
            }
        ],
        description="List of brochures for different CDS",
    )
]

BROCHURE_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Brochure Detail",
        value={
            "id": 1,
            "cdsCod": "CDS123",
            "academicYear": 2023,
            "cdsName": "Ingegneria Informatica",
            "courseClassName": "Scienze e Tecnologie Informatiche",
            "courseInterClassDes": "Ingegneria e Informatica",
            "languages": ["ITA", "ENG"],
            "durationYears": 3,
            "seatsNumber": 200,
            "video": "https://example.com/video.mp4",
            "intro": "Questo corso forma ingegneri informatici specializzati nello sviluppo software.",
            "admission": "Accesso tramite test d'ingresso.",
            "goals": "Formare professionisti nel settore IT con competenze avanzate.",
            "jobOpportunities": "Aziende IT, startup, ricerca accademica.",
            "taxes": "Tasse universitarie annuali a partire da 1000€.",
            "scholarships": "Disponibili borse di studio per merito e reddito.",
            "concessions": "Agevolazioni per studenti lavoratori.",
            "shortDescription": "Corso di laurea triennale in Ingegneria Informatica.",
            "studyPlan": "Algoritmi, Programmazione, Basi di Dati, Sistemi Operativi.",
            "enrollmentMode": "Iscrizione online sul sito dell'università.",
            "exStudents": [
                {
                    "id": 101,
                    "name": "Mario Rossi",
                    "order": 1,
                    "profile": "Ingegnere Software presso TechCorp",
                    "link": "https://linkedin.com/in/mariorossi",
                    "photo": "https://example.com/photos/mariorossi.jpg"
                }
            ],
            "links": [
                {
                    "id": 201,
                    "order": 1,
                    "description": "Sito ufficiale del corso",
                    "link": "https://university.it/corso-ingegneria-informatica"
                }
            ],
            "sliders": [
                {
                    "id": 301,
                    "order": 1,
                    "description": "Immagine rappresentativa del corso"
                }
            ]
        },
        description="Detail of a brochure for a CDS",
    )
]
