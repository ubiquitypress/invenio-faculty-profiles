# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resource for Faculty Profiles."""

from flask import current_app, g
from flask_resources import (
    Resource,
    ResourceConfig,
    request_body_parser,
    resource_requestctx,
    response_handler,
    route,
)
from invenio_records_resources.resources.records.resource import (
    RecordResource,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_search_ui.searchconfig import search_app_config

from .parser import RequestFileNameAndStreamParser

request_stream = request_body_parser(
    parsers={"application/octet-stream": RequestFileNameAndStreamParser()},
    default_content_type="application/octet-stream",
)

#
# Resource
#


class FacultyProfileSearchConfigResource(Resource):
    """Community search configuration resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("GET", routes["search-config"], self.search_config),
        ]

    @response_handler()
    def search_config(self):
        """Search configuration."""
        return (
            search_app_config(
                config_name="FACULTY_PROFILES_SEARCH",
                available_facets=current_app.config["FACULTY_PROFILES_FACETS"],
                sort_options=current_app.config["FACULTY_PROFILES_SORT_OPTIONS"],
                headers={"Accept": "application/vnd.inveniordm.v1+json"},
                pagination_options=(10, 20),
                endpoint="/api/faculty-profiles",
            ),
            200,
        )


class FacultyProfileSearchConfigResourceConfig(ResourceConfig, ConfiguratorMixin):
    """Communities search config resource configuration."""

    blueprint_name = "facilty_profiles_search_config_ubiquity"
    url_prefix = ""

    routes = {"search-config": "/config/faculty-profiles-search-config"}


class FacultyProfileResource(RecordResource):
    """Faculty Profile Resource class."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("GET", routes["list"], self.search),
            route("POST", routes["list"], self.create),
            route("GET", routes["item"], self.read),
            route("PUT", routes["item"], self.update),
            route("DELETE", routes["item"], self.delete),
            route("GET", routes["photo"], self.read_photo),
            route("PUT", routes["photo"], self.update_photo),
            route("DELETE", routes["photo"], self.delete_photo),
            route("GET", routes["cv"], self.read_cv),
            route("PUT", routes["cv"], self.update_cv),
            route("DELETE", routes["cv"], self.delete_cv),
            route("GET", routes["item-record-list"], self.item_record_search),
        ]

    @request_view_args
    def read_photo(self):
        """Read photo's content."""
        ep_pid = resource_requestctx.view_args["pid_value"]
        item = self.service.read_photo(
            g.identity,
            ep_pid,
        )
        return item.send_file(restricted=False)

    @request_view_args
    @request_stream
    @response_handler()
    def update_photo(self):
        """Upload photo content."""
        item = self.service.update_photo(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data["request_filename"],
            resource_requestctx.data["request_stream"],
            content_length=resource_requestctx.data["request_content_length"],
        )
        return item.to_dict(), 200

    @request_view_args
    def delete_photo(self):
        """Delete photo."""
        self.service.delete_photo(
            g.identity,
            resource_requestctx.view_args["pid_value"],
        )
        return "", 204

    @request_view_args
    def read_cv(self):
        """Read cv's content."""
        ep_pid = resource_requestctx.view_args["pid_value"]
        item = self.service.read_cv(
            g.identity,
            ep_pid,
        )
        return item.send_file(restricted=False)

    @request_view_args
    @request_stream
    @response_handler()
    def update_cv(self):
        """Upload cv content."""
        item = self.service.update_cv(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data["request_filename"],
            resource_requestctx.data["request_stream"],
            content_length=resource_requestctx.data["request_content_length"],
        )
        return item.to_dict(), 200

    @request_view_args
    def delete_cv(self):
        """Delete cv."""
        self.service.delete_cv(
            g.identity,
            resource_requestctx.view_args["pid_value"],
        )
        return "", 204

    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def item_record_search(self):
        """Perform a search for records that a faculty profile has created."""
        hits = self.service.search_records(
            identity=g.identity,
            faculty_profile_id=resource_requestctx.view_args["pid_value"],
            params=resource_requestctx.args,
            search_preference=search_preference(),
        )
        return hits.to_dict(), 200
