# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Communities Resource Serializers."""

from flask_resources import BaseListSchema, JSONSerializer, MarshmallowSerializer

from invenio_faculty_profiles.resources.ui_schema import UIFacultyProfileSchema


class UIFacultyProfileJSONSerializer(MarshmallowSerializer):
    """UI Community JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=UIFacultyProfileSchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )
