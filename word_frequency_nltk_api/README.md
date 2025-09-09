# TF-IDF Document Classifier API
FastAPI service for classifying documents using TF-IDF vectors from SQLite database.

## Features
- **Document Classification**: Find similar documents using cosine similarity
- **RESTful API**: FastAPI with automatic docs
- **TF-IDF Vectors**: Uses pre-calculated vectors from database
- **Cosine Similarity**: Mathematical document comparison

## Setup
```bash
conda create --name tfidf_api python=3.9 -y
conda activate tfidf_api
pip install -r requirements.txt
```

## Prerequisites
You need the `tfidf.db` database from the previous TF-IDF lab with some documents processed.

## Run API
```bash
python tfidf_classifier_api.py
```
API runs at: http://localhost:8000

## API Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. List Documents  
```bash
GET /documents
```

### 3. Classify Text
```bash
POST /classify
Content-Type: application/json

{
  "text": "Alice followed the white rabbit down the hole"
}
```

### 4. Document Top Words
```bash
GET /document/{doc_id}/top-words?limit=10
```

### 5. API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Test the API
```bash
python client.py
```

## How Classification Works
1. **Input**: Text to classify
2. **Preprocessing**: Clean and tokenize text
3. **TF-IDF Calculation**: Calculate query vector using database IDF scores
4. **Similarity**: Compare with all document vectors using cosine similarity
5. **Results**: Return ranked list of similar documents

## Sample Response
```json
{
  "results": [
    {
      "document_id": 1,
      "title": "Alice's Adventures in Wonderland",
      "similarity_score": 0.842156
    },
    {
      "document_id": 2, 
      "title": "Pride and Prejudice",
      "similarity_score": 0.123456
    }
  ],
  "query_word_count": 8
}
```