// This file is part of Invenio-Faculty-Profiles.
// Copyright (C) 2025 Ubiquity Press.
//
// Invenio-faculty-profiles is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import _truncate from "lodash/truncate";
import React, { Component } from "react";
import { Image, withCancel } from "react-invenio-forms";
import { Card, Grid, Message, Placeholder } from "semantic-ui-react";
import { http } from "react-invenio-forms";
import PropTypes from "prop-types";

const PlaceholderLoader = ({ size, isLoading, children, ...props }) => {
  const PlaceholderItem = () => (
    <Grid.Column width={3}>
      <Placeholder>
        <Placeholder.Image square />
      </Placeholder>
      <Placeholder>
        <Placeholder.Paragraph>
          <Placeholder.Line length="medium" />
          <Placeholder.Line length="short" />
        </Placeholder.Paragraph>
      </Placeholder>
    </Grid.Column>
  );
  let numberOfHeader = [];
  for (let i = 0; i < size; i++) {
    numberOfHeader.push(<PlaceholderItem key={i} />);
  }

  if (!isLoading) {
    return children;
  }
  return (
    <Grid columns="equal" stackable>
      {numberOfHeader}
    </Grid>
  );
};

PlaceholderLoader.propTypes = {
  size: PropTypes.number,
  isLoading: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired,
};

PlaceholderLoader.defaultProps = {
  size: 5,
};

const EmptyMessage = ({ message }) => {
  return <Message icon="info" header={message} />;
};

EmptyMessage.propTypes = {
  message: PropTypes.string.isRequired,
};

class FacultyProfileCard extends Component {
  render() {
    const { facultyProfile: {id, links, metadata}, defaultPhoto } = this.props;
    return (
      <Card fluid href={`/faculty-profiles/${id}`}>
        <Image
          wrapped
          centered
          ui={false}
          src={links.photo}
          fallbackSrc={defaultPhoto}
          loadFallbackFirst
        />
        <Card.Content>
          <Card.Header>
            {_truncate(metadata.given_names + ' ' + metadata.family_name, { length: 30 })}
          </Card.Header>
          {metadata.biography && (
            <Card.Description>
              <div className="truncate-lines-2" dangerouslySetInnerHTML={{ __html: metadata.biography }}/>
            </Card.Description>
          )}
        </Card.Content>
      </Card>
    );
  }
}

FacultyProfileCard.propTypes = {
  facultyProfile: PropTypes.object.isRequired,
  defaultPhoto: PropTypes.string.isRequired,
};

class FacultyProfilesCardGroup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      data: { hits: [] },
    };
  }

  componentDidMount() {
    this.fetchData();
  }

  componentWillUnmount() {
    this.cancellableFetch && this.cancellableFetch.cancel();
  }

  fetchData = async () => {
    const { fetchDataUrl } = this.props;
    this.setState({ isLoading: true });
    const headers = {
      Accept: "application/json",
    };
    this.cancellableFetch = withCancel(http.get(fetchDataUrl, { headers }));

    try {
      const response = await this.cancellableFetch.promise;

      this.setState({ data: response.data.hits, isLoading: false });
    } catch (error) {
      // TODO: handle error response
    }
  };

  renderCards() {
    const { data } = this.state;
    const { defaultPhoto } = this.props;

    return data.hits.map((facultyProfile) => {
      return (
        <FacultyProfileCard
          key={facultyProfile.id}
          facultyProfile={facultyProfile}
          defaultPhoto={defaultPhoto}
        />
      );
    });
  }

  render() {
    const { isLoading, data } = this.state;
    const { emptyMessage } = this.props;
    return (
      <PlaceholderLoader isLoading={isLoading}>
        {data.hits.length === 0 ? (
          <EmptyMessage message={emptyMessage} />
        ) : (
          <Card.Group
            doubling
            stackable
            itemsPerRow={5}
            className="faculty-profile-frontpage-cards"
          >
            {this.renderCards()}
          </Card.Group>
        )}
      </PlaceholderLoader>
    );
  }
}

FacultyProfilesCardGroup.propTypes = {
  fetchDataUrl: PropTypes.string.isRequired,
  defaultPhoto: PropTypes.string.isRequired,
  emptyMessage: PropTypes.string.isRequired,
};

export default FacultyProfilesCardGroup;
