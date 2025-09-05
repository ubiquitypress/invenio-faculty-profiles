# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Faculty Profile Services."""

import os

from flask import current_app
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.services import LinksTemplate
from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.uow import (
    RecordCommitOp,
    unit_of_work,
)
from invenio_search.engine import dsl

from ..errors import PhotoSizeLimitError


class FacultyProfileService(RecordService):
    """Faculty Profile Service class."""

    def __init__(self, config, files_service=None):
        """Constructor for RecordService."""
        super().__init__(config)
        self._files = files_service

    #
    # Subservices
    #
    @property
    def files(self):
        """Record files service."""
        return self._files

    def read_photo(self, identity, id_):
        """Read the faculty profile's photo."""
        return self._read_file(identity, "photo", id_)

    def read_cv(self, identity, id_):
        """Read the faculty profile's cv."""
        return self._read_file(identity, "cv", id_)

    @unit_of_work()
    def update_photo(
        self, identity, id_, filename, stream, content_length=None, uow=None
    ):
        """Update the faculty profile's photo."""
        # get the file extesion from filename
        extension = self._get_file_extension(filename)
        photo_size_limit = 10**6
        max_size = current_app.config["FACULTY_PROFILES_PHOTO_MAX_FILE_SIZE"]
        if type(max_size) is int and max_size > 0:
            photo_size_limit = max_size

        if content_length and content_length > photo_size_limit:
            raise PhotoSizeLimitError(photo_size_limit, content_length)

        return self._update_file(identity, id_, stream, "photo", extension, uow=uow)

    @unit_of_work()
    def update_cv(self, identity, id_, filename, stream, content_length=None, uow=None):
        """Update the faculty profile's cv."""
        # get the file extesion from filename
        extension = self._get_file_extension(filename)
        return self._update_file(identity, id_, stream, "cv", extension, uow=uow)

    @unit_of_work()
    def delete_photo(self, identity, id_, uow=None):
        """Delete the faculty profile's photo."""
        return self._delete_file(identity, id_, "photo", uow=uow)

    @unit_of_work()
    def delete_cv(self, identity, id_, uow=None):
        """Delete the faculty profile's cv."""
        return self._delete_file(identity, id_, "cv", uow=uow)

    #
    # Private methods
    #
    def _get_file_extension(self, filename):
        """Get the file extension from the filename."""
        extension = None
        if filename:
            _, extension = os.path.splitext(filename)
        return extension

    def _find_file_in_record(self, file_name, record):
        """Find the file in the record."""
        full_file_name = None
        for key in record.files.keys():
            prefix_to_check = f"{file_name}."
            if key.startswith(prefix_to_check):
                full_file_name = key
                break
        return full_file_name

    def _read_file(self, identity, file_name, id_):
        """Read the faculty profile file."""
        record = self.record_cls.pid.resolve(id_)
        self.require_permission(identity, "read", record=record)
        full_file_name = self._find_file_in_record(file_name, record)
        record_file = record.files.get(full_file_name)
        if record_file is None:
            raise FileNotFoundError()
        return self.files.file_result_item(
            self.files,
            identity,
            record_file,
            record,
            links_tpl=self.files.file_links_item_tpl(id_),
        )

    def _update_file(self, identity, id_, stream, file_name, file_extension, uow=None):
        """Update a faculty profile's file."""
        record = self.record_cls.pid.resolve(id_)
        self.require_permission(identity, "update", record=record)

        full_file_name = f"{file_name}{file_extension}" if file_extension else file_name
        if (
            record.files
            and full_file_name not in record.files
            and self._find_file_in_record(file_name, record)
        ):
            # Delete the old file of a different extension
            self._delete_file(identity, id_, file_name, uow=uow)
        record.files[full_file_name] = stream
        uow.register(RecordCommitOp(record))

        return self.files.file_result_item(
            self.files,
            identity,
            record.files[full_file_name],
            record,
            links_tpl=self.files.file_links_item_tpl(id_),
        )

    def _delete_file(self, identity, id_, file_name, uow=None):
        """Delete a faculty profile's file."""
        record = self.record_cls.pid.resolve(id_)
        # update permission on community is required to be able to remove file.
        self.require_permission(identity, "update", record=record)

        full_file_name = self._find_file_in_record(file_name, record)
        deleted_file = record.files.pop(full_file_name, None)
        if deleted_file is None:
            raise FileNotFoundError()

        deleted_file.delete(force=True)

        uow.register(RecordCommitOp(record))

        return self.files.file_result_item(
            self.files,
            identity,
            deleted_file,
            record,
            links_tpl=self.files.file_links_item_tpl(id_),
        )

    def _setup_record_query(self, record):
        """Setup the record search extra query so return only records with identifier or name of faculty profile."""
        # Prepare extra_filters
        identifiers = record.metadata.get("identifiers", [])
        name = (
            f"{record.metadata.get('family_name').strip()}, {record.metadata.get('given_names').strip()}"
            if record.metadata.get("family_name")
            else None
        )

        query_clauses = []
        for identifier in identifiers:
            query_clauses.append(
                dsl.Q(
                    "match_phrase",
                    **{
                        "metadata.creators.person_or_org.identifiers.identifier": identifier[
                            "identifier"
                        ]
                    },
                )
            )
        if name:
            query_clauses.append(
                dsl.Q("match_phrase", **{"metadata.creators.person_or_org.name": name})
            )
        # If no query clauses, return match_none
        return (
            dsl.Q("bool", should=query_clauses, minimum_should_match=1)
            if query_clauses
            else dsl.Q("match_none")
        )

    def search_records(
        self,
        identity,
        faculty_profile_id,
        params=None,
        search_preference=None,
        expand=False,
        **kwargs,
    ):
        """Search records for a faculty profile."""
        record = self.record_cls.pid.resolve(faculty_profile_id)
        # Permissions
        self.require_permission(identity, "search_records", record=record)

        # Prepare and execute the search
        params = params or {}
        search_result = current_rdm_records_service._search(
            "search",
            identity,
            params,
            search_preference,
            permission_action=None,
            extra_filter=self._setup_record_query(record),
            **kwargs,
        ).execute()

        return current_rdm_records_service.result_list(
            current_rdm_records_service,
            identity,
            search_result,
            params,
            links_tpl=LinksTemplate(
                current_rdm_records_service.config.links_search_versions,
                context={"args": params, "id": faculty_profile_id},
            ),
            links_item_tpl=current_rdm_records_service.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )
