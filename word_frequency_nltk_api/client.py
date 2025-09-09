import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_list_documents():
    """Test list documents endpoint."""
    response = requests.get(f"{BASE_URL}/documents")
    print("Documents in Database:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_classify(text):
    """Test document classification."""
    data = {"text": text}
    response = requests.post(f"{BASE_URL}/classify", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Classification Results for: '{text[:50]}...'")
        print(f"Query words found: {result['query_word_count']}")
        print("\nTop matches:")
        for i, match in enumerate(result['results'][:5], 1):
            print(f"{i}. {match['title']} (Score: {match['similarity_score']})")
    else:
        print(f"Error: {response.json()}")
    print()

def test_document_words(doc_id):
    """Test getting top words for a document."""
    response = requests.get(f"{BASE_URL}/document/{doc_id}/top-words?limit=10")
    if response.status_code == 200:
        result = response.json()
        print(f"Top words in '{result['title']}':")
        for word_data in result['top_words']:
            print(f"  {word_data['word']}: {word_data['tfidf_score']}")
    else:
        print(f"Error: {response.json()}")
    print()

if __name__ == "__main__":
    # Test all endpoints
    test_health()
    test_list_documents()
    
    # Test classification with different texts
    test_classify("Alice was a curious girl who followed a white rabbit down a hole")
    test_classify("Elizabeth Bennet was a strong-willed woman in 19th century England")
    test_classify("The monster created by Victor Frankenstein was terrifying")
    
    # Test getting top words for document 1
    test_document_words(1)