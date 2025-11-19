// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import _find from "lodash/find";
import _get from "lodash/get";
import _map from "lodash/map";
import PropTypes from "prop-types";
import React, { Component, createRef } from "react";
import ReactDOM from "react-dom";
import {
  AccordionField,
  BaseForm,
  FieldLabel,
  RichInputField,
  SelectField,
  TextField,
  withCancel,
} from "react-invenio-forms";
import {
  Card,
  Container,
  Grid,
  Icon,
  Message,
  Ref,
  Sticky,
} from "semantic-ui-react";
import { FacultyProfileApi } from "../api";
import { facultyProfileErrorSerializer } from "../api/serializers";
import { ActionBox } from "./ActionBox";
import CvUploader from "./CvUploader";
import DangerZone from "./DangerZone";
import { Identifiers } from "./Identifiers";
import PhotoUploader from "./PhotoUploader";

class FacultyProfileCreateForm extends Component {
  state = {
    error: "",
  };

  sidebarRef = createRef();

  setGlobalError = (error) => {
    const { message } = facultyProfileErrorSerializer(error);
    this.setState({ error: message });
  };

  deserializeProfile = (initialValues) => {
    return {
      ...initialValues,
      files: { enabled: initialProfile.files.enabled },
      metadata: {
        ...initialValues.metadata,
        identifiers: _map(
          _get(initialValues, "metadata.identifiers", []),
          "identifier",
        ),
      },
    };
  };

  serializeProfile = (submittedProfile) => {
    const { initialProfile } = this.props;
    const identifiersFieldPath = "metadata.identifiers";

    const findField = (arrayField, key, value) => {
      const knownField = _find(arrayField, {
        [key]: value,
      });
      return knownField ? knownField : { [key]: value };
    };

    // The form is saving only identifiers values, thus
    // identifiers with existing scheme are trimmed
    // Here we merge back the known scheme for the submitted identifiers
    const initialIdentifiers = _get(initialProfile, identifiersFieldPath, []);
    const submittedIdentifiers = _get(
      submittedProfile,
      identifiersFieldPath,
      [],
    );
    const identifiers = submittedIdentifiers.map((identifier) => {
      return findField(initialIdentifiers, "identifier", identifier);
    });
    const filtered = Object.fromEntries(
      Object.entries(submittedProfile.metadata).filter(
        ([_, v]) => v != null && v !== "",
      ),
    );
    return {
      ...submittedProfile,
      metadata: {
        ...filtered,
        identifiers,
      },
    };
  };

  onSubmit = async (values, { setSubmitting, setFieldError }) => {
    setSubmitting(true);
    const { initialProfile } = this.props;
    const isNewProfile = initialProfile.id === undefined;
    const client = new FacultyProfileApi();
    const payload = this.serializeProfile(values);

    if (isNewProfile) {
      this.cancellableCreate = withCancel(client.create(payload));
    } else {
      this.cancellableCreate = withCancel(
        client.update(initialProfile.id, payload),
      );
    }
    try {
      const response = await this.cancellableCreate.promise;
      setSubmitting(false);
      if (isNewProfile) window.location.href = response.data.links.edit_html;
    } catch (error) {
      if (error === "UNMOUNTED") return;
      const { message, errors } = facultyProfileErrorSerializer(error);

      setSubmitting(false);

      if (message) {
        this.setGlobalError(error);
      }

      if (errors) {
        errors.map(({ field, messages }) => setFieldError(field, messages[0]));
      }
    }
  };

