from drf_spectacular.utils import OpenApiExample

ADDRESSBOOK_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Addressbook Example",
        value={
            "name": "Rossi Mario",
            "id": "encrypted_id_001",
            "roles": [
                {
                    "role": "PA",
                    "description": "Professore Associato",
                    "priorita": 1,
                    "structureCod": "123",
                    "structure": "Dipartimento di Matematica",
                    "structureTypeCOD": "DIP"
                }
            ],
            "officeReference": "Edificio A - Piano 2",
            "email": "mario.rossi@university.it",
            "pec": "mario.rossi@pec.university.it",
            "telOffice": "+39 051 2090001",
            "telCelOffice": "+39 333 1234567",
            "fax": "+39 051 2090002",
            "webSite": "https://www.university.it/rossi",
            "cv": "https://www.university.it/rossi/cv",
            "profileId": "PRF001",
            "profileDescription": "Docente senior",
            "profileShortDescription": "Senior"
        },
        description="Esempio di voce della rubrica con contatti e ruolo",
    )
]

ADDRESSBOOK_FULL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        name="Full Addressbook Example",
        value={
            "name": "Rossi Mario",
            "surname": "Rossi",
            "id": "encrypted_id_001",
            "taxpayer_ID": "RSSMRA80A01H501Z",
            "roles": [
                {
                    "role": "PA",
                    "description": "Professore Associato",
                    "priorita": 1,
                    "structureCod": "123",
                    "structure": "Dipartimento di Matematica",
                    "structureTypeCOD": "DIP",
                    "start": "2015-11-01"
                }
            ],
            "officeReference": "Edificio A - Piano 2",
            "email": "mario.rossi@university.it",
            "pec": "mario.rossi@pec.university.it",
            "telOffice": "+39 051 2090001",
            "telCelOffice": "+39 333 1234567",
            "fax": "+39 051 2090002",
            "webSite": "https://www.university.it/rossi",
            "cv": "https://www.university.it/rossi/cv",
            "profileId": "PRF001",
            "profileDescription": "Docente senior",
            "profileShortDescription": "Senior"
        },
        description="Esempio esteso di voce della rubrica con codice fiscale e data inizio ruolo",
    )
]
ADDRESSBOOK_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Addressbook Detail",
        value={
            "id": "encrypted_id_001",
            "name": "Mario Giuseppe",
            "surname": "Rossi",
            "taxpayer_ID": "RSSMRA80A01F205X",
            "gender": "M",
            "profileId": "DOC",
            "profileDescription": "Docente",
            "profileShortDescription": "Prof.",
            "teacher": True,
            "teacherCVFull": "Laureato in Ingegneria Informatica presso l'Università di Bologna nel 2005. Dottorato di ricerca in Computer Science nel 2008. Attualmente professore associato presso il Dipartimento di Ingegneria dell'Informazione.",
            "teacherCVShort": "Prof. Associato in Informatica, specializzato in AI e Machine Learning.",
            "roles": [
                {
                    "role": "PA",
                    "description": "Professore Associato",
                    "priorita": 1,
                    "structureCod": "DIINF",
                    "structure": "Dipartimento di Ingegneria dell'Informazione",
                    "structureTypeCOD": "DIP"
                }
            ],
            "personFunctions": [
                {
                    "teacherRole": "Coordinatore Corso di Laurea",
                    "tunctionCod": "COORD_CL",
                    "structureCod": "DIINF",
                    "structureName": "Dipartimento di Ingegneria dell'Informazione"
                }
            ],
            "email": "mario.rossi@university.it",
            "pec": "mario.rossi@pec.university.it",
            "telOffice": "+39 051 2093001",
            "telCelOffice": "+39 347 1234567",
            "fax": "+39 051 2093002",
            "webSite": "https://www.university.it/docenti/mario-rossi",
            "cv": "https://www.university.it/cv/mario-rossi",
            "officeReference": "Edificio A, Piano 3, Stanza 301"
        },
        description="Example of detailed addressbook entry for a university teacher",
    )
]

