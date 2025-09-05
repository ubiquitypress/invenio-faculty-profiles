# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies for Faculty Profile extension and services."""

from flask import current_app
from werkzeug.local import LocalProxy

current_profiles = LocalProxy(
    lambda: current_app.extensions["invenio-faculty-profiles"]
)

current_profiles_service = LocalProxy(lambda: current_profiles.records_service)

current_profiles_file_service = LocalProxy(
    lambda: current_profiles.records_service.files
)
