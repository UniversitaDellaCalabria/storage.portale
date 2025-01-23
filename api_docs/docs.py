from drf_spectacular.utils import OpenApiExample

# VIEW SUMMARY AND DESCRIPTION

# DegreeType
DEGREETYPE_LIST_SUMMARY= "List of all degree types"
DEGREETYPE_LIST_DESCRIPTION= "Retrieve a list of all available degree types with their codes and descriptions."

# AcademicYear
ACADEMICYEAR_LIST_SUMMARY= "List of all academic years"
ACADEMICYEAR_LIST_DESCRIPTION= "Retrieve a list of all available academic years in descending order."

# StudyActivity
## List
STUDYACTIVITY_LIST_SUMMARY= "List of all study activities"
STUDYACTIVITY_LIST_DESCRIPTION= (
    "Retrieve a paginated list of all study activities with brief information. "
    "They can be filtered by academic year, course year, course code, department, "
    "SSD, teaching, teacher, and course year."
)
## Retrieve
STUDYACTIVITY_RETRIEVE_SUMMARY= "Retrieve a specific study activity"
STUDYACTIVITY_RETRIEVE_DESCRIPTION= (
    "Retrieve detailed information for a single study activity. "
    "The study activity is identified by its ID."
)

# CdsArea
CDSAREA_LIST_SUMMARY= "List of all the CDS areas"
CDSAREA_LIST_DESCRIPTION= "Retrieve a list of all distinct Course of Study areas in Italian or in English."

# CdsExpired
CDSEXPIRED_LIST_SUMMARY= "List of expired courses"
CDSEXPIRED_LIST_DESCRIPTION= (
    "Retrieve a list of expired courses that are no longer active. "
    "This excludes courses that have been morphed into new ones."
)

# CdsMorph
## List
CDSMORPH_LIST_SUMMARY= "List all CDS morphing histories"
CDSMORPH_LIST_DESCRIPTION= (
    "Retrieve a list of all Course of Study morphing histories. "
    "This shows how the ids of the curses have evolved over time, tracking their "
    "previous versions."
)
## Retrieve
CDSMORPH_RETRIEVE_SUMMARY= "Retrieve a specific CDS morphing history"
CDSMORPH_RETRIEVE_DESCRIPTION= (
    "Retrieve detailed information for a single Course of Study morphing history. "
    "The morphing history is identified by its ID."
)

# AcademicPaths
## List
ACADEMICPATHS_LIST_SUMMARY= "Academic Pathways Management"
ACADEMICPATHS_LIST_DESCRIPTION= (
    "API endpoints for managing academic pathways. Provides functionality to list all "
    "academic pathways and retrieve detailed information about specific pathways, "
    "including their associated study activities."
)
## Retrieve
ACADEMICPATHS_RETRIEVE_SUMMARY= "Retrieve a specific academic pathway"
ACADEMICPATHS_RETRIEVE_DESCRIPTION= (
    "Retrieve detailed information for a single academic pathway. "
    "The academic pathway is identified by its ID."
)

# SERIALIZERS SCHEMAS


CDS_SERIALIZER_EXAMPLE = [
    OpenApiExample(
    "CDS", 
     value={
            "regDidId": 123,
            "cdSId": 456,
            "cdSCod": "CDS123",
            "academicYear": 2023,
            "name": "Computer Science",
            "area": "Engineering",
            "departmentId": 789,
            "departmentCod": "ENG",
            "departmentName": "Engineering Department",
            "type": "Bachelor",
            "typeDescription": "Three-year degree",
            "courseClassCod": "L-31",
            "courseClassName": "Scienze e Tecnologie Informatiche",
            "courseInterClassCod": "L-8/L-31",
            "courseInterClassDes": "Ingegneria e Informatica",
            "erogationMode": "In presenza",
            "languages": ["ENG", "ITA"],
            "duration": 3,
            "ECTS": 180,
            "mandatoryAttendance": True,
            "status": "Active",
            "jointDegree": "Yes",
            "studyManifesto": "/media/path/manifesto.pdf",
            "didacticRegulation": "/media/path/regulation.pdf",
            "ordinamentoDidattico": "/media/path/ordinamento.pdf",
            "yearOrdinamentoDidattico": 2020,
        },
     description="Area of a CDS"
    )
]

CDS_AREA_SERIALIZER_EXAMPLE = [
    OpenApiExample(
    "CDS Area", 
    value={"areaCds": "Engineering"}, 
    description="Area of a CDS"
    )
]

CDS_EXPIRED_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Expired CDS",
            value={"cdsCod": "CS101", "aaRegDid": "2024", "cdsDuration": "3"},
            description="Information about an expired CDS",
        )
    ]

DEGREE_TYPE_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "CDS Morph",
            value={"idCds": 101, "idCdsPrec": 100},
            description="Information about the morphing of a CDS",
        )
    ]

