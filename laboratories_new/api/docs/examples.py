from drf_spectacular.utils import OpenApiExample

LABORATORY_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Laboratory Example",
        value={
            "id": 42,
            "completionReferentId": "encrypted_id_001",
            "completionReferentName": "Bianchi Laura",
            "scientificDirectorId": "encrypted_id_002",
            "scientificDirectorName": "Neri Giovanni",
            "name": "Laboratorio di Robotica Avanzata",
            "acronym": "LRA",
            "logo": "/media/laboratori/loghi/lra.png",
            "equipment": "Bracci robotici, stampanti 3D, sensori intelligenti",
            "departmentReferentId": 10,
            "departmentReferentCod": "DIINF",
            "departmentReferentName": "Dipartimento di Ingegneria dell'Informazione",
            "infrastructureId": 3,
            "infrastructureName": "Piattaforma Meccatronica Integrata",
            "interdepartmental": "SI",
            "extraDepartments": [
                {"id": "DMATH", "name": "Dipartimento di Matematica"},
                {"id": "DFIS", "name": "Dipartimento di Fisica"},
            ],
            "area": "Automazione e Meccatronica",
            "servicesScope": "Supporto a progetti industriali tramite prototipazione rapida",
            "researchScope": "Sviluppo di nuove architetture robotiche per l'interazione uomo-macchina",
            "teachingScope": "Laboratori didattici per corsi di robotica e automazione",
            "scopes": [
                {"id": 1, "description": "Servizi conto terzi"},
                {"id": 2, "description": "Ricerca interna"},
            ],
            "erc0": [
                {
                    "idErc0": "PE7",
                    "description": "Systems and communication engineering",
                    "erc1List": [
                        {
                            "idErc1": "PE7_4",
                            "description": "Automation, control systems",
                        }
                    ],
                }
            ],
            "researchPersonnel": [{"id": "encrypted_id_003", "name": "Verdi Luca"}],
            "techPersonnel": [
                {
                    "matricola": "encrypted_id_004",
                    "name": "Russo Carla",
                    "ruolo": "Tecnico di laboratorio",
                }
            ],
            "offeredServices": [
                {
                    "name": "Prototipazione rapida",
                    "description": "Servizio di stampa 3D per componenti meccanici",
                },
                {
                    "name": "Test su sistemi embedded",
                    "description": "Supporto alla validazione di firmware",
                },
            ],
            "location": [{"building": "Edificio 9", "floor": "2", "note": "Ala ovest"}],
            "URL": "http://laboratori.universita.it/lra",
            "visible": "SI",
        },
        description="Esempio completo di un laboratorio con referenti, dipartimenti, personale e servizi offerti",
    )
]

LABORATORIES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Laboratory Summary",
        value={
            "id": 42,
            "name": "Laboratorio di Robotica Avanzata",
            "acronym": "LRA",
            "logo": "/media/laboratori/loghi/lra_logo.png",
            "area": "Ingegneria e Tecnologie",
            "departmentName": "Dipartimento di Ingegneria Meccanica e Aerospaziale",
            "departmentId": 5,
            "departmentCod": "DIMEA",
            "interdepartmental": "SI",
            "extraDepartments": [
                {
                    "id": "DIEI",
                    "name": "Dipartimento di Ingegneria Elettrica e dell'Informazione",
                },
                {"id": "DII", "name": "Dipartimento di Ingegneria Industriale"},
            ],
            "infrastructureId": 3,
            "infrastructureName": "Centro per l’Innovazione Robotica",
            "dimension": "500 mq",
            "scientificDirector": "Dr. Maria Bianchi",
            "scientificDirectorId": "encrypted_id_001",
            "researchPersonnel": [
                {"id": "encrypted_id_002", "name": "Rossi Luca"},
                {"id": "encrypted_id_003", "name": "Verdi Chiara"},
            ],
            "scopes": [
                {"id": 1, "description": "Ricerca applicata"},
                {"id": 2, "description": "Collaborazioni industriali"},
            ],
            "techPersonnel": [
                {
                    "matricola": "encrypted_id_004",
                    "name": "Neri Paolo",
                    "ruolo": "Tecnico di laboratorio",
                }
            ],
            "servicesScope": "Supporto a progetti industriali nel settore della robotica.",
            "researchScope": "Sviluppo di algoritmi per la robotica autonoma.",
            "teachingScope": "Attività didattiche per corsi magistrali e dottorati.",
            "visible": "SI",
        },
        description="Example of a simplified laboratory object with main fields and aggregated data.",
    )
]

LABORATORIES_AREA_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio area laboratorio",
        value={"area": "Tecnologie dell'informazione"},
        response_only=True,
    )
]

LABORATORIES_SCOPES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio tipologia attività",
        value={"id": 1, "description": "Sviluppo software"},
        response_only=True,
    )
]

INFRASTRUCTURE_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio infrastruttura",
        value={"id": 10, "description": "Infrastruttura Cloud"},
        response_only=True,
    )
]

ERC0_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio ERC0",
        value={"idErc0": "PE", "description": "Physical Sciences and Engineering"},
        response_only=True,
    )
]

ERC1_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio ERC1",
        value={
            "idErc0": "PE",
            "description": "Physical Sciences and Engineering",
            "erc1List": [
                {"codErc1": "PE1", "description": "Mathematics"},
                {"codErc1": "PE2", "description": "Fundamental Physics"},
            ],
        },
        response_only=True,
    )
]

ERC2_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio ERC2",
        value={
            "idErc0": "PE",
            "description": "Physical Sciences and Engineering",
            "erc1List": [
                {
                    "codErc1": "PE1",
                    "description": "Mathematics",
                    "erc2List": [
                        {"codErc2": "PE1_1", "description": "Logic and Foundations"},
                        {"codErc2": "PE1_2", "description": "Algebra"},
                    ],
                }
            ],
        },
        response_only=True,
    )
]

ASTER1_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio ASTER1",
        value={
            "idErc0": "PE",
            "description": "Physical Sciences and Engineering",
            "aster1_list": [{"idAster1": 101, "description": "Tecnologie emergenti"}],
        },
        response_only=True,
    )
]

ASTER2_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Esempio ASTER2",
        value={
            "idErc0": "PE",
            "description": "Physical Sciences and Engineering",
            "aster1_list": [
                {
                    "idAster1": 101,
                    "description": "Tecnologie emergenti",
                    "aster2_list": [
                        {"idAster2": 201, "description": "Intelligenza Artificiale"},
                        {"idAster2": 202, "description": "Robotica"},
                    ],
                }
            ],
        },
        response_only=True,
    )
]
