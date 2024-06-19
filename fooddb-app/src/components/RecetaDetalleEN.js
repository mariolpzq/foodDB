import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import AuthContext from '../Auth';

function RecetaDetalleEN() {
  const { isAuthenticated } = useContext(AuthContext);
  const { id } = useParams();
  const [receta, setReceta] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchReceta = async () => {
      try {
        const token = localStorage.getItem('token');
        let response;

        response = await axios.get(`http://localhost:8000/recetas/mealrec/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true 
        });
      

        setReceta(response.data);
      } catch (error) {
        console.error('Error al obtener la receta:', error);
      }
    };

    fetchReceta();
  }, [id, user]);

  const renderOMS_Lights = (omsLights) => {
    if (!omsLights) {

      return <p>No disponible</p>;
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
          return 'Fats';
        case 'trans':
          return 'Trans fats';
        case 'salt':
          return 'Salt';
        case 'sug':
          return 'Sugars';
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
        return 'Appetizer';
      case 'main-dish':
        return 'Main dish';
      case 'dessert':
        return 'Dessert';
      default:
        return category;
    }
  };

  const getUnidad = (key) => {
    switch (key) {
      case 'fat':
      case 'pro':
      case 'sat':
      case 'sug':
      case 'fiber':
      case 'car':
        return 'g';
      case 'salt':
        return 'mg';
      case 'energy':
        return 'kcal';
      default:
        return '';
    }
  };

  const formatearNutriente = (key) => {
    switch (key) {
      case 'Car':
        return 'Carbohydrates';
      case 'Pro':
        return 'Proteins';
      case 'Fat':
        return 'Fats';
      case 'Sat':
        return 'Saturated fats';
      case 'Trans':
        return 'Trans fats';
      case 'Sug':
        return 'Sugars';
      default:
        return key; 
    }
  }


  const primeraLetraMayúscula = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  if (!receta) {
    return <div>Cargando...</div>;
  }

  const nutritionalInfo = receta.nutritional_info_100g;
  const nutritionalInfoPDV = receta.nutritional_info_PDV || {};


  if (!isAuthenticated) {
    return (
    <div id='enlace-registro'>
       <p>No estás autenticado. Por favor, <Link to="/login">inicia sesión</Link></p>
    </div>);
  }

  return (
    <div className="cell receta-detalles">
      <div className='oms-container'>
        <h3>OMS Nutritional lights</h3>
        <div>{renderOMS_Lights(receta.OMS_lights_per100g)}</div>
      </div>

      <h1 id='titulo-receta'>{receta.title}</h1>
      {user && user.role !== "user" && receta.source && <p><strong>Source:</strong> {receta.source}</p>}
      {receta.language && <p><strong>Language:</strong> {receta.language}</p>}
      {receta.n_diners && <p><strong>Number of diners:</strong> {receta.n_diners}</p>}
      {receta.origin_ISO && <p><strong>Country of origin:</strong> {receta.origin_ISO}</p>}
      {receta.difficulty && <p><strong>Difficulty:</strong> {receta.difficulty}</p>}
      {receta.category && <p><strong>Category:</strong> {formatCategory(receta.category)}</p>}
      {receta.subcategory && <p><strong>Subcategory:</strong> {receta.subcategory}</p>}
      {receta.minutes && <p><strong>Preparation time:</strong> {receta.minutes}</p>}
      

      <h3><strong>Nutritional information</strong></h3>
      <table className="nutritional-info-table">
        <thead>
          <tr>
            <th>Nutrient</th>
            <th>Per 100g</th>
            <th><i>PDV</i></th>
          </tr>
        </thead>
        <tbody>
          {nutritionalInfo && Object.keys(nutritionalInfo).map((key) => (
            <tr key={key}>
              <td>{formatearNutriente(key.charAt(0).toUpperCase() + key.slice(1))}</td>
              <td>{nutritionalInfo[key] ? `${nutritionalInfo[key]} ${getUnidad(key)}` : '-'}</td>
              <td>{nutritionalInfoPDV[key] ? `${nutritionalInfoPDV[key]} %` : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>


      <h3><strong>Ingredients</strong></h3>
      {receta.ingredients && (
        <div className='listado-ingredientes'>
          <ul>
            {receta.ingredients.map((ing, index) => (
              <li key={index}>
                {ing.ingredientID ? (
                    <Link to={`/ingredient/${ing.ingredientID}`}>{primeraLetraMayúscula(ing.ingredient)}</Link>
                ) : (
                  <span>{primeraLetraMayúscula(ing.ingredient)}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      <h3><strong>Steps</strong></h3>
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
      {receta.num_interactions > 0 && receta.interactions && (
        <div className='reviews'>
          <ul>
            {receta.interactions.map((interaction, index) => (
              <li key={index}>
                <p> <strong>Rating: </strong>{interaction.rating}&nbsp;&nbsp;&nbsp;&nbsp;<strong>Date:</strong> {interaction.date}</p>
                <p>"{interaction.review}"</p>
              </li>
            ))}
          </ul>
        </div>
      )}
      
    </div>
  );
}

export default RecetaDetalleEN;
