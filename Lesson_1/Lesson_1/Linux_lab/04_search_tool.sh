#!/bin/bash

# 04_search_tool.sh - Interactive search tool for beginners
# This script provides various search functions for Alice in Wonderland
# Learn: user input, functions, case statements, and advanced grep usage

echo "=== Alice in Wonderland Search Tool ==="
echo "Interactive search tool to explore the story"
echo

# Input file
INPUT_FILE="alice_wonderland.txt"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found!"
    echo "Please run 01_fetch_text.sh first to download the book."
    exit 1
fi

# Function to search for a word or phrase
search_word() {
    local search_term="$1"
    local line_numbers="$2"
    
    echo "Searching for: '$search_term'"
    echo
    
    if [ "$line_numbers" = "yes" ]; then
        # Show results with line numbers
        grep -in "$search_term" "$INPUT_FILE" | head -n 20
    else
        # Show results without line numbers
        grep -i "$search_term" "$INPUT_FILE" | head -n 20
    fi
    
    # Count total matches
    local count=$(grep -ic "$search_term" "$INPUT_FILE")
    echo
    echo "Found $count total matches"
}

# Function to search for quotes (lines with quotation marks)
search_quotes() {
    local character="$1"
    
    echo "Searching for quotes"
    if [ -n "$character" ]; then
        echo "   by or mentioning: $character"
        grep -i "\".*$character\|$character.*\"" "$INPUT_FILE" | head -n 10
    else
        echo "   (showing first 10 quotes)"
        grep "\".*\"" "$INPUT_FILE" | head -n 10
    fi
}

# Function to find context around a word
search_context() {
    local search_term="$1"
    
    echo "Showing context (3 lines before and after) for: '$search_term'"
    echo
    
    grep -in -A 3 -B 3 "$search_term" "$INPUT_FILE" | head -n 50
}

# Function to show menu
show_menu() {
    echo
    echo "What would you like to search for?"
    echo "1. Search for a word or phrase"
    echo "2. Find quotes (dialogue)"
    echo "3. Search with context (surrounding lines)"
    echo "4. Find chapter by keyword"
    echo "5. Character interaction search"
    echo "6. Exit"
    echo
    printf "Enter your choice (1-6): "
}

# Function to search chapters
search_chapters() {
    local keyword="$1"
    
    echo "Searching chapters for: '$keyword'"
    echo
    
    if [ -d "chapters" ]; then
        for chapter_file in chapters/chapter_*.txt; do
            if [ -f "$chapter_file" ] && grep -qi "$keyword" "$chapter_file"; then
                chapter_name=$(basename "$chapter_file" .txt)
                matches=$(grep -ic "$keyword" "$chapter_file")
                echo "  $chapter_name: $matches matches"
                
                # Show first match with some context
                echo "     Preview:"
                grep -i -A 1 -B 1 "$keyword" "$chapter_file" | head -n 3 | sed 's/^/       /'
                echo
            fi
        done
    else
        echo "Chapters not extracted yet. Run 02_extract_chapters.sh first."
    fi
}

# Function to search character interactions
search_interactions() {
    local char1="$1"
    local char2="$2"
    
    echo "Searching for interactions between '$char1' and '$char2'"
    echo
    
    # Find lines that mention both characters (within 5 lines of each other)
    grep -in -A 5 -B 5 "$char1" "$INPUT_FILE" | grep -i "$char2" | head -n 10
}

# Main interactive loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1)
            echo
            printf "Enter word or phrase to search: "
            read -r search_term
            printf "Show line numbers? (y/n): "
            read -r show_lines
            echo
            
            if [ "$show_lines" = "y" ] || [ "$show_lines" = "yes" ]; then
                search_word "$search_term" "yes"
            else
                search_word "$search_term" "no"
            fi
            ;;
        2)
            echo
            printf "Search quotes by specific character (or press Enter for all): "
            read -r character
            echo
            search_quotes "$character"
            ;;
        3)
            echo
            printf "Enter word to search with context: "
            read -r search_term
            echo
            search_context "$search_term"
            ;;
        4)
            echo
            printf "Enter keyword to search in chapters: "
            read -r keyword
            echo
            search_chapters "$keyword"
            ;;
        5)
            echo
            printf "Enter first character name: "
            read -r char1
            printf "Enter second character name: "
            read -r char2
            echo
            search_interactions "$char1" "$char2"
            ;;
        6)
            echo
            echo "Happy exploring Alice in Wonderland!"
            exit 0
            ;;
        *)
            echo
            echo "Invalid choice. Please enter 1-6."
            ;;
    esac
    
    echo
    printf "Press Enter to continue..."
    read -r
done