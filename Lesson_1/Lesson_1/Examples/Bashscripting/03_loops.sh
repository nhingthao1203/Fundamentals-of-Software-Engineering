#!/bin/bash
# If-else example
first_arg=$1
if [ $first_arg -gt 0 ]; then
    echo "First argument is positive"
elif [ $first_arg -eq 0 ]; then
    echo "First argument is zero"
else
    echo "First argument is negative"
fi
# # For loop
# for ((i=0; i<5; i++)); do
#     echo $i
# done
# # While loop
# i=5
# while [ $i -gt 0 ]; do
#     echo $i
#     ((i--))
# done