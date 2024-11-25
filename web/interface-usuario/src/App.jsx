import './App.css';
import { Outlet } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Outlet />
      </div>
    </AuthProvider>
  );
}

export default App;