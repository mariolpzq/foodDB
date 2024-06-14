import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import AuthContext from '../Auth';

function RecetaDetalle() {
  const { id } = useParams();
  const [receta, setReceta] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchReceta = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/recetas/mealrec/${id}`, {
          withCredentials: true // Enviar cookies de sesión o tokens
        });

        setReceta(response.data);
      } catch (error) {
        console.error('Error al obtener la receta:', error);
      }
    };

    fetchReceta();
  }, [id]);

  const renderOMS_Lights = (omsLights) => {
    if (!omsLights) {
      return <p>No data available</p>;
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
          marginRight: '10px' 
        }}>
          <strong>{getKey(key)}</strong>
        </div>
      )
    ));
  };

  const formatCategory = (category) => {
    switch (category) {
      case 'appetizer':
        return 'Entrante';
      case 'main-dish':
        return 'Plato principal';
      case 'dessert':
        return 'Postre';
      default:
        return category;
    }
  };

  const getUnit = (key) => {
    switch (key) {
      case 'fat':
      case 'pro':
      case 'sat':
      case 'sug':
      case 'fiber':
        return 'g';
      case 'salt':
        return 'mg';
      case 'energy':
        return 'kcal';
      case 'car':
        return 'g';
      default:
        return '';
    }
  };

  if (!receta) {
    return <div>Cargando...</div>;
  }

  const nutritionalInfo = receta.nutritional_info_100g;
  const nutritionalInfoPDV = receta.nutritional_info_PDV || {};

  return (
    <div className="cell receta-detalles">
      <div className='oms-container'>
        <h3>Semáforo nutricional</h3>
        <div>{renderOMS_Lights(receta.OMS_lights_per100g)}</div>
      </div>

      <h1 id='titulo-receta'>{receta.title}</h1>
      {user && user.role !== "user" && receta.source && <p><strong>Fuente:</strong> {receta.source}</p>}
      {receta.language && <p><strong>Idioma:</strong> {receta.language}</p>}
      {receta.origin && <p><strong>Origen:</strong> {receta.origin}</p>}
      {receta.n_diners && <p><strong>Número de comensales:</strong> {receta.n_diners}</p>}
      {receta.difficulty && <p><strong>Dificultad:</strong> {receta.difficulty}</p>}
      {receta.category && <p><strong>Categoría:</strong> {formatCategory(receta.category)}</p>}
      {receta.subcategory && <p><strong>Subcategoría:</strong> {receta.subcategory}</p>}
      {receta.minutes && <p><strong>Tiempo de preparación:</strong> {receta.minutes}</p>}
      
      {user && user.role !== "user" && (
        <>
          <h3><strong>Información Nutricional</strong></h3>
          <table className="nutritional-info-table">
            <thead>
              <tr>
                <th>Nutriente</th>
                <th>Por 100g</th>
                <th><i>PDV</i></th>
              </tr>
            </thead>
            <tbody>
              {nutritionalInfo && Object.keys(nutritionalInfo).map((key) => (
                <tr key={key}>
                  <td>{key.charAt(0).toUpperCase() + key.slice(1)}</td>
                  <td>{nutritionalInfo[key] ? `${nutritionalInfo[key]} ${getUnit(key)}` : '-'}</td>
                  <td>{nutritionalInfoPDV[key] ? `${nutritionalInfoPDV[key]} %` : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      <h3><strong>Ingredientes</strong></h3>
      {receta.ingredients && (
        <div className='listado-ingredientes'>
          <ul>
            {receta.ingredients.map((ing, index) => (
              <li key={index}>
                {ing.ingredientID ? (
                    <Link to={`/ingredient/${ing.ingredientID}`}>{ing.ingredient}</Link>
                ) : (
                  <span>{ing.ingredient}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      <h3><strong>Instrucciones de preparación</strong></h3>
      {receta.steps && (
        <div className='steps'>
          <ul>
            {receta.steps.map((step, index) => (
              <li key={index}><strong>{index+1}.</strong> {step}</li>
            ))}
          </ul>
        </div>
      )}
      <h3><strong>Reviews</strong></h3>
      {receta.num_interactions > 0 && (
        <div className='reviews'>
          <ul>
            {receta.interactions.map((interaction, index) => (
              <li key={index}>
                <p> <strong>Valoración: </strong>{interaction.rating}&nbsp;&nbsp;&nbsp;&nbsp;<strong>Fecha:</strong> {interaction.date}</p>
                <p>"{interaction.review}"</p>
              </li>
            ))}
          </ul>
        </div>
      )}
      
    </div>
  );
}

export default RecetaDetalle;
