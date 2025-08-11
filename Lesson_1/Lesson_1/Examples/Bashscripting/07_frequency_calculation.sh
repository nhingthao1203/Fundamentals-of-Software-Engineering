#!/bin/bash
# Calculates frequency of values in the 5th column of CSV files
# Usage: ./09_frequency_calculation.sh /Users/user/data
FOLDERNAME="$1"
filesArr=()
# Loop through CSV files, excluding those with 'copy' in the name
for filename in "$FOLDERNAME"/*.csv; do
    if [[ $filename != *"copy"* && -f "$filename" ]]; then
        tail -n +2 "$filename"
        echo
        filesArr+=("$filename")
    fi
done
flowerSpecies=()
for filename in "${filesArr[@]}"; do
    # Extract 5th column, skip header
    flowerSpecies+=($(awk -F, '{print $5}' "$filename" | tail -n +2))
done
# Sort and count unique values
(IFS=$'\n'; sort <<< "${flowerSpecies[*]}") | uniq -c | sort -n