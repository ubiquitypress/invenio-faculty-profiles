# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Config for Faculty Profile Resource."""

from flask_resources import (
    HTTPJSONException,
    JSONSerializer,
    ResponseHandler,
    create_error_handler,
)
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.resources.records import RecordResourceConfig
from invenio_records_resources.resources.records.headers import etag_headers
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig

from invenio_faculty_profiles.resources.serializer import UIFacultyProfileJSONSerializer

from ..errors import PhotoSizeLimitError

faculty_profile_error_handlers = RecordResourceConfig.error_handlers.copy()
faculty_profile_error_handlers.update(
    {
        FileNotFoundError: create_error_handler(
            HTTPJSONException(
                code=404,
                description="No file exists for this faculty profile.",
            )
        ),
        PhotoSizeLimitError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
        PIDDoesNotExistError: create_error_handler(
            HTTPJSONException(
                code=404,
                description="The persistent identifier does not exist.",
            )
        ),
    }
)


class FacultyProfileResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    """Blueprint configuration."""

    blueprint_name = "faculty-profiles"
    url_prefix = "/faculty-profiles"

    routes = {
        "list": "",
        "item": "/<pid_value>",
        "photo": "/<pid_value>/photo",
        "cv": "/<pid_value>/cv",
        "item-record-list": "/<pid_value>/records",
    }

    error_handlers = FromConfig(
        "FACULTY_PROFILES_ERROR_HANDLERS", default=faculty_profile_error_handlers
    )

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers),
        "application/vnd.inveniordm.v1+json": ResponseHandler(
            UIFacultyProfileJSONSerializer(), headers=etag_headers
        ),
    }
