# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Views."""

from .api import blueprint, create_config_blueprint, create_record_blueprint
from .ui import create_ui_blueprint

__all__ = (
    "blueprint",
    "create_record_blueprint",
    "create_config_blueprint",
    "create_ui_blueprint",
)
