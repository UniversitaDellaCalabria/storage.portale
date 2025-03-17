from drf_spectacular.utils import OpenApiExample

PROJECTS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Project",
        value={
            "id": 1,
            "startingYear": 2023,
            "infrastructureId": "INF001",
            "infrastructureDescription": "Laboratorio di Informatica",
            "territorialScopeId": 10,
            "territorialScopeDescription": "Regione Lombardia",
            "typeProgramId": 2,
            "typeProgramDescription": "Progetto di Ricerca",
            "title": "Studio sull'Intelligenza Artificiale",
            "description": "Un progetto dedicato all'esplorazione di tecniche avanzate di IA",
            "abstract": "Questo progetto analizza le reti neurali convoluzionali per il riconoscimento delle immagini.",
            "techAreaId": "TEC001",
            "techAreaDescription": "Tecnologie dell'Informazione",
            "projectImage": "https://example.com/project_image.jpg",
            "scientificDirectors": [
                {"id": "encrypted_id_1", "name": "Prof. Mario Rossi"},
                {"id": "encrypted_id_2", "name": "Dott.ssa Laura Bianchi"}
            ],
            "researchers": [
                {"id": "encrypted_id_3", "name": "Dr. Giuseppe Verdi"},
                {"id": "encrypted_id_4", "name": "Dott.ssa Anna Neri"}
            ],
            "isActive": True
        },
        description="Esempio di un progetto attivo con dettagli su infrastruttura, ambito territoriale e personale coinvolto."
    )
]

TERRITORIAL_SCOPES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Territorial Scope",
        value={
            "id": 101,
            "description": "Provincia di Milano"
        },
        description="Esempio di un ambito territoriale riferito alla Provincia di Milano."
    )
]

PROGRAM_TYPES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Program Type",
        value={
            "id": 201,
            "description": "Progetto Interdisciplinare"
        },
        description="Esempio di una tipologia di programma interdisciplinare."
    )
]

INFRASTRUCTURES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Infrastructure",
        value={
            "id": "INF002",
            "description": "Dipartimento di Ingegneria Elettronica"
        },
        description="Esempio di un'infrastruttura accademica dedicata all'Ingegneria Elettronica."
    )
]
