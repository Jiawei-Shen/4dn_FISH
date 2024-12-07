import React, { useState } from 'react';
import TextBox from './TextBox';

const FileUpload = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [textValue, setTextValue] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.csv')) {  // change to .fish
      setSelectedFile(file);
      if (onFileSelect) {
        onFileSelect(file);
      }
    } else {
      alert('Please select a .fish file');
    }
  };

  const handleUploadClick = () => {
    if (selectedFile) {
      console.log('File uploaded:', selectedFile);
    }
    else {
      alert('Please select a file first');
    }
  };

  const handleTextChange = (value) => {
    setTextValue(value)
  };

  const handleTextUploadClick = () => {
    if (textValue) {
        console.log('Text entered: ', textValue);
    }
    else {
        alert('Please input some text first')
  }
  };

  return (
    <div>
    <div>
      <h2>Upload a file</h2>
      <input
        type="file"
        onChange={handleFileChange}
        accept=".csv" // should be .fish, i put .csv for testing
      />
      {selectedFile && (
        <p>Selected file: {selectedFile.name}</p>
      )}
      <button onClick={handleUploadClick} style={{ marginTop: '10px', color: 'ffffff', backgroundColor: '#1876d2' }}>
        Upload File
      </button>
      <p> Note: only .fish styled file formats are allowed</p>
    </div>
    <div>
      <h2>Upload Path</h2>
      <TextBox placeholder='/Users/johndoe/file_path' onChange={handleTextChange}></TextBox>
      <button onClick={handleTextUploadClick} style={{ marginTop: '10px', color: 'ffffff', backgroundColor: '#1876d2'}}>
        Upload Path
      </button>
      <p> Note: Please only enter a valid path to a file on your computer</p>
    </div>
    </div>
  );
};

export default FileUpload;
