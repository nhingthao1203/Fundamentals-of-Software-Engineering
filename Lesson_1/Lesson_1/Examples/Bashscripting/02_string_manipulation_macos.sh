#!/bin/bash
my_path="/Users/user/example/path"
echo "Replaced the first 'home': ${my_path/home/house}"
# Split path into array, avoiding here-string for older Bash compatibility
IFS="/" read -ra my_array <<EOF
$my_path
EOF
# Print last element using portable indexing
echo "Last path component: ${my_array[$(( ${#my_array[@]} - 1 ))]}"
# Delete everything up to the last slash
echo "Delete everything up to the last slash: ${my_path##*/}"
# Case conversion using tr for compatibility
echo "Lower case: $(echo "$my_path" | tr '[:upper:]' '[:lower:]'); Upper case: $(echo "$my_path" | tr '[:lower:]' '[:upper:]')"
# Array example
my_array=(10 2 300)
echo "First element: ${my_array[0]}"
# Print last element using portable indexing
echo "Last element: ${my_array[$(( ${#my_array[@]} - 1 ))]}"
echo "Number of elements: ${#my_array[@]}"
# Write to file
cat << EOF > test.txt
machine learning
data engineering
EOF
# Conditional example
if (( 10 > 9 )); then
    echo10 > 9 is true"
else
    echo "10 > 9 is false"
fi