import torch
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import json
import numpy as np
import os

# Load the model globally
model = SentenceTransformer('all-MiniLM-L6-v2')
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Constants
WINDOW_SIZE = 250  
OVERLAP = 80      
MIN_WORDS = 150   

def preprocess_text(file_path):
    """Preprocess the input text from a Markdown (.md) file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    text = re.sub(r'#+\s', '', text)  
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  
    text = re.sub(r'\[.*?\]\(.*?\)', '', text) 
    text = re.sub(r'\*\*|\*|_|~~', '', text)  
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text) 
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

def sliding_window_tokenize(text, window_size, overlap, min_words):
    """Tokenize the text using a sliding window approach with a word length limit."""
    words = word_tokenize(text)
    windows = []
    start = 0
    while start < len(words):
        end = min(start + window_size, len(words))
        window = words[start:end]
        
        if len(window) >= min_words:
            windows.append(" ".join(window))
        
        start += window_size - overlap
    return windows

def get_embeddings_with_text(window_texts):
    """Get embeddings along with the corresponding text windows."""
    embeddings_with_text = []
    embeddings = model.encode(window_texts, convert_to_tensor=True)

    for i, window_text in enumerate(window_texts):
        embeddings_with_text.append({
            "text": window_text,
            "embedding": embeddings[i].cpu().numpy()
        })

    return embeddings_with_text

def process_text(file_path):
    """Main function to preprocess, tokenize, and compute embeddings."""
    # Preprocess text
    text = preprocess_text(file_path)
    segments = sliding_window_tokenize(text, WINDOW_SIZE, OVERLAP, MIN_WORDS)

    # Compute embeddings
    embeddings_list = []
    embeddings_with_text = get_embeddings_with_text(segments)

    for entry in embeddings_with_text:
        embeddings_list.append(entry["embedding"])

    return np.array(embeddings_list), embeddings_with_text

def save_results(file_path):
    """Save embeddings to files."""
    embeddings_array, embeddings_with_text = process_text(file_path)

    # Save embeddings as a NumPy array
    np.save("tezvec.npy", embeddings_array)

    # Save embeddings and text as JSON
    with open("tez1.json", "w", encoding="utf-8") as f:
        json.dump(
            [{"text": entry["text"], "embedding": entry["embedding"].tolist()} for entry in embeddings_with_text],
            f,
            ensure_ascii=False,
            indent=4
        )

    print("Processing complete. Embeddings saved as 'tezvec.npy' and 'tez1.json'.")

    return "tezvec.npy","tez1.json"
