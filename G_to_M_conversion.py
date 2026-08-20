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

band1 = int(sys.argv[1])-8
band2 = int(sys.argv[2])-8
# Define custom band labels mapping
band_label_map = {
    9: 1,
}

# Get custom band labels

print(f"Running conversion for bands {band1} → {band2} in {os.getcwd()}")
#Define Bands 
#band1 = 20
#band2 = 20
# Get custom band labels
custom_band1 = band_label_map.get(band1, band1)  # Use mapping or original if not in map
custom_band2 = band_label_map.get(band2, band2)


# Constants
m1, m2, m3 = 178.49, 58.6934, 118.71
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
omega1_THz, M1_array, Omega_O1 = process_frequency_data('EPW_1.txt')
omega2_THz, M2_array, Omega_O2 = process_frequency_data('EPW_2.txt')
omega3_THz, M3_array, Omega_O3 = process_frequency_data('EPW_3.txt')
omega4_THz, M4_array, Omega_O4 = process_frequency_data('EPW_4.txt')
omega5_THz, M5_array, Omega_O5 = process_frequency_data('EPW_5.txt')
omega6_THz, M6_array, Omega_O6 = process_frequency_data('EPW_6.txt')
omega7_THz, M7_array, Omega_O7 = process_frequency_data('EPW_7.txt')
omega8_THz, M8_array, Omega_O8 = process_frequency_data('EPW_8.txt')
omega9_THz, M9_array, Omega_O9 = process_frequency_data('EPW_9.txt')

# Store Omega_O and nu arrays
Omega_O = [Omega_O1, Omega_O2, Omega_O3, Omega_O4, Omega_O5, Omega_O6, Omega_O7, Omega_O8, Omega_O9]
nu = [omega[:, 0].reshape(-1, 1) for omega in Omega_O]

# === Prepare ODP data ===
omega_ODP_list = [Omega_O1, Omega_O2, Omega_O3, Omega_O4, Omega_O5, Omega_O6, Omega_O7, Omega_O8, Omega_O9]
M_ODP_list = [M1_array, M2_array, M3_array, M4_array, M5_array, M6_array, M7_array, M8_array, M9_array]

# Define x values
#x = np.linspace(0, 0.1, 26)
x = np.linspace(0, 0.1, 8)
#x = np.linspace(0, 0.05, 10)
arrays = [M1_array, M2_array, M3_array, M4_array, M5_array, M6_array, M7_array, M8_array, M9_array]

#save the data
data_dict = {
    'x': x,
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
    'omega_THz_O7': omega7_THz,
    'M_O7': M7_array,
    'omega_THz_O8': omega8_THz,
    'M_O8': M8_array,
    'omega_THz_O9': omega9_THz,
    'M_O9': M9_array,
}

# Create DataFrame and save
df_save = pd.DataFrame(data_dict)
df_save.to_csv('all_modes_matrix_elements.txt', sep='\t', index=False)

# check shapes
print(x.shape)
print(M1_array.shape)
print(M2_array.shape)
# Plotting
plt.rcParams['font.family'] = 'Liberation Serif'
plt.figure(figsize=(10, 6))
for i, arr in enumerate(arrays):
    plt.plot(x, arr, label=f'Optical Mode {i + 1}')
# Compute and plot the average
avg_array = np.mean(arrays, axis=0)
plt.plot(x, avg_array, 'k--', linewidth=2, label='Average')
plt.xlabel('x (fractional coordinate)')
plt.ylabel('Matrix Element (eV)')

# Set y-axis range
plt.ylim(0,5)
plt.title(f'Deformation Potentials for Optical Modes (YNiBi): CBM:{band1}-{band2}')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('deformation_potentials_optical_modes.png')  # Save the figure
#plt.show()


#plt.figure(figsize=(8, 6))
#plt.rcParams['font.family'] = 'Liberation Serif'
#plt.plot(x, M_TA_array, label='TA')
#slope_TA, intercept_TA = np.polyfit(x,M_TA_array,1)
#slope_TA = abs(slope_TA)
#plt.plot(x, M_TA2_array, label='TA2')
#slope_TA2, intercept_TA2 = np.polyfit(x,M_TA2_array,1)
#slope_TA2 = abs(slope_TA2)
#plt.plot(x, M_LA_array, label='LA')
#slope_LA, intercept_LA = np.polyfit(x,M_LA_array,1)
#slope_LA = abs(slope_LA)
#plt.xlabel('x (fractional coordinate)')
#plt.ylabel('Matrix Element (eV)')
#plt.title(f'Deformation for Acoustic Modes (YNiBi): CBM:C$_1$-C$_1$')
#plt.legend()
# --- Minor ticks customization ---
plt.minorticks_on()  # Turn on minor ticks

# Option 1: Automatic placement
#plt.gca().xaxis.set_minor_locator(AutoMinorLocator(10))  # 4 minor ticks per interval
#plt.gca().yaxis.set_minor_locator(AutoMinorLocator(10))

# Option 2 (manual control): specify fixed minor tick spacing
# plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
# plt.gca().yaxis.set_minor_locator(MultipleLocator(0.005))

