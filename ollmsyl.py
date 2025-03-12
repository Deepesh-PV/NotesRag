from datetime import datetime
import requests
import json
import re
### Functions ###

# 1. Query the Ollama model
def query_ollama_model(model_name, prompt):
    """
    Queries the Ollama model with a given prompt and returns the response.

    Args:
        model_name (str): The name of the model to query.
        prompt (str): The prompt to provide to the model.

    Returns:
        str: The model's response or an error message.
    """
    url = "http://localhost:11434/api/generate"  
    payload = {"model": model_name, "prompt": prompt}

    try:
        response = requests.post(url, json=payload, stream=True)
        if response.status_code == 200:
            response_text = ""
            first_line_skipped = False
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line.decode('utf-8'))
                        line_text = json_response.get("response", "")
                        if not first_line_skipped and line_text.strip():
                            first_line_skipped = True
                            continue
                        response_text += line_text
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
            return response_text
        else:
            return f"Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# 2. Load and slice text from a file
def load_and_slice_text(file_path):
    """
    Loads text from a file and slices it between the first and last occurrence of 'Module'.
    Args:
        file_path (str): Path to the file containing the text.
    Returns:
        str: The sliced text or an empty string if no valid slice is found.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Debugging: Print the lines being checked
    for i, line in enumerate(lines):
        if re.search(r"\bMODULE-\b", line, re.IGNORECASE):
            print(f"Match found at line {i}: {line.strip()}")
        

    # Use case-insensitive regex to match 'Module' anywhere in the line
    first_index = next((i for i, line in enumerate(lines) if re.search(r"\bMODULE-\b", line, re.IGNORECASE)), None)
    last_index = next((i for i, line in reversed(list(enumerate(lines))) if re.search(r"\bMODULE-\b", line, re.IGNORECASE)), None)

    if first_index is not None and last_index is not None:
        sliced_text = "".join(lines[first_index:last_index + 6])  # Include the last matched line
        return sliced_text
    else:
        if first_index is None:
            print("No first occurrence of 'Module' found.")
        if last_index is None:
            print("No last occurrence of 'Module' found.")
    # return ""


# 3. Generate a system prompt
def create_system_prompt():
    """
    Creates the system-level prompt for querying the model.

    Returns:
        str: The system prompt.
    """
    return (
        "Your role is to extract module wise topics. Provide only the module name followed by its topics in a clear and concise manner line by line topics.don't skip any topic. Don't give numbering"
    )

# 4. Combine prompts
def combine_prompts(system_prompt, user_prompt):
    """
    Combines the system prompt and the user prompt into a single query.

    Args:
        system_prompt (str): The system-level prompt.
        user_prompt (str): The user-provided input.

    Returns:
        str: The combined prompt.
    """
    return f"{system_prompt}\n\n{user_prompt}"

# 5. Save response to a file
def save_response_to_file(response, output_file):
    """
    Saves the model's response to a file.

    Args:
        response (str): The model's response.
        output_file (str): Path to the file where the response will be saved.
    """
    cleaned_response = "\n".join(response.splitlines()[1:])  # Skip the first line
    cleaned_response = cleaned_response.replace("*", "")  # Strip asterisks
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_response)

# 6. Log execution times
def log_execution_time(start_time, end_time):
    """
    Logs the start, end, and total execution times.

    Args:
        start_time (datetime): The start time of the execution.
        end_time (datetime): The end time of the execution.
    """
    print(f"Program started at: {start_time}")
    print(f"Program ended at: {end_time}")
    print(f"Total execution time: {end_time - start_time}")

### Main Script ###

def only_syll(input_file):
    """
    Main workflow to process the text, query the model, and save the output.
    """
    # Record start time
    start_time = datetime.now()

    # File paths
    output_file = "llmop.txt"
    model_name = "my-model"

    # Load and slice the user input
    user_prompt = load_and_slice_text(input_file)
    
    

    if user_prompt.strip():

        # Generate and combine prompts
        system_prompt = create_system_prompt()
        combined_prompt = combine_prompts(system_prompt, user_prompt)
        
        
        

        # Query the Ollama model
        response = query_ollama_model(model_name, combined_prompt)
        
    

        # Save the response to a file
        save_response_to_file(response, output_file)
        return output_file
    else:
        print("No valid text found between the first and last occurrence of 'Module'.")

# if __name__ == "__main__" :
#     news = only_syll("syl_text.txt")
    