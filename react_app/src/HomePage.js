import React, { useState } from 'react';
import './App.css';
import FunctionBar from './functionbar';
import Visualization from './visualization';

function App() {
  const [queryResult, setQueryResult] = useState(''); // State for query result
  const [filterResult, setFilterResult] = useState(''); // State for filter result
  const [dropdownValue, setDropdownValue] = useState(''); // State for chromosome

  // Function to update query result
  const handleQueryResult = (result) => {
    setQueryResult(result);
  };

  // Function to update filter result
  const handleFilterResult = (result) => {
    setFilterResult(result);
  };

  // Function to update dropdown value
  const handleDropdownValueChange = (value) => {
    setDropdownValue(value);
  };

  return (
    <div className="App">
      <FunctionBar
        onQueryResult={handleQueryResult}
        onFilterResult={handleFilterResult}
        onDropdownValueChange={handleDropdownValueChange}
      />
      <Visualization
        queryResult={queryResult}
        filterResult={filterResult}
        dropdownValue={dropdownValue}
      />
    </div>
  );
}

export default App;
