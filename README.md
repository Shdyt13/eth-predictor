# ETH/IDR Intelligent Prediction System 🚀

![Status](https://img.shields.io/badge/Status-Active-success)
![Tech](https://img.shields.io/badge/Stack-Fullstack-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> **Sistem Prediksi Harga Ethereum (ETH) berbasis AI menggunakan Deep Learning (LSTM) dan Analisis Sentimen Berita (NLP).**

---

## 📸 Tampilan Dashboard

(![Dashboard Preview](image.png))

Tampilan antarmuka dirancang dengan gaya **Modern Fintech Dashboard**, mengombinasikan warna **Deep Navy** dan **White Cards** untuk memberikan kesan profesional, futuristik, dan mudah dibaca.

---

## 🌟 Fitur Utama

### 1. 🧠 AI Prediction Engine (LSTM)
Menggunakan algoritma **Long Short-Term Memory (LSTM)** dari TensorFlow untuk memprediksi harga penutupan Ethereum (ETH/IDR) **1 jam ke depan** berdasarkan data historis.

### 2. 📰 News Sentiment Analysis (NLP)
Menerapkan **VADER (Valence Aware Dictionary and sEntiment Reasoner)** untuk menganalisis sentimen berita kripto global dan menentukan kondisi pasar (*Bullish* / *Bearish*).

### 3. 📊 Real-time Market Data
Terintegrasi dengan **Indodax API** melalui library `ccxt` untuk memperoleh data harga Ethereum (ETH/IDR) secara real-time.

### 4. 📈 Interactive Charting
Visualisasi pergerakan harga **50 jam terakhir** menggunakan grafik interaktif yang responsif.

### 5. ☁️ Cloud Architecture
- **Database:** Google Cloud Firestore (NoSQL)
- **Hosting:** Google Firebase Hosting

---

## 🛠️ Teknologi yang Digunakan (Tech Stack)

### 🔹 Frontend (User Interface)
- **React.js (Vite)** – Framework UI utama
- **Vanilla CSS (Custom Design System)** – Styling manual untuk desain presisi
- **Chart.js** – Visualisasi grafik data
- **Firebase SDK** – Koneksi real-time ke Firestore

### 🔹 Backend (AI & Data Processing)
- **Python 3.x**
- **TensorFlow / Keras** – Model Neural Network (LSTM)
- **Pandas & NumPy** – Manipulasi data
- **NLTK (VADER)** – Analisis sentimen berita
- **CCXT** – Integrasi API Bursa Kripto (Indodax)
- **Firebase Admin SDK** – Manajemen database server-side

---

## 📂 Struktur Proyek

```bash
eth-predictor/
├── backend/               # Logika Python & AI
│   ├── models/            # File model .h5 (LSTM)
│   ├── scheduler.py       # Script otomatisasi data (Jantung Sistem)
│   ├── data_ingestion.py  # Pengambilan data & training model
│   ├── sentiment.py       # Modul analisis sentimen berita
│   └── requirements.txt   # Daftar dependensi Python
│
├── frontend/              # Tampilan React.js
│   ├── src/
│   │   ├── components/    # Komponen UI (PredictionCard, PriceChart)
│   │   ├── App.css        # Styling Global (Design System)
│   │   └── firebase.js    # Konfigurasi Firebase Client
│   └── index.html
│
└── firebase.json          # Konfigurasi Firebase Hosting

Cara Menjalankan (Installation)
Prasyarat

- 'Node.js & NPM'
- 'Python 3.8+'
- 'Akun Google Firebase'