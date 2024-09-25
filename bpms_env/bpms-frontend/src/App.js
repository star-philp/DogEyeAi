import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import FinancialData from './components/FinancialData';
import StockData from './components/StockData';
import MacroeconomicData from './components/MacroeconomicData';
import CorporateData from './components/CorporateData';

function App() {
return (
<Router>
    <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/financial-data" element={<FinancialData />} />
    <Route path="/stock-market" element={<StockData />} />
    <Route path="/macroeconomic" element={<MacroeconomicData />} />
    <Route path="/corporate-data" element={<CorporateData />} />
    </Routes>
</Router>
);
}

export default App;
