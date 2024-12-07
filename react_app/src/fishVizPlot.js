
import React from 'react';
import Plot from 'react-plotly.js';

function getrandom(num , mul) // takes in the number of dots you want, and the range of the data(0*mul,1*mul)
	{
   var value = [ ];
   for(let i=0;i<=num;i++)
   {
    var rand = Math.random() * mul;
    value.push(rand);
   }
   return value;  // Returns a LIST
  }

var data=[
    {
     name: 'trace 1',
     opacity:0.4,
     type: 'scatter3d',
     x: getrandom(100 , 1000000),
     y: getrandom(100 , 1000000),
     z: getrandom(100 , 1000000),
    },
    {
     name: 'trace 2',
     opacity:0.5,
     type: 'scatter3d',
     x: getrandom(100 , 1000000),
     y: getrandom(100 , 1000000),
     z: getrandom(100 , 1000000),
    },
  	{
     name: 'trace 3',
     opacity:0.5,
     type: 'scatter3d',
     x: getrandom(100 , 1000000),
     y: getrandom(100 , 1000000),
     z: getrandom(100 , 1000000),
    }
];

var layout = {
  scene:{
   xaxis: {
    nticks: 10,
    range: [0, 1000000], // 1000000
  },
   yaxis: {
    nticks: 10,
    range: [0, 1000000],
  },
   zaxis: {
   nticks: 10,
   range: [0, 1000000],
  }},
  aspectmode: "cube",
  autosize: false,
  width: 700,
  height: 600,
  margin: {
    l: 0,
	  r: 0,
	  b: 10,
	  t: 10,
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
  