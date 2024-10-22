//import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css'

import AboutUs from './AboutUs'
import Layout from './Layout'
import PoliticianStock from './PoliticianStock'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<AboutUs />}/>
          <Route path="politician-stock" element={<PoliticianStock />}/>
          <Route path="*" element={<AboutUs />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App
