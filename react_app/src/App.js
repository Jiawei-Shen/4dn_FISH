import React, { useState } from 'react';
import './App.css';
import Button from './elements/Button';
import Slider from './elements/Slider';
import SmallTextBox from './elements/SmallTextBox';
import TextBox from './elements/TextBox';
import Dropdown from './elements/Dropdown';

function App() {
  const query_options = ['Change Query Option', 'Spot_ID', 'Chrom Start', 'Trace_ID', 'Cell_ID'];
  const chromosome_options = ['Select Option', 'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'X', 'Y']
  const [selectedOption, setSelectedOption] = useState(query_options[0]);
  const [textValue, setTextValue] = useState('');
  const [startValue, setStartValue] = useState('');
  const [endValue, setEndValue] = useState('');
  const [queryResult, setQueryResult] = useState(''); // New state variable for query result
  const [dropdownValue, setDropdownValue] = useState('');

  // Handle text change for TextBox component
  const handleTextChange = (value) => {
    setTextValue(value); // Update text value state
    console.log(`Text entered: ${value}`); // Debug: log entered text
  };

  // Handle change for start range in SmallTextBox
  const handleStartChange = (value) => {
    setStartValue(value); // Update start value state
  };

  // Handle change for end range in SmallTextBox
  const handleEndChange = (value) => {
    setEndValue(value); // Update end value state
  };

  // Handle change for slider value
  const handleSliderChange = (value) => {
    console.log(`Slider value: ${value}`); // Debug: log slider value
  };

  // Handle change for dropdown selection
  const handleDropdownChange = (value) => {
    setSelectedOption(value); // Update selected option state
    console.log(`Selected option: ${value}`); // Debug: log selected option
  };

  const handleChromDropdownChange = (value) => {
    setDropdownValue(value);
  }

  // Perform action based on selected dropdown option
  const handleQuery = () => {
    let result = '';
    switch (selectedOption) {
      case 'Spot_ID':
        if (startValue === '' || endValue === '') {
          alert('Please enter a value for both boxes');
        } else if (!isNaN(startValue) && !isNaN(endValue)) {
          result = `Spot_ID [${startValue}, ${endValue}]`;
        } else {
          alert('Only integers are accepted');
        }
        break;
      case 'Chrom Start':
        if (startValue === '' || endValue === '') {
          alert('Please enter a value for both boxes');
        } else if (!isNaN(startValue) && !isNaN(endValue)) {
          result = `Chromosome Start [${startValue}, ${endValue}]`;
        } else {
          alert('Only integers are accepted');
        }
        break;
      case 'Trace_ID':
        if (textValue === '') {
          alert('Please enter a value');
        } else if (!isNaN(textValue)) {
          result = `Trace_ID ${textValue}`;
        } else {
          alert('Only integers are accepted');
        }
        break;
      case 'Cell_ID':
        if (textValue === '') {
          alert('Please enter a value');
        } else if (!isNaN(textValue)) {
          result = `Cell_ID ${textValue}`;
        } else {
          alert('Only integers are accepted');
        }
        break;
      default:
        alert('No option selected');
    }
    if (result === '') {
      setQueryResult();
    }
    else {
      setQueryResult(result);
    }
    if (dropdownValue === 'Select Option') {
      setDropdownValue();
    }
    else {
      setDropdownValue(dropdownValue);
    }
  };

  return (
    <div className="App">
      <div className="left-column">
        <div className="scrollable-content">
          <h2>Functions</h2>

          {/* Dropdown menu for selecting options */}
          <h3>Chromosome</h3>
          <Dropdown options={chromosome_options} onChange={handleChromDropdownChange} />
          <h3>Query</h3>
          <Dropdown options={query_options} onChange={handleDropdownChange} />

          {/* Conditional rendering based on selected option */}
          {selectedOption === 'Spot_ID' && (
            <div className="spot_id">
              <SmallTextBox
                placeholder="0"
                onChange={handleStartChange} // Handle start value directly
              />
              <p> to </p>
              <SmallTextBox
                placeholder="100"
                onChange={handleEndChange} // Handle end value directly
              />
            </div>
          )}

          {selectedOption === 'Chrom Start' && (
            <div className="chrom-start-end">
              <SmallTextBox
                placeholder="0"
                onChange={handleStartChange} // Handle start value directly
              />
              <p> to </p>
              <SmallTextBox
                placeholder="100"
                onChange={handleEndChange} // Handle end value directly
              />
            </div>
          )}

          {selectedOption === 'Trace_ID' && (
            <TextBox
              placeholder="Enter Trace ID"
              onChange={handleTextChange} // Handle text change with value
            />
          )}

          {selectedOption === 'Cell_ID' && (
            <TextBox
              placeholder="Enter Cell ID"
              onChange={handleTextChange} // Handle text change with value
            />
          )}

          {/* Button to trigger query action */}
          <Button
            text="Query"
            color="#fff"
            backgroundColor="#800080"
            onClick={handleQuery}
          />

          {/* Slider component */}
          <Slider
            min={0}
            max={100}
            step={1}
            initialValue={50}
            onChange={handleSliderChange}
          />
        </div>
      </div>

      <div className="main-content">
        <p>Querying {dropdownValue} using {queryResult}...</p> {/* Display query result */}
        <div className="header">
          <h1>Welcome to My React App</h1>
        </div>

        {/* Example buttons with different colors */}
        <Button
          text="Red Button"
          color="#fff"
          backgroundColor="#ff0000"
          onClick={() => alert('Red Button clicked!')}
        />
        <Button
          text="Green Button"
          color="#fff"
          backgroundColor="#00ff00"
          onClick={() => alert('Green Button clicked!')}
        />
        <Button
          text="Blue Button"
          color="#fff"
          backgroundColor="#0000ff"
          onClick={() => alert('Blue Button clicked!')}
        />
      </div>
    </div>
  );
}

export default App;
