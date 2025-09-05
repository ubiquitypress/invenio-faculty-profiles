# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
# Copyright (C) 2024-2025 Ubiquiity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Decorators."""

from functools import wraps

from flask import g, request

from invenio_faculty_profiles.proxies import current_profiles
from invenio_faculty_profiles.resources.serializer import (
    UIFacultyProfileJSONSerializer,
)


def pass_faculty_profile(serialize):
    """Fetch the faculty profile record."""

    def decorator(f):
        @wraps(f)
        def view(**kwargs):
            pid_value = kwargs["pid_value"]
            faculty_profile = current_profiles.records_service.read(
                id_=pid_value, identity=g.identity
            )
            kwargs["faculty_profile"] = faculty_profile
            request.faculty_profile = faculty_profile.to_dict()
            if serialize:
                kwargs["faculty_profile_ui"] = (
                    UIFacultyProfileJSONSerializer().dump_obj(faculty_profile.to_dict())
                )
            return f(**kwargs)

        return view

    return decorator
