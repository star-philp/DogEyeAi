import React, { useEffect, useState } from 'react';
import api from '../services/apiClient';

const MainDashboard = () => {
const [financialData, setFinancialData] = useState([]);
const [stockData, setStockData] = useState([]);
const [macroData, setMacroData] = useState([]);
const [newsData, setNewsData] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

// Fetch data when component mounts
useEffect(() => {
const fetchData = async () => {
    try {
    const financial = await api.getFinancialStatements();
    const stock = await api.getStockPrices();
    const macro = await api.getMacroEconomicData();
    const news = await api.getCorporateNews();
    
    setFinancialData(financial);
    setStockData(stock);
    setMacroData(macro);
    setNewsData(news);
    } catch (err) {
    setError('Failed to load data.');
    } finally {
    setLoading(false);
    }
};

fetchData();
}, []);

if (loading) return <div>Loading...</div>;
if (error) return <div>{error}</div>;

return (
<div className="dashboard">
    <h1>Main Dashboard</h1>

    <section>
    <h2>Financial Statements</h2>
    <ul>
        {financialData.map((item, index) => (
        <li key={index}>{item.company_name}: {item.total_revenue}</li>
        ))}
    </ul>
    </section>

    <section>
    <h2>Stock Prices</h2>
    <ul>
        {stockData.map((item, index) => (
        <li key={index}>{item.company_name}: {item.close_price}</li>
        ))}
    </ul>
    </section>

    <section>
    <h2>Macroeconomic Data</h2>
    <ul>
        {macroData.map((item, index) => (
        <li key={index}>{item.indicator}: {item.value}</li>
        ))}
    </ul>
    </section>

    <section>
    <h2>Corporate News</h2>
    <ul>
        {newsData.map((item, index) => (
        <li key={index}>{item.title}: {item.summary}</li>
        ))}
    </ul>
    </section>
</div>
);
};

export default MainDashboard;
