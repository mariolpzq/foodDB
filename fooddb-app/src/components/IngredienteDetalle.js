import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function IngredienteDetalle() {
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

  if (!ingrediente) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="ingrediente-detalles">
      <h1>{ingrediente.name_esp}</h1>
      {ingrediente.oms_lights && (
        <div>
          <h3>Indicadores nutricionales de la OMS</h3>
          {renderOMS_Lights(ingrediente.oms_lights)}
        </div>
      )}
      {ingrediente.name_esp && <p><strong>Nombre en inglés:</strong> {ingrediente.name_en}</p>}
      {ingrediente.langual && <p><strong>Langual:</strong> {ingrediente.langual}</p>}
      {ingrediente.origin_ISO && <p><strong>Origen:</strong> {ingrediente.origin_ISO}</p>}
      {ingrediente.source && <p><strong>Fuente:</strong> {ingrediente.source}</p>}
      {ingrediente.category_esp && <p><strong>Categoría en español:</strong> {ingrediente.category_esp}</p>}
      {ingrediente.category_en && <p><strong>Categoría en inglés:</strong> {ingrediente.category_en}</p>}
      {ingrediente.nutritional_info_100g && (
        <div>
          <p><strong>Información nutricional por 100g:</strong></p>
          <ul>
            {Object.entries(ingrediente.nutritional_info_100g).map(([key, value]) => {
              if (key === 'fats' && typeof value === 'object') {
                return (
                  <li key={key}>
                    <strong>{key}:</strong>
                    <ul>
                      {Object.entries(value).map(([fatKey, fatValue]) => (
                        <li key={fatKey}><strong>{fatKey}:</strong> {fatValue}</li>
                      ))}
                    </ul>
                  </li>
                );
              } else {
                return (
                  <li key={key}><strong>{key}:</strong> {value}</li>
                );
              }
            })}
          </ul>
        </div>
      )}
      
    </div>
  );
}

export default IngredienteDetalle;
