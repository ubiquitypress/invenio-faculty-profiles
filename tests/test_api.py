# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test low level API."""

import pytest
from jsonschema import ValidationError

from invenio_faculty_profiles.records.api import FacultyProfile


def test_api_create(app, db, employee_profile_data, location):
    """Test low level api create."""
    profile = FacultyProfile.create(data=employee_profile_data)
    profile.commit()
    assert profile.schema
    assert profile.id is not None
    assert profile.metadata == employee_profile_data["metadata"]

    # Clear session
    db.session.expunge_all()

    created_profile = FacultyProfile.get_record(profile.id)
    assert created_profile.id == profile.id
    assert created_profile.metadata == profile.metadata


def test_wrong_metadata(app, db):
    """Test wrong metadata."""
    with pytest.raises(ValidationError):
        FacultyProfile.create(data={"gabage": {"foo": 1}})
