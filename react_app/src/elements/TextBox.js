import React from 'react';
import './TextBox.css';

const TextBox = ({ placeholder, onChange }) => {
  const handleChange = (e) => {
    // Pass the value from the event to the onChange handler
    onChange(e.target.value);
  };

  return (
    <input
      type="text"
      placeholder={placeholder}
      onChange={handleChange}
      className="text-box"
    />
  );
};

export default TextBox;
