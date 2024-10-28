import '../../styles/App.css'
import Navbar from '../../components/Navbar'
import { Routes, Route } from 'react-router-dom'
import AboutUs from '../AboutUs'
import PoliticianStock from '../PoliticianStock'


function App() {
  return (
    <>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<AboutUs />}/>
          <Route path='/AboutUs' element={<AboutUs />}></Route>
          <Route path='/PoliticianStock' element={<PoliticianStock />}></Route>
        </Routes>
      </div>
    </>
  )
}

export default App

