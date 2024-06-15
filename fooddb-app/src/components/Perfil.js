import React, { useContext, useEffect, useState } from 'react';
import AuthContext from '../Auth';
import axios from 'axios';

const languageMap = {
    EN: 'English',
    ES: 'Español'
};

const cuisineMap = {
    PAN: 'Panamá',
    ARG: 'Argentina',
    VEN: 'Venezuela',
    URY: 'Uruguay',
    SLV: 'El Salvador',
    PRI: 'Puerto Rico',
    CHL: 'Chile',
    CRI: 'Costa Rica',
    NIC: 'Nicaragua',
    MEX: 'México',
    DOM: 'República Dominicana',
    HND: 'Honduras',
    COL: 'Colombia',
    ESP: 'España',
    GTM: 'Guatemala',
    PER: 'Perú',
    PRY: 'Paraguay',
    ECU: 'Ecuador',
    BOL: 'Bolivia',
    CUB: 'Cuba'
};

const Perfil = () => {
    const { isAuthenticated } = useContext(AuthContext);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const response = await axios.get('http://localhost:8000/auth/users/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    setUser(response.data);
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchUserData();
    }, []);

    if (!isAuthenticated) {
        return <p>No estás autenticado. Por favor, inicia sesión.</p>;
    }

    if (!user) {
        return <p>Cargando información del usuario...</p>;
    }

    // Función para obtener el mensaje del nivel de actividad
    const getActivityMessage = () => {
        if (user.activity_level === 1) {
            return "No muy activo. Actividad predominantemente sedentaria, con poca actividad física.";
        } else if (user.activity_level === 2) {
            return "Medianamente activo. Participación ocasional en actividades que requieren estar de pie o movimientos ligeros.";
        } else if (user.activity_level === 3) {
            return "Activo. Involucrado en actividades que incluyen caminar o realizar tareas domésticas regulares.";
        } else if (user.activity_level === 4) {
            return "Muy activo. Participación en actividades físicas intensas, como deportes o trabajo físico.";
        } else {
            return "Inactivo.";
        }
    };

    return (
        <div className='cell perfil'>
            <h2>Perfil de {user.name}</h2>
            <p><strong>Nombre:</strong> {user.name}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Género:</strong> {user.gender}</p>
            <p><strong>Edad:</strong> {user.age} años</p>
            <p><strong>Altura:</strong> {user.height} cm</p>
            <p><strong>Peso:</strong> {user.weight} kg</p>
            <p><strong>Nivel de actividad:</strong> {user.activity_level} - {getActivityMessage()}</p>
            <p><strong>Ingesta calórica diaria recomendada:</strong> {user.daily_caloric_intake} kcal</p>
            
            {/* Mostrar restricciones en una tabla */}
            <div>
                <h3>Restricciones nutricionales</h3>
                <table className="restricciones-tabla">
                    <thead>
                        <tr>
                            <th>Nutriente</th>
                            <th>Calorías (kcal)</th>
                            <th>Gramos (g)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Grasas totales</td>
                            <td>{user.restrictions_kcal?.fats?.total || '-'}</td>
                            <td>{user.restrictions_grams?.fats?.total || '0'}</td>
                        </tr>
                        <tr>
                            <td>Grasas saturadas</td>
                            <td>{user.restrictions_kcal?.fats?.sat || '-'}</td>
                            <td>{user.restrictions_grams?.fats?.sat || '0'}</td>
                        </tr>
                        <tr>
                            <td>Grasas trans</td>
                            <td>{user.restrictions_kcal?.fats?.trans || '-'}</td>
                            <td>{user.restrictions_grams?.fats?.trans || '0'}</td>
                        </tr>
                        <tr>
                            <td>Azúcares</td>
                            <td>{user.restrictions_kcal?.sugars || '-'}</td>
                            <td>{user.restrictions_grams?.sugars || '0'}</td>
                        </tr>
                        <tr>
                            <td>Sodio</td>
                            <td>-</td>
                            <td>{user.restrictions_grams?.sodium || '0'}</td>
                        </tr>
                        <tr>
                            <td>Sal</td>
                            <td>-</td>
                            <td>{user.restrictions_grams?.salt || '0'}</td>
                        </tr>
                        <tr>
                            <td>Potasio</td>
                            <td>-</td>
                            <td>{user.restrictions_grams?.potassium || '0'}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {/* Mostrar preferencias de idiomas si el array no está vacío */}
            {user.preferences?.languages?.length > 0 && (
                <div>
                    <h3>Idiomas preferidos</h3>
                    <ul>
                        {user.preferences.languages.map((language, index) => (
                            <li key={index}>{languageMap[language]}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Mostrar preferencias de gastronomía si el array no está vacío */}
            {user.preferences?.cuisines?.length > 0 && (
                <div>
                    <h3>Gastronomías preferidas</h3>
                    <ul>
                        {user.preferences.cuisines.map((cuisine, index) => (
                            <li key={index}>{cuisineMap[cuisine]}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Perfil;
