import { Navbar as Navigation, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom'

function Navbar() {
    return <Navigation bg="dark" variant="dark" sticky="top" expand="sm" collapseOnSelect>
        <Navbar.Collapse id="responsive-navbar-nav" className="me-auto">
          <Nav className = "me-auto">
            <Nav.Link as={Link} to="/">About Us</Nav.Link>
            <Nav.Link as={Link} to="/politician-stock">Politician Stock</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navigation>
}

export default Navbar