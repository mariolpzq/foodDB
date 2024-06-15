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
    const navigate = useNavigate();

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
                                {dieta.appetizerID && dieta.appetizer && (
                                    <div className="dish">
                                        <p><strong>Entrante:</strong></p> 
                                        <p> <Link to={`/receta/${dieta.appetizerID}`}>{dieta.appetizer.title}</Link></p>
                                        <div>{renderOMS_Lights(dieta.appetizer?.OMS_lights_per100g)}</div>
                                    </div>
                                )}
                                {dieta.main_dishID && dieta.main_dish && (
                                    <div className="dish">
                                        <p><strong>Plato principal:</strong></p>
                                        <p> <Link to={`/receta/${dieta.main_dishID}`}>{dieta.main_dish.title}</Link></p>
                                        <div>{renderOMS_Lights(dieta.main_dish?.OMS_lights_per100g)}</div>
                                    </div>
                                )}
                                {dieta.dessertID && dieta.dessert && (
                                    <div className="dish">
                                        <p><strong>Postre:</strong> </p>
                                        <p><Link to={`/receta/${dieta.dessertID}`}>{dieta.dessert.title}</Link></p>
                                        <div>{renderOMS_Lights(dieta.dessert?.OMS_lights_per100g)}</div>
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
