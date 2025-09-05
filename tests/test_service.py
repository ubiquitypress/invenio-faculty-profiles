# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service tests."""

from copy import deepcopy

from invenio_access.permissions import system_identity

from invenio_faculty_profiles.proxies import current_profiles_service
from invenio_faculty_profiles.records.api import FacultyProfile


def test_service_layer(
    app, db, users, search_clear, search, location, employee_profile_data
):
    faculty_profile = current_profiles_service.create(
        system_identity, employee_profile_data
    )

    data = faculty_profile.to_dict()
    assert "id" in data
    # Checking that identifiers.scheme resolve correctly
    # we can't do == employee_profile_data
    assert data["metadata"] == {
        "preferred_pronouns": "Mr",
        "family_name": "Doe",
        "given_names": "John",
        "identifiers": [{"identifier": "0000-0002-1825-0097", "scheme": "orcid"}],
        "biography": "John Doe is a software engineer with over 10 years of experience in the tech industry. He specializes in backend development, particularly with Python and Django. He has a passion for clean, efficient code and enjoys working on complex, challenging problems.",
        "interests": "death",
        "title_status": "Professor",
        "department": "Biology",
        "institution": "Jail",
        "education": "some",
        "email_address": "johndoe@example.com",
        "contact_email_address": "johndoe-contact@example.com",
    }
    assert data["active"] is True

    FacultyProfile.index.refresh()

    # try to search for the profile
    all_profiles = current_profiles_service.search(system_identity)
    assert all_profiles.total == 1
    hits = list(all_profiles.hits)
    assert hits[0] == faculty_profile.data

    # try to search the profile with full name
    user_profiles = current_profiles_service.search(
        system_identity, q="metadata.family_name:Doe"
    )
    assert user_profiles.total == 1
    hits = list(user_profiles.hits)

    # try to search the profile with different user id
    user_profiles = current_profiles_service.search(
        system_identity, q="metadata.family_name:Barnes"
    )
    assert user_profiles.total == 0
