import React, { useEffect, useState } from 'react';
import { getStockData } from '../services/api'; // Make sure you're using the correct named import

const MacroeconomicData = () => {
    const [stockData, setStockData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getStockData();
                setStockData(data);
            } catch (error) {
                console.error('Error fetching stock data:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div>
            <h1>Macroeconomic Data</h1>
            <pre>{JSON.stringify(stockData, null, 2)}</pre>
        </div>
    );
};

export default MacroeconomicData;