import React from "react";
import PropTypes from "prop-types";

import { FacultyProfileCompactItemComputer } from "./FacultyProfileCompactItemComputer";
import { FacultyProfileCompactItemMobile } from "./FacultyProfileCompactItemMobile";

export function FacultyProfileCompactItem({
  result,
  actions,
  extraLabels,
  itemClassName,
  showPermissionLabel,
  detailUrl,
  isCommunityDefault,
}) {
  return (
    <>
      <FacultyProfileCompactItemComputer
        result={result}
        actions={actions}
        extraLabels={extraLabels}
        itemClassName={itemClassName}
        showPermissionLabel={showPermissionLabel}
        detailUrl={detailUrl}
        isCommunityDefault={isCommunityDefault}
      />
      <FacultyProfileCompactItemMobile
        result={result}
        actions={actions}
        extraLabels={extraLabels}
        itemClassName={itemClassName}
        showPermissionLabel={showPermissionLabel}
        detailUrl={detailUrl}
        isCommunityDefault={isCommunityDefault}
      />
    </>
  );
}

FacultyProfileCompactItem.propTypes = {
  result: PropTypes.object.isRequired,
  actions: PropTypes.node,
  extraLabels: PropTypes.node,
  itemClassName: PropTypes.string,
  showPermissionLabel: PropTypes.bool,
  detailUrl: PropTypes.string,
  isCommunityDefault: PropTypes.bool.isRequired,
};

FacultyProfileCompactItem.defaultProps = {
  actions: undefined,
  extraLabels: undefined,
  itemClassName: "",
  showPermissionLabel: false,
  detailUrl: undefined,
};
