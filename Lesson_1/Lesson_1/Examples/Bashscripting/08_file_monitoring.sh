#!/bin/bash
# Monitors file size changes and prints previous size, current size, and last line when size increases
# Uses stat -f%z for macOS
# Usage: ./10_file_monitoring.sh /Users/user/test.txt
FILENAME="$1"
prevSize="$(stat -f%z "$FILENAME")"
echo "Initial size: $prevSize"
while true; do
    currentSize="$(stat -f%z "$FILENAME")"
    if [[ $currentSize -gt $prevSize ]]; then
        echo "Previous size: $prevSize"
        echo "Current size: $currentSize"
        echo "Appended line: $(tail -1 "$FILENAME")"
        prevSize=$currentSize
    fi
    sleep 1  # Reduce CPU usage
done