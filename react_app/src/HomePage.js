import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import FunctionBar from './functionbar';
import Visualization from './visualization';

const HomePage = () => {
  return (
    <Container sx={{ maxWidth: '90vw', paddingLeft: 0, paddingRight: 0 }}>
      <Box display="flex" justifyContent="space-between" mt={4}>
        <Box flex={1} maxWidth="30%" >
          <FunctionBar />
        </Box>
        <Box flex={2} maxWidth="70%">
          <Visualization />
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;
