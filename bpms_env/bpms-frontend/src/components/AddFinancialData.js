// src/components/AddFinancialData.js
import React, { useState } from 'react';
import axios from '../services/api';
import { useNavigate } from 'react-router-dom';

function AddFinancialData() {
    const [formData, setFormData] = useState({
        company_name: '',
        report_type: '',
        period_start: '',
        period_end: '',
        total_revenue: '',
        operating_income: '',
        net_income: '',
        total_assets: '',
        total_liabilities: '',
        cash_from_operations: '',
        cash_from_investing: '',
        cash_from_financing: ''
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/financial_statements/', formData)
            .then(() => {
                navigate('/financial-data');
            })
            .catch(error => console.error('Error adding financial data', error));
    };

    return (
        <div>
            <h1>Add Financial Data</h1>
            <form onSubmit={handleSubmit}>
                <input name="company_name" placeholder="Company Name" value={formData.company_name} onChange={handleChange} required />
                <input name="report_type" placeholder="Report Type" value={formData.report_type} onChange={handleChange} required />
                <input name="period_start" placeholder="Period Start" value={formData.period_start} onChange={handleChange} required />
                <input name="period_end" placeholder="Period End" value={formData.period_end} onChange={handleChange} required />
                <input name="total_revenue" placeholder="Total Revenue" value={formData.total_revenue} onChange={handleChange} required />
                <input name="operating_income" placeholder="Operating Income" value={formData.operating_income} onChange={handleChange} required />
                <input name="net_income" placeholder="Net Income" value={formData.net_income} onChange={handleChange} required />
                <input name="total_assets" placeholder="Total Assets" value={formData.total_assets} onChange={handleChange} required />
                <input name="total_liabilities" placeholder="Total Liabilities" value={formData.total_liabilities} onChange={handleChange} required />
                <input name="cash_from_operations" placeholder="Cash from Operations" value={formData.cash_from_operations} onChange={handleChange} required />
                <input name="cash_from_investing" placeholder="Cash from Investing" value={formData.cash_from_investing} onChange={handleChange} required />
                <input name="cash_from_financing" placeholder="Cash from Financing" value={formData.cash_from_financing} onChange={handleChange} required />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default AddFinancialData;
