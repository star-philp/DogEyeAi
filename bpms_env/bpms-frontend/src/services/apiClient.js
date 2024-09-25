import axios from 'axios';

// API URL to communicate with the backend
const API_URL = 'http://localhost:8000';

// Axios instance for API communication
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000, // 10 seconds timeout
});

// API functions
const api = {
getFinancialStatements: async () => {
try {
    const response = await apiClient.get('/financial-statements');
    return response.data;
} catch (error) {
    console.error('Error fetching financial statements:', error.response || error);
    throw new Error('Failed to fetch financial statements');
}
},

getStockPrices: async () => {
try {
    const response = await apiClient.get('/stock-prices');
    return response.data;
} catch (error) {
    console.error('Error fetching stock prices:', error.response || error);
    throw new Error('Failed to fetch stock prices');
}
},

getMacroEconomicData: async () => {
try {
    const response = await apiClient.get('/macroeconomic-data');
    return response.data;
} catch (error) {
    console.error('Error fetching macroeconomic data:', error.response || error);
    throw new Error('Failed to fetch macroeconomic data');
}
},

getCorporateNews: async () => {
try {
    const response = await apiClient.get('/corporate-news');
    return response.data;
} catch (error) {
    console.error('Error fetching corporate news:', error.response || error);
    throw new Error('Failed to fetch corporate news');
}
}
};

export default api;
