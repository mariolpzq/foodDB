import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../Auth';
import '../App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

const Dietas = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const [dietas, setDietas] = useState([]);
  const [recetaDetails, setRecetaDetails] = useState({});
  const navigate = useNavigate();

  const cualidadesBuenas = [
    'Buen contenido de fibra',
    'Bueno en grasas',
    'Bueno para el sodio',
    'Buena fuente de fibra',
    'Bueno fuente de fibra',
    'Sin sodio o sin sal',
    'Sin carbohidratos',
    'Bajo en grasas',
    'Sin azúcar añadida o sin azúcares agregadas',
    'Bueno fuente de proteínas',
    'Bueno para vegetarianos',
    'Bajo en azúcar',
    'Sin grasa',
    'Bueno para el corazón',
    'Sin grasas saturadas',
    'Sin colesterol',
    'Sin grasas trans',
    'Sin azúcar añadida',
    'Sin azúcar',
    'Alto en proteínas',
    'Sin sodio',
    'Sin calorías',
    'Sin gelatina',
    'Sin sal',
    'Alto en fibra',
    'Bajo en calorías',
    'Sin gluten',
    'Bajo en colesterol',
    'Sin lactosa',
    'Bajo en grasas saturadas',
    'Cero en calorías',
    'Bueno en fibra',
    'Sin harina',
    'Sin grasa saturada',
    'Buena fuente de fibra',
    'Bueno en proteínas',
    'Bajo en calorías',
    'Alto en vitamina C',
    'Bajo en carbohidratos',
    'Bajo en sodio',
    'Alto contenido de fibra',
    'Alto en vitaminas'
  ];
  
  const cualidadesMalas = [
    'Alto en azúcar',
    'Alto en calorías',
    'Alto en grasas',
    'Sin fibra',
    'Alto en colesterol',
    'Alto en azúcar añadida',
    'Alto en grasas reducidas o con menos grasas',
    'Alto en proteínas',
    'Alto en cafeina',
    'Alto en grasas saturadas',
    'Alto en alcohol',
    'Alto en calorías saturadas',
    'Alto en sodio',
    'Alto en vinagre',
    'Alto en azúcares añadidos'
  ];

  useEffect(() => {
    const fetchDietas = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await axios.get('http://localhost:8000/dietas', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          setDietas(response.data.diets);
        }
      } catch (error) {
        console.error('Error al obtener las dietas:', error);
      }
    };

    fetchDietas();
  }, []);

  useEffect(() => {
    const fetchRecetaDetails = async (recetaID, source) => {
      const token = localStorage.getItem('token');
      if (!token) return null;

      try {
        const response = await axios.get(`http://localhost:8000/${source}/${recetaID}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        return response.data;
      } catch (error) {
        console.error(`Error al obtener la receta de ${source}:`, error);
        return null;
      }
    };

    const fetchReceta = async (recetaID) => {
      let receta = await fetchRecetaDetails(recetaID, 'recetas/mealrec');
      if (!receta) {
        receta = await fetchRecetaDetails(recetaID, 'abuela');
      }
      return receta;
    };

    const fetchAllRecetaDetails = async () => {
      const newRecetaDetails = {};

      for (const dieta of dietas) {
        if (dieta.appetizerID) {
          newRecetaDetails[dieta.appetizerID] = await fetchReceta(dieta.appetizerID);
        }
        if (dieta.main_dishID) {
          newRecetaDetails[dieta.main_dishID] = await fetchReceta(dieta.main_dishID);
        }
        if (dieta.dessertID) {
          newRecetaDetails[dieta.dessertID] = await fetchReceta(dieta.dessertID);
        }
      }

      setRecetaDetails(newRecetaDetails);
    };

    if (dietas.length > 0) {
      fetchAllRecetaDetails();
    }
  }, [dietas]);

  const handleDeleteDiet = async (dietaId) => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        await axios.delete(`http://localhost:8000/dietas/${dietaId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setDietas(dietas.filter(dieta => dieta._id !== dietaId));
      }
    } catch (error) {
      console.error('Error al eliminar la dieta:', error);
    }
  };

  const renderOMS_Lights = (omsLights) => {
    if (!omsLights) {
      return <p></p>;
    }

    const getColor = (value) => {
      switch (value) {
        case 'green':
          return '#28a745';
        case 'orange':
          return '#FA7224';
        case 'red':
          return '#dc3545';
        default:
          return '#6c757d';
      }
    };

    const getKey = (value) => {
      switch (value) {
        case 'fat':
          return 'Grasas';
        case 'trans':
          return 'Grasas trans';
        case 'salt':
          return 'Sal';
        case 'sug':
          return 'Azúcares';
        default:
          return value;
      }
    }

    return Object.keys(omsLights).map((key) => (
      omsLights[key] && (
        <div key={key} style={{
          backgroundColor: getColor(omsLights[key]),
          borderRadius: '20px',
          padding: '5px 10px',
          color: '#fff',
          display: 'inline-block',
          marginRight: '10px',
          marginTop: '10px'
        }}>
          <strong>{getKey(key)}</strong>
        </div>
      )
    ));
  };

  const renderDietaryPreferences = (qualities) => {
    if (!qualities) {
      return <p>No disponible</p>;
    }

    for (let i = 0; i < qualities.length; i++) {
      qualities[i] = qualities[i].replace('.', '');
    }

    const getColor = (quality) => {
      if (cualidadesBuenas.includes(quality)) {
        return '#28a745'; // Verde
      } else if (cualidadesMalas.includes(quality)) {
        return '#dc3545'; // Rojo
      } else {
        return '#6c757d'; // Gris por defecto
      }
    };

    return qualities.map((quality, index) => (
      <div key={index} style={{
        backgroundColor: getColor(quality),
        borderRadius: '20px',
        padding: '5px 10px',
        color: '#fff',
        display: 'inline-block',
        marginRight: '10px',
        marginTop: '10px'
      }}>
        <strong>{quality}</strong>
      </div>
    ));
  };

  const getLink = (receta) => {
    if (receta.language_ISO === 'ES') {
      return `/receta/${receta.id}`;
    } else {
      return `/recipe/${receta.id}`;
    }
  };


  if (!isAuthenticated) {
    return <p>No estás autenticado. Por favor, inicia sesión.</p>;
  }

  return (
    <div>
      <h1>Dietas</h1>
      <div className="dietas-container">
        <button className="new-dieta-btn" onClick={() => navigate('/create-dieta')}>Nueva dieta</button>
        <div className="diet-list">
          {dietas.map((dieta, index) => (
            <div key={index} className="diet-item">
              <div className="dish-row">
                {dieta.appetizerID && recetaDetails[dieta.appetizerID] && (
                  <div className="dish">
                    <p><strong>Entrante:</strong></p>
                    <p><Link to={getLink(recetaDetails[dieta.appetizerID])}>{recetaDetails[dieta.appetizerID].title}</Link></p>
                    <div>
                      {recetaDetails[dieta.appetizerID].source === 'MealREC'
                        ? renderOMS_Lights(recetaDetails[dieta.appetizerID].OMS_lights_per100g)
                        : renderDietaryPreferences(recetaDetails[dieta.appetizerID].dietary_preferences)
                      }
                    </div>
                  </div>
                )}
                {dieta.main_dishID && recetaDetails[dieta.main_dishID] && (
                  <div className="dish">
                    <p><strong>Plato principal:</strong></p>
                    <p><Link to={getLink(recetaDetails[dieta.main_dishID])}>{recetaDetails[dieta.main_dishID].title}</Link></p>
                    <div>
                      {recetaDetails[dieta.main_dishID].source === 'MealREC'
                        ? renderOMS_Lights(recetaDetails[dieta.main_dishID].OMS_lights_per100g)
                        : renderDietaryPreferences(recetaDetails[dieta.main_dishID].dietary_preferences)
                      }
                    </div>
                  </div>
                )}
                {dieta.dessertID && recetaDetails[dieta.dessertID] && (
                  <div className="dish">
                    <p><strong>Postre:</strong></p>
                    <p><Link to={getLink(recetaDetails[dieta.dessertID])}>{recetaDetails[dieta.dessertID].title}</Link></p>
                    <div>
                      {recetaDetails[dieta.dessertID].source === 'MealREC'
                        ? renderOMS_Lights(recetaDetails[dieta.dessertID].OMS_lights_per100g)
                        : renderDietaryPreferences(recetaDetails[dieta.dessertID].dietary_preferences)
                      }
                    </div>
                  </div>
                )}
              </div>
              <button className="delete-button" onClick={() => handleDeleteDiet(dieta._id)}>
                <FontAwesomeIcon icon={faTrash} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dietas;
