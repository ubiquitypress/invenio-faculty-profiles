# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""

import pytest
from flask_principal import Identity, Need, UserNeed
from flask_security import login_user
from invenio_access.models import ActionRoles
from invenio_accounts.models import Role
from invenio_accounts.testutils import login_user_via_session
from invenio_administration.permissions import administration_access_action
from invenio_app.factory import create_api
from invenio_cache.proxies import current_cache
from invenio_users_resources.proxies import current_users_service
from invenio_users_resources.services.schemas import (
    NotificationPreferences,
    UserPreferencesSchema,
)
from marshmallow import fields
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropConstraint, DropSequence, DropTable

from invenio_faculty_profiles.records.api import FacultyProfile

pytest_plugins = ("celery.contrib.pytest",)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


@compiles(DropConstraint, "postgresql")
def _compile_drop_constraint(element, compiler, **kwargs):
    return compiler.visit_drop_constraint(element) + " CASCADE"


@compiles(DropSequence, "postgresql")
def _compile_drop_sequence(element, compiler, **kwargs):
    return compiler.visit_drop_sequence(element) + " CASCADE"


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return create_api


#
# Application
#
@pytest.fixture(scope="module")
def app_config(app_config):
    """Override pytest-invenio app_config fixture."""
    app_config["THEME_FRONTPAGE"] = False  # FIXME:
    app_config["RECORDS_REFRESOLVER_CLS"] = (
        "invenio_records.resolver.InvenioRefResolver"
    )
    app_config["RECORDS_REFRESOLVER_STORE"] = (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    )
    # Variable not used. We set it to silent warnings
    app_config["JSONSCHEMAS_HOST"] = "not-used"
    # setting preferences schema to test notifications
    app_config["ACCOUNTS_USER_PREFERENCES_SCHEMA"] = UserPreferencesNotificationsSchema

    app_config["USERS_RESOURCES_GROUPS_ENABLED"] = True

    # Define files storage class list
    app_config["FILES_REST_STORAGE_CLASS_LIST"] = {
        "L": "Local",
        "F": "Fetch",
        "R": "Remote",
    }
    app_config["FILES_REST_DEFAULT_STORAGE_CLASS"] = "L"
    app_config["REST_CSRF_ENABLED"] = False
    return app_config


def _search_create_indexes(current_search, current_search_client):
    """Create all registered search indexes."""
    to_create = [
        FacultyProfile.index._name,
    ]
    # list to trigger iter
    list(current_search.create(ignore_existing=True, index_list=to_create))
    current_search_client.indices.refresh()


def _search_delete_indexes(current_search):
    """Delete all registered search indexes."""
    to_delete = [
        FacultyProfile.index._name,
    ]
    list(current_search.delete(index_list=to_delete))


@pytest.fixture()
def search_clear(search):
    """Clear search indices after test finishes (function scope).

    This fixture rollback any changes performed to the indexes during a test,
    in order to leave search in a clean state for the next test.
    """
    from invenio_search import current_search, current_search_client

    yield search
    _search_delete_indexes(current_search)
    _search_create_indexes(current_search, current_search_client)


@pytest.fixture(scope="module")
def testapp(base_app, database):
    """Application with just a database.

    Pytest-Invenio also initialises ES with the app fixture.
    """
    yield base_app


@pytest.fixture(scope="module")
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(Need(method="system_role", value="any_user"))
    return i


class UserPreferencesNotificationsSchema(UserPreferencesSchema):
    """Schema extending preferences with notification preferences."""

    notifications = fields.Nested(NotificationPreferences)


@pytest.fixture(scope="module")
def users_data():
    """Data for users."""
    return [
        {
            "username": "pubres",
            "email": "pubres@inveniosoftware.org",
            "profile": {
                "full_name": "Tim Smith",
                "affiliations": "CERN",
            },
            "preferences": {
                "visibility": "public",
                "email_visibility": "restricted",
            },
        },
    ]


@pytest.fixture()
def users(UserFixture, app, db, users_data):
    """Test users."""
    users = []
    for obj in users_data:
        u = UserFixture(
            username=obj["username"],
            email=obj["email"],
            password=obj["username"],
            user_profile=obj.get("profile"),
            preferences=obj.get("preferences"),
            active=obj.get("active", True),
            confirmed=obj.get("confirmed", True),
        )
        u.create(app, db)
        users.append(u)
    current_users_service.indexer.process_bulk_queue()
    current_users_service.record_cls.index.refresh()
    db.session.commit()
    return users


@pytest.fixture()
def authenticated_client(client, users):
    """Log in a user to the client."""
    user = users[0].user
    login_user(user)
    login_user_via_session(client, email=user.email)
    return client


@pytest.fixture()
def index_users():
    """Index users for an up-to-date user service."""

    def _index():
        current_users_service.indexer.process_bulk_queue()
        current_users_service.record_cls.index.refresh()

    return _index


@pytest.fixture()
def admin_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="administration-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=administration_access_action, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture()
def admin_client(client, users, app, db, admin_role_need):
    """Log in a user to the client."""
    user = users[0].user

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(user, "administration-access")
    datastore.add_role_to_user(user, role)
    db.session.commit()

    login_user(user)
    login_user_via_session(client, email=user.email)
    return client


@pytest.fixture()
def employee_profile_data():
    """Data for employee profiles."""
    return {
        "metadata": {
            "preferred_pronouns": "Mr",
            "family_name": "Doe",
            "given_names": "John",
            "identifiers": [
                {"identifier": "0000-0002-1825-0097"},
            ],
            "biography": "John Doe is a software engineer with over 10 years "
            "of experience in the tech industry. He specializes in backend development, "
            "particularly with Python and Django. He has a passion for clean, efficient code "
            "and enjoys working on complex, challenging problems.",
            "interests": "death",
            "title_status": "Professor",
            "department": "Biology",
            "institution": "Jail",
            "education": "some",
            "email_address": "johndoe@example.com",
            "contact_email_address": "johndoe-contact@example.com",
        },
        "files": {"enabled": False},
    }


@pytest.fixture()
def headers():
    """Default headers for making requests."""
    return {
        "content-type": "application/json",
        "accept": "application/json",
    }
