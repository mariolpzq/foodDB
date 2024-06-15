import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const CreateDieta = () => {
    const [recetas, setRecetas] = useState([]);
    const [searchTerm] = useState('');
    const [appetizerSearch, setAppetizerSearch] = useState('');
    const [mainDishSearch, setMainDishSearch] = useState('');
    const [dessertSearch, setDessertSearch] = useState('');
    const [selectedRecipes, setSelectedRecipes] = useState({
        appetizerID: '',
        main_dishID: '',
        dessertID: ''
    });

    const [selectedRecipeDetails, setSelectedRecipeDetails] = useState({
        appetizer: null,
        main_dish: null,
        dessert: null
    });

    const navigate = useNavigate();

    useEffect(() => {
        const fetchRecetas = async () => {
            try {
                const response = await axios.get('http://localhost:8000/recetas/mealrec');
                setRecetas(response.data.recetas);
            } catch (error) {
                console.error('Error al obtener las recetas:', error);
            }
        };

        fetchRecetas();
    }, []);

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

    const filterRecetas = (recetas, categorySearch) => {
        return recetas.filter(receta =>
            receta.category === categorySearch &&
            receta.title.toLowerCase().includes(searchTerm.toLowerCase())
        );
    };

    const handleSelectRecipe = (categoryID, categoryTitle, recipe) => {
        setSelectedRecipes({
            ...selectedRecipes,
            [categoryID]: recipe.id
        });
        setSelectedRecipeDetails({
            ...selectedRecipeDetails,
            [categoryTitle]: recipe
        });
    };

    const handleCreateDiet = async () => {
        try {
            const token = localStorage.getItem('token');
            if (token) {
                console.log('selectedRecipes:', selectedRecipes);
                await axios.post('http://localhost:8000/dietas', selectedRecipes, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                navigate('/dietas');
            }
        } catch (error) {
            console.error('Error al crear la dieta:', error);
        }
    };

    const appetizers = filterRecetas(recetas, 'appetizer').filter(receta =>
        receta.title.toLowerCase().includes(appetizerSearch.toLowerCase())
    );
    const mainDishes = filterRecetas(recetas, 'main-dish').filter(receta =>
        receta.title.toLowerCase().includes(mainDishSearch.toLowerCase())
    );
    const desserts = filterRecetas(recetas, 'dessert').filter(receta =>
        receta.title.toLowerCase().includes(dessertSearch.toLowerCase())
    );

    return (
        <div>
            <h1>Crear una nueva dieta</h1>
            <div className='diet-item'>
                <div className="dish-row selected-recipes">
                    <div className="dish selected-recipe">
                        <p><strong>Entrante:</strong></p>
                        <p>{selectedRecipeDetails.appetizer?.title || 'Selecciona un entrante'}</p>
                        <div>{renderOMS_Lights(selectedRecipeDetails.appetizer?.OMS_lights_per100g)}</div>
                    </div>
                    <div className="dish selected-recipe">
                        <p><strong>Plato principal:</strong></p>
                        <p>{selectedRecipeDetails.main_dish?.title || 'Selecciona un plato principal'}</p>
                        <div>{renderOMS_Lights(selectedRecipeDetails.main_dish?.OMS_lights_per100g)}</div>
                    </div>
                    <div className="dish selected-recipe">
                        <p><strong>Postre:</strong></p>
                        <p>{selectedRecipeDetails.dessert?.title || 'Selecciona un postre'}</p>
                        <div>{renderOMS_Lights(selectedRecipeDetails.dessert?.OMS_lights_per100g)}</div>
                    </div>
                </div>
            </div>

            <button className="new-dieta-btn" onClick={handleCreateDiet}>Crear dieta</button>
            <div className="recetas-container">
                <div className="column">
                    <h2>Entrantes</h2>
                    <div className="individual-search-bar">
                        <input
                            type="text"
                            placeholder="Buscar entrantes..."
                            value={appetizerSearch}
                            onChange={(e) => setAppetizerSearch(e.target.value)}
                        />
                    </div>
                    <ul>
                        {appetizers.map((receta) => (
                            <li key={receta.id} className="receta-item" onClick={() => handleSelectRecipe('appetizerID', 'appetizer', receta)}>
                                {receta.title}
                                <div className='oms-container-list'>
                                    <div>{renderOMS_Lights(receta.OMS_lights_per100g)}</div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="column">
                    <h2>Platos principales</h2>
                    <div className="individual-search-bar">
                        <input
                            type="text"
                            placeholder="Buscar platos principales..."
                            value={mainDishSearch}
                            onChange={(e) => setMainDishSearch(e.target.value)}
                        />
                    </div>
                    <ul>
                        {mainDishes.map((receta) => (
                            <li key={receta.id} className="receta-item" onClick={() => handleSelectRecipe('main_dishID', 'main_dish', receta)}>
                                {receta.title}
                                <div className='oms-container-list'>
                                    <div>{renderOMS_Lights(receta.OMS_lights_per100g)}</div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="column">
                    <h2>Postres</h2>
                    <div className="individual-search-bar">
                        <input
                            type="text"
                            placeholder="Buscar postres..."
                            value={dessertSearch}
                            onChange={(e) => setDessertSearch(e.target.value)}
                        />
                    </div>
                    <ul>
                        {desserts.map((receta) => (
                            <li key={receta.id} className="receta-item" onClick={() => handleSelectRecipe('dessertID', 'dessert', receta)}>
                                {receta.title}
                                <div className='oms-container-list'>
                                    <div>{renderOMS_Lights(receta.OMS_lights_per100g)}</div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default CreateDieta;
