#conda install numpy scipy pandas matplotlib
import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

if len(sys.argv) != 3:
    print("Usage: python G_to_M_conversion.py <band1> <band2>")
    sys.exit(1)

band1 = np.abs(int(sys.argv[1])-9)
band2 = np.abs(int(sys.argv[2])-9)

# Define custom band labels mapping
band_label_map = {
    6: 3,
    7: 2, 
    8: 1
}

# Get custom band labels
custom_band1 = band_label_map.get(band1, band1)  # Use mapping or original if not in map
custom_band2 = band_label_map.get(band2, band2)

print(f"Running conversion for bands {band1}→{band2} (displayed as {custom_band1}→{custom_band2}) in {os.getcwd()}")

# Constants
m1, m2, m3 = 92.224, 58.6934, 118.71
#m1, m2, m3 = 178.49, 58.6934, 118.71
hbar = 1.0546e-34
M = m1 + m2 + m3
fac = 1.6e-27
K = (2 * M * fac) / hbar

# Function to process each file
def process_frequency_data(filename):
    data = np.loadtxt(filename)
    omega_THz = data[:, 0] * 0.242  # Convert meV to THz
    matrix_elements = data[:, 1] * np.sqrt(K * omega_THz * 1e12) * 1e-13
    return omega_THz, matrix_elements, data

# Acoustic modes
omega_THz_TA, M_TA_array, Omega_TA = process_frequency_data('EPW_1.txt')
omega_THz_TA2, M_TA2_array, Omega_TA2 = process_frequency_data('EPW_2.txt')
omega_THz, M_LA_array, Omega_LA = process_frequency_data('EPW_3.txt')

# Optical modes
omega1_THz, M1_array, Omega_O1 = process_frequency_data('EPW_4.txt')
omega2_THz, M2_array, Omega_O2 = process_frequency_data('EPW_5.txt')
omega3_THz, M3_array, Omega_O3 = process_frequency_data('EPW_6.txt')
omega4_THz, M4_array, Omega_O4 = process_frequency_data('EPW_7.txt')
omega5_THz, M5_array, Omega_O5 = process_frequency_data('EPW_8.txt')
omega6_THz, M6_array, Omega_O6 = process_frequency_data('EPW_9.txt')

# Store Omega_O and nu arrays
Omega_O = [Omega_O1, Omega_O2, Omega_O3, Omega_O4, Omega_O5, Omega_O6]
nu = [omega[:, 0].reshape(-1, 1) for omega in Omega_O]

# === Prepare ODP data ===
omega_ODP_list = [Omega_O1, Omega_O2, Omega_O3, Omega_O4, Omega_O5, Omega_O6]
M_ODP_list = [M1_array, M2_array, M3_array, M4_array, M5_array, M6_array]

# Define x values
x = np.linspace(0, 0.1, 26)
arrays = [M1_array, M2_array, M3_array, M4_array, M5_array, M6_array]

# Save the data
data_dict = {
    'x': x,
    'omega_THz_TA': omega_THz_TA,
    'M_TA': M_TA_array,
    'omega_THz_TA2': omega_THz_TA2,
    'M_TA2': M_TA2_array,
    'omega_THz_LA': omega_THz,
    'M_LA': M_LA_array,
    'omega_THz_O1': omega1_THz,
    'M_O1': M1_array,
    'omega_THz_O2': omega2_THz,
    'M_O2': M2_array,
    'omega_THz_O3': omega3_THz,
    'M_O3': M3_array,
    'omega_THz_O4': omega4_THz,
    'M_O4': M4_array,
    'omega_THz_O5': omega5_THz,
    'M_O5': M5_array,
    'omega_THz_O6': omega6_THz,
    'M_O6': M6_array,
}

# Create DataFrame and save
df_save = pd.DataFrame(data_dict)
df_save.to_csv('all_modes_matrix_elements.txt', sep='\t', index=False)

# Check shapes
print(x.shape)
print(M1_array.shape)
print(M2_array.shape)

# Plotting - Optical Modes (ODP) - SCATTER ONLY
plt.rcParams['mathtext.fontset'] = 'custom'

# 2. Point the custom math styles to Times New Roman
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'
plt.figure(figsize=(10, 10))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.linewidth'] = 3.5  # Default is 0.8


# Different markers for different optical modes
markers = ['o', 'o', 'o', 'o', 'o', 'o']  # Different marker styles
colors = ['dodgerblue', 'olive', 'crimson', 'purple', 'orange', 'brown']  # Different colors

