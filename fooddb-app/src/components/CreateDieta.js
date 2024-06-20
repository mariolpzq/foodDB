import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import { useContext } from 'react';
import AuthContext from '../Auth';
import { Link } from 'react-router-dom';

const CreateDieta = () => {
  const { isAuthenticated, user } = useContext(AuthContext);
  const [recetas, setRecetas] = useState([]);
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

  const [nutrientCounts, setNutrientCounts] = useState({
    calories: 0,
    fat: 0,
    saturates: 0,
    salt: 0,
    sugar: 0
  });

  const navigate = useNavigate();

  const cualidadesBuenas = [
    'Buen contenido de fibra',
    'Bueno en grasas',
    'Bueno para el sodio',
    'Buena fuente de fibra',
    'Bueno fuente de fibra',
    'Sin sodio o sin sal',
    'Sin carbohidratos',
    'Bajo en grasas',
    'Sin azúcar añadida o sin azúcares agregadas',
    'Bueno fuente de proteínas',
    'Bueno para vegetarianos',
    'Bajo en azúcar',
    'Sin grasa',
    'Bueno para el corazón',
    'Sin grasas saturadas',
    'Sin colesterol',
    'Sin grasas trans',
    'Sin azúcar añadida',
    'Sin azúcar',
    'Alto en proteínas',
    'Sin sodio',
    'Sin calorías',
    'Sin gelatina',
    'Sin sal',
    'Alto en fibra',
    'Bajo en calorías',
    'Sin gluten',
    'Bajo en colesterol',
    'Sin lactosa',
    'Bajo en grasas saturadas',
    'Cero en calorías',
    'Bueno en fibra',
    'Sin harina',
    'Sin grasa saturada',
    'Buena fuente de fibra',
    'Bueno en proteínas',
    'Bajo en calorías',
    'Alto en vitamina C',
    'Bajo en carbohidratos',
    'Bajo en sodio',
    'Alto contenido de fibra',
    'Alto en vitaminas'
  ];
  
  const cualidadesMalas = [
    'Alto en azúcar',
    'Alto en calorías',
    'Alto en grasas',
    'Sin fibra',
    'Alto en colesterol',
    'Alto en azúcar añadida',
    'Alto en grasas reducidas o con menos grasas',
    'Alto en proteínas',
    'Alto en cafeina',
    'Alto en grasas saturadas',
    'Alto en alcohol',
    'Alto en calorías saturadas',
    'Alto en sodio',
    'Alto en vinagre',
    'Alto en azúcares añadidos'
  ];

  useEffect(() => {
    const fetchRecetas = async () => {
      if (user) {
        const languages = user.preferences.languages;
        const token = localStorage.getItem('token');
        if (token) {
          try {
            let allRecetas = [];

            if (languages.includes('EN')) {
              const englishResponse = await axios.get('http://localhost:8000/recetas/mealrec', {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              allRecetas = allRecetas.concat(englishResponse.data.recetas);
            }

            if (languages.includes('ES')) {
              if (user.preferences.cuisines && user.preferences.cuisines.length > 0) {
                const promises = user.preferences.cuisines.map((cuisine) =>
                  axios.get(`http://localhost:8000/recetas/abuela/pais/${cuisine}`, {
                    headers: {
                      'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                  })
                );
                const responses = await Promise.all(promises);
                const spanishRecetas = responses.flatMap(res => res.data.recetas);
                allRecetas = allRecetas.concat(spanishRecetas);
              } else {
                const spanishResponse = await axios.get('http://localhost:8000/recetas/abuela/', {
                  headers: {
                    'Authorization': `Bearer ${token}`
                  },
                  withCredentials: true
                });
                allRecetas = allRecetas.concat(spanishResponse.data.recetas);
              }
            }

            setRecetas(allRecetas);
          } catch (error) {
            console.error('Error al obtener las recetas:', error);
          }
        }
      }
    };

    fetchRecetas();
  }, [user]);

  useEffect(() => {
    const calculateNutrientCounts = () => {
      let fat = 0, saturates = 0, salt = 0, sugar = 0, calories = 0;
   
      const recipes = [selectedRecipeDetails.appetizer, selectedRecipeDetails.main_dish, selectedRecipeDetails.dessert];
   
      recipes.forEach(recipe => {
        if (recipe && recipe.nutritional_info_100g) {
          fat += recipe.nutritional_info_100g.fat || 0;
          saturates += recipe.nutritional_info_100g.sat || 0;
          salt += recipe.nutritional_info_100g.salt || 0;
          sugar += recipe.nutritional_info_100g.sug || 0;
          calories += recipe.nutritional_info_100g.energy || 0;
        }
      });
   
      setNutrientCounts({
        calories: { value: parseFloat(calories.toFixed(2)), exceeds: false },
        fat: { value: parseFloat(fat.toFixed(2)), exceeds: false },
        saturates: { value: parseFloat(saturates.toFixed(2)), exceeds: false },
        salt: { value: parseFloat(salt.toFixed(2)), exceeds: false },
        sugar: { value: parseFloat(sugar.toFixed(2)), exceeds: false }
      });
    };

    calculateNutrientCounts();
  }, [selectedRecipeDetails]);

  useEffect(() => {
    const checkRestrictions = () => {
      const restrictions = user.restrictions_grams;
      const dailyCaloricIntake = user.daily_caloric_intake;
  
      setNutrientCounts(prevCounts => {
        return {
          calories: { ...prevCounts.calories, exceeds: prevCounts.calories.value > dailyCaloricIntake },
          fat: { ...prevCounts.fat, exceeds: prevCounts.fat.value > restrictions.fats.total },
          saturates: { ...prevCounts.saturates, exceeds: prevCounts.saturates.value > restrictions.fats.sat },
          salt: { ...prevCounts.salt, exceeds: prevCounts.salt.value > restrictions.salt },
          sugar: { ...prevCounts.sugar, exceeds: prevCounts.sugar.value > restrictions.sugars }
        };
      });
    };
  
    checkRestrictions();
  }, [nutrientCounts, user]);

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

  const renderDietaryPreferences = (qualities) => {
    if (!qualities) {
      return <p>No disponible</p>;
    }

    for (let i = 0; i < qualities.length; i++) {
      qualities[i] = qualities[i].replace('.', '');
    }

    const getColor = (quality) => {

      if (cualidadesBuenas.includes(quality)) {
        return '#28a745'; // Verde
      } else if (cualidadesMalas.includes(quality)) {
        return '#dc3545'; // Rojo
      } else {
        return '#6c757d'; // Gris por defecto
      }
    };

    return qualities.map((quality, index) => (
      <div key={index} style={{
        backgroundColor: getColor(quality),
        borderRadius: '20px',
        padding: '5px 10px',
        color: '#fff',
        display: 'inline-block',
        marginRight: '10px',
        marginTop: '10px'
      }}>
        <strong>{quality}</strong>
      </div>
    ));
  };

  const filterRecetas = (recetas, categorySearch, searchTerm) => {
    const categories = {
      'appetizer': ['appetizer', 'entrante'],
      'main-dish': ['main-dish', 'plato principal'],
      'dessert': ['dessert', 'postre']
    };

    return recetas.filter(receta =>
      categories[categorySearch].includes(receta.category) &&
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

  const handleDeselectRecipe = (categoryID, categoryTitle) => {
    setSelectedRecipes({
      ...selectedRecipes,
      [categoryID]: ''
    });
    setSelectedRecipeDetails({
      ...selectedRecipeDetails,
      [categoryTitle]: null
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

  const primeraLetraMayúscula = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const appetizers = filterRecetas(recetas, 'appetizer', appetizerSearch);
  const mainDishes = filterRecetas(recetas, 'main-dish', mainDishSearch);
  const desserts = filterRecetas(recetas, 'dessert', dessertSearch);

  if (!isAuthenticated) {
    return (
    <div id='enlace-registro'>
       <p>No estás autenticado. Por favor, <Link to="/login">inicia sesión</Link></p>
    </div>);
  }

  return (
    <div>
      <h1>Crear una nueva dieta</h1>
      <div className='diet-item'>
        <div className="dish-row selected-recipes">
          <div className="create-dish selected-recipe">
            <p><strong>Entrante:</strong></p>
            <p>{selectedRecipeDetails.appetizer?.title || 'Selecciona un entrante'}</p>
            <div>{selectedRecipeDetails.appetizer?.source === 'MealREC'
              ? renderOMS_Lights(selectedRecipeDetails.appetizer?.OMS_lights_per100g)
              : renderDietaryPreferences(selectedRecipeDetails.appetizer?.dietary_preferences)
            }</div>
            {selectedRecipeDetails.appetizer && (
              <button className="delete-button" onClick={() => handleDeselectRecipe('appetizerID', 'appetizer')}>
                ✕
              </button>
            )}
          </div>
          <div className="create-dish selected-recipe">
            <p><strong>Plato principal:</strong></p>
            <p>{selectedRecipeDetails.main_dish?.title || 'Selecciona un plato principal'}</p>
            <div>{selectedRecipeDetails.main_dish?.source === 'MealREC'
              ? renderOMS_Lights(selectedRecipeDetails.main_dish?.OMS_lights_per100g)
              : renderDietaryPreferences(selectedRecipeDetails.main_dish?.dietary_preferences)
            }</div>
            {selectedRecipeDetails.main_dish && (
              <button className="delete-button" onClick={() => handleDeselectRecipe('main_dishID', 'main_dish')}>
                ✕
              </button>
            )}
          </div>
          <div className="create-dish selected-recipe">
            <p><strong>Postre:</strong></p>
            <p>{selectedRecipeDetails.dessert?.title || 'Selecciona un postre'}</p>
            <div>{selectedRecipeDetails.dessert?.source === 'MealREC'
              ? renderOMS_Lights(selectedRecipeDetails.dessert?.OMS_lights_per100g)
              : renderDietaryPreferences(selectedRecipeDetails.dessert?.dietary_preferences)
            }</div>
            {selectedRecipeDetails.dessert && (
              <button className="delete-button" onClick={() => handleDeselectRecipe('dessertID', 'dessert')}>
                ✕
              </button>
            )}
          </div>
        </div>
      </div>

      <button className="new-dieta-btn" onClick={handleCreateDiet}>Crear dieta</button>

      {user.preferences.languages.length === 1 && user.preferences.languages[0] === 'EN' && (
        <div className="nutrient-counter">
          <h3>Contador de nutrientes seleccionados</h3>
          <p className={nutrientCounts.calories.exceeds ? 'exceeds-limit' : ''}>
            <strong>Calorías:</strong> {nutrientCounts.calories.value} kcal
          </p>
          <p className={nutrientCounts.fat.exceeds ? 'exceeds-limit' : ''}>
            <strong>Grasas:</strong> {nutrientCounts.fat.value} g
          </p>
          <p className={nutrientCounts.saturates.exceeds ? 'exceeds-limit' : ''}>
            <strong>Grasas saturadas:</strong> {nutrientCounts.saturates.value} g
          </p>
          <p className={nutrientCounts.sugar.exceeds ? 'exceeds-limit' : ''}>
            <strong>Azúcares:</strong> {nutrientCounts.sugar.value} g
          </p>
          <p className={nutrientCounts.salt.exceeds ? 'exceeds-limit' : ''}>
            <strong>Sal:</strong> {nutrientCounts.salt.value} g
          </p>
        </div>
      )}

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
                {primeraLetraMayúscula(receta.title)}
                <div className='oms-container-list'>
                  <div>{receta.source === 'MealREC'
                    ? renderOMS_Lights(receta.OMS_lights_per100g)
                    : renderDietaryPreferences(receta.dietary_preferences)
                  }</div>
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
                {primeraLetraMayúscula(receta.title)}
                <div className='oms-container-list'>
                  <div>{receta.source === 'MealREC'
                    ? renderOMS_Lights(receta.OMS_lights_per100g)
                    : renderDietaryPreferences(receta.dietary_preferences)
                  }</div>
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
                {primeraLetraMayúscula(receta.title)}
                <div className='oms-container-list'>
                  <div>{receta.source === 'MealREC'
                    ? renderOMS_Lights(receta.OMS_lights_per100g)
                    : renderDietaryPreferences(receta.dietary_preferences)
                  }</div>
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
