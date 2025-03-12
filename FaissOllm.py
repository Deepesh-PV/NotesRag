import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
import requests

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize the SentenceTransformer model globally to avoid repeated loading
model = SentenceTransformer('all-MiniLM-L6-v2')

### Functions ###

# 1. Retrieve query embeddings
def get_query_embedding(query_text):
    query_embedding = model.encode(query_text, convert_to_tensor=False)
    return np.array(query_embedding).astype(np.float32)

# 2. Load texts from JSON file
def load_texts_from_json(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        embeddings_with_text_json = json.load(f)
    texts = [entry["text"] for entry in embeddings_with_text_json]
    return texts

# 3. Load embeddings from .npy file
def load_embeddings_from_npy(npy_file):
    embeddings = np.load(npy_file)
    if embeddings.ndim != 2:
        raise ValueError("The .npy file does not contain a 2D array. Ensure the file has shape (num_embeddings, embedding_dim).")
    return embeddings.astype(np.float32)

# 4. Search for similar embeddings using FAISS
def search_similar_embeddings(query_text, npy_file, json_file, k=5):
    query_embedding = get_query_embedding(query_text)
    embeddings = load_embeddings_from_npy(npy_file)
    texts = load_texts_from_json(json_file)

    if query_embedding.shape[0] != embeddings.shape[1]:
        raise ValueError(f"Dimension mismatch: query embedding shape {query_embedding.shape[0]} does not match embeddings shape {embeddings.shape[1]}")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    distances, indices = index.search(query_embedding.reshape(1, -1), k * 2)

    unique_sentences = set()
    result_sentences = []
    rank = 1
    for i, idx in enumerate(indices[0]):
        sentence = texts[idx]
        distance = distances[0][i]
        if sentence not in unique_sentences and rank <= k:
            result_sentences.append(sentence)
            unique_sentences.add(sentence)
            rank += 1
    return result_sentences

# 5. Query the Ollama model
def query_ollama_model(model_name, prompt):
    url = "http://localhost:11434/api/generate"  # Default Ollama API URL

    payload = {
        "model": model_name,
        "prompt": prompt
    }

    try:
        response = requests.post(url, json=payload, stream=True)

        if response.status_code == 200:
            response_text = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line.decode('utf-8'))
                        response_text += json_response.get("response", "")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
            return response_text
        else:
            return f"Error {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# 6. Create prompt and query Ollama
def generate_prompt_and_query(query_text, model_name, npy_file, json_file, result_file):
    similar_sentences = search_similar_embeddings(query_text, npy_file, json_file, k=5)

    if "Module" in query_text:
        print(f"Skipping query containing 'Module': Writing directly to the output file.")
        with open(result_file, "a", encoding="utf-8") as f:
            f.write(f"Query: {query_text}\n")
            f.write("\n".join(similar_sentences) + "\n")
            f.write("-" * 80 + "\n")
        return None

    prompt = f"""Write the following sentences as meaningful notes for students, use info from sentences provided according to query as paragraphs, combine everything into one by using given sentences:
Query: {query_text}
Sentences:
{chr(10).join([f"{i+1}. {sentence}" for i, sentence in enumerate(similar_sentences)])}
"""

    response = query_ollama_model(model_name, prompt)
    return response

# 7. Process a single query and save results
def process_query(query_text, model_name, npy_file, json_file, result_file):
    response = generate_prompt_and_query(query_text, model_name, npy_file, json_file, result_file)

    if response:
        with open(result_file, "a", encoding="utf-8") as f_out:
            f_out.write(f"\nQuery: {query_text}\n")
            f_out.write(f"{response}\n")
            f_out.write("-" * 80 + "\n")

# 8. Process multiple queries from a file
def process_queries_from_file(query_file, model_name, npy_file, json_file, result_file):
    with open(result_file, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")

    with open(query_file, "r", encoding="utf-8") as f:
        for query_text in f:
            query_text = query_text.strip()
            print(query_text)
            if not query_text or query_text.startswith("Module-"):
                with open(result_file, "a", encoding="utf-8") as f:  # Append instead of overwrite
                    f.write(query_text + "\n")  # Ensure proper formatting
                continue  # Move to the next query
            
            process_query(query_text, model_name, npy_file, json_file, result_file)


### Main Script ###

if __name__ == "__main__":
    # Files and configurations
    query_file = "llmop.txt"
    npy_file = "tezvec.npy"
    json_file = "tez1.json"
    result_file = "final_notes.txt"
    model_name = "llama3:latest"

    # Call specific functions as needed
    process_queries_from_file(query_file, model_name, npy_file, json_file, result_file)

