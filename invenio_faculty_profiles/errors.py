# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Faculty profilies base error."""

from math import ceil

from invenio_i18n import gettext as _


class FacultyProfileError(Exception):
    """Base exception for faculty profile errors."""


class PhotoSizeLimitError(FacultyProfileError):
    """The provided logo size exceeds limit."""

    def __init__(self, limit, file_size):
        """Initialise error."""
        super().__init__(
            _(
                "Picture size limit exceeded. Limit: {limit} bytes Given: {file_size} bytes".format(
                    limit=ceil(limit), file_size=ceil(file_size)
                )
            )
        )
