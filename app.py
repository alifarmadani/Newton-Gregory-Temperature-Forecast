import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Load CSS
def load_css(file_path):
    with open(file_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Wrap content
st.markdown('<div class="content"><h1>Newton-Gregory Interpolation</h1>', unsafe_allow_html=True)

# Header
st.markdown('<h3>Masukkan Data Jam dan Suhu</h3>', unsafe_allow_html=True)
# Newton-Gregory Function
def newton_gregory_forward(x_values, y_values, target_x):
    n = len(x_values)
    h = x_values[1] - x_values[0]
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

# Session state
if 'rows' not in st.session_state:
    st.session_state.rows = [
        {'jam': 06.0, 'suhu': 34.0},
        {'jam': 12.0, 'suhu': 33.0},
        {'jam': 17.0, 'suhu': 32.0},
        {'jam': 24.0, 'suhu': 28.0}
    ]

# Input Form
new_rows = []
for idx, row in enumerate(st.session_state.rows):
    with st.container():
        cols = st.columns([2, 2, 1])
        with cols[0]:
            jam = st.number_input(f"Jam {idx+1}", key=f"jam_{idx}", value=row['jam'], step=0.1, label_visibility="visible")
        with cols[1]:
            suhu = st.number_input(f"Suhu {idx+1}", key=f"suhu_{idx}", value=row['suhu'], step=0.1, label_visibility="visible")
        with cols[2]:
            st.markdown("<div style='height: 1.8em;'></div>", unsafe_allow_html=True)
            if st.button("❌", key=f"remove_{idx}"):
                continue
        new_rows.append({'jam': jam, 'suhu': suhu})

st.session_state.rows = new_rows

# Tombol tambah jam
if st.button("➕ Tambah Jam"):
    st.session_state.rows.append({'jam': 0.0, 'suhu': 0.0})

st.markdown("<hr>", unsafe_allow_html=True)

# Input jam yang ingin diprediksi
st.markdown('<h3>Prediksi Suhu</h3>', unsafe_allow_html=True)
target_x = st.number_input("Masukkan jam yang ingin diprediksi", value=10.0, step=0.1)

# Tombol prediksi
if st.button("Prediksi Sekarang"):
    x = [row['jam'] for row in st.session_state.rows]
    y = [row['suhu'] for row in st.session_state.rows]

    if len(x) < 2:
        st.markdown('<div class="stError">Masukkan minimal 2 data jam dan suhu.</div>', unsafe_allow_html=True)
    else:
        hasil, tabel = newton_gregory_forward(x, y, target_x)
        st.markdown(f'<div class="stSuccess">Prediksi suhu pada jam {target_x:.2f} adalah <strong>{hasil:.2f} °C</strong></div>', unsafe_allow_html=True)

        st.markdown('<h3>Tabel Beda Hingga:</h3>', unsafe_allow_html=True)
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

        st.markdown('<h3>Grafik Interpolasi</h3>', unsafe_allow_html=True)
        x_interp = np.linspace(min(x), max(x), 100)
        y_interp = [newton_gregory_forward(x, y, xi)[0] for xi in x_interp]

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

# Close content wrapper
st.markdown('</div>', unsafe_allow_html=True)
