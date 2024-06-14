import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../Auth';
import '../App.css';

const Navigation = () => {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <div id="menu">
      <nav>
        <ul>
          <li><Link to="/recetas">Recetas</Link></li>
          {isAuthenticated ? (
            <>
              <li><Link to="/dietas">Dietas</Link></li>
              <li><Link to="/perfil">Perfil</Link></li>
              <li><Link to="/logout">Logout</Link></li>
            </>
          ) : (
            <>
              <li><Link to="/login">Login</Link></li>            
            </>
          )}
        </ul>
      </nav>
    </div>
  );
};

export default Navigation;