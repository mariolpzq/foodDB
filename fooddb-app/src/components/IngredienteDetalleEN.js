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
  const [emision, setEmision] = useState(null);

  useEffect(() => {
    const fetchIngrediente = async () => {
      try {
        const response = await axios.get(`https://fooddb-up7u.onrender.com/ingredientes/${id}`, {
          withCredentials: true
        });
        setIngrediente(response.data);

        if (response.data.emissionsID) {
          const emisionResponse = await axios.get(`https://fooddb-up7u.onrender.com/emisiones/${response.data.emissionsID}`, {
            withCredentials: true
          });
          setEmision(emisionResponse.data);
        }
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
          return 'Fats';
        case 'trans':
          return 'Trans';
        case 'salt':
          return 'Salt';
        case 'sug':
          return 'Sugars';
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
        return key.charAt(0).toUpperCase() + key.slice(1); // Primera letra en mayúscula
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
          <h3>OMS nutritional lights</h3>
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
          <h3>Nutritional info per 100g</h3>
          <table className="nutritional-info-table">
            <thead>
              <tr>
                <th>Nutrient</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(ingrediente.nutritional_info_100g).map(([key, value]) => {
                if (value !== null && value !== '') { // Verifica si no es null
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

      {user && (user.role === 'nutritionist' || user.role === 'researcher') && ingrediente.compounds && ingrediente.compounds.length > 0 && (
        <div>
          <h3>Compounds</h3>
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {ingrediente.compounds.map((compound, index) => (
              <li key={index}>
                <div>
                  {compound.compounds.map((comp, i) => (
                    <span key={i} className="compound-item">
                      {comp}
                    </span>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {user && (user.role === 'researcher') && emision && (
        <div>
          <h3>Emissions per kg</h3>
          <table className="nutritional-info-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {emision.land_use_change !== null && (
                <tr>
                  <td>Land use change</td>
                  <td>{emision.land_use_change} Kg CO2</td>
                </tr>
              )}
              {emision.animal_feed !== null && (
                <tr>
                  <td>Animal feed</td>
                  <td>{emision.animal_feed} Kg CO2</td>
                </tr>
              )}
              {emision.farm !== null && (
                <tr>
                  <td>Farm</td>
                  <td>{emision.farm} Kg CO2</td>
                </tr>
              )}
              {emision.processing !== null && (
                <tr>
                  <td>Processing</td>
                  <td>{emision.processing} Kg CO2</td>
                </tr>
              )}
              {emision.transport !== null && (
                <tr>
                  <td>Transport</td>
                  <td>{emision.transport} Kg CO2</td>
                </tr>
              )}
              {emision.packaging !== null && (
                <tr>
                  <td>Packaging</td>
                  <td>{emision.packaging} Kg CO2</td>
                </tr>
              )}
              {emision.retail !== null && (
                <tr>
                  <td>Retail</td>
                  <td>{emision.retail} Kg CO2</td>
                </tr>
              )}
              {emision.total_emissions !== null && (
                <tr>
                  <td>Total emissions</td>
                  <td>{emision.total_emissions} Kg CO2</td>
                </tr>
              )}
              {(emision.euto.euto_1000kcal !== null || emision.euto.euto_100gr_protein !== null || emision.euto.euto_kilogram !== null) && (
                <>
                  <tr>
                    <td colSpan="2"><strong>Eutrophication</strong></td>
                  </tr>
                  {emision.euto.euto_1000kcal !== null && (
                    <tr>
                      <td>Per 1000 kcal</td>
                      <td>{emision.euto.euto_1000kcal} gPO<sub>4</sub>eq</td>
                    </tr>
                  )}
                  {emision.euto.euto_100gr_protein !== null && (
                    <tr>
                      <td>Per 100g protein</td>
                      <td>{emision.euto.euto_100gr_protein} gPO<sub>4</sub>eq</td>
                    </tr>
                  )}
                  {emision.euto.euto_kilogram !== null && (
                    <tr>
                      <td>Per kilogram</td>
                      <td>{emision.euto.euto_kilogram} gPO<sub>4</sub>eq</td>
                    </tr>
                  )}
                </>
              )}
              {(emision.withdrawals.withdrawals_1000kcal !== null || emision.withdrawals.withdrawals_100gr_protein !== null || emision.withdrawals.withdrawals_kilogram !== null) && (
                <>
                  <tr>
                    <td colSpan="2"><strong>Withdrawals</strong></td>
                  </tr>
                  {emision.withdrawals.withdrawals_1000kcal !== null && (
                    <tr>
                      <td>Per 1000 kcal</td>
                      <td>{emision.withdrawals.withdrawals_1000kcal} L</td>
                    </tr>
                  )}
                  {emision.withdrawals.withdrawals_100gr_protein !== null && (
                    <tr>
                      <td>Per 100g protein</td>
                      <td>{emision.withdrawals.withdrawals_100gr_protein} L</td>
                    </tr>
                  )}
                  {emision.withdrawals.withdrawals_kilogram !== null && (
                    <tr>
                      <td>Per kilogram</td>
                      <td>{emision.withdrawals.withdrawals_kilogram} L</td>
                    </tr>
                  )}
                </>
              )}
              {(emision.greenhouse.greenhouse_1000kcal !== null || emision.greenhouse.greenhouse_100gr_protein !== null) && (
                <>
                  <tr>
                    <td colSpan="2"><strong>Greenhouse</strong></td>
                  </tr>
                  {emision.greenhouse.greenhouse_1000kcal !== null && (
                    <tr>
                      <td>Per 1000 kcal</td>
                      <td>{emision.greenhouse.greenhouse_1000kcal} Kg CO2</td>
                    </tr>
                  )}
                  {emision.greenhouse.greenhouse_100gr_protein !== null && (
                    <tr>
                      <td>Per 100g protein</td>
                      <td>{emision.greenhouse.greenhouse_100gr_protein} Kg CO2</td>
                    </tr>
                  )}
                </>
              )}
              {(emision.land_use.land_use_1000kcal !== null || emision.land_use.land_use_100gr_protein !== null || emision.land_use.land_use_kilogram !== null) && (
                <>
                  <tr>
                    <td colSpan="2"><strong>Land use</strong></td>
                  </tr>
                  {emision.land_use.land_use_1000kcal !== null && (
                    <tr>
                      <td>Per 1000 kcal</td>
                      <td>{emision.land_use.land_use_1000kcal} m&sup2;</td>
                    </tr>
                  )}
                  {emision.land_use.land_use_100gr_protein !== null && (
                    <tr>
                      <td>Per 100g protein</td>
                      <td>{emision.land_use.land_use_100gr_protein} m&sup2;</td>
                    </tr>
                  )}
                  {emision.land_use.land_use_kilogram !== null && (
                    <tr>
                      <td>Per kilogram</td>
                      <td>{emision.land_use.land_use_kilogram} m&sup2;</td>
                    </tr>
                  )}
                </>
              )}
              {(emision.scarcity_water_use.scarcity_water_use_1000kcal !== null || emision.scarcity_water_use.scarcity_water_use_100gr_protein !== null || emision.scarcity_water_use.scarcity_water_use_kilogram !== null) && (
                <>
                  <tr>
                    <td colSpan="2"><strong>Scarcity water use</strong></td>
                  </tr>
                  {emision.scarcity_water_use.scarcity_water_use_1000kcal !== null && (
                    <tr>
                      <td>Per 1000 kcal</td>
                      <td>{emision.scarcity_water_use.scarcity_water_use_1000kcal} L</td>
                    </tr>
                  )}
                  {emision.scarcity_water_use.scarcity_water_use_100gr_protein !== null && (
                    <tr>
                      <td>Per 100g protein</td>
                      <td>{emision.scarcity_water_use.scarcity_water_use_100gr_protein} L</td>
                    </tr>
                  )}
                  {emision.scarcity_water_use.scarcity_water_use_kilogram !== null && (
                    <tr>
                      <td>Per kilogram</td>
                      <td>{emision.scarcity_water_use.scarcity_water_use_kilogram} L</td>
                    </tr>
                  )}
                </>
              )}
            </tbody>
          </table>
        </div>
      )}

    </div>
  );
}

export default IngredienteDetalleEN;
