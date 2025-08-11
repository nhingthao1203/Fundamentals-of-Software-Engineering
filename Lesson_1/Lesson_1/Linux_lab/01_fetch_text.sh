#!/bin/bash

# 01_fetch_text.sh - Basic text fetching script for beginners
# This script downloads Alice in Wonderland from Project Gutenberg
# Perfect for learning basic bash concepts: variables, commands, and output

echo "=== Alice in Wonderland Text Fetcher ==="
echo "This script downloads the famous book from Project Gutenberg"
echo

# Set the URL where the book is located
BOOK_URL="https://www.gutenberg.org/files/11/11-0.txt"

# Set the filename to save the book
OUTPUT_FILE="alice_wonderland.txt"

echo "Downloading Alice in Wonderland..."
echo "From: $BOOK_URL"
echo "To: $OUTPUT_FILE"
echo

# Download the book using curl
# -s = silent mode (no progress bar)
# -o = output to file
curl -s -o "$OUTPUT_FILE" "$BOOK_URL"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download successful!"
    echo
    echo "File information:"
    echo "File size: $(wc -c < "$OUTPUT_FILE") bytes"
    echo "Total lines: $(wc -l < "$OUTPUT_FILE") lines"
    echo "Total words: $(wc -w < "$OUTPUT_FILE") words"
    echo
    echo "First few lines of the book:"
    head -n 10 "$OUTPUT_FILE"
else
    echo "Download failed!"
    echo "Please check your internet connection and try again."
    exit 1
fi

echo
echo "Done! You can now read '$OUTPUT_FILE' or use it with other scripts."