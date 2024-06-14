import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Login from './components/Login';
import Recetas from './components/Recetas';
import RecetaDetalle from './components/RecetaDetalle';
import IngredienteDetalle from './components/IngredienteDetalle';
import Register from './components/Register';
import Logout from './components/Logout';
import Perfil from './components/Perfil';
import { AuthProvider } from './Auth';
import Navigation from './components/Navigation';
import Home from './components/Home'; 
import Dietas from './components/Dietas';
import CreateDieta from './components/CreateDieta';

function App() {
  const [backgroundClass, setBackgroundClass] = useState('default-background');

  return (
    <AuthProvider>
      <Router>
        <div className={`general-grid ${backgroundClass}`}>
          <header className="cell">
            <div id="titulo">
              <p>
                <a href="/">
                  <strong>FoodDB</strong>
                </a>
              </p>
            </div>
            <Navigation />
          </header>

          <main className='main-cell'>
            <BackgroundSetter setBackgroundClass={setBackgroundClass} />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/recetas" element={<Recetas />} />
              <Route path="/receta/:id" element={<RecetaDetalle />} />
              <Route path="/ingredient/:id" element={<IngredienteDetalle />} /> 
              <Route path="/dietas" element={<Dietas />} />
              <Route path="/create-dieta" element={<CreateDieta />} />
              <Route path="/perfil" element={<Perfil />} />
              <Route path="/logout" element={<Logout />} />
            </Routes>
          </main>

          <footer className="cell">
            <p>&copy; 2024 - Mario López Quesada</p>
            <address>
              <p>Correo electrónico: <a href="mailto:lopezmario@correo.ugr.es">lopezmario@correo.ugr.es</a></p>
            </address>
          </footer>
        </div>
      </Router>
    </AuthProvider>
  );
}

function BackgroundSetter({ setBackgroundClass }) {
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/') {
      setBackgroundClass('home-background');
    } else {
      setBackgroundClass('default-background');
    }
  }, [location, setBackgroundClass]);

  return null;
}

export default App;
