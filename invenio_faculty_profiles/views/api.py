# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""API."""

from flask import Blueprint

from ..resources.resource import (
    FacultyProfileSearchConfigResource,
    FacultyProfileSearchConfigResourceConfig,
)

blueprint = Blueprint(
    "invenio_faculty_profiles_ext",
    __name__,
    template_folder="../templates",
)


def create_record_blueprint(app):
    """Create the faculty profile blueprint."""
    blueprint = app.extensions[
        "invenio-faculty-profiles"
    ].records_resource.as_blueprint()
    return blueprint


def create_config_blueprint(app):
    """Creates a blueprint for the facilty profile search config resource."""
    resource = FacultyProfileSearchConfigResource(
        FacultyProfileSearchConfigResourceConfig.build(app)
    )
    blueprint = resource.as_blueprint()
    return blueprint
