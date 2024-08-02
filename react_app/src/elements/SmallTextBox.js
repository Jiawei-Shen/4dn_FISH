import React, { useState } from 'react';
import './SmallTextBox.css';

const SmallTextBox = ({ placeholder, onChange }) => {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    const newValue = e.target.value;
    setText(newValue);
    onChange(newValue); // Pass only the new value
  };

  return (
    <input
      type="text"
      value={text}
      placeholder={placeholder}
      onChange={handleChange}
      className="small-text-box"
    />
  );
};

export default SmallTextBox;
