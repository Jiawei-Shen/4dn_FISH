
import React from 'react';
import Plot from 'react-plotly.js';

function getrandom(num , mul) 
	{
   var value = [ ];
   for(let i=0;i<=num;i++)
   {
    var rand = Math.random() * mul;
    value.push(rand);
   }
   return value;
  }

var data=[
    {
     name: 'chr1',
     opacity:0.4,
     type: 'scatter3d',
     x: getrandom(5 , 125),
     y: getrandom(5 , 125),
     z: getrandom(5 , 125),
    },
    {
     name: 'chr2',
     opacity:0.5,
     type: 'scatter3d',
     x: getrandom(5 , 125),
     y: getrandom(50 , 75),
     z: getrandom(50 , 75),
    },
  	{
     name: 'chr3',
     opacity:0.5,
     type: 'scatter3d',
     x: getrandom(50 , 100),
     y: getrandom(50 , 100),
     z: getrandom(50 , 100),
    }
];

var layout = {
  scene:{
   aspectratio: {
     x: 1, y: 1, z: 1,
    },
   xaxis: {
    nticks: 10,
    range: [0, 150],
  },
   yaxis: {
    nticks: 10,
    range: [0, 150],
  },
   zaxis: {
   nticks: 10,
   range: [0, 150],
  }},
  aspectmode: "cube",
  autosize: false,
  width: 700,
  height: 600,
  margin: {
    l: 0,
	r: 0,
	b: 50,
	t: 50,
	pad: 4
  },
};


const MyPlot = () => {
    return (
      <Plot
        data = {data}
        layout={layout}
      />
    );
  };
  
  export default MyPlot;
  