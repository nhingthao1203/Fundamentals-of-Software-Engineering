from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import re
import math
from collections import Counter
from typing import List, Dict
import nltk
from nltk.corpus import stopwords

app = FastAPI(title="TF-IDF Document Classifier", version="1.0.0")

# Pydantic models
class DocumentInput(BaseModel):
    text: str

class ClassificationResult(BaseModel):
    document_id: int
    title: str
    similarity_score: float

class ClassificationResponse(BaseModel):
    results: List[ClassificationResult]
    query_word_count: int

def download_nltk_data():
    """Download stopwords if needed."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

def clean_text(text: str) -> List[str]:
    """Clean and tokenize text."""
    download_nltk_data()
    
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Tokenize
    words = text.lower().split()
    words = [word for word in words if len(word) > 2]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    return words

def get_db_connection():
    """Get database connection."""
    try:
        conn = sqlite3.connect('tfidf.db')
        return conn
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database connection failed")

def calculate_query_tfidf(words: List[str], idf_scores: Dict[str, float]) -> Dict[str, float]:
    """Calculate TF-IDF for query text."""
    word_count = Counter(words)
    total_words = len(words)
    
    query_tfidf = {}
    for word, count in word_count.items():
        if word in idf_scores:
            tf = count / total_words
            query_tfidf[word] = tf * idf_scores[word]
    
    return query_tfidf

def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Calculate cosine similarity between two TF-IDF vectors."""
    # Get common words
    common_words = set(vec1.keys()) & set(vec2.keys())
    
    if not common_words:
        return 0.0
    
    # Calculate dot product
    dot_product = sum(vec1[word] * vec2[word] for word in common_words)
    
    # Calculate magnitudes
    mag1 = math.sqrt(sum(score ** 2 for score in vec1.values()))
    mag2 = math.sqrt(sum(score ** 2 for score in vec2.values()))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_product / (mag1 * mag2)

@app.get("/")
def root():
    """API info."""
    return {
        "message": "TF-IDF Document Classifier API",
        "endpoints": {
            "/classify": "POST - Classify a document against database",
            "/documents": "GET - List all documents in database",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        conn.close()
        return {
            "status": "healthy",
            "documents_in_db": doc_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/documents")
def list_documents():
    """List all documents in database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title FROM documents")
    documents = cursor.fetchall()
    conn.close()
    
    return {
        "documents": [{"id": doc_id, "title": title} for doc_id, title in documents],
        "total": len(documents)
    }

@app.post("/classify", response_model=ClassificationResponse)
def classify_document(document: DocumentInput):
    """Classify input text against documents in database using TF-IDF similarity."""
    
    # Clean input text
    query_words = clean_text(document.text)
    
    if not query_words:
        raise HTTPException(status_code=400, detail="No valid words found in input text")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all documents
    cursor.execute("SELECT id, title FROM documents")
    documents = cursor.fetchall()
    
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found in database")
    
    # Get IDF scores for query words
    placeholders = ','.join('?' * len(query_words))
    cursor.execute(f"""
        SELECT word, idf FROM tfidf 
        WHERE word IN ({placeholders})
        GROUP BY word
    """, query_words)
    
    idf_data = cursor.fetchall()
    idf_scores = {word: idf for word, idf in idf_data}
    
    # Calculate query TF-IDF vector
    query_tfidf = calculate_query_tfidf(query_words, idf_scores)
    
    if not query_tfidf:
        raise HTTPException(status_code=404, detail="No matching words found in database vocabulary")
    
    # Calculate similarity with each document
    results = []
    
    for doc_id, title in documents:
        # Get document TF-IDF vector
        cursor.execute("""
            SELECT word, tfidf FROM tfidf 
            WHERE doc_id = ? AND word IN ({})
        """.format(placeholders), [doc_id] + query_words)
        
        doc_tfidf_data = cursor.fetchall()
        doc_tfidf = {word: score for word, score in doc_tfidf_data}
        
        # Calculate cosine similarity
        similarity = cosine_similarity(query_tfidf, doc_tfidf)
        
        if similarity > 0:
            results.append(ClassificationResult(
                document_id=doc_id,
                title=title,
                similarity_score=round(similarity, 6)
            ))
    
    conn.close()
    
    # Sort by similarity score (descending)
    results.sort(key=lambda x: x.similarity_score, reverse=True)
    
    return ClassificationResponse(
        results=results,
        query_word_count=len(query_words)
    )

@app.get("/document/{doc_id}/top-words")
def get_document_top_words(doc_id: int, limit: int = 10):
    """Get top TF-IDF words for a specific document."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if document exists
    cursor.execute("SELECT title FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Get top words
    cursor.execute("""
        SELECT word, tfidf FROM tfidf 
        WHERE doc_id = ? 
        ORDER BY tfidf DESC 
        LIMIT ?
    """, (doc_id, limit))
    
    words = cursor.fetchall()
    conn.close()
    
    return {
        "document_id": doc_id,
        "title": doc[0],
        "top_words": [{"word": word, "tfidf_score": round(score, 6)} for word, score in words]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)