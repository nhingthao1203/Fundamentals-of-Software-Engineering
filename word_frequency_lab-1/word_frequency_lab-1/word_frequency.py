# Import necessary libraries for web requests, text processing, and command-line arguments
import requests  # For downloading web content
import string    # Provides string constants like punctuation
from collections import Counter  # Efficient counting of hashable objects
import argparse  # For parsing command-line arguments

def download_text(url):
    """
    Downloads text content from a URL, specifically designed for Project Gutenberg ebooks.
    
    This function extracts only the actual book content by finding specific markers
    that Project Gutenberg uses to separate the book text from metadata.
    
    Args:
        url (str): The URL of the Project Gutenberg ebook
        
    Returns:
        str: The cleaned book text without Project Gutenberg headers/footers
        
    Raises:
        ValueError: If the expected start or end markers are not found
        requests.exceptions.RequestException: If the URL cannot be accessed
    """
    # Download the webpage content
    response = requests.get(url)
    
    # Check if the request was successful (raises exception if not)
    response.raise_for_status()
    
    # Get the raw text content
    text = response.text
    
    # Project Gutenberg books have standard markers to identify book content
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    # Find where the actual book content starts
    # text.find() returns the position of the marker, or -1 if not found
    start_index = text.find(start_marker)
    
    # This is an if statement: if the marker wasn't found (find returned -1)
    if start_index == -1:
        # We use raise to create an error and stop the program
        raise ValueError("Start marker not found")
    
    # Move past the marker line to the beginning of actual content
    # We find the next newline character after the marker
    start_index = text.find('\n', start_index) + 1
    
    # Find where the book content ends
    # We search for the end marker starting from our start position
    end_index = text.find(end_marker, start_index)
    
    # Another if statement: check if end marker was found
    if end_index == -1:
        # If not found, create an error
        raise ValueError("End marker not found")
    
    # Extract and return only the book content, removing extra whitespace
    return text[start_index:end_index].strip()

def clean_text(text):
    """
    Removes punctuation and converts text to lowercase for consistent word analysis.
    
    This preprocessing step ensures that words like "Hello!" and "hello" are treated
    as the same word, and punctuation doesn't interfere with word counting.
    
    Args:
        text (str): The raw text to be cleaned
        
    Returns:
        str: Cleaned text with no punctuation and all lowercase letters
    """
    # Create a translation table that maps all punctuation characters to None (removes them)
    # string.punctuation contains: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    translator = str.maketrans('', '', string.punctuation)
    
    # Apply the translation to remove all punctuation
    cleaned = text.translate(translator)
    
    # Convert to lowercase for consistent comparison
    cleaned = cleaned.lower()
    
    return cleaned

def get_words(text):
    """
    Splits the cleaned text into individual words.
    
    Uses whitespace as the delimiter to separate words. This works well after
    punctuation removal since words will be naturally separated by spaces.
    
    Args:
        text (str): The cleaned text to split into words
        
    Returns:
        list: A list of individual words as strings
    """
    return text.split()

def count_words(words):
    """
    Counts the frequency of each word using Python's Counter class.
    
    Counter is an efficient way to count hashable objects. It creates a dictionary
    where keys are words and values are their frequencies.
    
    Args:
        words (list): List of words to count
        
    Returns:
        Counter: A Counter object (dict-like) with word frequencies
    """
    return Counter(words)

def main():
    """
    Main function that orchestrates the word frequency analysis process.
    
    This function handles command-line arguments, coordinates all the processing steps,
    and displays the results. It also includes error handling for robust execution.
    """
    # Set up command-line argument parsing
    # ArgumentParser is like creating a rule book for what the user can type
    # when they run our program from the command line
    parser = argparse.ArgumentParser(description='Analyze word frequency in a text file from a URL.')
    
    # Required argument: URL of the text to analyze
    # This means the user MUST provide a URL when they run the program
    # Example: python word_frequency.py https://example.com/book.txt
    parser.add_argument('url', help='URL of the text file')
    
    # Optional argument: number of top words to display (default: 10)
    # The user can add -n followed by a number to change how many words to show
    # Example: python word_frequency.py https://example.com/book.txt -n 5
    # If they don't use -n, it will default to 10
    parser.add_argument('-n', type=int, default=10, help='Number of top words to display')
    
    # Parse the arguments provided by the user
    # This function looks at what the user typed and organizes it into variables
    # Now we can use args.url and args.n to get the values the user provided
    args = parser.parse_args()
    
    # TRY/EXCEPT:
    # try: means "attempt to do this code"
    # except: means "if any error happens, do this instead"
    # This prevents our program from crashing if something goes wrong
    try:
        # Step 1: Download the text content from the provided URL
        # We call download_text() function and pass the URL as an argument
        # The function returns the book text, which we store in the 'text' variable
        print("Downloading text...")
        text = download_text(args.url)
        
        # Step 2: Clean the text (remove punctuation, convert to lowercase)  
        # We call clean_text() function and pass our downloaded text as an argument
        # The function returns cleaned text, which we store in 'cleaned_text' variable
        print("Cleaning text...")
        cleaned_text = clean_text(text)
        
        # Step 3: Split the cleaned text into individual words
        # We call get_words() function and pass our cleaned text as an argument
        # The function returns a list of words, which we store in 'words' variable
        print("Extracting words...")
        words = get_words(cleaned_text)
        
        # Step 4: Count the frequency of each word
        # We call count_words() function and pass our list of words as an argument
        # The function returns a Counter object with word frequencies
        print("Counting word frequencies...")
        word_counts = count_words(words)
        
        # Step 5: Get the most common words (limited by -n argument)
        # We call the most_common() method on our Counter object
        # This method returns a list of tuples: [(word, count), (word, count), ...]
        top_words = word_counts.most_common(args.n)
        
        # Step 6: Display the results
        print(f"\nTop {args.n} most frequent words:")
        print("-" * 30)
        
        # This for loop goes through each tuple in our top_words list
        # Each tuple contains a word and its count: (word, count)
        for word, count in top_words:
            print(f'{word}: {count}')
        
        # Display some statistics
        # len() function counts how many unique words we found
        print(f"\nTotal unique words: {len(word_counts)}")
        
        # sum() function adds up all the word counts to get total words
        print(f"Total words analyzed: {sum(word_counts.values())}")
        
    except Exception as e:
        # EXCEPT: This block only runs if ANY error happened in the try block above
        # Think of it like: "if anything goes wrong, do this instead of crashing"
        # Common errors: bad URL, no internet connection, website is down, etc.
        # 'e' contains information about what went wrong
        print(f'An error occurred: {e}')
        print("Please check the URL and try again.")

# This ensures main() only runs when the script is executed directly,
# not when it's imported as a module
if __name__ == '__main__':
    main()