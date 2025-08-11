# Alice in Wonderland Bash Learning Scripts - Simple Makefile

# Variables
SCRIPTS = *.sh
TEXT_FILE = alice_wonderland.txt
CHAPTERS_DIR = chapters

# Default target - show help
help:
	@echo "Alice in Wonderland Learning Scripts"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup    - Make all scripts executable"
	@echo "  make fetch    - Download Alice in Wonderland text"
	@echo "  make all      - Run all scripts in sequence"
	@echo "  make clean    - Remove generated files"
	@echo "  make help     - Show this help"
	@echo ""
	@echo "Quick start: make setup fetch all"

# Make scripts executable
setup:
	chmod +x $(SCRIPTS)
	@echo "Scripts are now executable"

# Download the book
fetch: setup
	./01_fetch_text.sh

# Run all scripts in sequence
all: fetch
	./02_extract_chapters.sh
	./03_word_counter.sh
	./05_character_analyzer.sh
	@echo ""
	@echo "All scripts completed!"
	@echo "Run './04_search_tool.sh' for interactive search"

# Clean up generated files
clean:
	rm -f $(TEXT_FILE)
	rm -rf $(CHAPTERS_DIR)
	rm -f temp_*.txt
	@echo "Generated files removed"

.PHONY: help setup fetch all clean