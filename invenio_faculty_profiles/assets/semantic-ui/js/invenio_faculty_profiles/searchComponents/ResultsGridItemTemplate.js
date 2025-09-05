import React from "react";
import { Card } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ResultsGridItemTemplate = ({ result }) => {
  return (
    <Card fluid href={`/faculty-profiles/${result.id}`}>
      <Card.Content>
        <Card.Header>{result.given_names} {result.family_name}</Card.Header>
        <Card.Description>
          <div className="truncate-lines-2">{result.about_description}</div>
        </Card.Description>
      </Card.Content>
    </Card>
  );
};

ResultsGridItemTemplate.propTypes = {
  result: PropTypes.object.isRequired,
};
