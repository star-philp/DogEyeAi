// src/components/CorporateData.js
import React, { useState, useEffect } from 'react';
import axios from '../services/api';
import { getFinancialData, getStockData } from '../services/api';

function CorporateData() {
    const [corporateNews, setCorporateNews] = useState([]);

    useEffect(() => {
        axios.get('/corporate_news/')
            .then(response => setCorporateNews(response.data))
            .catch(error => console.error('Error fetching corporate news', error));
    }, []);

    return (
        <div>
            <h1>Company Data</h1>
            <ul>
                {corporateNews.map((news) => (
                    <li key={news.id}>
                        {news.title}: {news.summary}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default CorporateData;
