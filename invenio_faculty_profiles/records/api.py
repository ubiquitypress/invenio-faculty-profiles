# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records API."""

from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records.dumpers import SearchDumper
from invenio_records.dumpers.indexedat import IndexedAtDumperExt
from invenio_records.systemfields import ConstantField, ModelField, SystemField
from invenio_records_resources.records.api import (
    FileRecord,
    PersistentIdentifierWrapper,
    Record,
)
from invenio_records_resources.records.systemfields import FilesField, IndexField
from sqlalchemy.exc import NoResultFound, StatementError

from .models import FacultyProfileFileModel, FacultyProfileModel


class GetRecordResolver(object):
    """Resolver that simply uses get record."""

    def __init__(self, record_cls):
        """Initialize resolver."""
        self._record_cls = record_cls

    def resolve(self, pid_value, registered_only=False):
        """Simply get the record."""
        _ = registered_only
        try:
            return self._record_cls.get_record(pid_value)
        except (NoResultFound, StatementError):
            raise PIDDoesNotExistError("pid", pid_value)


class DirectIdPID(SystemField):
    """Helper emulate a PID field."""

    def __init__(self, id_field="id"):
        """Constructor."""
        self._id_field = id_field

    def obj(self, record):
        """Get the access object."""
        pid_value = getattr(record, self._id_field)
        if pid_value is None:
            return None
        return PersistentIdentifierWrapper(str(pid_value))

    def __get__(self, record, owner=None):
        """Evaluate the property."""
        if record is None:
            return GetRecordResolver(owner)
        # return DirectIdPID(getattr(record, self._id_field))
        return self.obj(record)


class FacultyProfileFile(FileRecord):
    """Faculty profile file API."""

    model_cls = FacultyProfileFileModel

    record_cls = None  # is defined inside the parent record


class FacultyProfile(Record):
    """Faculty profile record API."""

    model_cls = FacultyProfileModel

    id = ModelField()

    dumper = SearchDumper(
        extensions=[
            IndexedAtDumperExt(),
        ]
    )

    schema = ConstantField(
        "$schema", "local://faculty_profiles/faculty-profiles-v1.0.0.json"
    )

    # Systemfields
    index = IndexField(
        "facultyprofiles-facultyprofile-v1.0.0",
        search_alias="facultyprofiles",
    )

    pid = DirectIdPID()

    # Faculty Profile File related fields
    files = FilesField(
        file_cls=FacultyProfileFile, store=False, dump=True, dump_entries=True
    )
    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


FacultyProfileFile.record_cls = FacultyProfile
