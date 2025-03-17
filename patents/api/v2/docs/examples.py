from drf_spectacular.utils import OpenApiExample

PATENTS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Patent",
        value={
            "id": 1,
            "uniqueId": 123456,
            "title": "Sistema di monitoraggio ambientale basato su IA",
            "image": "https://example.com/patent_image.jpg",
            "abstract": "Un sistema avanzato che utilizza tecniche di intelligenza artificiale per monitorare i cambiamenti ambientali.",
            "urlKnowledgeShare": "https://knowledgeshare.com/patent/123456",
            "inizialTRL": "TRL 3 - Prova di concetto",
            "updatedTRL": "TRL 6 - Dimostrazione di sistema prototipale in ambiente rilevante",
            "enhancement": "Tecnologia brevettata implementata in sistemi di rilevazione ambientale.",
            "techAreaId": "TEC002",
            "areaDescription": "Tecnologie Ambientali e Sostenibilità",
            "inventors": [
                {"authorId": "encrypted_id_1", "authorName": "Prof. Marco Bianchi"},
                {"authorId": "encrypted_id_2", "authorName": "Dott.ssa Elena Verdi"}
            ],
            "isActive": True
        },
        description="Esempio di un brevetto attivo che illustra un sistema di monitoraggio ambientale basato su IA."
    )
]
