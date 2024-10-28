import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import "../styles/Navbar.module.css"
import logo from '../../../LOGO.png'

const Navbar = () => {

  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <nav>
      <div className="logo-container">
        <Link to="/" className="logo">
          <img src={logo} alt="Logo" className="aboutImg" />
        </Link>
        <Link to="/" className="title">CAPITOL GAINS</Link>
      </div>
      <div className='menu' onClick={() => {
        setMenuOpen(!menuOpen);
      }}>
        <span></span>
        <span></span>
        <span></span>
      </div>

        <ul className={menuOpen ? "open" : ""}> 
          <li>
            <NavLink to='/AboutUs'>About us</NavLink>
          </li>
          <li>
            <NavLink to='/PoliticianStock'>Politician Track</NavLink>
          </li>
        </ul>
    </nav>
  )
}

export default Navbar