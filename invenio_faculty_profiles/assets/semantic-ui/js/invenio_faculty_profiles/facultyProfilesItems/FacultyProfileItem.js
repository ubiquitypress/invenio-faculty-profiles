import React from "react";
import PropTypes from "prop-types";

import { FacultyProfileItemComputer } from "./FacultyProfileItemComputer";
import { FacultyProfileItemMobile } from "./FacultyProfileItemMobile";

export function FacultyProfileItem({ result }) {
  console.log(result);
  return (
    <>
      <FacultyProfileItemComputer result={result} />
      <FacultyProfileItemMobile result={result} />
    </>
  );
}

FacultyProfileItem.propTypes = {
  result: PropTypes.object.isRequired,
};
