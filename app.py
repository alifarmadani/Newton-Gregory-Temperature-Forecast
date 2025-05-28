import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Newton-Gregory Interpolation", layout="centered")

# Newton-Gregory function
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

# Inisialisasi session_state
if 'rows' not in st.session_state:
    st.session_state.rows = [
        {'jam': 12.0, 'suhu': 34.0},
        {'jam': 15.0, 'suhu': 33.0},
        {'jam': 18.0, 'suhu': 32.0},
        {'jam': 21.0, 'suhu': 28.0}
    ]

# Gaya khusus untuk tombol Remove
remove_button_style = """
    <style>
    .stButton button {
        background-color: #0000;
        color: white;
        border-radius: 6px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    .stButton button:hover {
        background-color: #e33e3e;
    }
    </style>
"""
st.markdown(remove_button_style, unsafe_allow_html=True)

st.title("Newton-Gregory Interpolation")
st.subheader("Masukkan Data Jam dan Suhu")

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
st.markdown(" ")
if st.button("➕ Tambah Jam"):
    st.session_state.rows.append({'jam': 0.0, 'suhu': 0.0})

st.markdown("---")

# Input jam yang ingin diprediksi
st.subheader("Prediksi Suhu")
target_x = st.number_input("Masukkan jam yang ingin diprediksi", value=10.0, step=0.1)

# Tombol prediksi
if st.button("Prediksi Sekarang"):
    x = [row['jam'] for row in st.session_state.rows]
    y = [row['suhu'] for row in st.session_state.rows]

    if len(x) < 2:
        st.error("Masukkan minimal 2 data jam dan suhu.")
    else:
        hasil, tabel = newton_gregory_forward(x, y, target_x)
        st.success(f"Prediksi suhu pada jam {target_x:.2f} adalah {hasil:.2f} °C")

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

        st.subheader("Grafik Interpolasi")
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
