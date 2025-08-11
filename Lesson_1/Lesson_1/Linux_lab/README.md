
## What You'll Learn

Each script progressively introduces new bash concepts:

1. **Basic commands and variables** (curl, echo, variables)
2. **File processing and loops** (while loops, text processing)
3. **Text analysis and pipes** (grep, sort, uniq, pipes)
4. **Interactive scripts and functions** (user input, functions, case statements)
5. **Advanced text processing** (arrays, complex pattern matching)

## Getting Started

### Prerequisites
- Bash shell (Linux, macOS, or Windows with WSL)
- `curl` command (for downloading)
- Internet connection (for initial download)

### Quick Start

**Option 1: Using Makefile (Recommended)**
```bash
# Run everything automatically
make setup fetch all

# Or run individual steps
make setup          # Make scripts executable
make fetch          # Download the book
make all            # Run all analysis scripts
make clean          # Clean up files when done

# Get help
make help
```

**Option 2: Manual Execution**
```bash
# 1. First, make scripts executable
chmod +x *.sh

# 2. Download the book
./01_fetch_text.sh

# 3. Then run any other script
./02_extract_chapters.sh
./03_word_counter.sh
./04_search_tool.sh
./05_character_analyzer.sh
```

## Script Details

### 01_fetch_text.sh - Text Fetching Basics
**Concepts:** Variables, curl, basic commands, exit codes
```bash
./01_fetch_text.sh
```
- Downloads Alice in Wonderland from Project Gutenberg
- Shows file statistics (size, lines, words)
- Demonstrates error handling

### 02_extract_chapters.sh - File Processing & Loops
**Concepts:** While loops, file I/O, pattern matching, conditionals
```bash
./02_extract_chapters.sh
```
- Splits the book into individual chapter files
- Creates organized directory structure
- Uses pattern matching to identify chapters

### 03_word_counter.sh - Text Analysis & Pipes
**Concepts:** Pipes, text transformation, sorting, arrays
```bash
./03_word_counter.sh
```
- Analyzes word frequency throughout the book
- Creates statistics and rankings
- Demonstrates advanced text processing pipelines

### 04_search_tool.sh - Interactive Scripts & Functions
**Concepts:** Functions, user input, case statements, grep advanced usage
```bash
./04_search_tool.sh
```
- Interactive menu-driven search tool
- Multiple search modes (word, context, quotes)
- Character interaction analysis

### 05_character_analyzer.sh - Advanced Processing
**Concepts:** Arrays, complex text analysis, data visualization
```bash
./05_character_analyzer.sh
```
- Character appearance frequency
- Relationship analysis between characters
- Chapter-by-chapter character tracking

## Example Output

After running all scripts, you'll have:
```
alice_wonderland.txt          # The complete book
chapters/                     # Individual chapter files
├── chapter_01.txt
├── chapter_02.txt
└── ...
```

## Bash Concepts Covered

- **Variables and Parameters:** `$1`, `$?`, `$INPUT_FILE`
- **Conditionals:** `if [ -f "$file" ]`, `[[ "$line" =~ pattern ]]`
- **Loops:** `while read`, `for item in array`
- **Functions:** Function definition and parameter passing
- **Text Processing:** `grep`, `sed`, `awk`, `sort`, `uniq`
- **I/O Redirection:** `>`, `>>`, `|`, `< file`
- **Arrays:** `declare -a`, array iteration
- **User Interaction:** `read`, `printf`, menu systems

## Troubleshooting

**Script won't run:**
```bash
chmod +x script_name.sh
```

**"File not found" errors:**
- Make sure to run `01_fetch_text.sh` first
- Check that you're in the correct directory

**Network issues:**
- Check internet connection
- Try running the curl command manually