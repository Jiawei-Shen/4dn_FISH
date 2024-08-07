import React, { useState } from 'react';
import Button from './elements/Button';
import SmallTextBox from './elements/SmallTextBox';
import TextBox from './elements/TextBox';
import Dropdown from './elements/Dropdown';

const FunctionBar = ({ onQueryResult, onDropdownValueChange, onFilterResult }) => {
  const query_options = ['Change Query Option', 'Spot_ID', 'Chrom Start', 'Trace_ID', 'Cell_ID'];
  const chromosome_options = ['Select Option', 'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'X', 'Y'];
  const [selectedOption, setSelectedOption] = useState(query_options[0]);
  const [textValue, setTextValue] = useState('');
  const [startValue, setStartValue] = useState('');
  const [endValue, setEndValue] = useState('');
  const [queryResult, setQueryResult] = useState('');
  const [dropdownValue, setDropdownValue] = useState('');

  const handleTextChange = (value) => {
    setTextValue(value);
  };

  const handleStartChange = (value) => {
    setStartValue(value);
  };

  const handleEndChange = (value) => {
    setEndValue(value);
  };

  const handleSliderChange = (value) => {
    console.log(`Slider value: ${value}`);
  };

  const handleDropdownChange = (value) => {
    setSelectedOption(value);
  };

  const handleChromDropdownChange = (value) => {
    setDropdownValue(value);
  };

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
    setQueryResult(result);
  };

  const handleFilter = () => {
    let filterResult = '';
    if (startValue === '' || endValue === '') {
      alert('Please enter a value for both boxes');
    } else if (!isNaN(startValue) && !isNaN(endValue)) {
      filterResult = `Filter Range [${startValue}, ${endValue}]`;
    } else {
      alert('Only integers are accepted');
    }
  };

  return (
    <div className="left-column">
      <div className="scrollable-content">
        <h2>Functions</h2>
        <h3>Chromosome</h3>
        <Dropdown options={chromosome_options} onChange={handleChromDropdownChange} />
        <h3>Query</h3>
        <Dropdown options={query_options} onChange={handleDropdownChange} />

        {selectedOption === 'Spot_ID' && (
          <div className="spot_id">
            <SmallTextBox placeholder="0" onChange={handleStartChange} />
            <p> to </p>
            <SmallTextBox placeholder="100" onChange={handleEndChange} />
          </div>
        )}

        {selectedOption === 'Chrom Start' && (
          <div className="chrom-start-end">
            <SmallTextBox placeholder="0" onChange={handleStartChange} />
            <p> to </p>
            <SmallTextBox placeholder="100" onChange={handleEndChange} />
          </div>
        )}

        {selectedOption === 'Trace_ID' && (
          <TextBox placeholder="Enter Trace ID" onChange={handleTextChange} />
        )}

        {selectedOption === 'Cell_ID' && (
          <TextBox placeholder="Enter Cell ID" onChange={handleTextChange} />
        )}

        <Button text="Query" color="#fff" backgroundColor="#800080" onClick={handleQuery} />
        <h3>Filter</h3>
        <div className="filter_range">
          <SmallTextBox placeholder="0" onChange={handleStartChange} />
          <p> to </p>
          <SmallTextBox placeholder="1000000" onChange={handleEndChange} />
        </div>
        <Button text="Filter" color="#fff" backgroundColor="#6495ED" onClick={handleFilter} />
      </div>
    </div>
  );
};

export default FunctionBar;
