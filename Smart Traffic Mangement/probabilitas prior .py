import numpy as np

class NaiveBayesTrafficPredictor:
    def __init__(self):
        # Probabilitas Prior (P(Kelas))
        # Asumsi 30% kemungkinan kemacetan secara default
        self.p_kemacetan = 0.3
        self.p_tidak_kemacetan = 1 - self.p_kemacetan

        # Probabilitas Kondisional (Likelihood) P(Fitur | Kelas)
        # Contoh nilai-nilai ini akan berasal dari data training historis
        # Format: {fitur: {nilai_fitur: {kemacetan: P(fitur|kemacetan), tidak_kemacetan: P(fitur|tidak_kemacetan)}}}
        self.likelihoods = {
            "Volume": {
                "Tinggi": {"kemacetan": 0.8, "tidak_kemacetan": 0.2},
                "Rendah": {"kemacetan": 0.2, "tidak_kemacetan": 0.8}
            },
            "Kecepatan": {
                "Lambat": {"kemacetan": 0.7, "tidak_kemacetan": 0.1},
                "Normal": {"kemacetan": 0.3, "tidak_kemacetan": 0.9}
            },
            "Antrean": {
                "Panjang": {"kemacetan": 0.85, "tidak_kemacetan": 0.15},
                "Pendek": {"kemacetan": 0.15, "tidak_kemacetan": 0.85}
            },
            "Durasi_Hijau": {
                "Optimal": {"kemacetan": 0.3, "tidak_kemacetan": 0.7},
                "Tidak_Optimal": {"kemacetan": 0.7, "tidak_kemacetan": 0.3}
            },
            "Kecelakaan": {
                "Ya": {"kemacetan": 0.6, "tidak_kemacetan": 0.05},
                "Tidak": {"kemacetan": 0.4, "tidak_kemacetan": 0.95}
            },
            "Cuaca": {
                "Buruk": {"kemacetan": 0.5, "tidak_kemacetan": 0.1},
                "Baik": {"kemacetan": 0.5, "tidak_kemacetan": 0.9}
            },
            "Jam_Puncak": {
                "Ya": {"kemacetan": 0.75, "tidak_kemacetan": 0.25},
                "Tidak": {"kemacetan": 0.25, "tidak_kemacetan": 0.75}
            },
            "Event": {
                "Ya": {"kemacetan": 0.9, "tidak_kemacetan": 0.1},
                "Tidak": {"kemacetan": 0.1, "tidak_kemacetan": 0.9}
            },
            "Perbaikan_Jalan": {
                "Ya": {"kemacetan": 0.8, "tidak_kemacetan": 0.2},
                "Tidak": {"kemacetan": 0.2, "tidak_kemacetan": 0.8}
            },
            "Jalur": {
                "Tersedia_Banyak": {"kemacetan": 0.2, "tidak_kemacetan": 0.8},
                "Tersedia_Sedikit": {"kemacetan": 0.8, "tidak_kemacetan": 0.2}
            }
        }

    def predict(self, observed_conditions):
        """
        Memprediksi probabilitas kemacetan dan tidak kemacetan
        berdasarkan kondisi yang diamati.
        observed_conditions: dictionary {nama_fitur: nilai_fitur_amati}
        """
        
        # Hitung probabilitas kemacetan (numerator)
        prob_numerator_kemacetan = self.p_kemacetan
        print(f"\n--- Perhitungan Likelihood untuk Kemacetan ---")
        for feature, observed_value in observed_conditions.items():
            if feature in self.likelihoods and observed_value in self.likelihoods[feature]:
                likelihood_val = self.likelihoods[feature][observed_value]["kemacetan"]
                prob_numerator_kemacetan *= likelihood_val
                print(f"  P({observed_value} | Kemacetan, {feature}) = {likelihood_val}")
            else:
                print(f"  Peringatan: Fitur/nilai '{feature}'/'{observed_value}' tidak ditemukan dalam model likelihood.")
                # Dalam kasus nyata, bisa gunakan smoothing atau default
                
        # Hitung probabilitas tidak kemacetan (numerator)
        prob_numerator_tidak_kemacetan = self.p_tidak_kemacetan
        print(f"\n--- Perhitungan Likelihood untuk Tidak Kemacetan ---")
        for feature, observed_value in observed_conditions.items():
            if feature in self.likelihoods and observed_value in self.likelihoods[feature]:
                likelihood_val = self.likelihoods[feature][observed_value]["tidak_kemacetan"]
                prob_numerator_tidak_kemacetan *= likelihood_val
                print(f"  P({observed_value} | Tidak Kemacetan, {feature}) = {likelihood_val}")
            else:
                # Sama seperti di atas
                pass # Already warned for 'kemacetan' case

        # Normalisasi untuk mendapatkan probabilitas posterior
        total_prob = prob_numerator_kemacetan + prob_numerator_tidak_kemacetan
        
        if total_prob == 0:
            print("\nError: Total probabilitas nol. Tidak dapat melakukan prediksi.")
            return {"Kemacetan": 0.5, "Tidak Kemacetan": 0.5} # Default atau error
            
        prob_posterior_kemacetan = prob_numerator_kemacetan / total_prob
        prob_posterior_tidak_kemacetan = prob_numerator_tidak_kemacetan / total_prob

        return {
            "Kemacetan": round(prob_posterior_kemacetan, 4),
            "Tidak Kemacetan": round(prob_posterior_tidak_kemacetan, 4)
        }

