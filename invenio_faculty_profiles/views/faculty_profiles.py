# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""UI views."""

from flask import current_app, g, render_template
from flask_login import login_required
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_vocabularies.proxies import current_service as vocabulary_service

from invenio_faculty_profiles.resources.ui_schema import TypesSchema

from ..proxies import current_profiles
from .decorators import pass_faculty_profile

HEADER_PERMISSIONS = {
    "read",
    "update",
}

PRIVATE_PERMISSIONS = HEADER_PERMISSIONS | {
    "create",
    "delete",
}


def faculty_profiles_search():
    """Faculty Profiles search page."""
    can_create = current_profiles.records_service.check_permission(g.identity, "create")
    return render_template(
        "invenio_faculty_profiles/search.html",
        permissions=dict(can_create=can_create),
    )


def faculty_profiles_frontpage():
    """Faculty Profiles index page."""
    can_create = current_profiles.records_service.check_permission(g.identity, "create")
    return render_template(
        "invenio_faculty_profiles/frontpage.html",
        permissions=dict(can_create=can_create),
    )


def _profile_serialized_types():
    _types = vocabulary_service.read_all(
        g.identity,
        fields=["id", "title"],
        type="profiletypes",
        max_records=10,
    )
    types_json = {
        "types": [{"id": i["id"], "title": i["title"]} for i in list(_types.hits)]
    }
    return TypesSchema().dump(types_json)


@login_required
def faculty_profiles_new():
    """Faculty Profiles creation page."""
    can_create = current_profiles.records_service.check_permission(g.identity, "create")
    if not can_create:
        raise PermissionDeniedError()

    photo_size_limit = 10**6
    max_size = current_app.config["FACULTY_PROFILES_PHOTO_MAX_FILE_SIZE"]
    if isinstance(max_size, int) and max_size > 0:
        photo_size_limit = max_size

    types_serialized = _profile_serialized_types()

    return render_template(
        "invenio_faculty_profiles/new.html",
        form_config=dict(
            SITE_UI_URL=current_app.config["SITE_UI_URL"],
        ),
        photo_quota=photo_size_limit,
        types=types_serialized["types"],
    )


@pass_faculty_profile(serialize=True)
def faculty_profiles_edit(pid_value, faculty_profile, faculty_profile_ui):
    """Community settings/profile page."""
    # Permissions are for checking for deletion or other custom permissions.
    permissions = faculty_profile.has_permissions_to(PRIVATE_PERMISSIONS)
    if not permissions["can_update"]:
        raise PermissionDeniedError()

    try:
        current_profiles.records_service.read_photo(g.identity, pid_value)
        photo = True
    except FileNotFoundError:
        photo = False

    try:
        current_profiles.records_service.read_cv(g.identity, pid_value)
        cv = True
    except FileNotFoundError:
        cv = False

    types_serialized = _profile_serialized_types()

    photo_size_limit = 10**6
    max_size = current_app.config["FACULTY_PROFILES_PHOTO_MAX_FILE_SIZE"]
    if isinstance(max_size, int) and max_size > 0:
        photo_size_limit = max_size

    return render_template(
        "invenio_faculty_profiles/edit.html",
        faculty_profile=faculty_profile,
        faculty_profile_ui=faculty_profile_ui,
        has_photo=True if photo else False,
        has_cv=True if cv else False,
        photo_quota=photo_size_limit,
        permissions=permissions,
        types=types_serialized["types"],
    )


@pass_faculty_profile(serialize=True)
def faculty_profile_detail(pid_value, faculty_profile, faculty_profile_ui):
    """Faculty Profile detail page."""
    # Permissions are for checking for deletion or other custom permissions.
    permissions = faculty_profile.has_permissions_to(PRIVATE_PERMISSIONS)
    if not permissions["can_read"]:
        raise PermissionDeniedError()

    return render_template(
        "invenio_faculty_profiles/detail.html",
        faculty_profile=faculty_profile,
        faculty_profile_ui=faculty_profile_ui,
        permissions=permissions,
    )
