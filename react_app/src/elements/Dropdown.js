import React, { useState } from 'react';
import './Dropdown.css';

const Dropdown = ({ options, onChange }) => {
  const [selectedOption, setSelectedOption] = useState(options[0]);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setSelectedOption(newValue);
    onChange(newValue);
  };

  return (
    <select value={selectedOption} onChange={handleChange} className="dropdown">
      {options.map((option, index) => (
        <option key={index} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
