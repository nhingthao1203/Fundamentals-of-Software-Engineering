#!/bin/bash
# Lists all .sh files in the current directory using a for loop
echo "All the .sh files in the current directory:"
for i in ./*.sh; do
    # Check if file exists to handle case when no .sh files are found
    if [ -f "$i" ]; then
        echo "$i"
    fi
done