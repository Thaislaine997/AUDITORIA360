// src/frontend/src/services/api.ts

import axios from 'axios';

const api = axios.create({
  // A URL base da nossa API FastAPI. 
  // In development, we'll use the direct API server URL
  baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:8001' : '/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;