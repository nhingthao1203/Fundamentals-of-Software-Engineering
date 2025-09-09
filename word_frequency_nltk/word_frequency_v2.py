import requests
import re
import argparse
from collections import Counter
import nltk
from nltk.corpus import stopwords

def download_nltk_data():
    """Download only stopwords data."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

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

def clean_text(text, remove_stopwords=True):
    """Clean text using regex and basic NLTK stopwords."""
    # Remove punctuation and numbers with regex
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Simple tokenization
    words = text.lower().split()
    words = [word for word in words if len(word) > 2]
    
    # Remove stopwords using NLTK
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
    
    return words

def count_words(words):
    """Count word frequencies."""
    return Counter(words)

def main():
    parser = argparse.ArgumentParser(description='Word frequency analysis with basic NLTK')
    parser.add_argument('url', help='URL of the text file')
    parser.add_argument('-n', type=int, default=15, help='Number of top words to display')
    parser.add_argument('--keep-stopwords', action='store_true', help='Keep stopwords')
    
    args = parser.parse_args()
    
    try:
        download_nltk_data()
        text = download_text(args.url)
        words = clean_text(text, remove_stopwords=not args.keep_stopwords)
        word_counts = count_words(words)
        
        print(f"Total words: {len(words):,}")
        print(f"Unique words: {len(word_counts):,}")
        print(f"\nTop {args.n} words:")
        
        for word, count in word_counts.most_common(args.n):
            print(f'{word}: {count}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()