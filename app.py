import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fuzzy Beasiswa", page_icon="🎓")

st.title("🎓 Sistem Fuzzy Kelayakan Beasiswa")

st.write("Masukkan nilai IPK mahasiswa untuk mengetahui tingkat kelayakan beasiswa.")

# Input IPK
ipk = st.slider(
    "Masukkan IPK",
    min_value=0.0,
    max_value=4.0,
    value=3.0,
    step=0.01
)

# Fungsi Keanggotaan
def tidak_layak(x):
    if x <= 1.5:
        return 1
    elif 1.5 < x < 2.5:
        return (2.5 - x)
    else:
        return 0

def dipertimbangkan(x):
    if x <= 1.5 or x >= 3.5:
        return 0
    elif 1.5 < x <= 2.5:
        return (x - 1.5)
    elif 2.5 < x < 3.5:
        return (3.5 - x)

def layak(x):
    if x <= 2.5:
        return 0
    elif 2.5 < x < 3.5:
        return (x - 2.5)
    else:
        return 1

# Hitung nilai fuzzy
mu_tidak = tidak_layak(ipk)
mu_dipertimbangkan = dipertimbangkan(ipk)
mu_layak = layak(ipk)

st.subheader("Hasil Fuzzifikasi")

st.write(f"**Tidak Layak:** {mu_tidak:.2f}")
st.write(f"**Dipertimbangkan:** {mu_dipertimbangkan:.2f}")
st.write(f"**Layak:** {mu_layak:.2f}")

# Kesimpulan
hasil = max(
    {
        "Tidak Layak": mu_tidak,
        "Dipertimbangkan": mu_dipertimbangkan,
        "Layak": mu_layak
    },
    key=lambda k: {
        "Tidak Layak": mu_tidak,
        "Dipertimbangkan": mu_dipertimbangkan,
        "Layak": mu_layak
    }[k]
)

st.success(f"Hasil Akhir: {hasil}")

# Grafik Membership Function
x = np.linspace(0, 4, 100)

y_tidak = [tidak_layak(i) for i in x]
y_dipertimbangkan = [dipertimbangkan(i) for i in x]
y_layak = [layak(i) for i in x]

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(x, y_tidak, label="Tidak Layak")
ax.plot(x, y_dipertimbangkan, label="Dipertimbangkan")
ax.plot(x, y_layak, label="Layak")

ax.set_title("Grafik Fungsi Keanggotaan")
ax.set_xlabel("IPK")
ax.set_ylabel("Derajat Keanggotaan")
ax.grid(True)
ax.legend()

st.pyplot(fig)
