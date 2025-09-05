# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2024 CERN.
# Copyright (C) 2024-2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Faculty Profiles UI views."""

from datetime import datetime

from babel.dates import format_datetime
from flask import Blueprint, current_app, g, render_template, url_for
from flask_login import current_user
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.errors import PermissionDeniedError

from ..searchapp import search_app_context
from .faculty_profiles import (
    faculty_profile_detail,
    faculty_profiles_edit,
    faculty_profiles_frontpage,
    faculty_profiles_new,
    faculty_profiles_search,
)


#
# Error handlers
#
def not_found_error(error):
    """Handler for 'Not Found' errors."""
    return render_template(current_app.config["THEME_404_TEMPLATE"]), 404


def record_permission_denied_error(error):
    """Handle permission denier error on record views."""
    if not current_user.is_authenticated:
        # trigger the flask-login unauthorized handler
        return current_app.login_manager.unauthorized()
    return render_template(current_app.config["THEME_403_TEMPLATE"]), 403


#
# Registration
#
def create_ui_blueprint(app):
    """Register blueprint routes on app."""
    routes = app.config.get("FACULTY_PROFILES_ROUTES")

    blueprint = Blueprint(
        "invenio_faculty_profiles",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Communities URL rules
    blueprint.add_url_rule(
        routes["frontpage"],
        view_func=faculty_profiles_frontpage,
        strict_slashes=False,
    )

    blueprint.add_url_rule(
        routes["search"],
        view_func=faculty_profiles_search,
        strict_slashes=False,
    )

    blueprint.add_url_rule(
        routes["new"],
        view_func=faculty_profiles_new,
    )

    blueprint.add_url_rule(
        routes["edit"],
        view_func=faculty_profiles_edit,
    )

    blueprint.add_url_rule(
        routes["detail"],
        view_func=faculty_profile_detail,
        strict_slashes=False,
    )

    # Register error handlers
    blueprint.register_error_handler(
        PermissionDeniedError, record_permission_denied_error
    )

    blueprint.register_error_handler(PIDDoesNotExistError, not_found_error)

    # Register context processor
    blueprint.app_context_processor(search_app_context)

    # Template filters
    @blueprint.app_template_filter()
    def invenio_format_datetime(value):
        date = datetime.fromisoformat(value)
        locale_value = current_app.config.get("BABEL_DEFAULT_LOCALE")
        return format_datetime(date, locale=locale_value)

    @blueprint.app_template_filter("resolve_faculty_profile_photo")
    def resolve_faculty_profile_photo(photo_link, faculty_profile_id):
        """Returns placeholder image link if passed faculty profile doesn't have a photo."""
        faculty_profile_service = current_service_registry.get("facultyprofiles")

        try:
            faculty_profile_service.read_photo(
                identity=g.identity,
                id_=faculty_profile_id,
            )
        except FileNotFoundError:
            return url_for("static", filename="images/square-placeholder.png")

        return photo_link

    return blueprint
