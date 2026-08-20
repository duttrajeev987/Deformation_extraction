import pandas as pd
import numpy as np

# Input and output filenames
input_file = "all_ODP.txt"   # change this to your actual input file
output_file = "final_D_ODP_values.txt"

# Read the input file
df = pd.read_csv(input_file, sep=r'\s+')

n_rows = len(df)
# Compute deformation potentials column-wise
D_ODP = np.sqrt(np.sum(df["D_ODP"]**2)/n_rows)/1

# Save results to file
with open(output_file, "w") as f:
    f.write("D_ODP\n")
    f.write(f"{D_ODP:.6f}\n")

print(f"Results saved to {output_file}")
