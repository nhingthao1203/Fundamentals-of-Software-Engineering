#!/bin/bash
first_arg=$1
echo "Your first variable is $first_arg"
for ((i=0; i<$first_arg; i++)); do
    echo $i
done
echo "exit loop"