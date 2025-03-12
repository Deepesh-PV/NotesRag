import re
import os
import traceback
from cobec_final import cobec_true

def split_text_by_modules(input_file):
    print("Running1")
    notes = list()
    try:
        # Read the contents of the input file with UTF-8 encoding
        with open(input_file, "r", encoding="utf-8", errors="replace") as file:
            content = file.read()
            print("Reading")

        # Clean up the content: remove extra spaces and tabs
        cleaned_content = content.replace('*', ' ')

        # Split the content into modules based on the module headings
        modules = re.split(r"(?i)(Module-[^\n]+)", cleaned_content)
        print(len(modules))

        for i in range(1, len(modules), 2):  # Step through every second element
            module_heading = modules[i].strip()
            module_content = modules[i + 1].strip() if i + 1 < len(modules) else ''

            if not module_content:
                print(f"Warning: No content found for {module_heading}")
                continue

            # Extract a clean module name
            module_name = re.sub(r'[^\w\s-]', '', module_heading.strip())

            # Save each module's content to a separate file
            file_path = save_module_to_file(module_name, module_content)
            if file_path:
                notes.append(file_path)
                print(file_path)
                
                cobec_true(file_path)

        print("Modules successfully saved.")
        

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())

    return notes

def save_module_to_file(module_name, content):
    """Helper function to save the module content to a file."""
    try:
        # Clean the content by replacing tabs with spaces and removing unnecessary whitespace
        content = content.replace('\t', ' ').strip()

        # Create a safe file name by replacing spaces with underscores
        file_name = f"{module_name.replace(' ', '_')}.txt"
        file_path = os.path.join(os.getcwd(), file_name)

        # Save the module content to the file with UTF-8 encoding
        with open(file_path, "w", encoding="utf-8") as module_file:
            module_file.write(f"{module_name}\n")
            module_file.write(content)

        print(f"Saved: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving {module_name}: {e}")
        print(traceback.format_exc())
        return None