from django.utils.translation import gettext_lazy as _


class BaseImportError(Exception):
    """Base class for file import errors"""


class MissingHeadersError(BaseImportError):
    """Raised if a required header is missing"""

    def __init__(self, headers):
        self.headers = headers

    def __str__(self):
        return _("{} Missing required headers: [{}]").format(
            super().__str__(), ", ".join(self.headers)
        )


class EntryImportError(BaseImportError):
    """Base class for errors generated from import entries"""

    def __init__(self, entry_name="", entry_id="", skip=False):
        self.entry_name = entry_name
        self.entry_id = entry_id
        self.is_entry_skipped = skip

    def set_entry_name(self, entry_name):
        self.entry_name = entry_name

    def set_entry_id(self, entry_id):
        self.entry_id = entry_id

    def skip_entry(self):
        self.is_entry_skipped = True

    def __str__(self):
        skipped = "[" + _("SKIPPED") + "]" if self.is_entry_skipped else ""
        return "{} {} {} {}".format(
            super().__str__(), self.entry_name, self.entry_id, skipped
        )


class MissingValueError(EntryImportError):
    """Raised if a required value for a specific field is missing"""

    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__()

    def __str__(self):
        return _("{} Required value for field '{}' is missing").format(
            super().__str__(), self.field_name
        )


class MissingKeysError(EntryImportError):
    """Raised if a required key is missing from a entry"""

    def __init__(self, keys):
        self.keys = keys
        super().__init__()

    def __str__(self):
        return _("{} Required keys [{}] are missing").format(
            super().__str__(), ", ".join(self.keys)
        )


class InvalidValueError(EntryImportError):
    """Raised if a provided value for a given field is not acceptable"""

    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value
        super().__init__()

    def __str__(self):
        return _("{} Invalid value for field '{}': '{}'").format(
            super().__str__(), self.field_name, self.value
        )
