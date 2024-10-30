import 'src/styles/App.css'
import Navbar from 'src/components/Navbar'
import { Routes, Route } from 'react-router-dom'
import AboutUs from 'src/pages/AboutUs'
import PoliticianStock from 'src/pages/PoliticianStock'
import Transaction from 'src/pages/Transaction'
import { useFilter, FilterContext } from 'src/contexts/Filters.js'


function App() {
  const [filters, setFilters] = useFilter();

  return (
    <>
      <div className="App">
        <FilterContext.Provider value={[filters, setFilters]}>
          <Navbar />
          <Routes>
            <Route path="/" element={<AboutUs />}  />
            <Route path="/about" element={<AboutUs />} />
            <Route path="/transactions" element={<PoliticianStock />} />
            <Route path='/transaction/:id' element={<Transaction />} />
          </Routes>
        </FilterContext.Provider>
      </div>
    </>
  );
}

export default App

