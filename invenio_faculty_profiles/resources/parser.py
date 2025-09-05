# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 Ubiquity Press.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource parsers."""

from flask import request


class RequestFileNameAndStreamParser:
    """Parse the request body."""

    def parse(self):
        """Parse the request body."""
        return {
            "request_filename": request.headers.get("X-Filename"),
            "request_stream": request.stream,
            "request_content_length": request.content_length,
        }
