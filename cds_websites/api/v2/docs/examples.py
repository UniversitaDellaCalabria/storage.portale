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
