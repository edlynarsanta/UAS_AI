import numpy as np
import pandas as pd

# Contoh data
data = {
    'volume_kendaraan': [100, 200, 300, 400, 500],
    'kecepatan_rata': [40, 30, 20, 10, 5],
    'kemacetan': [0, 0, 1, 1, 1]  # 0: tidak macet, 1: macet
}

df = pd.DataFrame(data)

# Menghitung probabilitas kemacetan
def hitung_probabilitas_kemacetan(volume, kecepatan):
    P_C = df['kemacetan'].mean()  # P(C)
    P_K_given_C = len(df[(df['kemacetan'] == 1) & (df['volume_kendaraan'] == volume) & (df['kecepatan_rata'] == kecepatan)]) / len(df[df['kemacetan'] == 1])  # P(K | C)
    P_K = len(df[(df['volume_kendaraan'] == volume) & (df['kecepatan_rata'] == kecepatan)]) / len(df)  # P(K)
    
    if P_K == 0:
        return 0  # Menghindari pembagian dengan nol
    
    P_C_given_K = (P_K_given_C * P_C) / P_K  # P(C | K)
    return P_C_given_K

# Contoh penggunaan
probabilitas_kemacetan = hitung_probabilitas_kemacetan(300, 20)
print(f'Probabilitas kemacetan: {probabilitas_kemacetan:.2f}')
