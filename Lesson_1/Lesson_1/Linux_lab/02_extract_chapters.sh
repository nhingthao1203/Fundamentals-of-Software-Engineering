#!/bin/bash

# 02_extract_chapters.sh - Chapter extraction script for beginners
# This script extracts individual chapters from Alice in Wonderland
# Learn: loops, text processing, file operations, and pattern matching

echo "=== Alice in Wonderland Chapter Extractor ==="
echo "This script separates the book into individual chapter files"
echo

# Input file (the book we downloaded)
INPUT_FILE="alice_wonderland.txt"

# Directory to store chapters
CHAPTERS_DIR="chapters"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found!"
    echo "Please run 01_fetch_text.sh first to download the book."
    exit 1
fi

# Create chapters directory
echo "Creating chapters directory..."
mkdir -p "$CHAPTERS_DIR"

echo "Extracting chapters from $INPUT_FILE..."
echo

# Initialize variables
chapter_num=0
current_file=""
in_chapter=false

# Process the file line by line
while IFS= read -r line; do
    # Check if line starts with "CHAPTER" (indicates start of new chapter)
    if [[ "$line" =~ ^CHAPTER ]]; then
        # Close previous chapter file if open
        if [ "$in_chapter" = true ]; then
            echo "Saved: $current_file"
        fi
        
        # Extract chapter number and title
        chapter_info=$(echo "$line" | sed 's/CHAPTER //')
        chapter_num=$((chapter_num + 1))
        
        # Create new chapter filename
        current_file="$CHAPTERS_DIR/chapter_$(printf "%02d" $chapter_num).txt"
        
        echo "Processing: $line"
        
        # Start new chapter file with the chapter header
        echo "$line" > "$current_file"
        in_chapter=true
        
    elif [ "$in_chapter" = true ]; then
        # Add line to current chapter file
        echo "$line" >> "$current_file"
    fi
    
done < "$INPUT_FILE"

# Close the last chapter
if [ "$in_chapter" = true ]; then
    echo " Saved: $current_file"
fi

echo
echo "Chapter extraction complete!"
echo "Summary:"
echo "Total chapters extracted: $chapter_num"
echo "Files saved in: $CHAPTERS_DIR/"
echo

# List the created chapter files
echo "Chapter files created:"
ls -la "$CHAPTERS_DIR"/*.txt 2>/dev/null | while read -r perm links owner group size month day time filename; do
    chapter_name=$(basename "$filename")
    word_count=$(wc -w < "$filename")
    echo "  $chapter_name - $word_count words"
done

echo
echo "Tip: You can read any chapter with: cat $CHAPTERS_DIR/chapter_01.txt"