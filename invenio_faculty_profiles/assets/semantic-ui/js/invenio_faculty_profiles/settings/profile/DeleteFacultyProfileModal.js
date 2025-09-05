/*
 * This file is part of Invenio.
 * Copyright (C) 2023 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { i18next } from "@translations/invenio_faculty_profiles/i18next";
import React, { Component } from "react";
import {
  Button,
  Icon,
  Loader,
  Modal,
  Message,
  Checkbox,
  Input,
} from "semantic-ui-react";
import PropTypes from "prop-types";
import { Trans } from "react-i18next";
import { facultyProfileErrorSerializer } from "../../api/serializers";
import { ErrorMessage, http, withCancel } from "react-invenio-forms";

export class DeleteFacultyProfileModal extends Component {
  constructor(props) {
    super(props);
    this.INITIAL_STATE = {
      modalOpen: false,
      loading: true,
      inputFullName: "",
      error: undefined,
    };
    this.checkboxRef = React.createRef();
    this.openModalBtnRef = React.createRef();
    this.state = this.INITIAL_STATE;
  }

  componentDidUpdate(prevProps, prevState) {
    const { loading, modalOpen } = this.state;
    if (!loading && modalOpen && modalOpen !== prevState.modalOpen) {
      const {
        current: { inputRef },
      } = this.checkboxRef;
      inputRef.current.focus();
    }
  }

  componentWillUnmount() {
    this.cancellableDelete && this.cancellableDelete.cancel();
  }

  handleInputChange = (event) => {
    this.setState({ inputFullName: event.target.value });
  };

  handleButtonDisabled = (fullName) => {
    const { inputFullName } = this.state;
    return !(inputFullName === fullName);
  };

  openConfirmModal = () => this.setState({ modalOpen: true });

  closeConfirmModal = () => {
    let { loading } = this.state;
    this.setState({ ...this.INITIAL_STATE, loading: loading });
    this.openModalBtnRef?.current?.focus();
  };

  handleDelete = async () => {
    this.setState({ loading: true });
    const { onDelete, redirectURL } = this.props;

    this.cancellableDelete = withCancel(onDelete());
    try {
      await this.cancellableDelete.promise;

      if (redirectURL) {
        window.location.href = redirectURL;
      }

      this.closeConfirmModal();
    } catch (error) {
      if (error === "UNMOUNTED") return;
      console.error(error);
      const { message } = facultyProfileErrorSerializer(error);
      if (message) {
        this.setState({ error: message, loading: false });
      }
    }
  };

  render() {
    const {
      modalOpen,
      loading,
      inputFullName,
      error,
    } = this.state;
    const { label, facultyProfile } = this.props;
    const facultyProfileFullName = facultyProfile.given_names.trim() + ' ' + facultyProfile.family_name.trim();
    return (
      <>
        <Button
          ref={this.openModalBtnRef}
          compact
          negative
          onClick={this.openConfirmModal}
          fluid
          icon
          labelPosition="left"
          type="button"
          aria-haspopup="dialog"
          aria-controls="warning-modal"
          aria-expanded={modalOpen}
          id="delete-community-button"
        >
          <Icon name="trash" />
          {label}
        </Button>

        <Modal
          id="warning-modal"
          role="dialog"
          aria-labelledby="delete-community-button"
          open={modalOpen}
          onClose={this.closeConfirmModal}
          size="tiny"
        >
          <Modal.Header as="h2">
            {i18next.t("Permanently delete researcher profile")}
          </Modal.Header>
          {loading && <Loader active={loading} />}
          <Modal.Content>
            <p>
              <Trans>
                Are you <strong>absolutely sure</strong> you want to delete the
                researcher profile?
              </Trans>
            </p>

            <Message negative>
              <Message.Header className="rel-mb-1">
                <Icon name="warning sign" className="rel-mr-1" />
                {i18next.t("This action CANNOT be undone!")}
              </Message.Header>
              <>
              </>
            </Message>

            <label htmlFor="confirm-delete">
              <Trans>
                Please type <strong>{{ facultyProfileFullName }}</strong> to confirm.
              </Trans>
            </label>
            <Input
              id="confirm-delete"
              fluid
              value={inputFullName}
              onChange={this.handleInputChange}
            />
          </Modal.Content>
          <Modal.Actions>
            {error && (
              <ErrorMessage
                header={i18next.t("Unable to delete")}
                content={i18next.t(error)}
                icon="exclamation"
                className="text-align-left"
                negative
              />
            )}
            <Button onClick={this.closeConfirmModal} floated="left">
              {i18next.t("Cancel")}
            </Button>
            <Button
              negative
              onClick={() => this.handleDelete()}
              disabled={this.handleButtonDisabled(facultyProfileFullName)}
            >
              {i18next.t("Permanently delete")}
            </Button>
          </Modal.Actions>
        </Modal>
      </>
    );
  }
}

DeleteFacultyProfileModal.propTypes = {
  onDelete: PropTypes.func.isRequired,
  redirectURL: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  facultyProfile: PropTypes.object.isRequired,
};
