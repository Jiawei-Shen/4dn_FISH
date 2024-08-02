import React, { useState } from 'react';
import './Slider.css';

const Slider = ({ min, max, step, initialValue, onChange }) => {
  const [value, setValue] = useState(initialValue);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
    onChange(newValue);
  };

  return (
    <div className="slider-container">
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        className="slider"
      />
      <span className="slider-value">{value}</span>
    </div>
  );
};

export default Slider;
