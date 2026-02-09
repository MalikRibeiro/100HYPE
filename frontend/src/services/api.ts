import axios from 'axios';

// O Vite expõe variáveis de ambiente via import.meta.env
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: baseURL,
  withCredentials: true, // Importante para cookies/sessão
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const login = async (username: string, password: string) => {
    const form = new FormData();
    form.append('username', username);
    form.append('password', password);
    const response = await api.post('/auth/access-token', form);
    return response.data;
};

export const register = async (data: any) => {
    const response = await api.post('/auth/signup', data);
    return response.data;
};

export const getPortfolio = async () => {
    const response = await api.get('/portfolio/portfolio');
    return response.data;
};

export const createAsset = async (asset: any) => {
    const response = await api.post('/portfolio/assets', asset);
    return response.data;
};

export const createTransaction = async (tx: any) => {
    const response = await api.post('/portfolio/transactions', tx);
    return response.data;
};

export const generateAnalysis = async (language: string = 'pt') => {
    const response = await api.post(`/analysis/generate?language=${language}`);
    return response.data;
};

export default api;
