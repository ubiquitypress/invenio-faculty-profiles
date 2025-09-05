/*
 * This file is part of Invenio.
 * Copyright (C) 2016-2024 CERN.
 * Copyright (C) 2021-2022 Northwestern University.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import { Formik } from "formik";
import _cloneDeep from "lodash/cloneDeep";
import _defaultsDeep from "lodash/defaultsDeep";
import _get from "lodash/get";
import _isArray from "lodash/isArray";
import _isBoolean from "lodash/isBoolean";
import _isEmpty from "lodash/isEmpty";
import _isNull from "lodash/isNull";
import _isNumber from "lodash/isNumber";
import _isObject from "lodash/isObject";
import _map from "lodash/map";
import _mapValues from "lodash/mapValues";
import _pick from "lodash/pick";
import _pickBy from "lodash/pickBy";
import _unset from "lodash/unset";
import React, { Component } from "react";
import {
  AccordionField,
  BooleanField,
  RichInputField,
  FieldLabel,
  TextField,
  TextAreaField,
} from "react-invenio-forms";
import { Button, Form, Grid, Icon, Message, Divider, LabelDetail } from "semantic-ui-react";
import * as Yup from "yup";
import { FacultyProfileApi } from "../../api";
import { facultyProfileErrorSerializer } from "../../api/serializers";
import PropTypes from "prop-types";
import { default as DangerZone } from "./DangerZone";
import { default as PhotoUploader } from "./PhotoUploader";
import { default as CvUploader } from "./CvUploader";
import Overridable from "react-overridable";

const FACULTY_PROFILES_VALIDATION_SCHEMA = Yup.object({
  preferred_pronouns: Yup.string().max(
    30,
    i18next.t("Maximum number of characters is 30")
  ),
  family_name: Yup.string().max(100, i18next.t("Maximum number of characters is 100")),
  given_names: Yup.string().max(100, i18next.t("Maximum number of characters is 100")),
  identifier: Yup.string().max(100, i18next.t("Maximum number of characters is 50")),
  about_description: Yup.string().max(
    50000,
    i18next.t("Maximum number of characters is 2000")
  ),
  research_interests: Yup.string().max(
    2000,
    i18next.t("Maximum number of characters is 2000")
  ),
  title_status: Yup.string().max(
    200,
    i18next.t("Maximum number of characters is 200")
  ),
  department: Yup.string().max(
    200,
    i18next.t("Maximum number of characters is 200")
  ),
  institution: Yup.string().max(
    200,
    i18next.t("Maximum number of characters is 200")
  ),
  education: Yup.string().max(
    50000,
    i18next.t("Maximum number of characters is 1000")
  ),
  email_address: Yup.string().email('Invalid email address'),
  contact_email_address: Yup.string().email('Invalid email address'),
});

/**
 * Remove empty fields from facultyProfile
 * Copied from react-invenio-deposit
 * @method
 * @param {object} obj - potentially empty object
 * @returns {object} facultyProfile - without empty fields
 */
const removeEmptyValues = (obj) => {
  if (_isArray(obj)) {
    let mappedValues = obj.map((value) => removeEmptyValues(value));
    return mappedValues.filter((value) => {
      if (_isBoolean(value) || _isNumber(value)) {
        return value;
      }
      return !_isEmpty(value);
    });
  } else if (_isObject(obj)) {
    let mappedValues = _mapValues(obj, (value) => removeEmptyValues(value));
    return _pickBy(mappedValues, (value) => {
      if (_isArray(value) || _isObject(value)) {
        return !_isEmpty(value);
      }
      return !_isNull(value);
    });
  }
  return _isNumber(obj) || _isBoolean(obj) || obj ? obj : null;
};

class FacultyProfileProfileForm extends Component {
  state = {
    error: "",
  };
  knownOrganizations = {};

