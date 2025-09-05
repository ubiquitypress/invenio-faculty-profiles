# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Faculty Profile models."""

from invenio_db import db
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import FileRecordModelMixin
from sqlalchemy_utils.types import UUIDType


class FacultyProfileModel(db.Model, RecordMetadataBase):
    """Faculty profile."""

    __tablename__ = "faculty_profiles_metadata"

    # kept here for easy searching
    active = db.Column(db.Boolean(name="active"))
    """Flag to say if the Faculty Profile is active or not ."""

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id), index=True)
    bucket = db.relationship(Bucket, foreign_keys=[bucket_id])


class FacultyProfileFileModel(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """File associated with a profile."""

    __record_model_cls__ = FacultyProfileModel
    __tablename__ = "faculty_profiles_files"
