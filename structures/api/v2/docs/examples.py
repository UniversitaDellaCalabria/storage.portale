from drf_spectacular.utils import OpenApiExample

STRUCTURES_LIST_EXAMPLES = [
    OpenApiExample(
        "Structure List Example",
        value=[
            {
                "cod": "DIP001",
                "name": "Dipartimento di Ingegneria dell'Informazione",
                "typeName": "Dipartimento",
                "typeCOD": "DIP",
                "URL": "https://dipartimento-informatica.univ.it",
                "childs": [
                    {
                        "cod": "LAB001",
                        "name": "Laboratorio di Intelligenza Artificiale",
                        "typeName": "Laboratorio",
                        "typeCOD": "LAB"
                    },
                    {
                        "cod": "SEZ002",
                        "name": "Sezione di Informatica Teorica",
                        "typeName": "Sezione",
                        "typeCOD": "SEZ"
                    }
                ]
            },
            {
                "cod": "DIP002",
                "name": "Dipartimento di Scienze Matematiche",
                "typeName": "Dipartimento",
                "typeCOD": "DIP",
                "URL": "https://dipartimento-matematica.univ.it",
                "childs": []
            }
        ],
        description="Esempio di lista di strutture con sottostrutture annidate",
        response_only=True,
    )
]

STRUCTURE_DETAIL_EXAMPLES = [
    OpenApiExample(
        "Structure Detail Example",
        value={
            "cod": "DIP001",
            "name": "Dipartimento di Ingegneria dell'Informazione",
            "typeName": "Dipartimento",
            "typeCOD": "DIP",
            "fatherId": "ATENEO",
            "fatherName": "Università degli Studi",
            "email": ["dipartimento.informatica@univ.it"],
            "pec": ["dipartimento.informatica@pec.univ.it"],
            "tfr": ["+39 0123456789"],
            "personnelFunctions": [
                {
                    "id": "enc_id_003",
                    "name": "Rossi Mario",
                    "function": "Direttore di Dipartimento",
                    "functionCod": "DIR"
                }
            ],
            "mission": "Promuovere la ricerca e la didattica nel campo dell'informatica e dell'ingegneria dell'informazione.",
            "URL": "https://dipartimento-informatica.univ.it"
        },
        description="Esempio di dettaglio di una struttura",
        response_only=True,
    )
]

STRUCTURE_TYPES_EXAMPLES = [
    OpenApiExample(
        "Structure Types Example",
        value=[
            {
                "typeName": "Dipartimento",
                "typeCOD": "DIP"
            },
            {
                "typeName": "Centro di Ricerca",
                "typeCOD": "CR"
            },
            {
                "typeName": "Laboratorio",
                "typeCOD": "LAB"
            },
            {
                "typeName": "Sezione",
                "typeCOD": "SEZ"
            }
        ],
        description="Esempio di tipi di struttura",
        response_only=True,
    )
]

STRUCTURE_FUNCTIONS_EXAMPLES = [
    OpenApiExample(
        "Structure Functions Example",
        value=[
            {
                "typeCOD": "DIP",
                "function": "DIR",
                "functionDescription": "Direttore di Dipartimento"
            },
            {
                "typeCOD": "DIP",
                "function": "VDIR",
                "functionDescription": "Vice Direttore di Dipartimento"
            },
            {
                "typeCOD": "LAB",
                "function": "RESP",
                "functionDescription": "Responsabile di Laboratorio"
            }
        ],
        description="Esempio di funzioni nelle strutture",
        response_only=True,
    )
]

DEPARTMENTS_EXAMPLES = [
    OpenApiExample(
        "Departments List Example",
        value=[
            {
                "id": 1,
                "cod": "DIINF",
                "name": "Dipartimento di Ingegneria dell'Informazione",
                "nameShort": "DIP. ING. INFO",
                "URL": "https://dipartimento-informatica.univ.it"
            },
            {
                "id": 2,
                "cod": "DISMAT",
                "name": "Dipartimento di Scienze Matematiche",
                "nameShort": "DIP. SC. MAT",
                "URL": "https://dipartimento-matematica.univ.it"
            },
            {
                "id": 3,
                "cod": "DISFIS",
                "name": "Dipartimento di Scienze Fisiche",
                "nameShort": "DIP. SC. FIS",
                "URL": "https://dipartimento-fisica.univ.it"
            }
        ],
        description="Esempio di lista dei dipartimenti",
        response_only=True,
    )
]

DEPARTMENT_DETAIL_EXAMPLES = [
    OpenApiExample(
        "Department Detail Example",
        value={
            "id": 1,
            "cod": "DIINF",
            "name": "Dipartimento di Ingegneria dell'Informazione",
            "nameShort": "DIP. ING. INFO",
            "URL": "https://dipartimento-informatica.univ.it"
        },
        description="Esempio di dettaglio di un dipartimento",
        response_only=True,
    )
]