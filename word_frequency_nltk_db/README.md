# Text to TF-IDF Database Lab
Simple Python lab to calculate **TF-IDF** (Term Frequency-Inverse Document Frequency) and save to **SQLite3** database.

> Built with **Python 3.9** • **SQLite3** • **NLTK**

## What is TF-IDF?
- **TF (Term Frequency)**: How often a word appears in a document
- **IDF (Inverse Document Frequency)**: How rare/common a word is across all documents  
- **TF-IDF**: TF × IDF - identifies important words that are frequent in one document but rare across the collection

## Features
- Download texts from Project Gutenberg
- Calculate TF-IDF scores for all words
- Store results in SQLite database
- Query top TF-IDF words per document

## Setup
```bash
conda create --name tfidf_lab python=3.9 -y
conda activate tfidf_lab
pip install -r requirements.txt
```

## Usage

### 1. Process Texts (Calculate TF-IDF)
```bash
# Process single text
python text_to_tfidf_db.py process https://www.gutenberg.org/files/11/11-0.txt

# Process multiple texts (better for TF-IDF comparison)
python text_to_tfidf_db.py process \
  https://www.gutenberg.org/files/11/11-0.txt \
  https://www.gutenberg.org/files/1342/1342-0.txt \
  https://www.gutenberg.org/files/84/84-0.txt
```

### 2. Query Results
```bash
# List all documents
python text_to_tfidf_db.py query

# Show top TF-IDF words for document ID 1
python text_to_tfidf_db.py query --doc-id 1 -n 20
```

## Sample Output
```bash
$ python text_to_tfidf_db.py process https://www.gutenberg.org/files/11/11-0.txt https://www.gutenberg.org/files/1342/1342-0.txt

[1/2] Processing: https://www.gutenberg.org/files/11/11-0.txt
   Processed "Alice's Adventures in Wonderland" (26436 words)
[2/2] Processing: https://www.gutenberg.org/files/1342/1342-0.txt  
   Processed "Pride and Prejudice" (122189 words)

Calculating TF-IDF and saving to database...
 Saved 2 documents to tfidf.db

$ python text_to_tfidf_db.py query --doc-id 1 -n 10

Top 10 TF-IDF words in "Alice's Adventures in Wonderland":
----------------------------------------
 1. alice           0.008234
 2. rabbit          0.003891  
 3. turtle          0.002156
 4. dormouse        0.001823
 5. gryphon         0.001645
```

## Database Schema
```sql
-- Documents table
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    url TEXT,
    content TEXT
);

-- TF-IDF scores table
CREATE TABLE tfidf (
    id INTEGER PRIMARY KEY,
    doc_id INTEGER,
    word TEXT,
    tf REAL,      -- Term Frequency
    idf REAL,     -- Inverse Document Frequency  
    tfidf REAL,   -- TF-IDF Score
    FOREIGN KEY (doc_id) REFERENCES documents (id)
);
```

## Sample Book URLs
- Alice in Wonderland: `https://www.gutenberg.org/files/11/11-0.txt`
- Pride and Prejudice: `https://www.gutenberg.org/files/1342/1342-0.txt`
- Frankenstein: `https://www.gutenberg.org/files/84/84-0.txt`