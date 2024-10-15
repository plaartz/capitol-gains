import { useEffect } from 'react'
import './App.css'

function App() {
  useEffect(()=>{fetch('/api/core/test')},[])

  return (
    <>
      <p> The start of the cs 506 congressional tracking app </p>
    </>
  )
}

export default App
