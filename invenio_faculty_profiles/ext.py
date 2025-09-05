# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Extension for Faculty Profile."""

from functools import cached_property

from flask import g
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services import FileService

from . import config
from .proxies import current_profiles
from .resources import FacultyProfileResource, FacultyProfileResourceConfig
from .services import (
    FacultyProfileFileServiceConfig,
    FacultyProfileService,
    FacultyProfileServiceConfig,
)


class FacultyProfileExtension:
    """Faculty Profile Extension Class."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Extension Initials when app is not None."""
        self.app = app

        self.init_config(app)
        self.init_services()
        self.init_resource()
        app.extensions["invenio-faculty-profiles"] = self

    def init_services(self):
        """Extension initialization of Service."""
        self.records_service = FacultyProfileService(
            config=self._service_config.record,
            files_service=FileService(self._service_config.file),
        )

    def init_resource(self):
        """Initialize resources."""
        self.records_resource = FacultyProfileResource(
            config=self._resource_config.record,
            service=self.records_service,
        )

    #     # region Private Methods

    @cached_property
    def _service_config(self):
        """Extension initialization of Service configs."""

        class ServiceConfigs:
            record = FacultyProfileServiceConfig.build(self.app)
            file = FacultyProfileFileServiceConfig.build(self.app)

        return ServiceConfigs

    @cached_property
    def _resource_config(self):
        """Extension initialization of Resource configs."""

        class ResourceConfigs:
            record = FacultyProfileResourceConfig.build(self.app)

        return ResourceConfigs

    def init_config(self, app):
        """Setup Extension config."""
        # Override configuration variables with the values in this package.
        for k in dir(config):
            if k.startswith("FACULTY_PROFILES_"):
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize app.

    NOTE: replace former @record_once decorator
    """
    init(app)
    register_menus(app)


def _show_create_faculty_profile_link():
    return current_profiles.records_service.check_permission(g.identity, "create")


def register_menus(app):
    """Register faculty profiles menu items."""
    current_menu.submenu("main.facultyprofiles").register(
        endpoint="invenio_faculty_profiles.faculty_profiles_frontpage",
        text=_("Researcher Profiles"),
        order=3,
    )

    current_menu.submenu("plus.facultyprofiles").register(
        endpoint="invenio_faculty_profiles.faculty_profiles_new",
        text=_("New faculty profile"),
        order=2,
        visible_when=_show_create_faculty_profile_link,
    )

    facultyprofiles = current_menu.submenu("facultyprofiles")

    facultyprofiles.submenu("search").register(
        "invenio_faculty_profiles.faculty_profile_detail",
        text=_("Stored Information"),
        order=10,
        expected_args=["pid_value"],
        **dict(icon="search", permissions=True),
    )

    facultyprofiles.submenu("settings").register(
        endpoint="invenio_faculty_profiles.faculty_profiles_settings",
        text=_("Edit"),
        order=20,
        expected_args=["pid_value"],
        **{"icon": "settings", "permissions": "can_update"},
    )


def api_finalize_app(app):
    """Finalize app for api.

    NOTE: replace former @record_once decorator
    """
    init(app)


def init(app):
    """Register  services."""
    ext = app.extensions["invenio-faculty-profiles"]
    service_id = ext.records_service.config.service_id
    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.records_service, service_id=service_id)
    # Register indexers
    iregistry = app.extensions["invenio-indexer"].registry
    iregistry.register(ext.records_service.indexer, indexer_id=service_id)
