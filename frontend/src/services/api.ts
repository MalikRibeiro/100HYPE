import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const login = async (username, password) => {
    const form = new FormData();
    form.append('username', username);
    form.append('password', password);
    const response = await api.post('/auth/access-token', form);
    return response.data;
};

export const register = async (data) => {
    const response = await api.post('/auth/signup', data);
    return response.data;
};

export const getPortfolio = async () => {
    const response = await api.get('/portfolio/portfolio');
    return response.data;
};

export const createAsset = async (asset) => {
    const response = await api.post('/portfolio/assets', asset);
    return response.data;
};

export const createTransaction = async (tx) => {
    const response = await api.post('/portfolio/transactions', tx);
    return response.data;
};

export const generateAnalysis = async (language = 'pt') => {
    const response = await api.post(`/analysis/generate?language=${language}`);
    return response.data;
};

export default api;