# --- Simulasi Sistem ---
if __name__ == "__main__":
    predictor = NaiveBayesTrafficPredictor()

    print("===== Skenario 1: Kemacetan Jam Puncak =====")
    kondisi1 = {
        "Volume": "Tinggi",
        "Kecepatan": "Lambat",
        "Antrean": "Panjang",
        "Jam_Puncak": "Ya",
        "Kecelakaan": "Tidak", # Tidak ada kecelakaan
        "Cuaca": "Baik",
        "Durasi_Hijau": "Optimal", # Lampu sudah dioptimalkan
        "Event": "Tidak",
        "Perbaikan_Jalan": "Tidak",
        "Jalur": "Tersedia_Banyak"
    }
    hasil1 = predictor.predict(kondisi1)
    print(f"\nProbabilitas Kemacetan (Skenario 1): {hasil1['Kemacetan']}")
    print(f"Probabilitas Tidak Kemacetan (Skenario 1): {hasil1['Tidak Kemacetan']}")
    if hasil1['Kemacetan'] > hasil1['Tidak Kemacetan']:
        print("Prediksi: **KEMACETAN TINGGI**")
    else:
        print("Prediksi: **TIDAK TERJADI KEMACETAN**")
    print("-" * 50)

    print("\n===== Skenario 2: Lalu Lintas Lancar =====")
    kondisi2 = {
        "Volume": "Rendah",
        "Kecepatan": "Normal",
        "Antrean": "Pendek",
        "Jam_Puncak": "Tidak",
        "Kecelakaan": "Tidak",
        "Cuaca": "Baik",
        "Durasi_Hijau": "Optimal",
        "Event": "Tidak",
        "Perbaikan_Jalan": "Tidak",
        "Jalur": "Tersedia_Banyak"
    }
    hasil2 = predictor.predict(kondisi2)
    print(f"\nProbabilitas Kemacetan (Skenario 2): {hasil2['Kemacetan']}")
    print(f"Probabilitas Tidak Kemacetan (Skenario 2): {hasil2['Tidak Kemacetan']}")
    if hasil2['Kemacetan'] > hasil2['Tidak Kemacetan']:
        print("Prediksi: **KEMACETAN TINGGI**")
    else:
        print("Prediksi: **TIDAK TERJADI KEMACETAN**")
    print("-" * 50)

    print("\n===== Skenario 3: Kecelakaan di Luar Jam Puncak =====")
    kondisi3 = {
        "Volume": "Rendah", # Volume awal rendah
        "Kecepatan": "Lambat", # Tapi kecepatan mendadak turun
        "Antrean": "Panjang", # Antrean terbentuk
        "Jam_Puncak": "Tidak",
        "Kecelakaan": "Ya", # Kunci: ada kecelakaan
        "Cuaca": "Baik",
        "Durasi_Hijau": "Optimal",
        "Event": "Tidak",
        "Perbaikan_Jalan": "Tidak",
        "Jalur": "Tersedia_Banyak"
    }
    hasil3 = predictor.predict(kondisi3)
    print(f"\nProbabilitas Kemacetan (Skenario 3): {hasil3['Kemacetan']}")
    print(f"Probabilitas Tidak Kemacetan (Skenario 3): {hasil3['Tidak Kemacetan']}")
    if hasil3['Kemacetan'] > hasil3['Tidak Kemacetan']:
        print("Prediksi: **KEMACETAN TINGGI**")
    else:
        print("Prediksi: **TIDAK TERJADI KEMACETAN**")
    print("-" * 50)
