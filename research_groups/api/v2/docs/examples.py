from drf_spectacular.utils import OpenApiExample

RESEARCH_GROUPS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Research Group",
        value={
            "id": 1,
            "name": "Artificial Intelligence and Machine Learning",
            "description": "Research on AI models, algorithms and applications.",
            "codErc1": "PE6",
            "descrizioneErc1": "Computer science and informatics",
            "teachers": [
                {
                    "id": "encrypted_id_001",
                    "name": "Rossi Mario",
                    "departmentName": "Dipartimento di Ingegneria dell'Informazione",
                    "departmentCod": "DIINF"
                },
                {
                    "id": "encrypted_id_002",
                    "name": "Verdi Anna",
                    "departmentName": "Dipartimento di Matematica",
                    "departmentCod": "DMATH"
                }
            ]
        },
        description="Example of a research group with associated teachers",
    )
]
