// NewPage.js
import React from 'react';
import { Container, Typography, Button } from '@mui/material';

const ImportPage = () => {
  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        New Page
      </Typography>
      <Typography variant="body1" component="p">
        This is a new page created with MUI.
      </Typography>
      <Button variant="contained" color="primary">
        A Button
      </Button>
    </Container>
  );
};

export default ImportPage;
