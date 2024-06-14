import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [gender, setGender] = useState('');
    const [age, setAge] = useState('');
    const [height, setHeight] = useState('');
    const [weight, setWeight] = useState('');
    const [activityLevel, setActivityLevel] = useState('');
    const [dietaryPreferences, setDietaryPreferences] = useState([]);
    const navigate = useNavigate();

    const calculateDailyCaloricIntake = (gender, age, height, weight, activityLevel) => {
        let MB; // Metabolismo Basal
        if (gender === 'Hombre') {
            MB =  (10 * weight) + (6.25 * height) - (5 * age) + 5;
        } else if (gender === 'Mujer') {
            MB = (10 * weight) + (6.25 * height) - (5 * age) - 161;
        } else {
            MB = 0;
        }

        let multiplicadorPorActividad;
        switch (activityLevel) {
            case 1:
                multiplicadorPorActividad = 1.2;
                break;
            case 2:
                multiplicadorPorActividad = 1.375;
                break;
            case 3:
                multiplicadorPorActividad = 1.55;
                break;
            case 4:
                multiplicadorPorActividad = 1.725;
                break;
            default:
                multiplicadorPorActividad = 1.0;
        }

        return Math.round(MB * multiplicadorPorActividad);
    };

    const calculateRestrictionsKcal = (dailyCaloricIntake, dietaryPreferences) => {
        if (dailyCaloricIntake === 0) {
            return {
                fats: {
                    total: 0,
                    sat: 0,
                    trans: 0
                },
                sugars: 0
            };
        } else {
            const lowerCaseDietaryPreferences = dietaryPreferences.map(pref => pref.toLowerCase()); // Convertir a minúsculas
            const restrictions = {
                fats: {
                    total: Math.round(dailyCaloricIntake * 0.3), // 30% de las calorías totales provienen de las grasas
                    sat: Math.round(dailyCaloricIntake * 0.1 ), // 10% de las calorías totales provienen de grasas saturadas
                    trans: Math.round(dailyCaloricIntake * 0.01) // 1% de las calorías totales provienen de grasas trans
                },
                sugars: Math.round(dailyCaloricIntake * 0.1) // 10% de las calorías totales provienen de azúcares
            };
    
            if (lowerCaseDietaryPreferences.includes('diabetes')) {
                restrictions.sugars = 0;
            }
    
            return restrictions;
        }
    };

    const calculateRestrictionsGrams = (dailyCaloricIntake, dietaryPreferences) => {
        if (dailyCaloricIntake === 0){
            return {
                fats: {
                    total: 0,
                    sat: 0,
                    trans: 0
                },
                sugars: 0,
                sodium: 0,
                salt: 0,
                potassium: 0
            };
        } else {

            const lowerCaseDietaryPreferences = dietaryPreferences.map(pref => pref.toLowerCase()); // Convertir a minúsculas
            const restrictions = {
                fats: {
                    total: Math.round(dailyCaloricIntake * 0.3 / 9), // Cada gramo de grasa tiene 9 calorías
                    sat: Math.round(dailyCaloricIntake * 0.1 / 9), 
                    trans: Math.round(dailyCaloricIntake * 0.01 / 9)
                },
                sugars: Math.round(dailyCaloricIntake * 0.1 / 4), // Cada gramo de azúcar tiene 4 calorías
                sodium: 2,
                salt: 5,
                potassium: 3.5
            };

            if (lowerCaseDietaryPreferences.includes('diabetes')) {
                restrictions.sugars = 0;
            }

            if (lowerCaseDietaryPreferences.includes('hipertensión')) {
                restrictions.salt = 0;
                restrictions.sodium = 0;
            }

            return restrictions;
        }
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const dietary_Preferences = dietaryPreferences && dietaryPreferences.length > 0 ? dietaryPreferences.split(',').map(pref => pref.trim()) : [];
            const dailyCaloricIntake = calculateDailyCaloricIntake(gender, parseInt(age) || 0, parseFloat(height) || 0.0, parseFloat(weight) || 0.0, parseInt(activityLevel) || 0);
            const restrictionsKcal = calculateRestrictionsKcal(dailyCaloricIntake, dietary_Preferences);
            const restrictionsGrams = calculateRestrictionsGrams(dailyCaloricIntake, dietary_Preferences);

            const response = await axios.post('http://localhost:8000/auth/register', {
                name,
                email,
                password,
                gender: gender || '', // Opcional pero debe ser una cadena
                age: age ? parseInt(age) : 0, // Opcional pero debe ser un entero
                height: height ? parseFloat(height) : 0.0, // Opcional pero debe ser un flotante
                weight: weight ? parseFloat(weight) : 0.0, // Opcional pero debe ser un flotante
                activity_level: activityLevel ? parseInt(activityLevel) : 0,
                daily_caloric_intake: dailyCaloricIntake,
                restrictions_kcal: restrictionsKcal,
                restrictions_grams: restrictionsGrams,
                dietary_preferences: dietary_Preferences,
                role: 'user', // Valor por defecto
                diets: [] // Lista vacía por defecto
            });
            console.log(response.data);
            navigate('/login');
        } catch (error) {
            console.error('Error en el registro:', error.response ? error.response.data : error.message);
        }
    };
    
    return (
        <div>
            <h1>Registro</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nombre"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Correo electrónico"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                >
                    <option value="">Seleccione su género</option>
                    <option value="Hombre">Hombre</option>
                    <option value="Mujer">Mujer</option>
                </select>
                <input
                    type="number"
                    placeholder="Edad"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Altura (cm)"
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Peso (kg)"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                />
                <select
                    value={activityLevel}
                    onChange={(e) => setActivityLevel(e.target.value)}
                >
                    <option value="">Seleccione su nivel de actividad</option>
                    <option value="1">1 - No muy activo. Actividad predominantemente sedentaria, con poca actividad física.</option>
                    <option value="2">2 - Medianamente activo. Participación ocasional en actividades que requieren estar de pie o movimientos ligeros.</option>
                    <option value="3">3 - Activo. Involucrado en actividades que incluyen caminar o realizar tareas domésticas regulares.</option>
                    <option value="4">4 - Muy activo. Participación en actividades físicas intensas, como deportes o trabajo físico.</option>
                </select>
                <input
                    type="text"
                    placeholder="Preferencias dietéticas (separadas por comas)"
                    value={dietaryPreferences}
                    onChange={(e) => setDietaryPreferences(e.target.value)}
                />
                <button type="submit">Registrarse</button>
            </form>
        </div>
    );
}

export default Register;
