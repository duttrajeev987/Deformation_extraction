#!/bin/bash

# Create main results directory
mkdir -p epw_xpoints_results

# Array mapping coordinates to folder names
declare -A file_mapping=(
    ["5_0_5"]="epw_x1_5000000000_0000000000_5000000000.out"
    ["5_5_0"]="epw_x2_5000000000_5000000000_0000000000.out"
    ["0_5_5"]="epw_x3_0000000000_5000000000_5000000000.out"
    ["n5_0_n5"]="epw_x4__5000000000_0000000000__5000000000.out"  # Check actual filename
    ["n5_n5_0"]="epw_x5__5000000000__5000000000_0000000000.out"  # Check actual filename
    ["0_n5_n5"]="epw_x6_0000000000__5000000000__5000000000.out"  # Check actual filename
)

echo "Please update the file_mapping array with your actual filenames:"
ls -1 epw_results/

# Initialize final output files
final_adp_file="final_D_ADP_values_x_all.txt"
final_odp_file="final_D_ODP_values_x_all.txt"

# Create headers for final files
echo "folder_name D_TA D_TA2 D_LA" > "$final_adp_file"
echo "folder_name D_ODP" > "$final_odp_file"

# Process each folder
for folder_name in "${!file_mapping[@]}"; do
    filename="${file_mapping[$folder_name]}"
    
    echo "=================================================="
    echo "Processing: $folder_name"
    echo "Looking for: $filename"
    echo "=================================================="
    
    # Create folder
    mkdir -p "epw_xpoints_results/$folder_name"
    
    # Find and copy the corresponding epw.out file
    # Look for files with the coordinates in the name
    coord_pattern=$(echo "$coords" | sed 's/\.//g' | sed 's/-\?0*\([0-9]*\)/\1/g' | sed 's/  */_/g' | sed 's/_$//')
    
    echo "Looking for files with pattern: *${coord_pattern}*"
    
    # Find the epw.out file
    if [ -f "epw_results/$filename" ]; then
        echo "Found file: epw_results/$filename"
        
        # Copy EPW file
        cp "epw_results/$filename" "epw_xpoints_results/$folder_name/epw.out"
        
        # Also copy the original onepoint.dat if available
        onepoint_file=$(find epw_results -name "*${coord_pattern}*.dat" -type f | head -1)
        if [ -n "$onepoint_file" ] && [ -f "$onepoint_file" ]; then
            cp "$onepoint_file" "epw_xpoints_results/$folder_name/onepoint.dat"
        fi
        
        # Copy the extraction script
        if [ -f "extraction_matrix_new.sh" ]; then
            cp "extraction_matrix_new.sh" "epw_xpoints_results/$folder_name/"
            cp *.py "epw_xpoints_results/$folder_name/"
            
            # Change to the folder and run the extraction script
            cd "epw_xpoints_results/$folder_name"
            echo "Running extraction script in $(pwd)"
            
            # Make the script executable and run it
            #chmod +x extraction_matrix_new.sh
            ./extraction_matrix_new.sh


            # Extract values from final files and append to consolidated files
            if [ -f "final_D_ADP_values.txt" ]; then
                # Read ADP values (skip header if exists)
                adp_values=$(tail -1 "final_D_ADP_values.txt" | awk '{print $1, $2, $3}')
                echo "$folder_name $adp_values" >> "../../$final_adp_file"
                echo "Added ADP values for $folder_name: $adp_values"
            else
                echo "Warning: final_D_ADP_values.txt not found in $folder_name"
            fi
            
            if [ -f "final_D_ODP_values.txt" ]; then
                # Read ODP value (skip header if exists)
                odp_value=$(tail -1 "final_D_ODP_values.txt" | awk '{print $1}')
                echo "$folder_name $odp_value" >> "../../$final_odp_file"
                echo "Added ODP value for $folder_name: $odp_value"
            else
                echo "Warning: final_D_ODP_values.txt not found in $folder_name"
            fi

            
            # Return to original directory
            cd ../..
            
            echo "Extraction completed for $folder_name"
        else
            echo "Warning: extraction_matrix_new.sh not found in current directory"
        fi
    else
        echo "Warning: No EPW output file found for coordinates: $coords"
        echo "Searched for pattern: *${coord_pattern}*"
    fi
    
    echo ""
done

echo "=================================================="
echo "All processing completed!"
echo "Results organized in epw_xpoints_results/"
echo "=================================================="

# Show final directory structure
echo "Final directory structure:"
tree epw_xpoints_results/ || ls -la epw_xpoints_results/
