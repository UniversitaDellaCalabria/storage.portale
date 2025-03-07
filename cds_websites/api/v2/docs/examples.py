from drf_spectacular.utils import OpenApiExample


TOPIC_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "TopicList",
        value={
            "id": 1,
            "description": "Programmazione Avanzata",
            "visibile": True,
        },
        description="Esempio di un topic visibile relativo a un CDS",
    ),
    OpenApiExample(
        "TopicList (Hidden)",
        value={
            "id": 2,
            "description": "Machine Learning",
            "visibile": False,
        },
        description="Esempio di un topic nascosto relativo a un CDS",
    ),
]


ARTICLES_TOPIC_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Article",
        value={
            "id": 1,
            "title": "Regolamento Esami",
            "topicId": "101",
            "topicDescription": "Norme relative agli esami",
            "visibile": True,
            "order": "1",
            "type": "Article",
            "content": {
                "text": "Gli esami devono essere sostenuti nelle date previste dal calendario accademico."
            },
            "subArticles": [
                {
                    "id": 11,
                    "ordine": "1.1",
                    "title": "Modalità d'esame",
                    "text": "L'esame può essere scritto o orale a seconda del corso.",
                    "visibile": True,
                }
            ],
            "otherData": [
                {
                    "id": 21,
                    "ordine": "2",
                    "title": "Riferimenti normativi",
                    "text": "Articolo 10 del regolamento accademico.",
                    "link": "https://www.universita.it/regolamento.pdf",
                    "typeId": "REF",
                    "type": "Reference",
                    "visibile": True,
                }
            ],
        },
        description="Esempio di un articolo relativo a un CDS con contenuto testuale, sotto-articoli e riferimenti normativi.",
    ),
    OpenApiExample(
        "Object",
        value={
            "id": 2,
            "title": "Struttura Didattica",
            "topicId": "102",
            "topicDescription": "Organizzazione dei corsi",
            "visibile": True,
            "order": "2",
            "type": "Object",
            "content": [
                {
                    "id": 201,
                    "yearRegDidID": 2023,
                    "objectId": 301,
                    "object": {"name": "Piano di Studi", "details": "Dettagli del corso"},
                    "classObjectId": 401,
                    "objectText": "Il piano di studi prevede corsi obbligatori e opzionali.",
                }
            ],
            "subArticles": [],
            "otherData": [],
        },
        description="Esempio di un oggetto relativo a un CDS che rappresenta una struttura didattica.",
    ),
]



STUDY_PLANS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Study Plan",
        value={
            "id": 1,
            "regDidId": 101,
            "relevanceCod": "A1",
            "yearCoorteId": "2023",
            "yearRegPlanId": 2023,
            "regPlanDes": "Piano di studi Informatica",
            "defFlg": "Y",
            "statusCod": "ACTIVE",
            "statusDes": "Attivo",
            "regPlansPdrId": "PDR001",
            "regPlansPdrCod": "PDR-INF",
            "regPlansPdrDes": "Piano regolatore Informatica",
            "regPlansPdrCoorteIdYear": "2023",
            "regPlansPdrYear": "2023",
            "flgExpSegStu": "N",
            "cdSDuration": "3",
            "planTabs": [
                {
                    "id": 201,
                    "des": "Primo Anno",
                    "cod": "Y1",
                    "pdsCod": "INF-Y1",
                    "pdsDes": "Anno 1 Informatica",
                    "claMiurCod": "L-31",
                    "claMiurDes": "Scienze e Tecnologie Informatiche",
                    "commonFlg": "N",
                    "statutario": True,
                    "APT": False,
                    "afRequired": [
                        {
                            "id": 301,
                            "des": "Matematica",
                            "vinId": "MAT101",
                            "year": 1,
                            "regSceCodType": "REQ",
                            "sceCodType": "BAS",
                            "eceDesType": "Fondamenti",
                            "regSceCodDes": "Obbligatorio",
                            "umRegSceCodType": "Crediti",
                            "minUnt": 6,
                            "maxUnt": 12,
                            "opzFlg": "N",
                            "required": [
                                {
                                    "scopeId": "SCI",
                                    "sceId": 401,
                                    "sceDes": "Analisi Matematica",
                                    "scopeDes": "Scienze di Base",
                                    "settCod": "MAT/05",
                                    "creditValue": 6,
                                    "cycleDes": "Semestre 1",
                                    "afDescription": "Analisi 1",
                                    "afId": 501,
                                    "afCod": "ANA101",
                                    "afType": "Obbligatorio",
                                    "afScope": "Matematica",
                                    "afSubModules": [
                                        {
                                            "id": 601,
                                            "cod": "ANA101-M1",
                                            "name": "Limiti e Derivate",
                                            "semester": "Semestre 1",
                                            "sttCod": "MAT/05",
                                            "creditValue": 3,
                                            "partitionCod": "PRIMAP",
                                            "partitionDescription": "Parte 1",
                                            "extendedPartitionCod": "EXT-PRIMAP",
                                            "extendedPartitionDes": "Modulo esteso",
                                        }
                                    ],
                                }
                            ],
                            "filAnd": [
                                {
                                    "filAndId": 701,
                                    "sceId": 301,
                                    "filOrId": "FILTRO1",
                                    "filOrDes": "Alternativa",
                                    "tipoFiltroCod": "OPT",
                                    "tipoFiltroDes": "Opzionale",
                                    "courseTypeSceFilAndCod": "B1",
                                    "cdsSceFilAndId": "CDS-INF",
                                    "cdsSceFilAndCod": "INF",
                                    "cdsSceFilAndNome": "Corso di Informatica",
                                    "notFlg": "N",
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        description="Esempio di un piano di studi con le relative materie obbligatorie e opzionali.",
    ),
]