# Customize appearance
#plt.tick_params(which='major', length=6, width=1.2, direction='inout')
#plt.tick_params(which='minor', length=3, width=0.8, direction='in', color='b')
#plt.text( 0.03, np.amax(np.concatenate([M_LA_array,M_TA_array])), 'Slope_TA : =%1.3f' %slope_TA)
#plt.text( 0.03, np.amax(np.concatenate([M_LA_array,M_TA_array]))-0.01, 'Slope_TA2 : =%1.3f' %slope_TA2)
#plt.text( 0.03, np.amax(np.concatenate([M_LA_array,M_TA_array]))-0.02, 'Slope_LA : =%1.3f' %slope_LA)
#plt.grid(True, which="both", ls="-", alpha=0.3)
#plt.tight_layout()
#plt.savefig('deformation_potentials_acoustic_modes.png')  # Save the figure

# Write slopes to a file in the current folder
#with open("slopes.txt", "w") as f:
#    f.write(f"band1: {band1}, band2: {band2}\n")
#    f.write(f"slope_TA: {slope_TA}\n")
#    f.write(f"slope_TA2: {slope_TA2}\n")
#    f.write(f"slope_LA: {slope_LA}\n")
#
# Optional: also print for logging
#print(f"Slopes saved in {os.path.join(os.getcwd(), 'slopes.txt')}")


# ============================
# === NEW: Compute D_ODP ===
# ============================
# Using raw ODP arrays (no unit conversion). We follow the formula:
# D_ODP = sqrt( omega_ODP * sum_over_modes( sum_over_q ( M^2 / omega_q ) ) )
# where omega_ODP is the mean of per-mode mean omega (raw units).

print("\n=== Computing D_ODP from ODP files ===")

sum_M2_over_omega = 0.0
per_mode_info = []

for i, (omega_arr, M_arr) in enumerate(zip(omega_ODP_list, M_ODP_list), start=1):
    # Convert to float arrays and guard zero omega
    omega_arr = omega_arr[:,0].astype(float)
    M_arr = M_arr[0:,].astype(float)
    #M_arr = np.asarray(M_arr, dtype=float).flatten()

    # Avoid divide by zero: replace zeros with nan so they get ignored in sums
    #omega_safe = np.where(omega_arr == 0.0, np.nan, omega_arr)

    contrib_q = np.divide(M_arr **2, omega_arr)    # shapes are equal now
        # Take per-mode averages
    mean_M2_over_omega = np.nanmean(contrib_q)
    mean_omega_mode = np.nanmean(omega_arr)
    n_q = len(omega_arr)
    #sum_q = np.nansum(contrib_q)
    #mean_omega_mode = np.nanmean(omega_arr)
    #n_q = contrib_q.size

    #contrib_q = np.divide(M_arr ** 2, omega_arr)

    # pick the last q-point instead of summing
    #M2_over_omega_last = contrib_q[-1]           # last element
    #omega_last = omega_arr[-1]                   # corresponding phonon frequency
    n_q = contrib_q.size

    # store per-mode info
    per_mode_info.append((i, n_q, mean_omega_mode, mean_M2_over_omega))
    sum_M2_over_omega += mean_M2_over_omega

    print(f"ODP mode {i}: n_q={n_q}, mean(ω)={mean_omega_mode:.6e}, "
          f"⟨M²/ω⟩={mean_M2_over_omega:.6e}")


    #per_mode_info.append((i, n_q, mean_omega_mode, sum_q))
   # sum_M2_over_omega += sum_q

    #print(f"ODP mode {i}: n_q={n_q}, mean(omega)={mean_omega_mode:.6e}, sum_q(M^2/omega)={sum_q:.6e}")

omega_ODP_raw = np.nanmean([info[2] for info in per_mode_info])
#print(f"ODP omega: {omega_ODP_raw}")
combined_raw = omega_ODP_raw * sum_M2_over_omega
#combined_raw = omega_ODP_raw * M2_over_omega_last
D_ODP_raw = np.sqrt(combined_raw) if combined_raw > 0 and not np.isnan(combined_raw) else np.nan

print("D_ODP_raw =", D_ODP_raw)


# Mean ω across all ODP modes
#omega_ODP_raw = np.nanmean([info[2] for info in per_mode_info])
#mean_ODP = np.divide(omega_ODP_raw,1)

# D_ODP formula (raw units)
#combined_raw = mean_ODP * M2_over_omega_last
#D_ODP_raw = np.sqrt(combined_raw) if combined_raw > 0 and not np.isnan(combined_raw) else np.nan

print("\n=== Optical Deformation Potential (mode-averaged) ===")
print(f"⟨ω_ODP⟩ = {omega_ODP_raw:.6e}")
print(f"Σ_modes ⟨M²/ω⟩ = {sum_M2_over_omega:.6e}")
print(f"D_ODP = sqrt(⟨ω⟩ * Σ ⟨M²/ω⟩) = {D_ODP_raw:.6e}")

