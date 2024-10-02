import React, { useEffect, useState } from 'react';
import { getFinancialData } from '../services/api';

const FinancialData = () => {
    const [financialData, setFinancialData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getFinancialData();
                setFinancialData(data);
            } catch (error) {
                console.error('Error fetching financial data:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div>
            <h1>Financial Data</h1>
            <pre>{JSON.stringify(financialData, null, 2)}</pre>
        </div>
    );
};

export default FinancialData;
