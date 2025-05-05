from drf_spectacular.utils import OpenApiExample

BASE_RESEARCH_LINES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Base Research Line",
        value={
            "id": 1,
            "description": "Studi teorici sull’intelligenza artificiale",
            "results": "5 pubblicazioni su riviste peer-reviewed",
            "year": 2023,
            "erc2Id": "PE6_11",
            "erc2Name": "Machine learning",
            "teachers": [
                {
                    "id": "encrypted_id_001",
                    "name": "Bianchi Luca",
                    "departmentName": "Dipartimento di Ingegneria dell'Informazione",
                    "departmentCod": "DIINF"
                }
            ],
            "visible": True
        },
        description="Example of a base research line with ERC classification and related teachers",
    )
]

APPLIED_RESEARCH_LINES_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Applied Research Line",
        value={
            "id": 2,
            "description": "Sviluppo di prototipi per la diagnosi automatica",
            "results": "1 brevetto depositato, 2 progetti applicati",
            "year": 2022,
            "aster2Id": "AST01",
            "aster2Name": "Tecnologie per la salute",
            "teachers": [
                {
                    "id": "encrypted_id_002",
                    "name": "Rossi Maria",
                    "departmentName": "Dipartimento di Ingegneria Biomedica",
                    "departmentCod": "DIBIO"
                }
            ],
            "visible": True
        },
        description="Example of an applied research line with ASTER classification and related teachers",
    )
]

