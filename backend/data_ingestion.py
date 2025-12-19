import xml.etree.ElementTree as ET
import os
import ccxt
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Load Environment Variables
load_dotenv()

# 2. Inisialisasi Firebase (Hanya jika belum terinisialisasi)
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_market_data(symbol='ETH/IDR', limit=100):
    """
    Mengambil data OHLCV (Open, High, Low, Close, Volume) dari Indodax via CCXT.
    """
    print(f"🔄 Mengambil data pasar untuk {symbol}...")
    
    # Menggunakan exchange Indodax untuk pair IDR
    exchange = ccxt.indodax() 
    
    try:
        # Fetch OHLCV (Timeframe 1 jam = '1h')
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=limit)
        
        # Konversi ke List of Dictionaries agar mudah masuk ke Firestore
        data_list = []
        for candle in ohlcv:
            # candle structure: [timestamp, open, high, low, close, volume]
            timestamp_ms = candle[0]
            dt_object = datetime.fromtimestamp(timestamp_ms / 1000.0)
            
            data_list.append({
                'timestamp': timestamp_ms,
                'datetime': dt_object, # Untuk query sorting di Firestore
                'open': candle[1],
                'high': candle[2],
                'low': candle[3],
                'close': candle[4],
                'volume': candle[5],
                'symbol': symbol
            })
            
        print(f"✅ Berhasil mengambil {len(data_list)} data candle.")
        return data_list
        
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return []

def fetch_news_data(currency='ETH'):
    """
    Mengambil berita terbaru dari Google News RSS (Paling Stabil).
    """
    print(f"🔄 Mengambil berita via Google News untuk {currency}...")
    
    # URL Google News RSS (Query: Ethereum Crypto)
    # hl=en-US: Bahasa Inggris (lebih baik untuk NLP Sentiment Analysis nanti)
    url = "https://news.google.com/rss/search?q=Ethereum+crypto+currency&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Parsing XML
        root = ET.fromstring(response.content)
        
        news_list = []
        # Google News strukturnya: channel -> item
        for item in root.findall('.//item'):
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            link = item.find('link').text
            guid = item.find('guid').text
            source = item.find('source').text if item.find('source') is not None else "Google News"
            
            news_list.append({
                'id': guid, # Google news GUID cukup unik
                'title': title,
                'published_at': pub_date,
                'source': source,
                'url': link,
                'currency': currency
            })
            
            # Kita batasi ambil 15 berita terbaru saja agar tidak spamming
            if len(news_list) >= 15:
                break
        
        print(f"✅ Berhasil mengambil {len(news_list)} berita dari Google News.")
        return news_list
        
    except Exception as e:
        print(f"❌ Error fetching Google News: {e}")
        return []

def save_to_firestore(collection_name, data, id_field):
    """
    Menyimpan data ke Firestore.
    PENTING: Kita menggunakan custom ID agar tidak ada duplikasi data.
    """
    print(f"💾 Menyimpan ke koleksi '{collection_name}'...")
    collection_ref = db.collection(collection_name)
    count = 0
    
    batch = db.batch() # Menggunakan batch write untuk performa
    
    for item in data:
        # Tentukan Document ID. 
        # Untuk harga: gunakan timestamp (karena unik per jam).
        # Untuk berita: gunakan ID dari CryptoPanic.
        doc_id = str(item[id_field])
        
        doc_ref = collection_ref.document(doc_id)
        batch.set(doc_ref, item) # .set() akan menimpa data jika ID sudah ada (Upsert)
        count += 1
        
        # Firestore batch limit adalah 500, kita commit setiap 400 untuk aman
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            
    batch.commit() # Commit sisa data
    print(f"🚀 Sukses menyimpan {count} dokumen ke {collection_name}!")

if __name__ == "__main__":
    # 1. Jalankan Ingest Data Harga
    market_data = fetch_market_data()
    if market_data:
        # Simpan ke koleksi 'prices', gunakan 'timestamp' sebagai ID
        save_to_firestore('prices', market_data, 'timestamp')
        
    print("-" * 30)
    
    # 2. Jalankan Ingest Berita
    news_data = fetch_news_data()
    if news_data:
        # Simpan ke koleksi 'news', gunakan 'id' sebagai ID
        save_to_firestore('news', news_data, 'id')