import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './routes/UserRegister/UserRegister'
import UserRegister from './routes/UserRegister/UserRegister'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='App'>
        <UserRegister>
          
        </UserRegister>

    </div>
  )
}

export default App
