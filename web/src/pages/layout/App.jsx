import 'src/styles/App.css'
import Navbar from 'src/components/Navbar'
import { Routes, Route } from 'react-router-dom'
import AboutUs from 'src/pages/AboutUs'
import PoliticianStock from 'src/pages/PoliticianStock'


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

