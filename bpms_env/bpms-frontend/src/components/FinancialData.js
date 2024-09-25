import React, { useState, useEffect } from 'react';
import axios from '../services/api';

const FinancialData = () => {
const [financialData, setFinancialData] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
axios.get('/financial_data/')
    .then(response => {
    setFinancialData(response.data);
    setLoading(false);
    })
    .catch(error => {
    console.error("Error fetching financial data:", error);
    setError("Failed to load financial data");
    setLoading(false);
    });
}, []);

if (loading) return <p>Loading financial data...</p>;
if (error) return <p>{error}</p>;

return (
<div>
    <h2>Financial Data Overview</h2>
    {financialData.length > 0 ? (
    <table>
        <thead>
        <tr>
            <th>Company Name</th>
            <th>Report Type</th>
            <th>Total Revenue</th>
            <th>Net Income</th>
        </tr>
        </thead>
        <tbody>
        {financialData.map((item, index) => (
            <tr key={index}>
            <td>{item.company_name}</td>
            <td>{item.report_type}</td>
            <td>{item.total_revenue}</td>
            <td>{item.net_income}</td>
            </tr>
        ))}
        </tbody>
    </table>
    ) : (
    <p>No financial data available</p>
    )}
</div>
);
};

export default FinancialData;
