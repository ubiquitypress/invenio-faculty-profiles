// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import PropTypes from "prop-types";
import React, { useState } from "react";
import Dropzone from "react-dropzone";
import { Button, Divider, Header, Icon, Message } from "semantic-ui-react";
import { FacultyProfileApi } from "../api";
import { DeleteButton } from "./DeleteButton";

function noCacheUrl(url) {
  const result = new URL(url);
  const randomValue = new Date().getMilliseconds() * 5;
  result.searchParams.set("no-cache", randomValue.toString());
  return result.toString();
}

const CvUploader = ({ facultyProfile, hasCv, onError }) => {
  /* State */
  // props initilization is fine since original props don't change after
  // initial mounting.
  const [cvUrl, cvSetUrl] = useState(facultyProfile?.links?.cv);
  const [cvUpdated, cvSetUpdated] = useState(false);
  const [cvExists, cvSetExists] = useState(hasCv);

  let dropzoneParams = {
    preventDropOnDocument: true,
    onDropAccepted: async (acceptedFiles) => {
      const file = acceptedFiles[0];

      try {
        const client = new FacultyProfileApi();
        await client.updateCv(facultyProfile.id, file);

        const cvUrlNoCache = noCacheUrl(cvUrl);
        cvSetUrl(cvUrlNoCache);
        cvSetUpdated(true);
        cvSetExists(true);
      } catch (error) {
        onError(error);
      }
    },
    onDropRejected: (rejectedFiles) => {
      // TODO: show error message when files are rejected e.g size limit
      console.error(rejectedFiles[0].errors);
    },
    multiple: false,
    noClick: true,
    noDrag: true,
    noKeyboard: true,
    disabled: false,
    maxFiles: 1,
    maxSize: 50000000, // 50Mb limit
    accept: ".doc,.docx,.pdf,.txt",
    className: "dropzone " + cvUrl ? "" : "disabled",
  };

  const deleteCv = async () => {
    const client = new FacultyProfileApi();
    await client.deleteCv(facultyProfile.id);

    const cvUrlNoCache = noCacheUrl(cvUrl);
    cvSetUrl(cvUrlNoCache);
    cvSetUpdated(true);
    cvSetExists(false);
  };

  return (
    <Dropzone {...dropzoneParams}>
      {({ getRootProps, getInputProps, open: openFileDialog }) => (
        <>
          <span {...getRootProps()}>
            <input {...getInputProps()} />
          </span>
          {cvUrl ? null : (
            <p className="rel-mt-1 rel-mb-3 center aligned">
              Save the profile to upload the CV.
            </p>
          )}
          <Button
            fluid
            icon
            disabled={cvUrl === undefined}
            labelPosition="left"
            type="button"
            onClick={openFileDialog}
            className="rel-mt-1 rel-mb-1"
          >
            <Icon name="upload" />
            {i18next.t("Upload new CV")}
          </Button>
          {cvExists && (
            <DeleteButton
              id="delete-cv-button"
              label={i18next.t("Delete CV")}
              confirmationMessage={
                <Header as="h2" size="medium">
                  {i18next.t("Are you sure you want to delete this CV?")}
                </Header>
              }
              onDelete={deleteCv}
              onError={onError}
            />
          )}
          {cvUpdated && (
            <Message
              info
              icon="warning circle"
              size="small"
              content={i18next.t(
                "It may take a few moments for changes to be visible everywhere",
              )}
            />
          )}
        </>
      )}
    </Dropzone>
  );
};

CvUploader.propTypes = {
  facultyProfile: PropTypes.object.isRequired,
  hasCv: PropTypes.bool.isRequired,
  onError: PropTypes.func.isRequired,
};

export default CvUploader;
