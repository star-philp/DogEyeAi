import React, { useState, useEffect } from 'react';
import api from '../services/api';  // Corrected path for API import
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StockDataVisual = () => {
const [stockData, setStockData] = useState([]);

useEffect(() => {
api.getStockData().then(data => setStockData(data));
}, []);

return (
<div>
    <h1>Stock Data Visualization</h1>
    <ResponsiveContainer width="100%" height={400}>
    <LineChart data={stockData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="close_price" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="open_price" stroke="#82ca9d" />
    </LineChart>
    </ResponsiveContainer>
</div>
);
};

export default StockDataVisual;
