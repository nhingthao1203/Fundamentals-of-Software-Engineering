#!/bin/bash
# Reads a CSV file and prints the last column of each row using a while loop
# Example CSV file: ../data/Employees.csv
filepath="../data/Employees.csv"
my_readfile_func() {
    while read -r line; do
        # Split line into array using IFS=','
        IFS=',' read -ra my_record <<EOF
$line
EOF
        # Print last element using portable indexing
        echo "${my_record[$(( ${#my_record[@]} - 1 ))]}"
    done < "$1"
}
# Run the function with filepath
my_readfile_func "$filepath"