"""Facult Profile Config Variables."""

from idutils import is_gnd, is_isni, is_orcid, is_ror
from invenio_i18n import lazy_gettext as _

from .resources.config import faculty_profile_error_handlers
from .services import facets

FACULTY_PROFILES_ROUTES = {
    "frontpage": "/faculty-profiles",
    "search": "/faculty-profiles/search",
    "new": "/faculty-profiles/new",
    "edit": "/faculty-profiles/<pid_value>/edit",
    "detail": "/faculty-profiles/<pid_value>",
}

#
# Faculty Profile Search configuration
#
FACULTY_PROFILES_FACETS = {
    "type": {
        "facet": facets.type,
        "ui": {
            "field": "type",
        },
    },
}

FACULTY_PROFILES_SORT_OPTIONS = {
    "family-name-asc": {
        "title": _("Family Name [A-Z]"),
        "fields": [
            "metadata.family_name",
            "metadata.given_names",
            "-created",
        ],
    },
    "family-name-desc": {
        "title": _("Family Name [Z-A]"),
        "fields": [
            "-metadata.family_name",
            "-metadata.given_names",
            "-created",
        ],
    },
    "bestmatch": dict(
        title=_("Best match"),
        fields=["_score"],  # ES defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
    "oldest": dict(
        title=_("Oldest"),
        fields=["created"],
    ),
}
"""Definitions of available record sort options."""


FACULTY_PROFILES_SEARCH = {
    "facets": ["type"],
    "sort": [
        "bestmatch",
        "family-name-asc",
        "family-name-desc",
        "newest",
        "oldest",
    ],
    "sort_default_no_query": "family-name-asc",
    "sort_default": "bestmatch",
}
"""Faculty Profile search configuration."""


FACULTY_PROFILES_PHOTO_MAX_FILE_SIZE = 10**6
"""Faculty Profile image photo size quota, in bytes."""


FACULTY_PROFILES_ERROR_HANDLERS = {
    **faculty_profile_error_handlers,
}


FACULTY_PROFILES_ALWAYS_SHOW_CREATE_LINK = False
"""Controls visibility of 'New Faculty Profile' btn based on user's permission when set to True."""


def always_valid(identifier):
    """Gives every identifier as valid."""
    return True


FACULTY_PROFILES_IDENTIFIERS_SCHEMES = {
    "orcid": {"label": _("ORCID"), "validator": is_orcid, "datacite": "ORCID"},
    "isni": {"label": _("ISNI"), "validator": is_isni, "datacite": "ISNI"},
    "gnd": {"label": _("GND"), "validator": is_gnd, "datacite": "GND"},
    "ror": {"label": _("ROR"), "validator": is_ror, "datacite": "ROR"},
}

FACULTY_PROFILES_HANDLERS = {
    "linkedin": {
        "label": _("LinkedIn"),
        "validator": always_valid,
    },
}
