// src/Button.js

import React from 'react';
import './Button.css';

const Button = ({ text, color, backgroundColor, onClick }) => {
  return (
    <button
      className="custom-button"
      style={{ color, backgroundColor }}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default Button;
