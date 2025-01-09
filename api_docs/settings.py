import enum

from django.utils.text import slugify


class API_CONTEXTS(enum.Enum):
    ACADEMIC = (
        "Academic",
        [
            "cds",
            "cds_brochure",
            "cds_websites",
            "advanced_training",
            "phd",
            "teachers",
            "laboratories",
            "regdid",
        ],
    )
    RESEARCH = (
        "Research",
        [
            "research_groups",
            "research_lines",
            "patents",
            "projects",
        ],
    )
    INTEGRATION = (
        "Integration",
        [
            "esse3",
            "pentaho",
        ],
    )
    ADMINISTRATIVE = (
        "Administrative",
        [
            "accounts",
            "addressbook",
            "structures",
        ],
    )
    EXTERNAL_RELATIONS = (
        "External Relations",
        [
            "companies",
        ],
    )

    def __init__(self, display_name, apps):
        self._display_name = display_name
        self._url_slug = slugify(display_name)
        self._apps = apps

    @property
    def display_name(self):
        return self._display_name

    @property
    def url_slug(self):
        return self._url_slug

    @property
    def apps(self):
        return self._apps
