// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import { connect as connectFormik } from "formik";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { Button, Grid } from "semantic-ui-react";

export class ActionBoxComponent extends Component {
  handleSave = (event) => {
    const { formik } = this.props;
    const { handleSubmit } = formik;

    handleSubmit(event);
  };

  render() {
    const { formik, facultyProfile } = this.props;
    const { isSubmitting } = formik;

    const profileUrl = facultyProfile?.links?.self_html;
    const viewButtonDisabled = profileUrl ? "" : "disabled";

    return (
      <Grid verticalAlign="middle" className="mt-5 mb-5" relaxed>
        <Grid.Row centered className="pt-5 pb-5 padded">
          <Grid.Column width={8}>
            <Button
              name="save"
              disabled={isSubmitting}
              onClick={(event) => this.handleSave(event)}
              icon="save"
              fluid
              loading={isSubmitting}
              labelPosition="left"
              content={i18next.t("Save")}
            />
          </Grid.Column>
          <Grid.Column width={8}>
            <a
              href={profileUrl}
              className={`ui labeled icon button fluid ${viewButtonDisabled}`}
            >
              <i className="eye icon"></i>
              {i18next.t("View")}
            </a>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    );
  }
}

ActionBoxComponent.propTypes = {
  formik: PropTypes.object.isRequired,
  facultyProfile: PropTypes.object.isRequired,
};

ActionBoxComponent.defaultProps = {};

export const ActionBox = connectFormik(ActionBoxComponent);
