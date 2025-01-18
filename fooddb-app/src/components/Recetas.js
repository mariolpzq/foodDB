import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import '../App.css';
import { useContext } from 'react';
import AuthContext from '../Auth';

function Recetas() {
  const { isAuthenticated } = useContext(AuthContext);
  const [recetas, setRecetas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [appetizerSearch, setAppetizerSearch] = useState('');
  const [mainDishSearch, setMainDishSearch] = useState('');
  const [dessertSearch, setDessertSearch] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await axios.get('https://fooddb-up7u.onrender.com/auth/users/me', { 
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          setUser(response.data);
        }
      } catch (error) {
        console.error('Error al obtener el usuario:', error);
      }
    };

    fetchUser();
  }, []);

  useEffect(() => {
    const fetchRecetas = async () => {

      
      if (user) {
        const languages = user.preferences.languages;
        const token = localStorage.getItem('token');

      
        if (token) {
          try {
            let allRecetas = [];
            
            // Incluir recetas en inglés si el idioma está presente
            if (languages.includes('EN')) {
              const englishResponse = await axios.get('https://fooddb-up7u.onrender.com/recetas/mealrec', {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              allRecetas = allRecetas.concat(englishResponse.data.recetas);
            }

            // Incluir recetas en español si el idioma está presente
            if (languages.includes('ES')) {
              if (user.preferences.cuisines && user.preferences.cuisines.length > 0) {
                const promises = user.preferences.cuisines.map((cuisine) =>
                  axios.get(`https://fooddb-up7u.onrender.com/recetas/abuela/pais/${cuisine}`, {
                    headers: {
                      'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                  })
                );
                const responses = await Promise.all(promises);
                const spanishRecetas = responses.flatMap(res => res.data.recetas);
                allRecetas = allRecetas.concat(spanishRecetas);
              } else {
                const spanishResponse = await axios.get('https://fooddb-up7u.onrender.com/recetas/abuela/', {
                  headers: {
                    'Authorization': `Bearer ${token}`
                  },
                  withCredentials: true
                });
                allRecetas = allRecetas.concat(spanishResponse.data.recetas);
              }
            }

            setRecetas(allRecetas);
          } catch (error) {
            console.error('Error al obtener las recetas:', error);
          }
        }
      }
    };
        



    fetchRecetas();
  }, [user]);

  const filterRecetas = (recetas, categorySearch, language) => {
    const categories = language === 'EN'
      ? {
          'appetizer': ['appetizer', 'entrante'],
          'main-dish': ['main-dish', 'plato principal'],
          'dessert': ['dessert', 'postre']
        }
      : {
          'entrante': ['appetizer', 'entrante'],
          'plato principal': ['main-dish', 'plato principal'],
          'postre': ['dessert', 'postre']
        };

    return recetas.filter(receta =>
      categories[categorySearch].includes(receta.category) &&
      receta.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const primeraLetraMayúscula = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const appetizers = filterRecetas(recetas, 'appetizer', 'EN');
  const mainDishes = filterRecetas(recetas, 'main-dish', 'EN');
  const desserts = filterRecetas(recetas, 'dessert', 'EN');

  const getLink = (receta) => {
    if (receta.language_ISO === 'ES') {
      return `/receta/${receta.id}`;
    } else {
      return `/recipe/${receta.id}`;
    }
  };

  if (!isAuthenticated) {
    return (
    <div id='enlace-registro'>
       <p>No estás autenticado. Por favor, <Link to="/login">inicia sesión</Link></p>
    </div>);
  }

  const idiomas = user ? user.preferences.languages : [];
  return (
    <div>
      <div className="recetas-titulo">
        {idiomas.length === 2 && <h1>Recipes / Recetas </h1> }
        {idiomas.length === 1 && idiomas[0] === 'EN' && <h1>Recipes</h1>}
        {idiomas.length === 1 && idiomas[0] === 'ES' && <h1>Recetas</h1>}
      </div>
      <div className="recetas-search-bar">
        <input
          type="text"
          placeholder={idiomas.length === 1 && idiomas[0] === 'EN'  ? "Search recipes..." : "Buscar recetas..."}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <div className="recetas-container">
        <div className="column">
          {idiomas.length === 2 && <h2>Appetizers / Entrantes </h2> }
          {idiomas.length === 1 && idiomas[0] === 'EN' && <h2>Appetizers</h2>}
          {idiomas.length === 1 && idiomas[0] === 'ES' && <h2>Entrantes</h2>}
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder={idiomas.length === 1 && idiomas[0] === 'EN'  ? "Search appetizers..." : "Buscar entrantes..."}
              value={appetizerSearch}
              onChange={(e) => setAppetizerSearch(e.target.value)}
            />
          </div>
          <ul>
            {appetizers.filter(receta =>
              receta.title.toLowerCase().includes(appetizerSearch.toLowerCase())
            ).map((receta) => (
              <li key={receta.id}>
                <Link to={getLink(receta)}>{primeraLetraMayúscula(receta.title)}</Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="column">
          {idiomas.length === 2 && <h2>Main dishes / Platos principales </h2> }
          {idiomas.length === 1 && idiomas[0] === 'EN' && <h2>Main dishes</h2>}
          {idiomas.length === 1 && idiomas[0] === 'ES' && <h2>Platos principales</h2>}
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder={idiomas.length === 1 && idiomas[0] === 'EN'  ? "Search main dishes..." : "Buscar platos principales..."}
              value={mainDishSearch}
              onChange={(e) => setMainDishSearch(e.target.value)}
            />
          </div>
          <ul>
            {mainDishes.filter(receta =>
              receta.title.toLowerCase().includes(mainDishSearch.toLowerCase())
            ).map((receta) => (
              <li key={receta.id}>
                <Link to={getLink(receta)}>{primeraLetraMayúscula(receta.title)}</Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="column">
          {idiomas.length === 2 && <h2>Desserts / Postres </h2> }
          {idiomas.length === 1 && idiomas[0] === 'EN' && <h2>Desserts</h2>}
          {idiomas.length === 1 && idiomas[0] === 'ES' && <h2>Postres</h2>}
          <div className="individual-search-bar">
            <input
              type="text"
              placeholder={idiomas.length === 1 && idiomas[0] === 'EN'  ? "Search desserts..." : "Buscar postres..."}
              value={dessertSearch}
              onChange={(e) => setDessertSearch(e.target.value)}
            />
          </div>
          <ul>
            {desserts.filter(receta =>
              receta.title.toLowerCase().includes(dessertSearch.toLowerCase())
            ).map((receta) => (
              <li key={receta.id}>
                <Link to={getLink(receta)}>{primeraLetraMayúscula(receta.title)}</Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Recetas;
