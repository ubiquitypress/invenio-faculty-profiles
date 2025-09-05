# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for Faculty Profile service functions."""

from invenio_administration.generators import Administration
from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess
from invenio_records_resources.services.files.generators import IfTransferType
from invenio_records_resources.services.files.transfer import LOCAL_TRANSFER_TYPE


class FacultyProfilePermissionPolicy(RecordPermissionPolicy):
    """Faculty Profile Permission Policy class."""

    can_search = [AnyUser(), SystemProcess()]
    can_create = [Administration(), SystemProcess()]
    can_update = [Administration(), SystemProcess()]
    can_delete = [Administration(), SystemProcess()]
    can_read = [AnyUser(), SystemProcess()]
    can_create_files = [Administration(), SystemProcess()]
    can_set_content_files = [Administration(), SystemProcess()]
    can_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, AnyUser()),
        SystemProcess(),
    ]
    can_commit_files = [
        Administration(),
        IfTransferType(LOCAL_TRANSFER_TYPE, AnyUser()),
        SystemProcess(),
    ]
    can_read_files = [AnyUser(), SystemProcess()]
    can_update_files = [Administration(), SystemProcess()]
    can_delete_files = [Administration(), SystemProcess()]
    can_search_records = [AnyUser(), SystemProcess()]
