import React from 'react';
import './App.css'; // Import CSS Baru
import PredictionCard from './components/PredictionCard';
import PriceChart from './components/PriceChart';

function App() {
  return (
    <div className="dashboard-container">
      
      {/* Header */}
      <header className="dashboard-header">
        <h1 className="main-title">ETH / IDR</h1>
        <p className="sub-title">Intelligent Prediction System</p>
      </header>

      {/* Konten Utama */}
      <main>
        <PredictionCard />
        <PriceChart />
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        © 2025 Sapar Hidayat. S | All Right Reserve
      </footer>

    </div>
  )
}

export default App;