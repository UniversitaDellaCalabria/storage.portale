from drf_spectacular.utils import OpenApiExample

PHD_DETAIL_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "PhD Course",
        value={
            "academicYear": 2023,
            "departmentID": 101,
            "departmentCod": "INF",
            "departmentName": "Dipartimento di Informatica",
            "cdsCOD": "DOTT123",
            "cdsName": "Dottorato in Informatica",
            "regID": 2023001,
            "regCOD": "REG2023INF",
            "cdSDuration": 3,
            "cdSECTS": 180,
            "cdSAttendance": True,
            "courseType": "DOTT",
            "courseName": "Dottorato",
            "cycleNumber": 39,
            "studyPlanCOD": "PDS01",
            "studyPlanDes": "Piano didattico 2023/2024"
        },
        description="Detail of a PhD course"
    )
]

PHD_ACTIVITY_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "PhD Activity",
        value={
            "id": 1,
            "activityName": "Machine Learning Avanzato",
            "ssd": "INF/01",
            "hours": 30,
            "cfu": 6,
            "activityType": "LEZ",
            "activityTypology": "Lezione frontale",
            "referentPhd": "Dottorato in Informatica",
            "cycle": "39",
            "referentStructureId": "INF001",
            "referentStructureName": "Dipartimento di Informatica",
            "activityContents": "Apprendimento supervisionato e reti neurali",
            "prerequisites": "Programmazione, Statistica",
            "minStudents": 3,
            "maxStudents": 20,
            "finalTest": "Progetto finale",
            "finalTestMode": "Elaborato scritto",
            "activityStart": "2025-03-01",
            "activityEnd": "2025-05-30",
            "classroomsTimetable": "Lun e Mer 10:00-12:00",
            "showTimetable": "true",
            "notes": "Frequenza obbligatoria",
            "mainTeachers": [
                {
                    "personId": "encrypted_id_1",
                    "personName": "Prof. Mario Rossi"
                }
            ],
            "otherTeachers": [
                {
                    "personId": "encrypted_id_2",
                    "personName": "Dr.ssa Anna Verdi"
                }
            ]
        },
        description="Detail of a PhD activity"
    )
]

PHD_ACTIVITY_TYPOLOGY_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Activity Typology",
        value={
            "id": 10,
            "name": "Seminario"
        },
        description="Typology of a PhD activity"
    )
]

PHD_ACTIVITY_TYPE_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Activity Type",
        value={
            "activityType": "LEZ"
        },
        description="Type of a PhD activity (e.g. lecture, seminar)"
    )
]
PHD_SSD_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Scientific Sector",
        value={
            "ssd": "INF/01"
        },
        description="Scientific disciplinary sector of the activity"
    )
]
PHD_REF_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "PhD Reference",
        value={
            "referentPhd": "Dottorato in Scienze dei Dati"
        },
        description="Reference to the PhD program"
    )
]
PHD_REF_STRUCTURE_SERIALIZER_EXAMPLE = [
    OpenApiExample(
        "Structure Reference",
        value={
            "referentStructureName": "Dipartimento di Matematica"
        },
        description="Name of the referring structure for the activity"
    )
]
