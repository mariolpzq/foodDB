import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../Auth';
import '../App.css';

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
                                {dieta.appetizerID && dieta.appetizer_title && (
                                    <div className="dish">
                                        <p><strong>Entrante:</strong></p> 
                                        <p> <Link to={`/receta/${dieta.appetizerID}`}>{dieta.appetizer_title}</Link></p>
                                    </div>
                                )}
                                {dieta.main_dishID && dieta.main_dish_title && (
                                    <div className="dish">
                                        <p><strong>Plato principal:</strong></p>
                                        <p> <Link to={`/receta/${dieta.main_dishID}`}>{dieta.main_dish_title}</Link></p>
                                    </div>
                                )}
                                {dieta.dessertID && dieta.dessert_title && (
                                    <div className="dish">
                                        <p><strong>Postre:</strong> </p>
                                        <p><Link to={`/receta/${dieta.dessertID}`}>{dieta.dessert_title}</Link></p>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>

    );
};

export default Dietas;