# Different dash patterns for lines
dash_patterns = ['--', '-.', ':', (0, (3, 5, 1, 5)), (0, (5, 5)), (0, (5, 1))]

for i, (arr, marker, color, dash_patterns) in enumerate(zip(arrays, markers, colors, dash_patterns)):
    plt.plot(x, arr, label=f'mode {i + 4}', 
                marker=marker, color=color, linestyle=dash_patterns,
             markersize=15, markeredgecolor='black', markeredgewidth=0.0,
             linewidth=1.5, alpha=0.8 )

plt.xlabel(r'q [2 $\pi$/a] ($\Gamma$-K)', fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.ylabel(r'|M| [eV $\AA^{-1}$]', fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.figtext(0.5, 0.86, 'Short range', ha='center', fontsize=48, fontfamily='Times New Roman', fontweight='normal')

# Set y-axis range
plt.xlim(0,0.1)
plt.ylim(0,3)
plt.title(f'Optical Modes VBM:V$_{{{custom_band1}}}$-V$_{{{custom_band2}}}$', fontsize=48, fontfamily='Times New Roman', fontweight='normal', pad=20)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[::-1], labels[::-1],loc='upper left', 
           bbox_to_anchor=(0.48, 0.95),  # (x, y) position: x=center, y=88% from bottom
           fontsize=36, frameon=False)
# --- Minor ticks customization ---
# --- Custom x-tick labels ---
# Set custom tick positions and labels
custom_xticks = [0, 0.02, 0.04, 0.06, 0.08, 0.1]
custom_xtick_labels = ['0', '0.02', '0.04', '0.06', '0.08', '0.1']
custom_yticks = [0, 1.0, 2.0, 3.0, 4.0]
custom_ytick_labels = ['0', '1.0', '2.0', '3.0', '4.0']

plt.xticks(ticks=custom_xticks, labels=custom_xtick_labels,
           fontsize=48, fontfamily='Times New Roman')
plt.yticks(ticks=custom_yticks, labels=custom_ytick_labels,
           fontsize=48, fontfamily='Times New Roman')
plt.minorticks_on()
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(1))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(1))

# Customize appearance
plt.tick_params(which='major', length=6, width=1.2, direction='in', labelsize='36', pad=20)
plt.tick_params(which='minor', length=3, width=0.8, direction='in', labelsize='36', pad=20)
plt.tight_layout(pad=1.0)
plt.savefig('deformation_potentials_optical_modes.png')
plt.close()

# Plotting - Acoustic Modes (ADP) - SCATTER ONLY
plt.rcParams['mathtext.fontset'] = 'custom'

# 2. Point the custom math styles to Times New Roman
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'
plt.figure(figsize=(10, 10))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.linewidth'] = 3.5  # Default is 0.8

# Scatter plot for TA mode
plt.plot(x, M_TA_array, label='mode 1', 
         marker='o', color='blue', linestyle='--',
         markersize=15, markeredgecolor='black', markeredgewidth=0.0,
         linewidth=1.5, alpha=0.8)
slope_TA, intercept_TA = np.polyfit(x, M_TA_array, 1)
slope_TA = abs(slope_TA)

# Scatter plot for TA2 mode
plt.plot(x, M_TA2_array, label='mode 2', 
         marker='s', color='red', linestyle='-.',
         markersize=15, markeredgecolor='black', markeredgewidth=0.0,
         linewidth=1.5, alpha=0.8)
slope_TA2, intercept_TA2 = np.polyfit(x, M_TA2_array, 1)
slope_TA2 = abs(slope_TA2)

# Scatter plot for LA mode
#x_filtered = np.delete(x, [1,2])
#y_filtered = np.delete(M_LA_array, [1,2])
plt.plot(x, M_LA_array, label='mode 3', 
         marker='^', color='green', linestyle=':',
         markersize=15, markeredgecolor='black', markeredgewidth=0.0,
         linewidth=1.5, alpha=0.8)
slope_LA, intercept_LA = np.polyfit(x, M_LA_array, 1)
slope_LA = abs(slope_LA)

