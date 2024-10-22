import { Outlet, Link } from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';

function Layout() {
  return (
    <>
      <Navbar bg="dark" variant="dark" sticky="top" expand="sm" collapseOnSelect>
        <Navbar.Collapse id="responsive-navbar-nav" className="me-auto">
          <Nav className = "me-auto">
            <Nav.Link as={Link} to="/">About Us</Nav.Link>
            <Nav.Link as={Link} to="/politician-stock">Politician Stock</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <br/>
        <Outlet />
    </>
  );
}

export default Layout;
