import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../Auth';
import '../App.css';

const Navigation = () => {
  const { isAuthenticated, user } = useContext(AuthContext);

  if(user){
    var languages = user.preferences.languages;
  }
    

  if (user && languages.length === 1 && languages[0] === 'EN') {

    return (
      <div id="menu">
        <nav>
          <ul>
            {isAuthenticated ? (
              <>
                <li><Link to="/recetas">Recipes</Link></li>
                <li><Link to="/dietas">Diets</Link></li>
                <li><Link to="/perfil">Profile</Link></li>
                <li><Link to="/logout">Logout</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/register">Register</Link></li>
                <li><Link to="/login">Login</Link></li>
              </>
            )}
          </ul>
        </nav>
      </div>
    );

  }

  else {

    return (
      <div id="menu">
        <nav>
          <ul>
            
            {isAuthenticated ? (
              <>
                <li><Link to="/recetas">Recetas</Link></li>
                <li><Link to="/dietas">Dietas</Link></li>
                <li><Link to="/perfil">Perfil</Link></li>
                <li><Link to="/logout">Logout</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/register">Registro</Link></li>
                <li><Link to="/login">Login</Link></li>            
              </>
            )}
          </ul>
        </nav>
      </div>
    );

  };

};


export default Navigation;