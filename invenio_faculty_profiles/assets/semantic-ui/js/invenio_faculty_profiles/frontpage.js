// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";

import FacultyProfileCardGroup from "./FacultyProfileCardGroup";

const latestFacultyProfilesContainer = document.getElementById("latest-faculty-profiles");

if (latestFacultyProfilesContainer) {
  ReactDOM.render(
    <FacultyProfileCardGroup
      fetchDataUrl="/api/faculty-profiles?q=&sort=newest&page=1&size=5"
      emptyMessage="There are no new researcher profiles."
      defaultPhoto="/static/images/square-placeholder.png"
    />,
    latestFacultyProfilesContainer
  );
}
