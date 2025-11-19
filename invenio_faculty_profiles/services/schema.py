# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Ubiquity Press.
#
# Invenio-Faculty-Profiles is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Faculty Profile Service Schema."""

from functools import partial

import phonenumbers
from flask import current_app
from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from invenio_vocabularies.contrib.awards.schema import AwardRelationSchema
from invenio_vocabularies.contrib.funders.schema import FunderRelationSchema
from invenio_vocabularies.contrib.subjects.schema import SubjectRelationSchema
from invenio_vocabularies.services.schema import (
    VocabularyRelationSchema as VocabularySchema,
)
from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
)
from marshmallow_utils.fields import (
    IdentifierSet,
    NestedAttribute,
    SanitizedHTML,
    SanitizedUnicode,
)
from marshmallow_utils.schemas import IdentifierSchema
from werkzeug.local import LocalProxy

from ..proxies import current_profiles_service

facuty_profiles_handlers = LocalProxy(
    lambda: current_app.config["FACULTY_PROFILES_HANDLERS"]
)
identifiers_schemes = LocalProxy(
    lambda: current_app.config["FACULTY_PROFILES_IDENTIFIERS_SCHEMES"]
)


class FileSchema(Schema):
    """File schema."""

    # File fields
    id = fields.String(attribute="file.id")
    checksum = fields.String(attribute="file.checksum")
    ext = fields.String(attribute="file.ext")
    size = fields.Integer(attribute="file.size")
    mimetype = fields.String(attribute="file.mimetype")
    storage_class = fields.String(attribute="file.storage_class")

    # FileRecord fields
    key = SanitizedUnicode()


class FilesSchema(Schema):
    """Basic files schema class."""

    enabled = fields.Bool(missing=True)

    entries = fields.Dict(
        keys=SanitizedUnicode(),
        values=NestedAttribute(FileSchema),
        dump_only=True,
    )


class FundingSchema(Schema):
    """Funding schema."""

    funder = fields.Nested(FunderRelationSchema, required=True)
    award = fields.Nested(AwardRelationSchema)


class FacultyProfileMetadataSchema(Schema):
    """Metadata schema."""

    preferred_pronouns = SanitizedUnicode()
    family_name = SanitizedUnicode(required=True)
    given_names = SanitizedUnicode(required=True)

    identifiers = IdentifierSet(
        fields.Nested(
            partial(
                IdentifierSchema,
                allowed_schemes=identifiers_schemes,
            )
        )
    )
    type = fields.Nested(VocabularySchema, metadata={"type": "profiletypes"})

    handlers = IdentifierSet(
        fields.Nested(
            partial(
                IdentifierSchema,
                allowed_schemes=facuty_profiles_handlers,
            )
        )
    )
    website = SanitizedUnicode(validate=validate.URL(error=_("Not a valid URL.")))
    telephone = SanitizedUnicode()

    funding = fields.List(fields.Nested(FundingSchema))

    keywords = fields.List(fields.Nested(SubjectRelationSchema))

    biography = SanitizedHTML(validate=validate.Length(min=3))

    interests = SanitizedHTML(validate=validate.Length(min=3))
    title_status = SanitizedUnicode()
    department = SanitizedUnicode()
    institution = SanitizedUnicode()
    education = SanitizedUnicode()

    email_address = fields.Email()
    contact_email_address = fields.Email()
    office_address = SanitizedHTML(validate=validate.Length(min=3))

    @validates("telephone")
    def validate_description(self, value):
        """Validate a phone number."""
        try:
            p = phonenumbers.parse(value, "US")  # FIXME: get current locale
            if not phonenumbers.is_valid_number(p):
                raise ValidationError(_("Invalid phone number format"))
        except Exception as ex:
            raise ValidationError(_("Invalid phone number format")) from ex


class FacultyProfileSchema(InvenioBaseRecordSchema):
    """Faculty profile schema."""

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE

    id = fields.String(dump_only=True)
    metadata = NestedAttribute(FacultyProfileMetadataSchema, required=True)
    active = fields.Boolean(default=True)
    files = NestedAttribute(FilesSchema)

    permissions = fields.Method("load_permissions")

    def load_permissions(self, *args, **kwargs):
        """."""
        record = self.context["record"]
        identity = self.context["identity"]
        return {
            f"can_{action}": current_profiles_service.check_permission(
                identity, action, record=record
            )
            for action in (
                "create",
                "update",
                "delete",
                "set_content_files",
                "commit_files",
                "update_files",
                "delete_files",
            )
        }
