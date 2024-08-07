// NewPage.js
import React from 'react';
import { Container, Typography, Button } from '@mui/material';
import FileUpload from './elements/FileUpload';

const ImportPage = () => {

  const handleFileSelect = (file) => {
    console.log('Selected file:', file);
    // You can handle the file here (e.g., display it, upload it to the server, etc.)
  };

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Upload Your Compressed File
      </Typography>
      <FileUpload onFileSelect={handleFileSelect} />
      <Typography variant="body1" component="p">
        Note: only .fish styled file formats are allowed
      </Typography>
    </Container>
  );
};

export default ImportPage;