  render() {
    const { error } = this.state;
    const {
      initialProfile,
      hasCv,
      hasPhoto,
      defaultPhoto,
      permissions,
      types,
    } = this.props;

    const deserializedProfile = this.deserializeProfile(initialProfile);

    return (
      <BaseForm
        onSubmit={this.onSubmit}
        formik={{
          enableReinitialize: true,
          initialValues: deserializedProfile,
        }}
      >
        <Message hidden={error === ""} negative className="flashed">
          <Grid container centered>
            <Grid.Column mobile={16} tablet={12} computer={8} textAlign="left">
              <strong>{error}</strong>
            </Grid.Column>
          </Grid>
        </Message>

        <Container id="rdm-deposit-form" className="rel-mt-1">
          <Grid className="m-25">
            <Grid.Column mobile={16} tablet={16} computer={11}>
              <AccordionField
                includesPaths={[]}
                active
                label={i18next.t("Basic information")}
              >
                <Grid>
                  <Grid.Column width="4">
                    <TextField
                      id="preferred_pronouns"
                      fluid
                      fieldPath="metadata.preferred_pronouns"
                      placeholder={i18next.t("e.g. they/them")}
                      label={
                        <FieldLabel
                          htmlFor="preferred_pronouns"
                          icon="user"
                          label={i18next.t("Preferred Pronouns")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="6">
                    <TextField
                      required
                      id="family_name"
                      fluid
                      fieldPath="metadata.family_name"
                      label={
                        <FieldLabel
                          htmlFor="family_name"
                          icon="user"
                          label={i18next.t("Family Name")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="6">
                    <TextField
                      required
                      id="given_names"
                      fluid
                      fieldPath="metadata.given_names"
                      label={
                        <FieldLabel
                          htmlFor="given_names"
                          icon="book"
                          label={i18next.t("Given Names")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width={16}>
                    <Identifiers
                      initialOptions={_map(
                        _get(deserializedProfile, "metadata.identifiers", []),
                        (identifier) => ({
                          text: identifier,
                          value: identifier,
                          key: identifier,
                        }),
                      )}
                    />
                  </Grid.Column>
                  <Grid.Column width={16}>
                    <RichInputField
                      className="description-field"
                      fieldPath="metadata.biography"
                      label={
                        <FieldLabel
                          htmlFor="biography"
                          icon="pencil"
                          label={i18next.t("Biography")}
                        />
                      }
                      optimized
                    />
                  </Grid.Column>
                </Grid>
              </AccordionField>
              <AccordionField
                includesPaths={[]}
                active
                label={i18next.t("Institutional information")}
              >
                <Grid>
                  <Grid.Column width={16}>
                    <RichInputField
                      className="description-field"
                      fieldPath="metadata.interests"
                      label={
                        <FieldLabel
                          htmlFor="interests"
                          icon="flask"
                          label={i18next.t("Research interest")}
                        />
                      }
                      optimized
                    />
                  </Grid.Column>
                  <Grid.Column width="4">
                    <TextField
                      id="title_status"
                      fluid
                      fieldPath="metadata.title_status"
                      label={
                        <FieldLabel
                          htmlFor="title_status"
                          icon="graduation cap"
                          label={i18next.t("Title")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="6">
                    <TextField
                      id="department"
                      fluid
                      fieldPath="metadata.department"
                      label={
                        <FieldLabel
                          htmlFor="department"
                          icon="building outline"
                          label={i18next.t("Department")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="6">
                    <TextField
                      id="institution"
                      fluid
                      fieldPath="metadata.institution"
                      label={
                        <FieldLabel
                          htmlFor="instituion"
                          icon="building outline"
                          label={i18next.t("Institution")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="6">
                    <TextField
                      id="type"
                      fluid
                      fieldPath="metadata.type"
                      label={
                        <FieldLabel
                          htmlFor="type"
                          icon="building outline"
                          label={i18next.t("type")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width={16}>
                    <SelectField
                      search
                      clearable
                      fieldPath="metadata.type.id"
                      label={
                        <FieldLabel
                          htmlFor="metadata.type.id"
                          icon="tag"
                          label={i18next.t("Type")}
                        />
                      }
                      options={types.map((ct) => {
                        return {
                          value: ct.id,
                          text: ct?.title_l10n ?? ct.id,
                        };
                      })}
                    />
                  </Grid.Column>
                  <Grid.Column width={16}>
                    <RichInputField
                      className="description-field"
                      fieldPath="metadata.education"
                      label={
                        <FieldLabel
                          htmlFor="education"
                          icon="university"
                          label={i18next.t("Education")}
                        />
                      }
                      optimized
                    />
                  </Grid.Column>
                </Grid>
              </AccordionField>
              <AccordionField
                includesPaths={[]}
                active
                label={i18next.t("Contact")}
              >
                <Grid>
                  <Grid.Column width="8">
                    <TextField
                      id="website"
                      fluid
                      fieldPath="metadata.website"
                      label={
                        <FieldLabel
                          htmlFor="website"
                          icon="world"
                          label={i18next.t("Website")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="8">
                    <TextField
                      id="telephone"
                      fluid
                      fieldPath="metadata.telephone"
                      label={
                        <FieldLabel
                          htmlFor="telephone"
                          icon="phone"
                          label={i18next.t("Phone number")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="8">
                    <TextField
                      id="email_address"
                      fluid
                      fieldPath="metadata.email_address"
                      label={
                        <FieldLabel
                          htmlFor="email_address"
                          icon="mail"
                          label={i18next.t("Email address")}
                        />
                      }
                    />
                  </Grid.Column>
                  <Grid.Column width="8">
                    <TextField
                      id="contact_email_address"
                      fluid
                      fieldPath="metadata.contact_email_address"
                      label={
                        <FieldLabel
                          htmlFor="contact_email_address"
                          icon="mail"
                          label={i18next.t("Contacnt email address")}
                        />
                      }
                    />
                  </Grid.Column>
                </Grid>
              </AccordionField>
            </Grid.Column>

            <Ref innerRef={this.sidebarRef}>
              <Grid.Column
                as="section"
                mobile={16}
                tablet={5}
                computer={4}
                floated="right"
              >
                <Sticky context={this.sidebarRef} offset={20}>
                  <Card fluid>
                    <Card.Content>
                      <Card.Header>
                        <span>
                          <Icon name="cogs" />
                          {i18next.t("Actions")}
                        </span>
                      </Card.Header>
                    </Card.Content>
                    <Card.Content>
                      <ActionBox facultyProfile={initialProfile} />
                    </Card.Content>
                  </Card>
                  <Card fluid>
                    <Card.Content>
                      <Card.Header>
                        <span>
                          <Icon name="id badge" />
                          {i18next.t("Profile picture")}
                        </span>
                      </Card.Header>
                    </Card.Content>
                    <Card.Content>
                      <PhotoUploader
                        facultyProfile={initialProfile}
                        hasPhoto={hasPhoto}
                        defaultPhoto={defaultPhoto}
                        photoMaxSize={photoMaxSize}
                      />
                    </Card.Content>
                  </Card>
                  <Card fluid>
                    <Card.Content>
                      <Card.Header>
                        <span>
                          <Icon name="file" />
                          {i18next.t("CV")}
                        </span>
                      </Card.Header>
                    </Card.Content>
                    <Card.Content>
                      <CvUploader
                        facultyProfile={initialProfile}
                        hasCv={hasCv}
                      />
                    </Card.Content>
                  </Card>
                </Sticky>
              </Grid.Column>
            </Ref>

            <Grid.Column className="danger-zone" as="section" width={16}>
              <DangerZone
                facultyProfile={initialProfile}
                onError={this.setGlobalError}
                permissions={permissions}
              />
            </Grid.Column>
          </Grid>
        </Container>
      </BaseForm>
    );
  }
}

FacultyProfileCreateForm.propTypes = {
  initialProfile: PropTypes.object,
  defaultPhoto: PropTypes.string.isRequired,
  hasPhoto: PropTypes.bool,
  hasCv: PropTypes.bool,
  photoMaxSize: PropTypes.number,
  permissions: PropTypes.object,
  types: PropTypes.array.isRequired,
};

FacultyProfileCreateForm.defaultProps = {
  initialProfile: null,
  hasPhoto: false,
  hasCv: false,
  photoMaxSize: 0,
};

const optionalJSONParse = (value, missing = null) => {
  return value !== undefined ? JSON.parse(value) : missing;
};

const domContainer = document.getElementById("app");
const initialProfile = optionalJSONParse(
  domContainer.dataset.facultyProfile,
  {},
);
const hasPhoto = optionalJSONParse(domContainer.dataset.hasPhoto, false);
const hasCv = optionalJSONParse(domContainer.dataset.hasCv, false);
const photoMaxSize = optionalJSONParse(domContainer.dataset.photoMaxSize, 0);
const permissions = optionalJSONParse(domContainer.dataset.permissions, {});
const types = optionalJSONParse(domContainer.dataset.types, []);

ReactDOM.render(
  <FacultyProfileCreateForm
    initialProfile={initialProfile}
    hasPhoto={hasPhoto}
    hasCv={hasCv}
    defaultPhoto="/static/images/square-placeholder.png"
    photoMaxSize={photoMaxSize}
    permissions={permissions}
    types={types}
  />,
  domContainer,
);
export default FacultyProfileCreateForm;
