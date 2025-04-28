import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication service
export const authService = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('userId', response.data.user_id);
    localStorage.setItem('email', response.data.email);
    return response.data;
  },

  signup: async (email: string, password: string) => {
    const response = await api.post('/auth/signup', { email, password });
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('userId', response.data.user_id);
    localStorage.setItem('email', response.data.email);
    return response.data;
  },

  googleLogin: async (idToken: string) => {
    const response = await api.post('/auth/google-login', { id_token: idToken });
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('userId', response.data.user_id);
    localStorage.setItem('email', response.data.email);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('email');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

// Chat service
export const chatService = {
  getChatHistory: async () => {
    const response = await api.get('/chat/history');
    return response.data.messages;
  },

  sendMessage: async (message: string, useRag: boolean = true) => {
    const response = await api.post('/chat/message', { message, use_rag: useRag });
    return response.data;
  }
};

export default api; 