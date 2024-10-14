from generics.filters import GenericApiFilter
from addressbook.models import Personale


class AddressbookListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by last name (starts with).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "phone",
            "description": "Phone number to filter.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "structure",
            "description": "Organizational structure ID to filter.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "structuretypes",
            "description": "Structure type codes to filter (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "role",
            "description": "Roles to filter (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": ",".join(
                    f"{role['cd_ruolo']}"
                    for role in Personale.objects.all()
                    .values("cd_ruolo", "ds_ruolo_locale")
                    .order_by("ds_ruolo_locale")
                    .distinct()[:3]
                ),
            },
        },
        {
            "name": "structuretree",
            "description": "Structure tree ID to filter.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "taxpayer_id",
            "description": "Taxpayer ID to filter.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
            },
        },
    ]


class PersonnelCfListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "roles",
            "description": "Roles to filter (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": ",".join(
                    f"{role['cd_ruolo']}"
                    for role in Personale.objects.all()
                    .values("cd_ruolo", "ds_ruolo_locale")
                    .order_by("ds_ruolo_locale")
                    .distinct()[:3]
                ),
            },
        },
    ]


class AddressbookStructuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by the name of the organizational structure.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "Department of Mathematics",
            },
        },
        {
            "name": "father",
            "description": "ID of the parent structure (if applicable). Must be a valid ID of an existing organizational unit.",
            "required": False,
            "in": "query",
            "schema": {
                "type": "integer",
                "example": 1234,
                "format": "int32",
            },
        },
        {
            "name": "type",
            "description": "List of types of organizational structures (comma-separated).",
            "required": False,
            "in": "query",
            "schema": {
                "type": "string",
                "example": "DPT,FAC",
            },
        },
    ]
