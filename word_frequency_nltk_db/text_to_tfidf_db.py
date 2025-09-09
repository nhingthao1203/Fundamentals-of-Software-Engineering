import requests
import sqlite3
import re
import argparse
import math
from collections import Counter
import nltk
from nltk.corpus import stopwords

def download_nltk_data():
    """Download only stopwords data."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

def create_database(db_name):
    """Create SQLite database for TF-IDF storage."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    
    # Create TF-IDF table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tfidf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            word TEXT NOT NULL,
            tf REAL NOT NULL,
            idf REAL NOT NULL,
            tfidf REAL NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id)
        )
    ''')
    
    conn.commit()
    return conn

def download_text(url):
    """Download text from Project Gutenberg URL."""
    response = requests.get(url)
    response.raise_for_status()
    text = response.text
    
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    start_index = text.find(start_marker)
    if start_index == -1:
        raise ValueError("Start marker not found")
    start_index = text.find('\n', start_index) + 1
    
    end_index = text.find(end_marker, start_index)
    if end_index == -1:
        raise ValueError("End marker not found")
    
    return text[start_index:end_index].strip()

def extract_title(text):
    """Extract book title from text."""
    lines = text.split('\n')[:10]
    for line in lines:
        line = line.strip()
        if line and not line.startswith('***'):
            return line
    return "Unknown Title"

def clean_text(text):
    """Clean text and return words."""
    download_nltk_data()
    
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Get words
    words = text.lower().split()
    words = [word for word in words if len(word) > 2]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    return words

def calculate_tf(words):
    """Calculate Term Frequency for each word."""
    word_count = Counter(words)
    total_words = len(words)
    
    tf = {}
    for word, count in word_count.items():
        tf[word] = count / total_words
    
    return tf

def calculate_idf(all_documents):
    """Calculate Inverse Document Frequency."""
    total_docs = len(all_documents)
    all_words = set()
    
    # Get all unique words
    for words in all_documents:
        all_words.update(set(words))
    
    idf = {}
    for word in all_words:
        docs_with_word = sum(1 for doc in all_documents if word in doc)
        idf[word] = math.log(total_docs / docs_with_word)
    
    return idf

def calculate_tfidf(tf, idf):
    """Calculate TF-IDF scores."""
    tfidf = {}
    for word, tf_score in tf.items():
        tfidf[word] = tf_score * idf[word]
    
    return tfidf

def save_to_database(conn, documents_data):
    """Save documents and TF-IDF to database."""
    cursor = conn.cursor()
    
    # Get all document words for IDF calculation
    all_documents = [doc['words'] for doc in documents_data]
    idf_scores = calculate_idf(all_documents)
    
    for doc_data in documents_data:
        # Save document
        cursor.execute('''
            INSERT INTO documents (title, url, content)
            VALUES (?, ?, ?)
        ''', (doc_data['title'], doc_data['url'], doc_data['content']))
        
        doc_id = cursor.lastrowid
        
        # Calculate TF-IDF for this document
        tf_scores = calculate_tf(doc_data['words'])
        tfidf_scores = calculate_tfidf(tf_scores, idf_scores)
        
        # Save TF-IDF scores
        tfidf_data = []
        for word, tfidf_score in tfidf_scores.items():
            tfidf_data.append((
                doc_id, 
                word, 
                tf_scores[word], 
                idf_scores[word], 
                tfidf_score
            ))
        
        cursor.executemany('''
            INSERT INTO tfidf (doc_id, word, tf, idf, tfidf)
            VALUES (?, ?, ?, ?, ?)
        ''', tfidf_data)
    
    conn.commit()

def process_texts(urls, db_name):
    """Process multiple texts and save TF-IDF to database."""
    conn = create_database(db_name)
    documents_data = []
    
    # Download and process all texts
    for i, url in enumerate(urls, 1):
        try:
            print(f"[{i}/{len(urls)}] Processing: {url}")
            
            content = download_text(url)
            title = extract_title(content)
            words = clean_text(content)
            
            documents_data.append({
                'title': title,
                'url': url,
                'content': content,
                'words': words
            })
            
            print(f"  Processed '{title}' ({len(words)} words)")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Calculate and save TF-IDF
    if documents_data:
        print("\nCalculating TF-IDF and saving to database...")
        save_to_database(conn, documents_data)
        print(f"✓ Saved {len(documents_data)} documents to {db_name}")
    
    conn.close()

def query_tfidf(db_name, doc_id=None, top_n=10):
    """Query TF-IDF scores from database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    if doc_id:
        # Show top TF-IDF words for specific document
        cursor.execute('''
            SELECT d.title, t.word, t.tfidf
            FROM tfidf t
            JOIN documents d ON t.doc_id = d.id
            WHERE d.id = ?
            ORDER BY t.tfidf DESC
            LIMIT ?
        ''', (doc_id, top_n))
        
        results = cursor.fetchall()
        if results:
            title = results[0][0]
            print(f"\nTop {top_n} TF-IDF words in '{title}':")
            print("-" * 40)
            for i, (_, word, score) in enumerate(results, 1):
                print(f"{i:2d}. {word:<15} {score:.6f}")
    else:
        # Show all documents
        cursor.execute('SELECT id, title FROM documents')
        docs = cursor.fetchall()
        print(f"\nDocuments in database ({len(docs)} total):")
        print("-" * 40)
        for doc_id, title in docs:
            print(f"{doc_id}. {title}")
    
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Convert text to TF-IDF and save to SQLite')
    parser.add_argument('--db', default='tfidf.db', help='Database file name')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process texts and save TF-IDF')
    process_parser.add_argument('urls', nargs='+', help='URLs to process')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query TF-IDF scores')
    query_parser.add_argument('--doc-id', type=int, help='Document ID to query')
    query_parser.add_argument('-n', type=int, default=15, help='Number of top words')
    
    args = parser.parse_args()
    
    if args.command == 'process':
        process_texts(args.urls, args.db)
        
    elif args.command == 'query':
        query_tfidf(args.db, args.doc_id, args.n)
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()