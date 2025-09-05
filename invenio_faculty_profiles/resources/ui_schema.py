# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""UI faculty profile schema."""

from flask_resources import BaseObjectSchema
from invenio_vocabularies.resources import VocabularyL10Schema
from marshmallow import Schema, fields


class UIFacultyProfileSchema(BaseObjectSchema):
    """Schema for dumping extra information of the Faculty Profile for the UI."""


class TypesSchema(Schema):
    """Schema for dumping types in the UI."""

    types = fields.List(fields.Nested(VocabularyL10Schema), attribute="types")
