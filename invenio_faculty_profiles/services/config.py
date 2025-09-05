# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Employee Profile service configuration."""

from invenio_records_resources.services import FileLink, FileServiceConfig
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfigSearchOptions,
    SearchOptionsMixin,
)
from invenio_records_resources.services.records import RecordServiceConfig
from invenio_records_resources.services.records.components import DataComponent
from invenio_records_resources.services.records.config import (
    SearchOptions as SearchOptionsBase,
)
from invenio_records_resources.services.records.params import (
    FacetsParam,
    PaginationParam,
    QueryStrParam,
    SortParam,
)

from ..records.api import FacultyProfile
from .links import FPLink
from .permissions import FacultyProfilePermissionPolicy
from .schema import FacultyProfileSchema


class SearchOptions(SearchOptionsBase, SearchOptionsMixin):
    """Search options."""

    facets = {}
    params_interpreters_cls = [
        QueryStrParam,
        PaginationParam,
        SortParam,
        FacetsParam,
    ]


class FacultyProfileServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Employee Profile Service configuration Class."""

    service_id = "facultyprofiles"

    # Record specific configuration
    record_cls = FacultyProfile

    # Search configuration
    search = FromConfigSearchOptions(
        "FACULTY_PROFILES_SEARCH",
        "FACULTY_PROFILES_SORT_OPTIONS",
        "FACULTY_PROFILES_FACETS",
        search_option_cls=SearchOptions,
    )

    # Service schema
    schema = FacultyProfileSchema

    # Common configuration
    permission_policy_cls = FacultyProfilePermissionPolicy
    indexer_queue_name = "facultyprofiles"

    components = [
        DataComponent,
    ]

    links_item = {
        "self": FPLink("{+api}/faculty-profiles/{id}"),
        "self_html": FPLink("{+ui}/faculty-profiles/{id}"),
        "edit_html": FPLink("{+ui}/faculty-profiles/{id}/edit"),
        "photo": FPLink("{+api}/faculty-profiles/{id}/photo"),
        "cv": FPLink("{+api}/faculty-profiles/{id}/cv"),
        "records": FPLink("{+api}/faculty-profiles/{id}/records"),
    }


class FacultyProfileFileServiceConfig(FileServiceConfig, ConfiguratorMixin):
    """Faculty Profile File Record service config."""

    permission_policy_cls = FacultyProfilePermissionPolicy

    record_cls = FacultyProfile

    file_links_item = {
        "self": FileLink("{+api}/faculty-profiles/{id}/{+key}"),
    }