plt.xlabel(r'q [2 $\pi$/a] ($\Gamma$-K)', fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.ylabel(r'|M| [eV $\AA^{-1}$]', fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.title(f'Acoustic Modes VBM:V$_{{{custom_band1}}}$-V$_{{{custom_band2}}}$', fontsize=48, fontfamily='Times New Roman', fontweight='normal',pad=20)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[::-1], labels[::-1],loc='upper right',
           bbox_to_anchor=(0.50, 0.79),  # (x, y) position: x=center, y=88% from bottom
           fontsize=36, frameon=False)

plt.xlim(0,0.1)
plt.ylim(0,np.max(np.concatenate([M_LA_array, M_TA_array, M_TA2_array]))+0.05)
# --- Custom x-tick labels ---
# Set custom tick positions and labels
custom_xticks = [0, 0.02, 0.04, 0.06, 0.08, 0.1]
custom_xtick_labels = ['0', '0.02', '0.04', '0.06', '0.08', '0.1']
custom_yticks = [0, 0.1, 0.2, 0.3]
custom_ytick_labels = ['0', '0.1', '0.2', '0.3']

plt.xticks(ticks=custom_xticks, labels=custom_xtick_labels,
           fontsize=48, fontfamily='Times New Roman')
plt.yticks(ticks=custom_yticks, labels=custom_ytick_labels,
           fontsize=48, fontfamily='Times New Roman')
# --- Minor ticks customization ---
plt.minorticks_on()
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(1))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(1))

# Customize appearance
plt.tick_params(which='major', length=6, width=1.2, direction='in', labelsize='36', pad=20)
plt.tick_params(which='minor', length=3, width=0.8, direction='in', labelsize='36', pad=20)

plt.tight_layout(pad=1.0)
plt.savefig('deformation_potentials_acoustic_modes.png')
plt.close()

# Write slopes to a file in the current folder
with open("slopes.txt", "w") as f:
    f.write(f"original_bands: {band1} → {band2}\n")
    f.write(f"display_bands: {custom_band1} → {custom_band2}\n")
    f.write(f"slope_TA: {slope_TA}\n")
    f.write(f"slope_TA2: {slope_TA2}\n")
    f.write(f"slope_LA: {slope_LA}\n")

print(f"Slopes saved in {os.path.join(os.getcwd(), 'slopes.txt')}")

# ============================
# === Compute D_ODP ===
# ============================
print("\n=== Computing D_ODP from ODP files ===")

sum_M2_over_omega = 0.0
per_mode_info = []

for i, (omega_arr, M_arr) in enumerate(zip(omega_ODP_list, M_ODP_list), start=1):
    # Convert to float arrays
    omega_arr = omega_arr[:,0].astype(float)
    M_arr = M_arr[0:,].astype(float)
    
    # Avoid divide by zero
    omega_safe = np.where(omega_arr == 0.0, np.nan, omega_arr)
    
    # Calculate contribution
    contrib_q = np.divide(M_arr ** 2, omega_safe)
    
    # Take per-mode averages
    mean_M2_over_omega = np.nanmean(contrib_q)
    mean_omega_mode = np.nanmean(omega_safe)
    n_q = len(omega_arr)
    
    # Store per-mode info
    per_mode_info.append((i, n_q, mean_omega_mode, mean_M2_over_omega))
    sum_M2_over_omega += mean_M2_over_omega
    
    print(f"ODP mode {i}: n_q={n_q}, mean(ω)={mean_omega_mode:.6e}, "
          f"⟨M²/ω⟩={mean_M2_over_omega:.6e}")

# Mean ω across all ODP modes
omega_ODP_raw = np.nanmean([info[2] for info in per_mode_info])
combined_raw = omega_ODP_raw * sum_M2_over_omega
D_ODP_raw = np.sqrt(combined_raw) if combined_raw > 0 and not np.isnan(combined_raw) else np.nan

print("\n=== Optical Deformation Potential (mode-averaged) ===")
print(f"⟨ω_ODP⟩ = {omega_ODP_raw:.6e}")
print(f"Σ_modes ⟨M²/ω⟩ = {sum_M2_over_omega:.6e}")
print(f"D_ODP = sqrt(⟨ω⟩ * Σ ⟨M²/ω⟩) = {D_ODP_raw:.6e}")

# Save to file
with open("D_ODP_result.txt", "w") as f:
    f.write(f"Band transition: {custom_band1} → {custom_band2}\n")
    f.write(f"Original bands: {band1} → {band2}\n")
    f.write(f"mean_omega_ODP: {omega_ODP_raw:.12e}\n")
    f.write(f"sum_M2_over_omega: {sum_M2_over_omega:.12e}\n")
    f.write(f"D_ODP_raw: {D_ODP_raw:.12e}\n")

print(f"D_ODP result saved to {os.path.join(os.getcwd(), 'D_ODP_result.txt')}")
