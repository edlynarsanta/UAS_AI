import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TrafficAnalyzer:
    def __init__(self):
        # Dalam proyek nyata, model ML akan dimuat di sini
        # self.prediction_model = load_pretrained_model("traffic_prediction_model.pkl")
        pass

    def analyze_current_traffic(self, data_persimpangan):
        """
        Menganalisis kondisi lalu lintas saat ini di sebuah persimpangan.
        Menentukan arah mana yang paling padat.
        """
        print(f"\n--- Analisis Lalu Lintas Saat Ini untuk {data_persimpangan['persimpangan_id']} ---")
        kondisi_arah = {}
        for arah, data in data_persimpangan.items():
            if arah not in ["persimpangan_id", "waktu_timestamp"]:
                # Menghitung "skor kepadatan" sederhana
                # Bobot bisa disesuaikan: volume lebih penting dari antrean, dll.
                skor_kepadatan = (data["volume_kendaraan"] * 0.7) + \
                                 (data["panjang_antrean"] * 0.2) + \
                                 (50 - data["kecepatan_rata_rata"]) * 0.1 # Kecepatan rendah = kepadatan tinggi

                kondisi_arah[arah] = {
                    "volume": data["volume_kendaraan"],
                    "antrean": data["panjang_antrean"],
                    "kecepatan": data["kecepatan_rata_rata"],
                    "skor_kepadatan": round(skor_kepadatan, 2)
                }
                print(f"  {arah.replace('_', ' ').title()}: Volume={data['volume_kendaraan']}, "
                      f"Antrean={data['panjang_antrean']}m, Kecepatan={data['kecepatan_rata_rata']} km/j, "
                      f"Skor Kepadatan={kondisi_arah[arah]['skor_kepadatan']}")

        # Menemukan arah dengan kepadatan tertinggi
        arah_terpadat = max(kondisi_arah, key=lambda k: kondisi_arah[k]['skor_kepadatan'])
        print(f"\nArah terpadat saat ini: {arah_terpadat.replace('_', ' ').title()} "
              f"(Skor: {kondisi_arah[arah_terpadat]['skor_kepadatan']})")
        
        return kondisi_arah, arah_terpadat

    def predict_future_traffic(self, historis_data, persimpangan_id, waktu_prediksi_menit=15):
        """
        (Konseptual) Memprediksi kondisi lalu lintas di masa depan
        Bisa menggunakan model ML (misal LSTM) yang dilatih dengan data historis.
        Untuk contoh ini, kita asumsikan prediksi sederhana berdasarkan tren atau data historis.
        """
        print(f"\n--- Prediksi Lalu Lintas untuk {persimpangan_id} dalam {waktu_prediksi_menit} menit ---")
        
        # Dalam implementasi nyata, ini akan menjadi keluaran dari model ML yang kompleks.
        # Misalnya, model akan memprediksi volume dan antrean untuk setiap arah.
        
        # Contoh prediksi sederhana: asumsikan sedikit peningkatan kepadatan di arah terpadat
        # dan sedikit penurunan di arah yang lancar.
        prediksi_kepadatan = {}
        for arah in ["arah_utara", "arah_timur", "arah_selatan", "arah_barat"]:
            # Ini hanya placeholder, ML model akan melakukan pekerjaan ini
            prediksi_kepadatan[arah] = np.random.uniform(50, 150) # Skor kepadatan acak
        
        print(f"  (Simulasi) Prediksi kondisi lalu lintas dalam {waktu_prediksi_menit} menit: {prediksi_kepadatan}")
        return prediksi_kepadatan

# --- Contoh Penggunaan Modul Analisis Data ---
# analyzer = TrafficAnalyzer()
# kondisi_saat_ini, arah_terpadat_saat_ini = analyzer.analyze_current_traffic(data_persimpangan)
# prediksi_masa_depan = analyzer.predict_future_traffic([], data_persimpangan['persimpangan_id'])