# Save to file
with open("D_ODP_result.txt", "w") as f:
    f.write("Optical Deformation Potential (mode-averaged, raw units)\n")
    f.write(f"mean_omega_ODP: {omega_ODP_raw:.12e}\n")
    f.write(f"sum_M2_over_omega: {sum_M2_over_omega:.12e}\n")
    f.write(f"D_ODP_raw: {D_ODP_raw:.12e}\n")

print(f"D_ODP result saved to {os.path.join(os.getcwd(), 'D_ODP_result.txt')}")


# ============================
# USER-SUPPLIED INPUT:
# omega_list  : list of phonon frequencies for ALL branches
# M_list      : list of matrix element arrays for ALL branches
# ============================

# Example naming (ensure your real variables match these names)
# omega_list = omega_all_branches_list
# M_list     = M_all_branches_list
print("\n=== Computing D_IVS using all phonon branches ===")

sum_M2_over_omega = 0.0
per_branch_info = []

all_freq_meV = []
all_M_values = []
all_branch_colors = []
all_branch_ids = []

# unique color for each branch
#colors = plt.colormaps["tab10"].colors
colors = ['blue', 'red' , 'green' , 'dodgerblue', 'olive', 'crimson', 'purple', 'orange', 'brown']  # Different colors

for idx, (omega_arr, M_arr) in enumerate(zip(omega_ODP_list, M_ODP_list)):

    omega_arr = omega_arr[:, 0].astype(float)   # THz
    M_arr     = M_arr.astype(float).flatten()   # matrix elements consistent with THz

    # avoid divide by zero
    omega_safe = np.where(omega_arr == 0, np.nan, omega_arr)

    # M^2 / ω
    contrib_q = (M_arr**2) / omega_safe    

    mean_M2_over_omega = np.nanmean(contrib_q)
    mean_omega_branch  = np.nanmean(omega_arr)

    per_branch_info.append((idx, mean_omega_branch, mean_M2_over_omega))
    sum_M2_over_omega += mean_M2_over_omega

    # convert THz → meV ONLY for plotting X-axis
    omega_meV = omega_arr * 1.000000000   # THz * h = meV

    # store plotting data
    all_freq_meV.extend(omega_meV)
    all_M_values.extend(np.abs(M_arr))
    all_branch_colors.extend([colors[idx % 10]] * len(omega_arr))
    all_branch_ids.extend([idx] * len(omega_arr))  # assign branch ID for legend

    print(f"Branch {idx+1}: <ω>={mean_omega_branch:.6e}, <M²/ω>={mean_M2_over_omega:.6e}")

# compute D_IVS using THz
omega_IVS_mean = np.nanmean([info[1] for info in per_branch_info])
D_IVS = np.sqrt(omega_IVS_mean * sum_M2_over_omega)

print("\n=== Intervalley Deformation Potential (D_IVS) ===")
print(f"⟨ω⟩ (meV) = {omega_IVS_mean:.6e}")
print(f"Σ⟨M²/ω⟩ = {sum_M2_over_omega:.6e}")
print(f"D_IVS = {D_IVS:.6e}\n")

# Save results
with open("D_IVS_result.txt", "w") as f:
    f.write(f"mean_omega (meV): {omega_IVS_mean}\n")
    f.write(f"sum_M2_over_omega: {sum_M2_over_omega}\n")
    f.write(f"D_IVS: {D_IVS}\n")

# ===== PLOT =====
plt.figure(figsize=(10,10))
plt.rcParams['mathtext.fontset'] = 'custom'
         
# 2. Point the custom math styles to Times New Roman
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'
plt.figure(figsize=(10, 10))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.linewidth'] = 3.5  # Default is 0.8

plt.tick_params(axis='both', which='major', labelsize=36, direction='in', length=10, width=2, pad=20)

# Scatter each branch separately with label for legend
for mode_index in range(len(omega_ODP_list)):
    mask = np.array(all_branch_ids) == mode_index
    freq_mode = np.array(all_freq_meV)[mask]
    M_mode    = np.array(all_M_values)[mask]
    plt.scatter(freq_mode, M_mode,
                s=70, alpha=0.8,
                color=colors[mode_index % 10],
                label=f"mode {mode_index+1}")

handles, labels = plt.gca().get_legend_handles_labels()
plt.xlabel("Phonon Frequency [meV]", fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.ylabel(r'|M| [eV $\AA^{-1}$]', fontsize=48, fontfamily='Times New Roman', fontweight='normal', labelpad=20)
plt.xlim(0,30)
plt.ylim(0,1.2)
plt.title("Intervalley CBM:C$_1$", fontsize=48, fontfamily='Times New Roman', fontweight='normal',pad=20)
plt.grid(True, alpha=0.3)
plt.legend(handles[::-1], labels[::-1], handletextpad=0.2, fontsize=36,loc="lower left",bbox_to_anchor=(-0.05, 0.02),markerscale=1.0,frameon=False)
plt.tight_layout()
plt.savefig("M_vs_omega_IVS_colored_ZrNiSn.png")
print("Plot saved as M_vs_omega_IVS_colored.png")



