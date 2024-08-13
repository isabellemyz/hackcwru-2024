import React from 'react';
import logo from '../assets/unnamed.jpg'

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <img src={logo} alt="Logo" />
      </div>
      <div className="header-title">
        Vocally
      </div>
      <div className="header-placeholder"></div>
    </header>
  );
};

export default Header;