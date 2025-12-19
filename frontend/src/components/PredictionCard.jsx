import React, { useEffect, useState } from 'react';
import { doc, onSnapshot } from "firebase/firestore";
import { db } from "../firebase"; 
import { Brain, BarChart3 } from 'lucide-react';
import './PredictionCard.css'; // Import CSS

const PredictionCard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onSnapshot(doc(db, "predictions", "latest"), (doc) => {
      if (doc.exists()) setData(doc.data());
      setLoading(false);
    });
    return () => unsub(); 
  }, []);

  const formatIDR = (num) => new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2 }).format(num);

  if (loading) return <div style={{textAlign:'center', color:'white'}}>Memuat Data AI...</div>;
  if (!data) return <div style={{textAlign:'center', color:'white'}}>Data Tidak Ditemukan</div>;

  return (
    <div className="prediction-wrapper">
      
      {/* Label Header */}
      <div className="section-label">
        <Brain size={28} />
        <h2>AI Prediction Engine</h2>
      </div>

      {/* Grid Kartu */}
      <div className="cards-grid">
        
        {/* Kartu 1: Harga */}
        <div className="white-card">
            <h3 className="card-title">Prediksi Harga (Next Hour)</h3>
            <p className="price-main">
                Rp {formatIDR(data.predicted_price_lstm)}
            </p>
            <p className="price-sub">
                Harga Saat Ini: <span>Rp {formatIDR(data.current_price)}</span>
            </p>
        </div>

        {/* Kartu 2: Sentimen */}
        <div className="white-card">
            <h3 className="card-title">Sentimen Berita</h3>
            <div style={{display:'flex', alignItems:'center', gap:'10px', marginBottom:'1rem'}}>
                <BarChart3 size={24} color="#000" />
                <span className="sentiment-value">{data.sentiment_label}</span>
            </div>
            <p className="price-sub">
                Sinyal Teknikal: <span className="signal-text">{data.technical_signal}</span>
            </p>
        </div>

      </div>
    </div>
  );
};

export default PredictionCard;