import numpy as np

# === Physical constants ===
#hbar_eVs = 4.135667e-15 / (2 * np.pi)  # Planck's constant [eV·s]
#THz_to_eV = hbar_eVs * 1e12             # 1 THz = hbar * ω = 4.1357e-3 eV
#K = 1.0e5  # <-- your prefactor constant (check with your existing code)
# Constants
m1, m2, m3 = 44.956, 58.7000, 121.7600
hbar = 1.0546e-34
M = m1 + m2 + m3
fac = 1.6e-27
K = (2 * M * fac) / hbar

# === Step 1: Load frequencies and matrix elements from each file ===
def process_frequency_data(filename):
    data = np.loadtxt(filename)
    omega_THz = data[:, 0] * 0.242  # convert meV → THz
    matrix_elements = data[:, 1] * np.sqrt(K * omega_THz * 1e12) * 1e-13
    return omega_THz, matrix_elements, data

# Acoustic modes (if needed for reference)
omega_THz_TA, M_TA_array, _ = process_frequency_data("EPW_1.txt")
omega_THz_TA2, M_TA2_array, _ = process_frequency_data("EPW_2.txt")
omega_THz_LA, M_LA_array, _ = process_frequency_data("EPW_3.txt")

# Optical modes (these we use for ODP)
optical_files = [f"EPW_{i}.txt" for i in range(4, 10)]
Omega_O, M_arrays, freq_eV_modes = [], [], []

for fname in optical_files:
    omega_THz, M_array, raw = process_frequency_data(fname)
    Omega_O.append(raw)
    M_arrays.append(M_array)
    freq_eV_modes.append(omega_THz)  # convert THz → eV

# === Step 2: Compute D_ODP^{e-ph} ===

sum_matrix_elements = 0.0
frequencies = []  # store ⟨ω⟩ for each optical mode

for M_mn_nu, omega_eV in zip(M_arrays, freq_eV_modes):
    # element-wise M² / ω
    delta_M_mn_nu = (M_mn_nu ** 2) / omega_eV

    # SUM over q-points
    sum_contrib = np.sum(delta_M_mn_nu)
    sum_matrix_elements += sum_contrib

    # mean ω for this mode
    mean_omega = np.mean(omega_eV)
    frequencies.append(mean_omega)

# mean frequency across optical modes
omega_ODP = np.mean(frequencies)

# combine results
sum_matrix_elements *= omega_ODP
D_ODP_eph = np.sqrt(sum_matrix_elements)

# === Output ===
print("--------------------------------------")
print(f"Mean ω_ODP = {omega_ODP:.4e} eV")
print(f"Σ (M²/ω) (optical) = {sum_matrix_elements/omega_ODP:.4e} eV")
print(f"D_ODP^(e-ph) = {D_ODP_eph:.6e} eV")
print("--------------------------------------")

