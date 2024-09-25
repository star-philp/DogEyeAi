import React from 'react';
import './NavigationBar.css'; // Ensure this path is correct

function NavigationBar() {
    return (
        <nav className="navbar">
            <a href="/">Dashboard</a>
            <a href="/financial-data">Financial Data</a>
            <a href="/stocks-market">Stocks Market</a>
            <a href="/macroeconomic">Macroeconomic Data</a>
            <a href="/corporate-data">Corporate Data</a>
        </nav>
    );
}

export default NavigationBar;
