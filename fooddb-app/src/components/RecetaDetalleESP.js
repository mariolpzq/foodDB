import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import AuthContext from '../Auth';

function RecetaDetalleESP() {
  const { isAuthenticated } = useContext(AuthContext);
  const { id } = useParams();
  const [receta, setReceta] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchReceta = async () => {
      try {
        const token = localStorage.getItem('token');
        let response;

        response = await axios.get(`http://localhost:8000/recetas/abuela/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true 
        });
      
        setReceta(response.data);
      } catch (error) {
        console.error('Error al obtener la receta:', error);
      }
    };

    fetchReceta();
  }, [id, user]);


  const eliminarComillas = (string) => {
    return string.replace(/['"]+/g, '');
  };

  const formatOrigin_ISO = (origin_ISO) => {
    switch (origin_ISO) {
        case 'PAN':
            return 'Panamá';
        case 'ARG':
            return 'Argentina';
        case 'VEN':
            return 'Venezuela';
        case 'URY':
            return 'Uruguay';
        case 'SLV':
            return 'El Salvador';
        case 'PRI':
            return 'Puerto Rico';
        case 'CHL':
            return 'Chile';
        case 'CRI':
            return 'Costa Rica';
        case 'NIC':
            return 'Nicaragua';
        case 'MEX':
            return 'México';
        case 'DOM':
            return 'República Dominicana';
        case 'HND':
            return 'Honduras';
        case 'COL':
            return 'Colombia';
        case 'ESP':
            return 'España';
        case 'GTM':
            return 'Guatemala';
        case 'PER':
            return 'Perú';
        case 'PRY':
            return 'Paraguay';
        case 'ECU':
            return 'Ecuador';
        case 'BOL':
            return 'Bolivia';
        case 'CUB':
            return 'Cuba';
        default:
            return origin_ISO;
      }
  };

  const primeraLetraMayúscula = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

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
    'Alto contenido de fibra'
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
  
  const renderDietaryPreferences = (qualities) => {
    if (!qualities) {
      return <p>No disponible</p>;
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



  if (!receta) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    return (
    <div id='enlace-registro'>
       <p>No estás autenticado. Por favor, <Link to="/login">inicia sesión</Link></p>
    </div>);
  }


  return (
    <div className="cell receta-detalles">

      <h1 id='titulo-receta'>{primeraLetraMayúscula(receta.title)}</h1>
      {user && user.role !== "user" && receta.source && <p><strong>Fuente:</strong> {receta.source}</p>}
      {receta.language && <p><strong>Idioma:</strong> {receta.language}</p>}
      {receta.n_diners && <p><strong>Número de comensales:</strong> {receta.n_diners}</p>}
      {receta.origin_ISO && <p><strong>País de origen:</strong> {formatOrigin_ISO(receta.origin_ISO)}</p>}
      {receta.difficulty && <p><strong>Dificultad:</strong> {receta.difficulty}</p>}
      {receta.category && <p><strong>Categoría:</strong> {primeraLetraMayúscula(receta.category)}</p>}
      {receta.subcategory && <p><strong>Subcategoría:</strong> {receta.subcategory.map((subcat, index) => ( <span key={index}>{primeraLetraMayúscula(subcat)}</span>))}</p>}
      {receta.minutes && <p><strong>Tiempo de preparación:</strong> {receta.minutes} m</p>}
      

      <h3><strong>Información nutricional</strong></h3>
        {receta.dietary_preferences && (
          <div>
              {renderDietaryPreferences(receta.dietary_preferences)}
          </div>
        )}
  
    

      <h3><strong>Ingredientes</strong></h3>
      {receta.ingredients && (
        <div className='listado-ingredientes'>
          <ul>
            {receta.ingredients.map((ing, index) => (
              <li key={index}>
                {ing.ingredientID ? (
                    <Link to={`/ingrediente/${ing.ingredientID}`}>{eliminarComillas(ing.ingredient)}</Link>
                ) : (
                  <span>{ing.ingredient}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      <h3><strong>Instrucciones de preparación</strong></h3>
      {receta.steps && (
        <div className='steps'>
          <ul>
            {receta.steps.map((step, index) => (
              <li key={index}><strong>{index+1}.</strong> {step}</li>
            ))}
          </ul>
        </div>
      )}
     
    </div>
  );
}

export default RecetaDetalleESP;
