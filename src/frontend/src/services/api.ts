// src/frontend/src/services/api.ts

import axios from 'axios';

const api = axios.create({
  // A URL base da nossa API FastAPI. 
  // Em desenvolvimento, o Vite proxy irá redirecionar isto. Em produção, apontará para o URL da API.
  baseURL: '/api/v1', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;