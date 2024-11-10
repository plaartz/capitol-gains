import React from "react";
import { Dropdown, ButtonGroup, Button } from "react-bootstrap";

const PageSize = ({pgSiz}) => {
  return (
    <div className="d-flex justify-content-end">
      <Dropdown as={ButtonGroup} drop="up">
        <Dropdown.Toggle variant="danger" id="dropdown-basic">
          Page size
        </Dropdown.Toggle>

        <Dropdown.Menu>
          <Dropdown.Item onClick={() => pgSiz(100)} href="#">100</Dropdown.Item>
          <Dropdown.Item onClick={() => pgSiz(50)} href="#">50</Dropdown.Item>
          <Dropdown.Item onClick={() => pgSiz(25)} href="#">25</Dropdown.Item>
          <Dropdown.Item onClick={() => pgSiz(10)} href="#">10</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
};

export default PageSize;
