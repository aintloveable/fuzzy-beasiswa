import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Fuzzy Kelayakan Beasiswa",
    page_icon="🎓"
)

# Judul
st.title("🎓 Sistem Fuzzy Kelayakan Beasiswa")

st.write("""
Aplikasi ini digunakan untuk menentukan tingkat kelayakan
penerima beasiswa berdasarkan nilai IPK menggunakan Logika Fuzzy.
""")

# Input
st.subheader("1. Input IPK")

ipk = st.slider(
    "Masukkan Nilai IPK",
    min_value=0.0,
    max_value=4.0,
    value=3.0,
    step=0.01
)

# Fungsi Keanggotaan
st.subheader("2. Fungsi Keanggotaan")

st.markdown("""
### Tidak Layak
- 1 jika IPK ≤ 1.5
- (2.5 - IPK) jika 1.5 < IPK < 2.5
- 0 jika IPK ≥ 2.5

### Dipertimbangkan
- 0 jika IPK ≤ 1.5 atau ≥ 3.5
- (IPK - 1.5) jika 1.5 < IPK ≤ 2.5
- (3.5 - IPK) jika 2.5 < IPK < 3.5

### Layak
- 0 jika IPK ≤ 2.5
- (IPK - 2.5) jika 2.5 < IPK < 3.5
- 1 jika IPK ≥ 3.5
""")

# Fungsi fuzzy
def tidak_layak(x):
    if x <= 1.5:
        return 1
    elif x < 2.5:
        return 2.5 - x
    else:
        return 0

def dipertimbangkan(x):
    if x <= 1.5 or x >= 3.5:
        return 0
    elif x <= 2.5:
        return x - 1.5
    else:
        return 3.5 - x

def layak(x):
    if x <= 2.5:
        return 0
    elif x < 3.5:
        return x - 2.5
    else:
        return 1

# Perhitungan
mu_tidak = tidak_layak(ipk)
mu_pertimbangan = dipertimbangkan(ipk)
mu_layak = layak(ipk)

st.subheader("3. Perhitungan Derajat Keanggotaan")

st.write(f"μ Tidak Layak = {mu_tidak:.2f}")
st.write(f"μ Dipertimbangkan = {mu_pertimbangan:.2f}")
st.write(f"μ Layak = {mu_layak:.2f}")

# Menentukan kategori
kategori = max(
    {
        "Tidak Layak": mu_tidak,
        "Dipertimbangkan": mu_pertimbangan,
        "Layak": mu_layak
    },
    key=lambda x: {
        "Tidak Layak": mu_tidak,
        "Dipertimbangkan": mu_pertimbangan,
        "Layak": mu_layak
    }[x]
)

# Grafik
st.subheader("4. Grafik Himpunan Fuzzy")

x = np.linspace(0, 4, 500)

y_tidak = [tidak_layak(i) for i in x]
y_pertimbangan = [dipertimbangkan(i) for i in x]
y_layak = [layak(i) for i in x]

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(x, y_tidak, label="Tidak Layak", linewidth=2)
ax.plot(x, y_pertimbangan, label="Dipertimbangkan", linewidth=2)
ax.plot(x, y_layak, label="Layak", linewidth=2)

# Garis IPK
ax.axvline(
    ipk,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'IPK = {ipk:.2f}'
)

# Titik hasil
ax.scatter(ipk, mu_tidak, s=100)
ax.scatter(ipk, mu_pertimbangan, s=100)
ax.scatter(ipk, mu_layak, s=100)

ax.set_xlabel("IPK")
ax.set_ylabel("Derajat Keanggotaan")
ax.set_title("Grafik Fungsi Keanggotaan Kelayakan Beasiswa")
ax.set_xlim(0, 4)
ax.set_ylim(0, 1.1)

ax.grid(True)
ax.legend()

st.pyplot(fig)

# Interpretasi
st.subheader("5. Interpretasi Hasil")

st.success(
    f"IPK {ipk:.2f} termasuk kategori "
    f"{kategori} dengan derajat keanggotaan tertinggi "
    f"{max(mu_tidak, mu_pertimbangan, mu_layak):.2f}"
)

# Ringkasan
st.info(
    f"""
    Ringkasan:
    - IPK : {ipk:.2f}
    - μ Tidak Layak : {mu_tidak:.2f}
    - μ Dipertimbangkan : {mu_pertimbangan:.2f}
    - μ Layak : {mu_layak:.2f}
    - Kategori : {kategori}
    """
)
