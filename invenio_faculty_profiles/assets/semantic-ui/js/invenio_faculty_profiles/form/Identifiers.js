// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import _unickBy from "lodash/unionBy";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { FieldLabel, SelectField } from "react-invenio-forms";

export class Identifiers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOptions: props.initialOptions,
    };
  }

  handleIdentifierAddition = ({ data }) => {
    const { value } = data;
    this.setState((prevState) => ({
      selectedOptions: _unickBy(
        [
          {
            text: value,
            value: value,
            key: value,
          },
          ...prevState.selectedOptions,
        ],
        "value",
      ),
    }));
  };

  valuesToOptions = (options) =>
    options.map((option) => ({
      text: option,
      value: option,
      key: option,
    }));

  handleChange = ({ data, formikProps }) => {
    this.setState({
      selectedOptions: this.valuesToOptions(data.value),
    });
    formikProps.form.setFieldValue("metadata.identifiers", data.value);
  };

  render() {
    const { selectedOptions } = this.state;

    return (
      <SelectField
        fieldPath="metadata.identifiers"
        label={
          <FieldLabel
            htmlFor="identifiers"
            icon="barcode"
            label={i18next.t("Identifiers")}
          />
        }
        options={selectedOptions}
        placeholder={i18next.t("e.g. ORCID, ISNI or GND.")}
        noResultsMessage={i18next.t("Type the value of an identifier...")}
        search
        multiple
        selection
        allowAdditions
        onChange={this.handleChange}
        // `icon` is set to `null` in order to hide the dropdown default icon
        icon={null}
        onAddItem={this.handleIdentifierAddition}
        optimized
      />
    );
  }
}

Identifiers.propTypes = {
  initialOptions: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
      value: PropTypes.string.isRequired,
    }),
  ).isRequired,
};

Identifiers.defaultProps = {};
