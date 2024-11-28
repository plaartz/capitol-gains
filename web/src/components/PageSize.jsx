import { Dropdown, ButtonGroup } from "react-bootstrap";

const PageSize = ({pageSizer}) => {
  return (
    <div className="d-flex justify-content-end">
      <Dropdown as={ButtonGroup} drop="up">
        <Dropdown.Toggle variant="danger" id="dropdown-basic">
          Page size
        </Dropdown.Toggle>

        <Dropdown.Menu>
          <Dropdown.Item onClick={() => pageSizer(100)} href="#">100</Dropdown.Item>
          <Dropdown.Item onClick={() => pageSizer(50)} href="#">50</Dropdown.Item>
          <Dropdown.Item onClick={() => pageSizer(25)} href="#">25</Dropdown.Item>
          <Dropdown.Item onClick={() => pageSizer(10)} href="#">10</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
};

export default PageSize;
