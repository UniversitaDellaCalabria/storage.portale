from drf_spectacular.utils import OpenApiExample

COMPANIES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Company",
        value={
            "id": 1,
            "PIva": "IT12345678901",
            "agencyName": "Tech Innovations SRL",
            "agencyUrl": "https://techinnovations.com",
            "image": "https://example.com/company_logo.jpg",
            "description": "Azienda specializzata in innovazioni tecnologiche.",
            "unicalReferent": "Prof. Luigi Bianchi",
            "unicalReferentId": "encrypted_id_1",
            "techAreaId": 301,
            "techAreaDescription": "Informatica e Automazione",
            "isSpinoff": True,
            "isStartup": False,
            "isActive": True
        },
        description="Esempio di un'azienda innovativa attiva con dettagli su area tecnologica e referente universitario."
    )
]

TECH_AREA_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Tech Area",
        value={
            "id": 401,
            "description": "Robotica e Automazione"
        },
        description="Esempio di un'area tecnologica dedicata alla robotica e all'automazione."
    )
]
