import pandas as pd
import numpy as np

# Input and output filenames
input_file = "final_D_ADP_values_x_all.txt"   # change this to your actual input file
output_file = "final_ADP_values_x_average.txt"

# Read the input file
df = pd.read_csv(input_file, sep=r'\s+')

n_rows = len(df)
# Compute deformation potentials column-wise
D_TA = np.sqrt(np.sum(df["D_TA"]**2)/n_rows)
D_TA2 = np.sqrt(np.sum(df["D_TA2"]**2)/n_rows)
D_LA = np.sqrt(np.sum(df["D_LA"]**2)/n_rows)

# Save results to file
with open(output_file, "w") as f:
    f.write("D_TA\tD_TA2\tD_LA\n")
    f.write(f"{D_TA:.6f}\t{D_TA2:.6f}\t{D_LA:.6f}\n")

print(f"Results saved to {output_file}")
