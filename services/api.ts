// src/frontend/src/services/api.ts

import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:8001' : '/api'),
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;