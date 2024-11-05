import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from 'src/pages/layout/App.jsx'
import 'src/styles/index.css'
import { BrowserRouter } from 'react-router-dom'

createRoot(document.getElementById('root')).render(
  // remove the strict mode
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
