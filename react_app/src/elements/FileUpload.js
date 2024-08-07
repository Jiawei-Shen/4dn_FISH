import React, { useState } from 'react';

const FileUpload = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);

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
    } else {
      alert('Please select a file first');
    }
  };

  return (
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
        Upload
      </button>
    </div>
  );
};

export default FileUpload;
