// src/components/MacroeconomicData.js
import React, { useState, useEffect } from 'react';
import axios from '../services/api';

function MacroeconomicData() {
    const [macroData, setMacroData] = useState([]);

    useEffect(() => {
        axios.get('/macroeconomic_data/')
            .then(response => setMacroData(response.data))
            .catch(error => console.error('Error fetching macroeconomic data', error));
    }, []);

    return (
        <div>
            <h1>Macroeconomic Data</h1>
            <ul>
                {macroData.map((item) => (
                    <li key={item.id}>
                        {item.indicator}: {item.value}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default MacroeconomicData;
