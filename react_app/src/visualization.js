// src/components/Visualization.js
import React from 'react';
import MyPlot from './plotly3d';

const Visualization = () => {
  return (
    <div className="main-content">
      <div className="header">
        <h1>FISH React App</h1>
      </div>
      <MyPlot />
    </div>
  );
};

export default Visualization;
