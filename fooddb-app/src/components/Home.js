import React from 'react';

function Home() {
  return (
    <div className='home'>
      <h1>¡Bienvenido a FoodDB!</h1>
      <button className='button-style' onClick={() => window.location.href = '/recetas'}>Descubre nuestras recetas</button>
    </div>
  );
}

export default Home;
