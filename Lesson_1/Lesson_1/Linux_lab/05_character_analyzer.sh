#!/bin/bash

# 05_character_analyzer.sh - Character analysis script for beginners
# This script analyzes character appearances and relationships in Alice in Wonderland
# Learn: associative arrays, advanced text processing, and data visualization in bash

echo "=== Alice in Wonderland Character Analyzer ==="
echo "This script analyzes character appearances and relationships"
echo

# Input file
INPUT_FILE="alice_wonderland.txt"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found!"
    echo "Please run 01_fetch_text.sh first to download the book."
    exit 1
fi

# Define main characters to analyze
declare -a CHARACTERS=("Alice" "Rabbit" "Queen" "King" "Hatter" "Duchess" "Caterpillar" "Cheshire" "Mouse" "Dodo")

# Create temporary files for analysis
temp_dir="temp_analysis"
mkdir -p "$temp_dir"

echo "Analyzing character appearances..."
echo

# Function to count character mentions
count_character_mentions() {
    local character="$1"
    grep -io "$character" "$INPUT_FILE" | wc -l
}

# Function to find character co-occurrences (appearing in same paragraph)
find_character_relationships() {
    local char1="$1"
    local char2="$2"
    
    # Split text into paragraphs and count co-occurrences
    awk 'BEGIN{RS="\n\n"} tolower($0) ~ /'"$(echo "$char1" | tr '[:upper:]' '[:lower:]')"'/ && tolower($0) ~ /'"$(echo "$char2" | tr '[:upper:]' '[:lower:]')"'/ {count++} END{print count+0}' "$INPUT_FILE"
}

# Character appearance analysis
echo "Character Appearance Frequency:"
echo "Character     | Mentions | Relative Frequency"
echo "--------------|----------|-------------------"

total_character_mentions=0

for character in "${CHARACTERS[@]}"; do
    count=$(count_character_mentions "$character")
    total_character_mentions=$((total_character_mentions + count))
    printf "%-12s | %8d |\n" "$character" "$count"
done

echo
echo "Total character mentions analyzed: $total_character_mentions"
echo

# Character relationship matrix
echo "Character Relationship Analysis:"
echo "   (Numbers show how often characters appear in the same paragraph)"
echo

# Create header
printf "%-10s" ""
for char in "${CHARACTERS[@]:0:6}"; do  # Show first 6 characters to fit screen
    printf " %6s" "$(echo "$char" | cut -c1-6)"
done
echo

# Create relationship matrix
for char1 in "${CHARACTERS[@]:0:6}"; do
    printf "%-10s" "$(echo "$char1" | cut -c1-10)"
    for char2 in "${CHARACTERS[@]:0:6}"; do
        if [ "$char1" = "$char2" ]; then
            printf " %6s" "-"
        else
            relationships=$(find_character_relationships "$char1" "$char2")
            printf " %6d" "$relationships"
        fi
    done
    echo
done

echo

# Chapter-by-chapter character analysis
if [ -d "chapters" ]; then
    echo "Character Appearances by Chapter:"
    echo
    
    # Create chapter analysis file
    chapter_analysis="$temp_dir/chapter_analysis.txt"
    echo "Chapter,Alice,Rabbit,Queen,King,Hatter" > "$chapter_analysis"
    
    for chapter_file in chapters/chapter_*.txt; do
        if [ -f "$chapter_file" ]; then
            chapter_name=$(basename "$chapter_file" .txt | sed 's/chapter_/Ch/')
            alice_count=$(grep -ic "alice" "$chapter_file")
            rabbit_count=$(grep -ic "rabbit" "$chapter_file")
            queen_count=$(grep -ic "queen" "$chapter_file")
            king_count=$(grep -ic "king" "$chapter_file")
            hatter_count=$(grep -ic "hatter" "$chapter_file")
            
            echo "$chapter_name,$alice_count,$rabbit_count,$queen_count,$king_count,$hatter_count" >> "$chapter_analysis"
            
            printf "%-8s: Alice(%2d) Rabbit(%2d) Queen(%2d) King(%2d) Hatter(%2d)\n" \
                "$chapter_name" "$alice_count" "$rabbit_count" "$queen_count" "$king_count" "$hatter_count"
        fi
    done
    
    echo
else
    echo "To see chapter-by-chapter analysis, run 02_extract_chapters.sh first"
    echo
fi

# Find character first appearances
echo "Character First Appearances:"
echo

for character in "${CHARACTERS[@]}"; do
    # Find the first line number where character appears
    first_line=$(grep -in "$character" "$INPUT_FILE" | head -n 1 | cut -d: -f1)
    if [ -n "$first_line" ]; then
        # Get some context around first appearance
        context=$(sed -n "${first_line}p" "$INPUT_FILE" | cut -c1-60)
        printf "%-12s: Line %4d - %s...\n" "$character" "$first_line" "$context"
    fi
done

echo

# Character dialogue analysis
echo "Character Dialogue Analysis:"
echo "   (Estimated based on nearby quotation marks)"
echo

for character in "${CHARACTERS[@]:0:5}"; do  # Analyze first 5 characters
    # Count lines with character name near quotes (within 2 lines)
    dialogue_count=$(grep -i -A 2 -B 2 "$character" "$INPUT_FILE" | grep -c '"')
    printf "%-12s: ~%3d dialogue lines\n" "$character" "$dialogue_count"
done

echo

# Most active chapters (by total character mentions)
if [ -d "chapters" ]; then
    echo "Most Character-Active Chapters:"
    echo
    
    for chapter_file in chapters/chapter_*.txt; do
        if [ -f "$chapter_file" ]; then
            chapter_name=$(basename "$chapter_file" .txt)
            total_chars=0
            
            for character in "${CHARACTERS[@]}"; do
                count=$(grep -ic "$character" "$chapter_file")
                total_chars=$((total_chars + count))
            done
            
            echo "$total_chars $chapter_name"
        fi
    done | sort -nr | head -n 5 | while read -r count chapter; do
        printf "  %-12s: %3d character mentions\n" "$chapter" "$count"
    done
fi

# Clean up
rm -rf "$temp_dir"

echo
echo "Analysis Tips:"
echo "  - High co-occurrence numbers suggest characters interact frequently"
echo "  - Alice appears most often as she's the protagonist"
echo "  - Try running 04_search_tool.sh to explore specific character interactions"

echo
echo "Character analysis complete!"