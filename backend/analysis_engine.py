import os
import numpy as np
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from ta.volatility import BollingerBands
from dotenv import load_dotenv

# 1. Setup & Koneksi Database
load_dotenv()
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
    firebase_admin.initialize_app(cred)
db = firestore.client()

def get_data_from_firestore():
    """Mengambil data harga dan berita dari Firestore ke Pandas DataFrame"""
    print("📥 Memuat data dari Firestore...")
    
    # Ambil Data Harga
    prices_ref = db.collection('prices').order_by('timestamp').stream()
    price_list = [doc.to_dict() for doc in prices_ref]
    df_prices = pd.DataFrame(price_list)
    
    # Ambil Data Berita
    news_ref = db.collection('news').stream()
    news_list = [doc.to_dict() for doc in news_ref]
    df_news = pd.DataFrame(news_list)
    
    return df_prices, df_news

def analyze_sentiment(df_news):
    """Menghitung skor sentimen rata-rata dari judul berita"""
    print("🧠 Menganalisis Sentimen Berita...")
    analyzer = SentimentIntensityAnalyzer()
    
    if df_news.empty:
        return 0, "Neutral"
    
    # Hitung compound score untuk setiap judul
    df_news['score'] = df_news['title'].apply(lambda title: analyzer.polarity_scores(title)['compound'])
    
    # Rata-rata skor
    avg_score = df_news['score'].mean()
    
    # Tentukan Label
    if avg_score >= 0.05:
        label = "Bullish (Positif)"
    elif avg_score <= -0.05:
        label = "Bearish (Negatif)"
    else:
        label = "Neutral"
        
    print(f"   Skor Sentimen: {avg_score:.4f} ({label})")
    return avg_score, label

def analyze_technicals(df):
    """Menghitung indikator teknikal (Bollinger Bands)"""
    print("📈 Menghitung Indikator Teknikal...")
    
    # Bollinger Bands
    indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)
    df['bb_high'] = indicator_bb.bollinger_hband()
    df['bb_low'] = indicator_bb.bollinger_lband()
    df['bb_mid'] = indicator_bb.bollinger_mavg()
    
    # Simple Signal logic (Bisa dikembangkan lagi)
    last_row = df.iloc[-1]
    signal = "HOLD"
    if last_row['close'] < last_row['bb_low']:
        signal = "BUY (Oversold)"
    elif last_row['close'] > last_row['bb_high']:
        signal = "SELL (Overbought)"
        
    return df, signal

def train_lstm_model(df):
    """Melatih model LSTM sederhana untuk prediksi harga"""
    print("🤖 Melatih Model LSTM (Deep Learning)...")
    
    data = df.filter(['close']).values
    
    # Scaling data (0 sampai 1) agar LSTM mudah belajar
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Persiapan data Training
    # Kita gunakan 60 data jam terakhir untuk memprediksi jam ke-61
    prediction_days = 60 
    
    if len(scaled_data) <= prediction_days:
        print("⚠️ Data tidak cukup untuk training LSTM (Butuh > 60 data). Melewati fase ini.")
        return None, 0
    
    x_train = []
    y_train = []
    
    for i in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[i-prediction_days:i, 0])
        y_train.append(scaled_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Membangun Arsitektur LSTM
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1)) # Output layer (1 harga prediksi)
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Training (Epochs dikecilkan biar cepat untuk demo)
    model.fit(x_train, y_train, batch_size=1, epochs=3, verbose=1)
    
    # Prediksi 1 langkah ke depan
    last_60_days = scaled_data[-prediction_days:]
    X_test = []
    X_test.append(last_60_days)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    
    pred_price_scaled = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price_scaled) # Kembalikan ke harga asli (Rupiah)
    
    print(f"   Prediksi Harga Berikutnya: {pred_price[0][0]:.2f}")
    return float(pred_price[0][0])

def save_prediction(sentiment_score, sentiment_label, technical_signal, predicted_price, current_price):
    """Menyimpan hasil analisis ke Firestore"""
    print("💾 Menyimpan Hasil Prediksi ke Firestore...")
    
    result = {
        'timestamp': firestore.SERVER_TIMESTAMP,
        'sentiment_score': sentiment_score,
        'sentiment_label': sentiment_label,
        'technical_signal': technical_signal,
        'predicted_price_lstm': predicted_price,
        'current_price': current_price,
        'prediction_source': 'Hybrid (VADER + Bollinger + LSTM)'
    }
    
    # Simpan ke koleksi 'predictions', dokumen terbaru selalu bernama 'latest'
    # agar Frontend mudah mengambilnya nanti.
    db.collection('predictions').document('latest').set(result)
    
    # Opsional: Simpan juga history prediksi dengan timestamp
    # db.collection('prediction_history').add(result)
    
    print("🚀 Selesai! Data siap untuk Dashboard.")

if __name__ == "__main__":
    # 1. Load Data
    df_prices, df_news = get_data_from_firestore()
    
    if not df_prices.empty:
        # 2. Analisis Sentimen
        sent_score, sent_label = analyze_sentiment(df_news)
        
        # 3. Analisis Teknikal
        df_prices, tech_signal = analyze_technicals(df_prices)
        
        # 4. Prediksi ML (LSTM)
        current_price = df_prices['close'].iloc[-1]
        predicted_price = train_lstm_model(df_prices)
        
        if predicted_price is None:
            predicted_price = current_price # Fallback jika data kurang
            
        # 5. Simpan Hasil
        save_prediction(sent_score, sent_label, tech_signal, predicted_price, current_price)
    else:
        print("❌ Data harga kosong. Jalankan data_ingestion.py dulu!")