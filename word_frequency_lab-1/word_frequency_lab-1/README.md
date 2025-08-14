# Word Frequency Lab

A simple Python lab to analyze word frequency in "Alice's Adventures in Wonderland" from Project Gutenberg.

> Written in **Python 3.9**

## File Structure

```
word_frequency_lab/
├── word_frequency.py         # Main script
├── requirements.txt          # List of dependencies
└── README.md                 # Setup & usage guide
```

---

## Setup Steps

1. Create and activate a conda environment
```bash
conda create --name lab_python python=3.9 -y && conda activate lab_python
```
2. Install required package:
```bash
pip install -r requirements.txt
```

## How to Run

Run the script with the URL:
```bash
python word_frequency.py https://www.gutenberg.org/files/11/11-0.txt
```

Optional: Specify number of top words (default is 10):
```bash
python word_frequency.py https://www.gutenberg.org/files/11/11-0.txt -n 20
```

