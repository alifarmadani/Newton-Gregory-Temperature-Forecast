import streamlit as st
import matplotlib.pyplot as plt
import numpy as np  # untuk membuat titik interpolasi

def newton_gregory_forward(x_values, y_values, target_x):
    n = len(x_values)
    h = x_values[1] - x_values[0]  # Asumsi interval tetap
    diff_table = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        diff_table[i][0] = y_values[i]

    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    p = (target_x - x_values[0]) / h
    result = y_values[0]
    p_term = 1

    for i in range(1, n):
        p_term *= (p - i + 1) / i
        result += p_term * diff_table[0][i]

    return result, diff_table

# Streamlit UI
st.set_page_config(page_title="Prediksi Suhu - Newton Gregory", layout="centered")

st.title("Prediksi Suhu Harian dengan Newton-Gregory")
st.markdown("Masukkan data suhu secara berkala (misalnya per jam):")

x_values = st.text_input("Masukkan daftar jam (pisahkan dengan koma)", "8,9,10,11")
y_values = st.text_input("Masukkan daftar suhu (pisahkan dengan koma)", "24,26,28,31")
target_x = st.number_input("Jam yang ingin diprediksi (misal: 10.5)", value=10.5, step=0.1)

if st.button("Prediksi"):
    try:
        x = [float(i) for i in x_values.split(",")]
        y = [float(i) for i in y_values.split(",")]

        if len(x) != len(y):
            st.error("Jumlah jam dan suhu harus sama.")
        elif len(x) < 2:
            st.error("Minimal masukkan 2 data.")
        else:
            hasil, tabel = newton_gregory_forward(x, y, target_x)
            st.success(f"Prediksi suhu pada jam {target_x} adalah: **{hasil:.2f} °C**")

            st.subheader("Tabel Beda Hingga:")
            tabel_terformat = []
            for i in range(len(tabel)):
                row = []
                for j in range(len(tabel[i])):
                    if j <= len(tabel) - i - 1:
                        row.append(tabel[i][j])
                    else:
                        row.append("")
                tabel_terformat.append(row)
            st.table(tabel_terformat)

            # Grafik interpolasi dan data asli
            st.subheader("Grafik Kurva Interpolasi dan Data Asli")

            # Titik-titik kurva interpolasi
            x_interp = np.linspace(min(x), max(x), 100)
            y_interp = [newton_gregory_forward(x, y, xi)[0] for xi in x_interp]

            # Plot grafik
            fig, ax = plt.subplots()
            ax.plot(x, y, 'bo-', label="Data Asli")
            ax.plot(x_interp, y_interp, 'g--', label="Kurva Interpolasi")
            ax.scatter(target_x, hasil, color='red', label=f"Prediksi ({target_x}, {hasil:.2f})", zorder=5)
            ax.set_xlabel("Jam")
            ax.set_ylabel("Suhu (°C)")
            ax.set_title("Kurva Interpolasi Newton-Gregory")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
