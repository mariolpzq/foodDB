import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import AuthContext from '../Auth';

function IngredienteDetalleESP() {
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
        return 'España';
      case 'USA':
        return 'Estados Unidos';
      case 'GBR':
        return 'Reino Unido';
      default:
        return origin_ISO;
    }
  };

  const getNombreNutriente = (key) => {
    switch (key) {
      case 'car':
        return 'Carbohidratos';
      case 'energy_kcal':
        return 'Energía (kcal)';
      case 'energy_kj':
        return 'Energía (kJ)';
      case 'pro':
        return 'Proteínas';
      case 'wat':
        return 'Agua';
      case 'sug':
        return 'Azúcares';
      case 'total_fat':
        return 'Grasas totales';
      case 'sat':
        return 'Grasas saturadas';
      case 'trans':
        return 'Grasas trans';
      case 'fiber':
        return 'Fibra';
      case 'cal':
        return 'Calcio';
      case 'clhoride':
        return 'Cloruro';
      case 'iron':
        return 'Hierro';
      case 'mag':
        return 'Magnesio';
      case 'phos':
        return 'Fósforo';
      case 'pot':
        return 'Potasio';
      case 'sod':
        return 'Sodio';
      case 'cholesterol':
        return 'Colesterol';
      case 'salt':
        return 'Sal';
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

      <h1 id='titulo-ingrediente'>{ingrediente.name_esp}</h1>
      
      {ingrediente.category_esp && <p><strong>Categoría:</strong> {ingrediente.category_esp}</p>}
      {ingrediente.origin_ISO && <p><strong>Origen:</strong> {getOrigen(ingrediente.origin_ISO)}</p>}
      {user && user.role !== 'user' && ingrediente.source && <p><strong>Fuente:</strong> {ingrediente.source}</p>}
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
                if (value) { // Verifica si hay un valor
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

export default IngredienteDetalleESP;
