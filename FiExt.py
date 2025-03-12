import fitz

def extract_text_from_pdf(file_path, output_text_file):
    """
    Extracts text from a PDF and saves it to a text file.

    Args:
        file_path (str): The path to the PDF file provided by GUI.
        output_text_file (str): The path to the output text file.
    Returns:
        str: The extracted text.
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text)
    return text

def syll_read(syllabus_file, output_text_file):
    """
    Extracts text from the syllabus PDF and saves it to a text file.

    Args:
        syllabus_file (str): The path to the syllabus PDF file provided by GUI.
        output_text_file (str): The path to the output text file.
    Returns:
        str: The extracted text.
    """
    text = ""
    with fitz.open(syllabus_file) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text)
    return text

# Example usage
if __name__ == "__main__":
    # Simulate receiving file paths from a GUI
    textbook_pdf_path = input("Enter the path to the textbook PDF file: ")  # Replace with GUI file picker
    textbook_output_path = "textbook_output.txt"
    syllabus_pdf_path = input("Enter the path to the syllabus PDF file: ")  # Replace with GUI file picker
    syllabus_output_path = input("Enter the path for the syllabus output text file: ")  # Replace with GUI output selection

    # Process the textbook PDF
    print(f"Extracting text from {textbook_pdf_path}...")
    extract_text_from_pdf(textbook_pdf_path, textbook_output_path)
    print(f"Text extracted and saved to {textbook_output_path}")

    # Process the syllabus PDF
    print(f"Extracting text from {syllabus_pdf_path}...")
    syll_read(syllabus_pdf_path, syllabus_output_path)
    print(f"Text extracted and saved to {syllabus_output_path}")
