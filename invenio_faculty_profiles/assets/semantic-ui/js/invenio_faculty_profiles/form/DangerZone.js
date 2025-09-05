/*
 * This file is part of Invenio.
 * Copyright (C) 2016-2023 CERN.
 * Copyright (C) 2021-2022 Northwestern University.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import React from "react";
import { Grid, Header, Segment } from "semantic-ui-react";
import { FacultyProfileApi } from "../api";
import PropTypes from "prop-types";
import { DeleteFacultyProfileModal } from "./DeleteFacultyProfileModal";

const DangerZone = ({ facultyProfile, onError, permissions }) => {
  if (permissions.can_delete || permissions.can_rename) {
    return (
      <Segment className="negative rel-mt-2">
        <Header as="h2" className="negative">
          {i18next.t("Danger zone")}
        </Header>
        <Grid>
          {permissions.can_delete && (
            <>
              <Grid.Column mobile={16} tablet={10} computer={12} floated="left">
                <Header as="h3" size="small">
                  {i18next.t("Delete researcher profile")}
                </Header>
                <p>
                  {i18next.t(
                    "Once deleted, it will be gone forever. Please be certain."
                  )}
                </p>
              </Grid.Column>
              <Grid.Column mobile={16} tablet={6} computer={4} floated="right">
                <DeleteFacultyProfileModal
                  facultyProfile={facultyProfile}
                  label={i18next.t("Delete researcher profile")}
                  redirectURL="/faculty-profiles"
                  onDelete={async () => {
                    const client = new FacultyProfileApi();
                    await client.delete(facultyProfile.id);
                  }}
                />
              </Grid.Column>
            </>
          )}
        </Grid>
      </Segment>
    );
  } else {
    return null;
  }
};

DangerZone.propTypes = {
  facultyProfile: PropTypes.object.isRequired,
  onError: PropTypes.func.isRequired,
  permissions: PropTypes.object.isRequired,
};

export default DangerZone;
