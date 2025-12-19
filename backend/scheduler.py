import time
import subprocess
from datetime import datetime

def run_pipeline():
    print(f"\n⏰ [{datetime.now()}] MEMULAI PIPELINE OTOMATIS...")
    
    # 1. Jalankan Data Ingestion (Ambil Data)
    print("   Running: Data Ingestion...")
    subprocess.run(["python", "data_ingestion.py"], check=True)
    
    # 2. Jalankan Analysis Engine (Proses AI)
    print("   Running: AI Analysis...")
    subprocess.run(["python", "analysis_engine.py"], check=True)
    
    print(f"✅ [{datetime.now()}] PIPELINE SELESAI. Menunggu siklus berikutnya...\n")

if __name__ == "__main__":
    print("🚀 SYSTEM STARTED: Menjalankan update setiap 1 JAM (3600 detik)")
    
    # Jalankan sekali di awal agar tidak menunggu 1 jam
    try:
        run_pipeline()
    except Exception as e:
        print(f"❌ Error pada run pertama: {e}")

    # Loop selamanya
    while True:
        try:
            # Tunggu 1 jam (3600 detik)
            time.sleep(3600) 
            run_pipeline()
        except KeyboardInterrupt:
            print("\n🛑 System Stopped by User.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")