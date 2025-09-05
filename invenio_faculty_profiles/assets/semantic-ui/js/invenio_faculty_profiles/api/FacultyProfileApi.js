// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2024 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { http } from "react-invenio-forms";

/**
 * API Client for communities.
 *
 * It mostly uses the API links passed to it from responses.
 *
 */
export class FacultyProfileApi {
  baseUrl = "/api/faculty-profiles";

  /**
   * Create a new facultyProfile.
   *
   * @param {object} payload - Serialized faculty profile
   * @param {object} options - Custom options
   */
  async create(payload, options) {
    options = options || {};
    const headers = {
      "Accept": "application/json",
    };
    return http.post(this.baseUrl, payload, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Update a pre-existing facultyProfile.
   *
   * @param {string} facultyProfileId - identifier
   * @param {object} payload - Serialized facultyProfile
   * @param {object} options - Custom options
   */
  async update(facultyProfileId, payload, options) {
    options = options || {};
    const headers = {
      "Accept": "application/json",
    };
    return http.put(`${this.baseUrl}/${facultyProfileId}`, payload, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Delete the facultyProfile.
   *
   * @param {string} facultyProfileId - Identifier
   * @param {object} options - Custom options
   */
  async delete(facultyProfileId, options) {
    options = options || {};
    return http.delete(`${this.baseUrl}/${facultyProfileId}`, {
      ...options,
    });
  }

  /**
   * Update the facultyProfile photo.
   *
   * @param {string} facultyProfileId - Identifier
   * @param {object} payload - File
   * @param {object} options - Custom options
   */
  async updatePhoto(facultyProfileId, payload, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
      "X-Filename": payload.name,
    };
    return http.put(`${this.baseUrl}/${facultyProfileId}/photo`, payload, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Delete the facultyProfile photo.
   *
   * @param {string} facultyProfileId - Identifier
   * @param {object} options - Custom options
   */
  async deletePhoto(facultyProfileId, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
    };
    return http.delete(`${this.baseUrl}/${facultyProfileId}/photo`, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Update the facultyProfile cv.
   *
   * @param {string} facultyProfileId - Identifier
   * @param {object} payload - File
   * @param {object} options - Custom options
   */
  async updateCv(facultyProfileId, payload, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
      "X-Filename": payload.name,
    };
    return http.put(`${this.baseUrl}/${facultyProfileId}/cv`, payload, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Delete the facultyProfile cv.
   *
   * @param {string} facultyProfileId - Identifier
   * @param {object} options - Custom options
   */
  async deleteCv(facultyProfileId, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
    };
    return http.delete(`${this.baseUrl}/${facultyProfileId}/cv`, {
      headers: headers,
      ...options,
    });
  }
}
