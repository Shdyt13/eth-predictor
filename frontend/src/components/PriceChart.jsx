import React, { useEffect, useState, useRef } from 'react';
import { collection, query, orderBy, limit, getDocs } from "firebase/firestore";
import { db } from "../firebase";
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler } from 'chart.js';
import { format } from 'date-fns';
import './PriceChart.css'; // Import CSS

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler);

const PriceChart = () => {
  const [chartData, setChartData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchHistory = async () => {
      const q = query(collection(db, "prices"), orderBy("timestamp", "desc"), limit(50));
      const querySnapshot = await getDocs(q);
      const rawData = [];
      querySnapshot.forEach((doc) => rawData.push(doc.data()));
      const sortedData = rawData.reverse();

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const gradient = ctx.createLinearGradient(0, 0, 0, 300);
      gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)'); 
      gradient.addColorStop(1, 'rgba(37, 99, 235, 0.0)');

      setChartData({
        labels: sortedData.map(d => format(new Date(d.timestamp), 'HH:mm')),
        datasets: [{
          label: 'Harga',
          data: sortedData.map(d => d.close),
          borderColor: '#2563EB',
          backgroundColor: gradient,
          borderWidth: 2,
          tension: 0.3,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 6,
        }]
      });
    };
    fetchHistory();
  }, []);

  if (!chartData) return <div className="chart-card" style={{display:'flex', alignItems:'center', justifyContent:'center'}}>Loading Chart...</div>;

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { 
        legend: { display: false },
        tooltip: {
            titleFont: { family: 'Inter', size: 14 },
            bodyFont: { family: 'JetBrains Mono', size: 14 },
            backgroundColor: '#1E293B',
            padding: 12,
            displayColors: false
        }
    },
    scales: {
      x: { 
        grid: { color: '#E2E8F0' }, 
        ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, maxTicksLimit: 8 } 
      },
      y: { 
        position: 'left',
        grid: { color: '#E2E8F0' },
        ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, padding: 10 } 
      }
    },
    interaction: { mode: 'nearest', axis: 'x', intersect: false },
    layout: { padding: { left: 0, right: 10, top: 10, bottom: 0 } }
  };

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3 className="chart-title">Pergerakan Harga (50 Jam Terakhir)</h3>
        <span className="chart-source">Source: Indodax</span>
      </div>
      <div className="canvas-container">
        <Line ref={chartRef} data={chartData} options={options} />
      </div>
    </div>
  );
};

export default PriceChart;