from generics.filters import GenericApiFilter
from addressbook.models import Personale


class ApiAddressbookListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search by surname (starts with)",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "phone",
            "description": "Phone number to filter",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "structure",
            "description": "Organizational structure ID to filter",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "structuretypes",
            "description": "Structure type codes to filter (comma-separated)",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "role",
            "description": "Roles to filter (comma-separated)",
            "required": False,
            "schema": {
                "type": "string",
                "example": ",".join(
                    f"{role['cd_ruolo']}"
                    for role in Personale.objects.all()
                    .values("cd_ruolo", "ds_ruolo_locale")
                    .order_by("ds_ruolo_locale")
                    .distinct()[:3]  # Limit to 3 roles
                ),
            },
        },
        {
            "name": "structuretree",
            "description": "Structure tree ID to filter",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
        {
            "name": "taxpayer_id",
            "description": "Taxpayer ID to filter",
            "required": False,
            "schema": {
                "type": "string",
            },
        },
    ]


class ApiPersonnelCfListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "roles",
            "description": ("Roles to filter (comma-separated)"),
            "required": False,
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


class ApiAddressbookStructuresListFilter(GenericApiFilter):
    search_params = [
        {
            "name": "search",
            "description": "Search the name of the organizational structure. Supports partial search.",
            "required": False,
            "schema": {
                "type": "string",
                "example": "Department of Mathematics",
            },
        },
        {
            "name": "father",
            "description": "ID of the parent structure (if applicable). Must be a valid ID of an existing organizational unit.",
            "required": False,
            "schema": {
                "type": "integer",
                "example": 1234,
                "format": "int32",
            },
        },
        {
            "name": "type",
            "description": "Type of organizational structure, separated by commas.",
            "required": False,
            "schema": {
                "type": "string",
                "example": "DPT,FAC",
            },
        },
    ]
