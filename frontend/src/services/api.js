import axios from 'axios';

// Create an Axios instance with your backend base URL
const api = axios.create({
  baseURL: 'http://localhost:8080',  // FastAPI backend URL
});

// Export the Axios instance
export default api;