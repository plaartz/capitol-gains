import 'src/styles/App.css'
import Navbar from 'src/components/Navbar'
import { Routes, Route } from 'react-router-dom'
import AboutUs from 'src/pages/AboutUs'
import PoliticianStock from 'src/pages/PoliticianStock'
import { useFilter, FilterContext} from 'src/contexts/Filter.js'


function App() {
  const [filters, setFilters] = useFilter();

  return (
    <>
      <div className="App">
        <FilterContext.Provider values={[filters, setFilters]}>
          <Navbar />
          <Routes>
            <Route path="/" element={<AboutUs />} />
            <Route path="/about" element={<AboutUs />}></Route>
            <Route path="/transactions" element={<PoliticianStock />}></Route>
          </Routes>
        </FilterContext.Provider>
      </div>
    </>
  );
}

export default App

