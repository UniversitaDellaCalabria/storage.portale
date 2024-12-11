from generics.filters import GenericApiFilter


class CdsListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "academicyear",
            "description": "Academic year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
                "example": 2024,
            },
        },
        {
            "name": "departmentcod",
            "description": "Code of a department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "departmentid",
            "description": "ID of a department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "departmentname",
            "description": "Name of a department.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "coursetype",
            "description": "Type of course of study.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "courseclasscod",
            "description": "Code of the course of study class.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "courseclassname",
            "description": "Name of the course of study class.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "jointdegree",
            "description": "Joint degree type.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "array",
                "items": {
                    "type": "string",
                },
                "example": ["D", "N", "S"],
            },
        },
        {
            "name": "regdid",
            "description": "ID of the didactic regulation.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cdscod",
            "description": "Code of a course of study.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "cdslanguage",
            "description": "Language of the course of study.",
            "required": False,
            "in": "query",
            "schema": {"type": "string", "example": "eng"},
        },
        {
            "name": "area",
            "description": "Area of the course of study.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]


class AllActivitiesListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "department",
            "description": "Department code.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "cds",
            "description": "Course of study name.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "period",
            "description": "Period of the course.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "academic_year",
            "description": "Academic year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "ssd",
            "description": "SSD (Scientific Disciplinary Sector).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "teaching",
            "description": "Teaching name.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "teacher",
            "description": "Teacher's last name.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "course_year",
            "description": "Course year.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
        {
            "name": "cds_cod",
            "description": "Code of a course of study.",
            "required": False,
            "in": "query",
            "schema": {"type": "string"},
        },
        {
            "name": "teacher_code",
            "description": "Teacher's encrpyted matricola.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]


class CdsExpiredFilter(GenericApiFilter):
    search_params = [
        {
            "name": "coursetypes",
            "description": "Types of course of study (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "L,LM,LM5,LM6"
            },
        },
        {
            "name": "yearfrom",
            "description": "First year of the search window.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "format": "int32",
            },
        },
    ]