ACADEMIC_YEARS_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Academic Year",
            value={"aaRegDid": "2024/2025"},
            description="Academic year information",
        )
    ]

STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Esempio di DidatticaAttivitaFormativa",
            summary="Esempio completo di oggetto DidatticaAttivitaFormativa",
            value={
                "af_id": 1,
                "cds": 101,
                "cdsord_id": 202,
                "cdsord_cod": "CDS001",
                "aa_ord_id": 303,
                "stato_cdsord_cod": "ATT",
                "regdid": 404,
                "regdid_cod": "REG001",
                "aa_regdid_id": 505,
                "stato_regdid_cod": "VAL",
                "stato_appr_regdid_cod": "APP",
                "pds_regdid": 606,
                "pds_cod": "PDS001",
                "pds_des": "Descrizione del percorso",
                "comune_flg": 1,
                "attinenza_cod": "ATT001",
                "of_id": 707,
                "aa_off_id": 808,
                "stato_of_cod": "ATT",
                "tipo_comp_af_id": 909,
                "tipo_comp_af_cod": "TIP001",
                "des_tipo_comp_af": "Descrizione componente attività formativa",
                "af_gen_id": 1010,
                "af_gen_cod": "GEN001",
                "des": "Descrizione attività formativa",
                "af_gen_des_eng": "General description in English",
                "anno_corso": 2,
                "lista_anni_corso": "1, 2, 3",
                "af_regdid_id": 1111,
                "sett_cod": "SETT001",
                "sett_des": "Settore disciplinare",
                "tipo_af_cod": "TAF001",
                "tipo_af_des": "Tipologia attività formativa",
                "tipo_af_intercla_cod": "INTER001",
                "tipo_af_intercla_des": "Interclasse",
                "amb_id": 1212,
                "ambito_des": "Ambito disciplinare",
                "peso": 6,
                "um_peso_cod": "CFU",
                "um_peso_des": "Crediti formativi universitari",
                "freq_obblig_flg": 1,
                "ore_min_freq": 20,
                "ore_att_front": 30,
                "num_max_reit": 3,
                "libera_flg": 0,
                "scelta_mod_flg": 1,
                "tipo_esa_cod": "ESA001",
                "tipo_esa_des": "Esame scritto",
                "tipo_val_cod": "VAL001",
                "tipo_val_des": "Valutazione orale",
                "tipo_ins_cod": "INS001",
                "tipo_ins_des": "Insegnamento obbligatorio",
                "serale_flg": 0,
                "no_media_flg": 1,
                "sostegno_flg": 0,
                "nota": "Nota aggiuntiva",
                "af_pdr_id": 1313,
                "af_radice_id": 1414,
                "num_liv_albero": 2,
                "ciclo_des": "Primo ciclo",
                "data_inizio": "2023-09-01T00:00:00Z",
                "data_fine": "2024-06-30T00:00:00Z",
                "tipo_ciclo_cod": "CIC001",
                "des_tipo_ciclo": "Ciclo unico",
                "matricola_resp_did": 1515,
                "cod_fis_resp_did": "CODFIS001",
                "ruolo_resp_did_cod": "DOC",
                "url_sito_web": "https://www.university.it/corso",
                "lista_lin_did_af": "IT, EN",
                "lista_mod_did_af": "Modulo 1, Modulo 2",
                "lista_taf_set_cfu": "TAF1-SET1-6CFU",
                "mutuata_flg": 0,
                "af_master_id": 1616,
                "num_af_figlie": 2,
                "num_af_foglie": 5,
                "non_erogabile_flg": 0,
                "fat_part_stu_cod": "FAT001",
                "fat_part_stu_des": "Partecipazione obbligatoria",
                "part_stu_id": 1717,
                "part_stu_cod": "PART001",
                "part_stu_des": "Partecipazione studente",
            },
        )
    ]

STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE =[
        OpenApiExample(
            "Single",
            value=[
                {
                    "id": "AF001",
                    "genCod": "GEN123",
                    "des": "...",
                    "cdsId": "CDS001",
                    "cdsCod": "IT101",
                    "language": ["IT", "EN"],
                    "fatherCode": "F001",
                    "fatherName": "Computer Science",
                    "regDidId": "REG2025",
                    "dipDes": "Dipartimento di Informatica",
                    "dipCod": "DI123",
                    "courseYear": "1",
                    "academicYear": "2025",
                    "semester": "Second",
                    "SSDCod": "INF/01",
                    "SSD": "Informatica",
                    "partitionCod": "P001",
                    "partitionDes": "Standard",
                    "extendedPartitionCod": "EP001",
                    "extendedPartitionDes": "Advanced Topics",
                    "cdsName": "Computer Science",
                    "teacherId": "encrypted-id",
                    "teacherName": "Prof. Mario Rossi",
                    "studyPlanDes": "Piano di Studi Base",
                }
            ],
            description="Details of a single study activity",
        ),
        OpenApiExample(
            "Multiple",
            value=[
                {
                    "id": "AF001",
                    "genCod": "GEN123",
                    "des": "...",
                    "cdsId": "CDS001",
                    "cdsCod": "IT101",
                    "language": ["IT", "EN"],
                    "fatherCode": "F001",
                    "fatherName": "Computer Science",
                    "regDidId": "REG2025",
                    "dipDes": "Dipartimento di Informatica",
                    "dipCod": "DI123",
                    "courseYear": "1",
                    "academicYear": "2025",
                    "semester": "Second",
                    "SSDCod": "INF/01",
                    "SSD": "Informatica",
                    "partitionCod": "P001",
                    "partitionDes": "Standard",
                    "extendedPartitionCod": "EP001",
                    "extendedPartitionDes": "Advanced Topics",
                    "cdsName": "Computer Science",
                    "teacherId": "encrypted-id",
                    "teacherName": "Prof. Mario Rossi",
                    "studyPlanDes": "Piano di Studi Base",
                },
                {
                    "id": "AF002",
                    "genCod": "GEN456",
                    "des": "Data Structures",
                    "cdsId": "CDS002",
                    "cdsCod": "IT102",
                    "language": ["EN"],
                    "fatherCode": "F002",
                    "fatherName": "Software Engineering",
                    "regDidId": "REG2026",
                    "dipDes": "Dipartimento di Informatica",
                    "dipCod": "DI124",
                    "courseYear": "2",
                    "academicYear": "2026",
                    "semester": "First",
                    "SSDCod": "INF/02",
                    "SSD": "Algoritmi",
                    "partitionCod": "P002",
                    "partitionDes": "Standard",
                    "extendedPartitionCod": "EP002",
                    "extendedPartitionDes": "Core Topics",
                    "cdsName": "Software Engineering",
                    "teacherId": "encrypted-id-2",
                    "teacherName": "Dr. Anna Bianchi",
                    "studyPlanDes": "Piano di Studi Avanzato",
                },
            ],
            description="Details of multiple study activities",
        ),
    ]
STUDY_ACTIVITY_LITE_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Study Activity Lite",
            value={
                "id": 1,
                "name": "Mathematics",
                "year": 1,
                "cycle": "First Semester",
                "etcs": 6,
                "type": "Basic",
            },
            description="Simplified view of a study activity",
        )
    ]
CDS_MORPH_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Single",
            value={
                "cds": 101,
                "cds_prec": 100,
            },
            description="Represents a single link between two cds, where `cds` is the current and `cds_prec` is the previous one.",
        ),
        OpenApiExample(
            "Multiple",
            value=[
                {
                    "cds": 201,
                    "cds_prec": 200,
                },
                {
                    "cds": 301,
                    "cds_prec": 300,
                },
            ],
            description="Represents multiple links between cds.",
        ),
    ]

ACADEMIC_PATHWAYS_LIST_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Single",
            value=[
                {
                    "id": 1,
                    "cod": "123",
                    "name": "GENERIC",
                    "duration": 2,
                }
            ],
            description="Single academic pathway",
        ),
        OpenApiExample(
            "Multiple",
            value=[
                {
                    "id": 1,
                    "cod": "123",
                    "name": "GENERIC",
                    "duration": 2,
                },
                {
                    "id": 2,
                    "cod": "321",
                    "name": "OTHER",
                    "duration": 3,
                },
            ],
            description="Multiple academic pathways",
        ),
    ]

ACADEMIC_PATHWAYS_DETAIL_SERIALIZER_EXAMPLE = [
        OpenApiExample(
            "Example Academic Pathway",
            value={
                "id": 1,
                "cod": "PDS001",
                "name": "Example Academic Pathway",
                "activities": {
                    1: [
                        {
                            "af_id": 101,
                            "cod": "AF001",
                            "name": "Mathematics I",
                            "anno_corso": 1,
                            "cfu": 6,
                            "tipo_af_cod": "BASE",
                            "tipo_af_des": "Basic Activity",
                        },
                        {
                            "af_id": 102,
                            "cod": "AF002",
                            "name": "Physics I",
                            "anno_corso": 1,
                            "cfu": 6,
                            "tipo_af_cod": "BASE",
                            "tipo_af_des": "Basic Activity",
                        },
                    ],
                    2: [
                        {
                            "af_id": 201,
                            "cod": "AF003",
                            "name": "Advanced Mathematics",
                            "anno_corso": 2,
                            "cfu": 9,
                            "tipo_af_cod": "CHAR",
                            "tipo_af_des": "Characterizing Activity",
                        },
                    ],
                },
            },
            description="An example representation of an academic pathway with its activities grouped by year.",
        )
    ]