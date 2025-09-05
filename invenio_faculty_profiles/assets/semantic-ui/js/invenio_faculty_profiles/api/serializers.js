// This file is part of Invenio-communities
// Copyright (C) 2022 CERN.
//
// Invenio-communities is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

export const facultyProfileErrorSerializer = (error) => ({
  message: error?.response?.data?.message,
  errors: error?.response?.data?.errors,
  status: error?.response?.data?.status,
});
