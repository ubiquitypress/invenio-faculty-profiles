# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resources for users faculty profiles."""

from .config import FacultyProfileResourceConfig
from .resource import FacultyProfileResource

__all__ = (
    "FacultyProfileResource",
    "FacultyProfileResourceConfig",
)