  getInitialValues = () => {
    const { facultyProfile } = this.props;
    let initialValues = _defaultsDeep(facultyProfile, {
      id: "",
      preferred_pronouns: "",
      family_name: "",
      given_names: "",
      identifier: "",
      about_description: "",
      research_interests: "",
      title_status: "",
      department: "",
      institution: "",
      education: "",
      email_address: "",
      contact_email_address: "",
      active: false,
    });

    // create a map with all organizations that are not custom (part of the
    // vocabulary), so that on form submission, newly custom organization input
    // by the user can be identified and correctly sent to the backend.

    const genericVocabFields = [];

    return {
      ...initialValues,
    };
  };

  /**
   * Serializes facultyProfile values
   *
   * @param {object} values
   *
   * @returns
   */
  serializeValues = (values) => {

    let submittedFacultyProfile = _cloneDeep(values);

    submittedFacultyProfile = {
      ...submittedFacultyProfile,
    };

    // Clean values
    submittedFacultyProfile = removeEmptyValues(submittedFacultyProfile);

    return submittedFacultyProfile;
  };

  setGlobalError = (error) => {
    const { message } = facultyProfileErrorSerializer(error);
    this.setState({ error: message });
  };

  onSubmit = async (values, { setSubmitting, setFieldError }) => {
    setSubmitting(true);
    let payload = this.serializeValues(values);
    _unset(payload, "ui");
    const client = new FacultyProfileApi();
    const { facultyProfile } = this.props;

    try {
      await client.update(facultyProfile.id, payload);
      window.location.reload();
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
    const {
      facultyProfile,
      hasPhoto,
      hasCv,
      defaultPhoto,
      photoMaxSize,
      permissions,
    } = this.props;
    const { error } = this.state;
    return (
      <Formik
        initialValues={this.getInitialValues(facultyProfile)}
        validationSchema={FACULTY_PROFILES_VALIDATION_SCHEMA}
        onSubmit={this.onSubmit}
      >
        {({ isSubmitting, isValid, handleSubmit }) => (
          <Form onSubmit={handleSubmit} className="communities-profile">
            <Message hidden={error === ""} negative>
              <Grid container>
                <Grid.Column width={15} textAlign="left">
                  <strong>{error}</strong>
                </Grid.Column>
              </Grid>
            </Message>
            <Grid>
              <Grid.Row>
                <Grid.Column
                  as="section"
                  mobile={16}
                  tablet={10}
                  computer={11}
                  className="rel-pb-2"
                >
                  <AccordionField
                    includesPaths={[
                      "preferred_pronouns",
                      "family_name",
                      "given_names",
                      "identifier",
                      "about_description",
                      "research_interests",
                      "title_status",
                      "department",
                      "institution",
                      "education",
                      "email_address",
                      "contact_email_address",
                      "active",
                    ]}
                    label={i18next.t("Basic information")}
                    active
                  >
                    <div className="rel-ml-1 rel-mr-1">
                      <TextField
                        fluid
                        fieldPath="preferred_pronouns"
                        label={
                          <FieldLabel
                            htmlFor="preferred_pronouns"
                            icon="user"
                            label={i18next.t("Preferred Pronouns")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="family_name"
                        label={
                          <FieldLabel
                            htmlFor="family_name"
                            icon="user"
                            label={i18next.t("Family Name")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="given_names"
                        label={
                          <FieldLabel
                            htmlFor="given_names"
                            icon="user"
                            label={i18next.t("Given Names")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="identifier"
                        label={
                          <FieldLabel
                            htmlFor="identifier"
                            icon="user"
                            label={i18next.t("Identifier")}
                          />
                        }
                      />
                      <Overridable
                        id="InvenioCommunities.FacultyProfileProfileForm.TextAreaField.AboutDescription"
                        facultyProfile={facultyProfile}
                      >
                        <RichInputField
                          fieldPath="about_description"
                          label={
                            <FieldLabel
                              htmlFor="about_description"
                              icon="pencil"
                              label={i18next.t("About")}
                            />
                          }
                          fluid
                        />
                      </Overridable>
                      <Overridable
                        id="InvenioCommunities.FacultyProfileProfileForm.TextAreaField.ResearchInterests"
                        facultyProfile={facultyProfile}
                      >
                        <TextAreaField
                          fieldPath="research_interests"
                          label={
                            <FieldLabel
                              htmlFor="research_interests"
                              icon="pencil"
                              label={i18next.t("Research Interests")}
                            />
                          }
                          fluid
                        />
                      </Overridable>
                      <TextField
                        fluid
                        fieldPath="title_status"
                        label={
                          <FieldLabel
                            htmlFor="title_status"
                            icon="user"
                            label={i18next.t("Title")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="department"
                        label={
                          <FieldLabel
                            htmlFor="department"
                            icon="user"
                            label={i18next.t("Department")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="institution"
                        label={
                          <FieldLabel
                            htmlFor="institution"
                            icon="user"
                            label={i18next.t("Institution")}
                          />
                        }
                      />
                      <Overridable
                        id="InvenioCommunities.FacultyProfileProfileForm.TextAreaField.Education"
                        facultyProfile={facultyProfile}
                      >
                        <RichInputField
                          fieldPath="education"
                          label={
                            <FieldLabel
                              htmlFor="education"
                              icon="pencil"
                              label={i18next.t("Education")}
                            />
                          }
                          fluid
                        />
                      </Overridable>
                      <TextField
                        fluid
                        fieldPath="email_address"
                        label={
                          <FieldLabel
                            htmlFor="email_address"
                            icon="user"
                            label={i18next.t("Email Address")}
                          />
                        }
                      />
                      <TextField
                        fluid
                        fieldPath="contact_email_address"
                        label={
                          <FieldLabel
                            htmlFor="contact_email_address"
                            icon="user"
                            label={i18next.t("Contact Email Address")}
                          />
                        }
                      />
                      <BooleanField
                        fluid
                        fieldPath="active"
                        label={
                          <FieldLabel
                            htmlFor="active"
                            icon="user"
                            label={i18next.t("Active")}
                          />
                        }
                      />
                    </div>
                  </AccordionField>


                  <Divider hidden />
                  <Divider />
                  <Button
                    disabled={!isValid || isSubmitting}
                    loading={isSubmitting}
                    labelPosition="left"
                    primary
                    type="button"
                    icon
                    onClick={(event) => handleSubmit(event)}
                  >
                    <Icon name="save" />
                    {i18next.t("Save")}
                  </Button>
                </Grid.Column>
                <Grid.Column
                  as="section"
                  mobile={16}
                  tablet={5}
                  computer={4}
                  floated="right"
                >
                  <Overridable
                    id="InvenioFacultyProfiles.FacultyProfileProfileForm.PhotoUploader.ProfilePicture"
                    facultyProfile={facultyProfile}
                  >
                    <PhotoUploader
                      facultyProfile={facultyProfile}
                      hasPhoto={hasPhoto}
                      defaultPhoto={defaultPhoto}
                      onError={this.setGlobalError}
                      photoMaxSize={photoMaxSize}
                    />
                  </Overridable>
                  <Overridable
                    id="InvenioFacultyProfiles.FacultyProfileProfileForm.CvUploader.ProfileCv"
                    facultyProfile={facultyProfile}
                  >
                    <CvUploader
                      facultyProfile={facultyProfile}
                      hasCv={hasCv}
                      defaultCv={defaultPhoto}
                      onError={this.setGlobalError}
                    />
                  </Overridable>
                </Grid.Column>
              </Grid.Row>
              <Overridable
                id="InvenioCommunities.FacultyProfileProfileForm.GridRow.DangerZone"
                facultyProfile={facultyProfile}
              >
                <Grid.Row className="danger-zone">
                  <Grid.Column as="section" width={16}>
                    <DangerZone
                      facultyProfile={facultyProfile}
                      onError={this.setGlobalError}
                      permissions={permissions}
                    />
                  </Grid.Column>
                </Grid.Row>
              </Overridable>
            </Grid>
          </Form>
        )}
      </Formik>
    );
  }
}

FacultyProfileProfileForm.propTypes = {
  facultyProfile: PropTypes.object.isRequired,
  defaultPhoto: PropTypes.string.isRequired,
  hasPhoto: PropTypes.bool.isRequired,
  hasCv: PropTypes.bool.isRequired,
  photoMaxSize: PropTypes.number.isRequired,
  permissions: PropTypes.object.isRequired,
};

export default FacultyProfileProfileForm;
