import pandas as pd
import numpy as np

# Input and output filenames
input_file = "all_slopes.txt"   # change this to your actual input file
output_file = "final_D_ADP_values.txt"

# Read the input file
df = pd.read_csv(input_file, sep=r'\s+')

n_rows = len(df)
# Compute deformation potentials column-wise
D_TA = np.sqrt(np.sum(df["slope_TA"]**2)/n_rows)/1
D_TA2 = np.sqrt(np.sum(df["slope_TA2"]**2)/n_rows)/1
D_LA = np.sqrt(np.sum(df["slope_LA"]**2)/n_rows)/1

# Save results to file
with open(output_file, "w") as f:
    f.write("D_TA\tD_TA2\tD_LA\n")
    f.write(f"{D_TA:.6f}\t{D_TA2:.6f}\t{D_LA:.6f}\n")

print(f"Results saved to {output_file}")
