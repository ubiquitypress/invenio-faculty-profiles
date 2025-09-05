/*
 * This file is part of Invenio.
 * Copyright (C) 2016-2022 CERN.
 * Copyright (C) 2021-2023 Northwestern University.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import React, { useState } from "react";
import Dropzone from "react-dropzone";
import { humanReadableBytes } from "react-invenio-forms";
import { Image } from "react-invenio-forms";
import { Button, Divider, Header, Icon, Message } from "semantic-ui-react";
import { FacultyProfileApi } from "../../api";
import { DeleteButton } from "./DeleteButton";
import PropTypes from "prop-types";

function noCacheUrl(url) {
  const result = new URL(url);
  const randomValue = new Date().getMilliseconds() * 5;
  result.searchParams.set("no-cache", randomValue.toString());
  return result.toString();
}

const PhotoUploader = ({ facultyProfile, defaultPhoto, hasPhoto, onError, photoMaxSize }) => {
  /* State */
  // props initilization is fine since original props don't change after
  // initial mounting.
  const [photoUrl, photoSetUrl] = useState(facultyProfile.links.photo);
  const [photoUpdated, photoSetUpdated] = useState(false);
  const [photoExists, photoSetExists] = useState(hasPhoto);

  // Nicer naming
  const photoDefault = defaultPhoto;

  let dropzoneParams = {
    preventDropOnDocument: true,
    onDropAccepted: async (acceptedFiles) => {
      const file = acceptedFiles[0];

      try {
        const client = new FacultyProfileApi();
        await client.updatePhoto(facultyProfile.id, file);

        const photoUrlNoCache = noCacheUrl(photoUrl);
        photoSetUrl(photoUrlNoCache);
        photoSetUpdated(true);
        photoSetExists(true);
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
    accept: ".bmp,.gif,.jpeg,.jpg,.png,.webp,.svg,.avif"
  };

  const deletePhoto = async () => {
    const client = new FacultyProfileApi();
    await client.deletePhoto(facultyProfile.id);

    const photoUrlNoCache = noCacheUrl(photoUrl);
    photoSetUrl(photoUrlNoCache);
    photoSetUpdated(true);
    photoSetExists(false);
  };

  return (
    <Dropzone {...dropzoneParams}>
      {({ getRootProps, getInputProps, open: openFileDialog }) => (
        <>
          <span {...getRootProps()}>
            <input {...getInputProps()} />
            <Header as="h2" size="small" className="mt-0">
              {i18next.t("Profile picture")}
            </Header>
            <Image
              /* Change in key will cause a remounting. */
              key={photoUrl}
              src={photoUrl}
              fallbackSrc={photoDefault}
              loadFallbackFirst
              fluid
              wrapped
              rounded
              className="community-photo settings"
            />

            <Divider hidden />
          </span>

          <Button
            fluid
            icon
            labelPosition="left"
            type="button"
            onClick={openFileDialog}
            className="rel-mt-1 rel-mb-1"
          >
            <Icon name="upload" />
            {i18next.t("Upload new picture")}
          </Button>
          <label className="helptext">
            {i18next.t("File must be smaller than {{fileSize}}", {
              fileSize: humanReadableBytes(photoMaxSize, true),
            })}
          </label>
          {photoExists && (
            <DeleteButton
              id="delete-picture-button"
              label={i18next.t("Delete picture")}
              confirmationMessage={
                <Header as="h2" size="medium">
                  {i18next.t("Are you sure you want to delete this picture?")}
                </Header>
              }
              onDelete={deletePhoto}
              onError={onError}
            />
          )}
          {photoUpdated && (
            <Message
              info
              icon="warning circle"
              size="small"
              content={i18next.t(
                "It may take a few moments for changes to be visible everywhere"
              )}
            />
          )}
        </>
      )}
    </Dropzone>
  );
};

PhotoUploader.propTypes = {
  facultyProfile: PropTypes.object.isRequired,
  defaultPhoto: PropTypes.string.isRequired,
  hasPhoto: PropTypes.bool.isRequired,
  onError: PropTypes.func.isRequired,
  photoMaxSize: PropTypes.number.isRequired,
};

export default PhotoUploader;
