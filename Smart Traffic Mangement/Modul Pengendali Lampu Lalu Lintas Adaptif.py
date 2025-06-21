class TrafficLightController:
    def __init__(self, persimpangan_id, default_duration=30):
        self.persimpangan_id = persimpangan_id
        self.default_duration = default_duration # detik
        self.lampu_saat_ini = "merah" # default, bisa diatur hijau
        self.arah_hijau = None

    def set_light_status(self, arah, status):
        """
        Mensimulasikan perubahan status lampu.
        Dalam sistem nyata, ini akan mengirim perintah ke hardware lampu lalu lintas.
        """
        print(f"  --> Lampu {arah.replace('_', ' ').title()} sekarang: {status.upper()} <--")
        self.lampu_saat_ini = status
        if status == "hijau":
            self.arah_hijau = arah

    def optimize_light_duration(self, kondisi_arah, prediksi_kepadatan):
        """
        Menentukan durasi lampu hijau berdasarkan kondisi lalu lintas.
        Menggunakan kombinasi skor kepadatan saat ini dan prediksi.
        """
        print(f"\n--- Mengoptimalkan Durasi Lampu Lalu Lintas untuk {self.persimpangan_id} ---")

        # Prioritaskan arah dengan skor kepadatan tertinggi
        arah_prioritas = max(kondisi_arah, key=lambda k: kondisi_arah[k]['skor_kepadatan'])
        
        # Bobotkan durasi berdasarkan kepadatan
        # Logika ini bisa jauh lebih kompleks, melibatkan fuzzy logic atau reinforcement learning
        durasi_hijau = {}
        total_skor_kepadatan = sum(data['skor_kepadatan'] for data in kondisi_arah.values())

        if total_skor_kepadatan == 0: # Hindari pembagian nol
            for arah in kondisi_arah:
                durasi_hijau[arah] = self.default_duration
        else:
            for arah, data in kondisi_arah.items():
                proporsi = data['skor_kepadatan'] / total_skor_kepadatan
                # Durasi minimum dan maksimum bisa diatur
                durasi = self.default_duration * (1 + proporsi * 1.5) # Bobot lebih tinggi untuk yang padat
                durasi_hijau[arah] = int(min(max(durasi, 15), 60)) # Min 15s, Max 60s

        print(f"  Durasi lampu hijau yang direkomendasikan:")
        for arah, durasi in durasi_hijau.items():
            print(f"    {arah.replace('_', ' ').title()}: {durasi} detik")
        
        # Contoh sederhana: putar lampu hijau ke arah terpadat dulu
        urutan_arah = sorted(kondisi_arah, key=lambda k: kondisi_arah[k]['skor_kepadatan'], reverse=True)
        print(f"\n  Urutan prioritas lampu hijau: {[a.replace('_', ' ').title() for a in urutan_arah]}")

        # Implementasi sederhana: atur lampu secara berurutan
        for i, arah in enumerate(urutan_arah):
            self.set_light_status(arah, "hijau")
            print(f"  Lampu {arah.replace('_', ' ').title()} hijau selama {durasi_hijau[arah]} detik.")
            # Dalam sistem nyata, ada fase kuning antar hijau
            # Waktu tunggu simulasi (misalnya: time.sleep(durasi_hijau[arah]))
            self.set_light_status(arah, "merah") # Kembali merah setelah durasi

        print("\n--- Pengaturan Lampu Lalu Lintas Selesai ---")

# --- Contoh Penggunaan Modul Pengendali Lampu Lalu Lintas ---
# controller = TrafficLightController("P001")
# controller.optimize_light_duration(kondisi_saat_ini, prediksi_masa_depan)
