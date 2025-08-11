#!/bin/bash
my_path="/home/user/example/path"
echo "Replaced the first 'home': ${my_path/home/house}"
IFS="/" read -ra my_array <<< "$my_path" && echo "${my_array[-1]}"
echo "Delete everything up to the last slash: ${my_path##*/}"
echo "Lower case: ${my_path,,}; Upper case: ${my_path^^}"
# Array example
my_array=(10 2 300)
echo "First element: ${my_array[0]}"
echo "Last element: ${my_array[-1]}"
echo "Number of elements: ${#my_array[@]}"
# Write to file
cat << EOF > test.txt
machine learning
data engineering
EOF
# Conditional example
if (( 10 > 9 )); then
    echo "10 > 9 is true"
else
    echo "10 > 9 is false"
fi