/*
 * This file is part of Invenio.
 * Copyright (C) 2016-2023 CERN.
 * Copyright (C) 2021-2022 Northwestern University.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import ReactDOM from "react-dom";
import { default as FacultyProfileProfileForm } from "./FacultyProfileProfileForm";
import { OverridableContext, overrideStore } from "react-overridable";

const domContainer = document.getElementById("app");
const facultyProfile = JSON.parse(domContainer.dataset.facultyProfile);
const hasPhoto = JSON.parse(domContainer.dataset.hasPhoto);
const hasCv = JSON.parse(domContainer.dataset.hasCv);
const photoMaxSize = JSON.parse(domContainer.dataset.photoMaxSize);
const permissions = JSON.parse(domContainer.dataset.permissions);
const overriddenComponents = overrideStore.getAll();

ReactDOM.render(
  <OverridableContext.Provider value={overriddenComponents}>
    <FacultyProfileProfileForm
      facultyProfile={facultyProfile}
      hasPhoto={hasPhoto}
      hasCv={hasCv}
      defaultPhoto="/static/images/square-placeholder.png"
      photoMaxSize={photoMaxSize}
      permissions={permissions}
    />
  </OverridableContext.Provider>,
  domContainer
);
