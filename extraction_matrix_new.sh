#!/bin/bash
set -euo pipefail

# Input EPW file
input_file="epw.out"

# List of bands to process
bands=(9)

# Phonon indices range
values=$(seq 1 9)

# Create folders for all band combinations
for b1 in "${bands[@]}"; do
  for b2 in "${bands[@]}"; do
    mkdir -p "${b1}_to_${b2}"
  done
done

echo "Processing data from $input_file ..."

# Extract data for each phonon index and band pair
for i in $values; do
  echo "  -> Processing phonon index $i ..."
  for b1 in "${bands[@]}"; do
    for b2 in "${bands[@]}"; do
      grep -E "^[[:space:]]*$b1[[:space:]]+$b2[[:space:]]+$i[[:space:]]" "$input_file" \
        | cut -c 57-92 > "${b1}_to_${b2}/EPW_${i}.txt"
    done
  done
done

# Master files
master_file_ODP="all_ODP.txt"
echo "band1 band2 D_ODP" > "$master_file_ODP"

master_file_IVS="all_D_IVS.txt"
echo "band1 band2 D_ODP D_IVS omega_IVS" > "$master_file_IVS"

echo "Generating plots and computing deformation potentials ..."

# Loop over bands
for b1 in "${bands[@]}"; do
  for b2 in "${bands[@]}"; do

    # Run Python script
    (
      cd "${b1}_to_${b2}"
      python3 ../G_to_M_conversion.py "$b1" "$b2"
    )

    # --- Extract D_ODP ---
    D_ODP_FILE="${b1}_to_${b2}/D_ODP_result.txt"
    if [[ -f "$D_ODP_FILE" ]]; then
        D_ODP=$(awk -F': ' '/^D_ODP_raw:/ {print $2}' "$D_ODP_FILE")
    else
        echo "Warning: $D_ODP_FILE not found"
        D_ODP=NaN
    fi

    # Append D_ODP to master file
    echo "$b1 $b2 $D_ODP" >> "$master_file_ODP"

    # --- Extract D_IVS and mean frequency ---
    D_IVS_FILE="${b1}_to_${b2}/D_IVS_result.txt"
    if [[ -f "$D_IVS_FILE" ]]; then
        D_IVS=$(awk -F': ' '/^D_IVS:/ {print $2}' "$D_IVS_FILE")
        omega_IVS=$(awk -F': ' '/^mean_omega/ {print $NF}' "$D_IVS_FILE")
    else
        echo "Warning: $D_IVS_FILE not found"
        D_IVS=NaN
        omega_IVS=NaN
    fi

    # Append to IVS master file
    echo "$b1 $b2 $D_ODP $D_IVS $omega_IVS" >> "$master_file_IVS"

  done
done

# Optional: run final plotting script
python3 final_ODP.py

echo "Process completed successfully!"

