#!/bin/bash

# 03_word_counter.sh - Word counting and statistics script for beginners
# This script analyzes word frequency and statistics in Alice in Wonderland
# Learn: text processing, sorting, arrays, and mathematical operations

echo "=== Alice in Wonderland Word Counter ==="
echo "This script analyzes word frequency and creates statistics"
echo

# Input file
INPUT_FILE="alice_wonderland.txt"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found!"
    echo "Please run 01_fetch_text.sh first to download the book."
    exit 1
fi

echo "Analyzing word statistics for $INPUT_FILE..."
echo

# Basic statistics
total_lines=$(wc -l < "$INPUT_FILE")
total_words=$(wc -w < "$INPUT_FILE")
total_chars=$(wc -c < "$INPUT_FILE")

echo "Basic Statistics:"
echo "  Total lines: $total_lines"
echo "  Total words: $total_words"
echo "  Total characters: $total_chars"
echo "  Average words per line: $((total_words / total_lines))"
echo

# Create word frequency list
echo "Creating word frequency analysis..."
temp_words="temp_words.txt"

# Extract all words, convert to lowercase, remove punctuation, sort and count
cat "$INPUT_FILE" | \
    tr '[:upper:]' '[:lower:]' | \
    tr -d '[:punct:]' | \
    tr ' ' '\n' | \
    grep -v '^$' | \
    sort | \
    uniq -c | \
    sort -nr > "$temp_words"

# Get total unique words
unique_words=$(wc -l < "$temp_words")

echo "Word Analysis Results:"
echo "  Unique words: $unique_words"
echo

echo "Top 20 Most Frequent Words:"
echo "  Rank | Count | Word"
echo "  -----|-------|----------"

# Display top 20 words with ranking
head -n 20 "$temp_words" | nl -w 4 -s ' | ' | while read -r line; do
    echo "  $line"
done

echo

# Find specific character mentions
echo "Character Mentions:"
characters=("Alice" "Rabbit" "Queen" "King" "Hatter" "Duchess" "Caterpillar" "Cheshire")

for character in "${characters[@]}"; do
    # Count mentions (case insensitive)
    count=$(grep -io "$character" "$INPUT_FILE" | wc -l)
    printf "  %-12s: %3d mentions\n" "$character" "$count"
done

echo

# Long words analysis
echo "Word Length Analysis:"
echo "  Longest words (8+ characters):"

# Find words with 8 or more characters
cat "$temp_words" | while read -r count word; do
    if [ ${#word} -ge 8 ]; then
        printf "    %-15s (%d letters, used %d times)\n" "$word" "${#word}" "$count"
    fi
done | head -n 10

echo

# Chapter-specific analysis (if chapters directory exists)
if [ -d "chapters" ]; then
    echo "Chapter Word Counts:"
    for chapter_file in chapters/chapter_*.txt; do
        if [ -f "$chapter_file" ]; then
            chapter_name=$(basename "$chapter_file" .txt)
            word_count=$(wc -w < "$chapter_file")
            printf "  %-12s: %4d words\n" "$chapter_name" "$word_count"
        fi
    done
fi

# Clean up temporary file
rm -f "$temp_words"

echo
echo "Tips for further analysis:"
echo "  - Use 'grep -i alice $INPUT_FILE' to find all Alice mentions"
echo "  - Use 'grep -o \"[A-Z][a-z]*\" $INPUT_FILE | sort | uniq' to find proper nouns"
echo "  - Try 'head -n 100 $INPUT_FILE' to read the beginning of the story"

echo
echo "Word analysis complete!"