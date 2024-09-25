import React, { useState, useEffect } from 'react';
import axios from '../services/api';

const StockData = () => {
const [stockData, setStockData] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
axios.get('/stock_data/')
    .then(response => {
    setStockData(response.data);
    setLoading(false);
    })
    .catch(error => {
    console.error("Error fetching stock data:", error);
    setError("Failed to load stock data");
    setLoading(false);
    });
}, []);

if (loading) return <p>Loading stock data...</p>;
if (error) return <p>{error}</p>;

return (
<div>
    <h2>Stock Market Overview</h2>
    {stockData.length > 0 ? (
    <table>
        <thead>
        <tr>
            <th>Company Name</th>
            <th>Date</th>
            <th>Open Price</th>
            <th>Close Price</th>
        </tr>
        </thead>
        <tbody>
        {stockData.map((item, index) => (
            <tr key={index}>
            <td>{item.company_name}</td>
            <td>{item.date}</td>
            <td>{item.open_price}</td>
            <td>{item.close_price}</td>
            </tr>
        ))}
        </tbody>
    </table>
    ) : (
    <p>No stock data available</p>
    )}
</div>
);
};

export default StockData;
