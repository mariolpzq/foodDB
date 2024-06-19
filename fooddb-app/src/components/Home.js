import React from 'react';
import { useContext } from 'react';
import AuthContext from '../Auth';



function Home() {
  const { isAuthenticated } = useContext(AuthContext);
  let redireccion;

  if (!isAuthenticated) {
    redireccion = '/login';
  } else {
    redireccion = '/recetas';
  }

  return (
    <div className='home'>
      <h1>¡Bienvenido a FoodDB!</h1>
      <button className='button-style' onClick={() => window.location.href = redireccion}>Descubre nuestras recetas</button>
    </div>
  );
}

export default Home;
