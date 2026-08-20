#!/bin/bash
set -euo pipefail

input_file="epw.out"
bands=(6 7 8)   # <== change this list to whatever bands you need
values=$(seq 1 9)   # <== phonon indices range

# Create all combinations of band_i_to_band_j
for b1 in "${bands[@]}"; do
  for b2 in "${bands[@]}"; do
    mkdir -p "${b1}_to_${b2}"
  done
done

echo "Processing data from $input_file ..."

for i in $values; do
  echo "  -> Processing value $i ..."
  for b1 in "${bands[@]}"; do
    for b2 in "${bands[@]}"; do
      grep -E "^[[:space:]]*$b1[[:space:]]+$b2[[:space:]]+$i[[:space:]]" "$input_file" \
        | cut -c 57-92 > "${b1}_to_${b2}/EPW_${i}.txt"
    done
  done
done
##########files for the slope of acoustical modes################
master_file_ADP="all_slopes.txt"
echo "band1 band2 slope_TA slope_TA2 slope_LA" > "$master_file_ADP"

master_file_ODP="all_ODP.txt"
echo "band1 band2 D_ODP" > "$master_file_ODP"

echo "Generating plots ..."
for b1 in "${bands[@]}"; do
  for b2 in "${bands[@]}"; do
    (
      cd "${b1}_to_${b2}"
      python3 ../G_to_M_conversion.py "$b1" "$b2"
    )
     # Append slopes to master file
       slopes=$(awk '
        /^slope_TA: / {ta=$2} 
        /^slope_TA2: / {ta2=$2} 
        /^slope_LA: / {la=$2} 
        END{print ta, ta2, la}' "${b1}_to_${b2}/slopes.txt")
     #slopes=$(awk -F': ' '/slope_TA/ {ta=$2} /slope_TA2/ {ta2=$2} /slope_LA/ {la=$2} END{print ta, ta2, la}' "${b1}_to_${b2}/slopes.txt")
    echo "$b1 $b2 $slopes" >> "$master_file_ADP"
    # Append D_ODP to master file 
       D_ODP=$(awk ' 
        /^D_ODP_raw: / {odp=$2}
        END{print odp}' "${b1}_to_${b2}/D_ODP_result.txt")
    #slope_line=$(awk 'NR>1 {print $3, $4}' "${b1}_to_${b2}/slopes.txt")
        echo "$b1 $b2 $D_ODP" >> "$master_file_ODP"
  done
done

python3 final_D.py
python3 final_ODP.py

echo "Process completed successfully!"
