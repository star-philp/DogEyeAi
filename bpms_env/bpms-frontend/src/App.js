import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FinancialData from './components/FinancialData';
import StockData from './components/StockData'; // Ensure correct imports
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';


const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<FinancialData />} />
                    <Route path="/financial-data" element={<FinancialData />} />
                    <Route path="/stock-data" element={<StockData />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
