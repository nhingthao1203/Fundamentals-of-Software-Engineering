# Enhanced Word Frequency Lab
Simple Python lab using **NLTK** and **regex** for improved text analysis.

> Built with **Python 3.10** • **NLTK 3.8+**

## NLTK Library
- **Stopword filtering** using NLTK corpus
- **Regex cleaning** for punctuation removal
- **Basic text statistics**
- **Simple setup** (only downloads stopwords)

## File Structure
```
word_frequency_lab_v2/
├── word_frequency_v2.py    
├── requirements.txt        
└── README.md               
```

## Setup
1. **Create conda environment:**
```bash
conda create --name lab_python_v2 python=3.10 -y
conda activate lab_python_v2
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
python word_frequency_v2.py https://www.gutenberg.org/files/11/11-0.txt
```

### With Options
```bash
# Keep stopwords
python word_frequency_v2.py https://www.gutenberg.org/files/11/11-0.txt --keep-stopwords

# Show more words
python word_frequency_v2.py https://www.gutenberg.org/files/11/11-0.txt -n 25
```

## Arguments
- `url` - Project Gutenberg text URL
- `-n` - Number of top words (default: 15)
- `--keep-stopwords` - Include common words like "the", "and"

## Sample Output
```
Total words: 26,436
Unique words: 2,847

Top 15 words:
alice: 386
said: 323
little: 128
one: 101
know: 87
```