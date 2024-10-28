import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import barStyle from "src/styles/Navbar.module.css"
import logo from '../../public/LOGO.png'

const Navbar = () => {

  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <nav>
      <div className={barStyle.logoContainer}>
        <Link to="/" className={barStyle.logo}>
          <img src={logo} alt="Logo" className={barStyle.aboutImg} />
        </Link>
        <span to="/" className={barStyle.title}>CAPITOL GAINS</span>
      </div>
      <div className={barStyle.menu} onClick={() => {
        setMenuOpen(!menuOpen);
      }}>
        <span></span>
        <span></span>
        <span></span>
      </div>

        <ul className={menuOpen ? barStyle.open : ""}> 
          <li>
            <NavLink to='/AboutUs'>About us</NavLink>
          </li>
          <li>
            <NavLink to='/PoliticianStock'>Transactions</NavLink>
          </li>
        </ul>
    </nav>
  )
}

export default Navbar