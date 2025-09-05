# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration helper for React-SearchKit."""

from functools import partial

from flask import current_app
from invenio_search_ui.searchconfig import search_app_config


def search_app_context():
    """Search app context processor."""
    return {
        "search_app_faculty_profiles_config": partial(
            search_app_config,
            config_name="FACULTY_PROFILES_SEARCH",
            available_facets=current_app.config["FACULTY_PROFILES_FACETS"],
            sort_options=current_app.config["FACULTY_PROFILES_SORT_OPTIONS"],
            headers={"Accept": "application/json"},
            pagination_options=(10, 20),
            endpoint="/api/faculty-profiles",
        ),
    }
