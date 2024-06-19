import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../Auth';
import { Link } from 'react-router-dom';

function IngredienteDetalleEN() {
  const { isAuthenticated, user } = useContext(AuthContext);
  const { id } = useParams();
  const [ingrediente, setIngrediente] = useState(null);

  useEffect(() => {
    const fetchIngrediente = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/ingredientes/${id}`, {
          withCredentials: true
        });
        setIngrediente(response.data);
      } catch (error) {
        console.error('Error al obtener el ingrediente:', error);
      }
    };

    fetchIngrediente();
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
        case 'total_fat':
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
    };

    return Object.keys(omsLights).map((key) => (
      omsLights[key] && (
        <div key={key} style={{ 
          backgroundColor: getColor(omsLights[key]), 
          borderRadius: '20px', 
          padding: '5px 10px', 
          color: '#fff', 
          display: 'inline-block', 
          marginRight: '10px',
          marginBottom: '10px' 
        }}>
          <strong>{getKey(key)}</strong>
        </div>
      )
    ));
  };

  const getOrigen = (origin_ISO) => {
    switch (origin_ISO) {
      case 'ES':
        return 'Spain';
      case 'USA':
        return 'United States of America';
      case 'GBR':
        return 'United Kingdom';
      default:
        return origin_ISO;
    }
  };

  const getNombreNutriente = (key) => {
    switch (key) {
      case 'car':
        return 'Carbohydrates';
      case 'energy_kcal':
        return 'Energy (kcal)';
      case 'energy_kj':
        return 'Energy (kJ)';
      case 'pro':
        return 'Proteins';
      case 'wat':
        return 'Water';
      case 'sug':
        return 'Sugars';
      case 'total_fat':
        return 'Total fat';
      case 'sat':
        return 'Saturated fat';
      case 'trans':
        return 'Trans fat';
      case 'fiber':
        return 'Fiber';
      case 'cal':
        return 'Calcium';
      case 'clhoride':
        return 'Chloride';
      case 'iron':
        return 'Iron';
      case 'mag':
        return 'Magnesium';
      case 'phos':
        return 'Phosphorus';
      case 'pot':
        return 'Potassium';
      case 'sod':
        return 'Sodium';
      case 'cholesterol':
        return 'Cholesterol';
      case 'salt':
        return 'Salt';
      default:
        return key.charAt(0).toUpperCase() + key.slice(1); // Capitaliza el primer carácter
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
      case 'wat':
      case 'total_fat':
      case 'trans':
      case 'salt':
        return 'g';
      case 'cal':
      case 'chloride':
      case 'iron':
      case 'mag':
      case 'phos':
      case 'pot':
      case 'sod':
      case 'cholesterol':
        return 'mg';
      case 'energy_kcal':
        return 'kcal';
      case 'energy_kj':
        return 'kJ';
      default:
        return '';
    }
  };

  if (!isAuthenticated) {
    return (
    <div id='enlace-registro'>
       <p>No estás autenticado. Por favor, <Link to="/login">inicia sesión</Link></p>
    </div>);
  }
  if (!ingrediente) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="cell ingrediente-detalles">

      {ingrediente.oms_lights && (
        <div className='oms-container'>
          <h3>Indicadores nutricionales de la OMS</h3>
          <div>{renderOMS_Lights(ingrediente.oms_lights)}</div>
        </div>
      )}

<h1 id='titulo-ingrediente'>{ingrediente.name_en}</h1>
      
{ingrediente.category_esp && <p><strong>Category:</strong> {ingrediente.category_en}</p>}
      {ingrediente.origin_ISO && <p><strong>Origin:</strong> {getOrigen(ingrediente.origin_ISO)}</p>}
      {user && user.role !== 'user' && ingrediente.source && <p><strong>Source:</strong> {ingrediente.source}</p>}
      {user && user.role !== 'user' && ingrediente.langual && (
      <p>
        <strong>Langual:</strong>
        <br /> <br />
        {ingrediente.langual}
      </p>
      )}
      
      {ingrediente.nutritional_info_100g && (
        <div>
          <h3>Información nutricional por 100g</h3>
          <table className="nutritional-info-table">
            <thead>
              <tr>
                <th>Nutriente</th>
                <th>Cantidad</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(ingrediente.nutritional_info_100g).map(([key, value]) => {
                if (value !== null) { // Verifica si no es null
                  if (key === 'fats' && typeof value === 'object') {
                    return (
                      Object.entries(value).map(([fatKey, fatValue]) => (
                        fatValue !== null && (
                          <tr key={fatKey}>
                            <td>{getNombreNutriente(fatKey)}</td>
                            <td>{fatValue} {getUnidad(fatKey)}</td>
                          </tr>
                        )
                      ))
                    );
                  } else {
                    return (
                      <tr key={key}>
                        <td>{getNombreNutriente(key)}</td>
                        <td>{value} {getUnidad(key)}</td>
                      </tr>
                    );
                  }
                }
                return null;
              })}
            </tbody>
          </table>
        </div>
      )}
      
    </div>
  );
}

export default IngredienteDetalleEN;