ADDRESSBOOK_FULL_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Addressbook Full Detail",
        value={
            "id": "encrypted_id_002",
            "name": "Anna Maria",
            "surname": "Verdi",
            "taxpayer_ID": "VRDNMR75B15H501Y",
            "gender": "F",
            "profileId": "PO",
            "profileDescription": "Professore Ordinario",
            "profileShortDescription": "Prof. Ord.",
            "teacher": True,
            "teacherCVFull": "Laureata in Matematica presso l'Università di Milano nel 2000. Dottorato di ricerca in Matematica Applicata nel 2003. Ricercatrice dal 2005 al 2010, Professore Associato dal 2010 al 2018, Professore Ordinario dal 2018.",
            "teacherCVShort": "Prof. Ordinario in Matematica, esperta in Analisi Numerica e Calcolo Scientifico.",
            "roles": [
                {
                    "role": "PO",
                    "description": "Professore Ordinario",
                    "priorita": 1,
                    "structureCod": "DMATH",
                    "structure": "Dipartimento di Matematica",
                    "structureTypeCOD": "DIP",
                    "start": "2018-11-01"
                }
            ],
            "personFunctions": [
                {
                    "teacherRole": "Direttore di Dipartimento",
                    "tunctionCod": "DIR_DIP",
                    "structureCod": "DMATH",
                    "structureName": "Dipartimento di Matematica"
                },
                {
                    "teacherRole": "Membro Senato Accademico",
                    "tunctionCod": "MEMBRO_SA",
                    "structureCod": "ATENEO",
                    "structureName": "Ateneo"
                }
            ],
            "email": "anna.verdi@university.it",
            "pec": "anna.verdi@pec.university.it",
            "telOffice": "+39 051 2094001",
            "telCelOffice": "+39 338 9876543",
            "fax": "+39 051 2094002",
            "webSite": "https://www.university.it/docenti/anna-verdi",
            "cv": "https://www.university.it/cv/anna-verdi",
            "officeReference": "Edificio B, Piano 2, Stanza 205"
        },
        description="Example of full detailed addressbook entry with role start date and multiple functions",
    )
]
PERSONNEL_CF_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Personnel CF",
        value={
            "name": "Rossi Mario Giuseppe",
            "Cf": "RSSMRA80A01F205X",
            "ID": "12345",
            "roleDescription": "Professore Associato",
            "role": "PA",
            "infrastructureId": "DIINF",
            "infrastructureDescription": "Dipartimento di Ingegneria dell'Informazione"
        },
        description="Example of personnel data with fiscal code and basic role information",
    )
]

ADDRESSBOOK_STRUCTURES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Addressbook Structure",
        value={
            "cod": "DIINF",
            "name": "Dipartimento di Ingegneria dell'Informazione",
            "typeName": "DIP",
            "typeCOD": "Dipartimento"
        },
        description="Example of organizational structure (department)",
    ),
    OpenApiExample(
        "Faculty Structure",
        value={
            "cod": "FING",
            "name": "Facoltà di Ingegneria",
            "typeName": "FAC",
            "typeCOD": "Facoltà"
        },
        description="Example of organizational structure (faculty)",
    ),
    OpenApiExample(
        "Research Center Structure",
        value={
            "cod": "CRAI",
            "name": "Centro di Ricerca in Intelligenza Artificiale",
            "typeName": "CEN",
            "typeCOD": "Centro di Ricerca"
        },
        description="Example of organizational structure (research center)",
    )
]

ROLES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Academic Roles",
        value=[
            {
                "role": "PO",
                "roleDescription": "Professore Ordinario"
            },
            {
                "role": "PA",
                "roleDescription": "Professore Associato"
            },
            {
                "role": "RIC",
                "roleDescription": "Ricercatore"
            }
        ],
        description="Example of available academic roles",
    ),
    OpenApiExample(
        "Administrative Roles",
        value=[
            {
                "role": "DIRIG",
                "roleDescription": "Dirigente"
            },
            {
                "role": "FUNZ",
                "roleDescription": "Funzionario"
            },
            {
                "role": "TECH",
                "roleDescription": "Tecnico"
            }
        ],
        description="Example of available administrative roles",
    )
]