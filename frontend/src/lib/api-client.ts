import axios, { AxiosInstance } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://web-production-8c988.up.railway.app';

// Create axios instance with defaults
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Set to true if using cookies
});

// Request interceptor for auth tokens
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API methods
export const api = {
  // Health check
  health: () => apiClient.get('/health'),
  
  // Opportunities
  getOpportunities: (limit = 10) => apiClient.get(`/api/opportunities?limit=${limit}`),
  
  // Scan operations
  triggerScan: (category = 'all') => 
    apiClient.post('/api/scan/trigger', { category }),
  
  getScanStatus: () => apiClient.get('/api/scan/status'),
  
  // Stats
  getStats: () => apiClient.get('/api/stats'),
};

export default apiClient;
