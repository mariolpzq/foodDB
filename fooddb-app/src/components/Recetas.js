import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import '../App.css';

function Recetas() {
  const [recetas, setRecetas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [appetizerSearch, setAppetizerSearch] = useState('');
  const [mainDishSearch, setMainDishSearch] = useState('');
  const [dessertSearch, setDessertSearch] = useState('');

  useEffect(() => {
    const fetchRecetas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/recetas/mealrec');
        setRecetas(response.data.recetas);
      } catch (error) {
        console.error('Error al obtener las recetas:', error);
      }
    };

    fetchRecetas();
  }, []);

  const filterRecetas = (recetas, categorySearch) => {
    return recetas.filter(receta =>
      receta.category === categorySearch &&
      receta.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const appetizers = filterRecetas(recetas, 'appetizer').filter(receta =>
    receta.title.toLowerCase().includes(appetizerSearch.toLowerCase())
  );
  const mainDishes = filterRecetas(recetas, 'main-dish').filter(receta =>
    receta.title.toLowerCase().includes(mainDishSearch.toLowerCase())
  );
  const desserts = filterRecetas(recetas, 'dessert').filter(receta =>
    receta.title.toLowerCase().includes(dessertSearch.toLowerCase())
  );

  return (
    <div>
      <div className="recetas-titulo">
      <h1>Recetas</h1>
      </div>
      <div className="recetas-search-bar">
        <input
          type="text"
          placeholder="Buscar en todas las recetas..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <div className="recetas-container">
        <div className="column">
          <h2>Entrantes</h2>
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder="Buscar entrantes..."
              value={appetizerSearch}
              onChange={(e) => setAppetizerSearch(e.target.value)}
            />
          </div>
          <ul>
            {appetizers.map((receta) => (
              <li key={receta.id}>
                <Link to={`/receta/${receta.id}`}>{receta.title}</Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="column">
          <h2>Platos principales</h2>
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder="Buscar platos principales..."
              value={mainDishSearch}
              onChange={(e) => setMainDishSearch(e.target.value)}
            />
          </div>
          <ul>
            {mainDishes.map((receta) => (
              <li key={receta.id}>
                <Link to={`/receta/${receta.id}`}>{receta.title}</Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="column">
          <h2>Postres</h2>
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder="Buscar postres..."
              value={dessertSearch}
              onChange={(e) => setDessertSearch(e.target.value)}
            />
          </div>
          <ul>
            {desserts.map((receta) => (
              <li key={receta.id}>
                <Link to={`/receta/${receta.id}`}>{receta.title}</Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Recetas;
