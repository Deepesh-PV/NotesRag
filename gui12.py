import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
import webbrowser
from oneclick import oneclick
from QnA import model
# Create a directory for dummy files




# Dummy function to simulate processing PDF files
def process_pdfs(textbook_path, syllabus_path):
    """
    Simulates processing of textbook and syllabus PDFs.
    Returns a list of dummy text file paths as output.
    """
    return oneclick(text_file=textbook_path,syl_file=syllabus_path)


# Function to open the file
def open_file(file_path):
    if os.path.exists(file_path):
        webbrowser.open(file_path)
    else:
        messagebox.showerror("File Not Found", f"File does not exist: {file_path}")

# Function to process the files and generate buttons dynamically
def process_files():
    textbook_path = textbook_entry.get().strip()
    syllabus_path = syllabus_entry.get().strip()
    
    if not textbook_path or not syllabus_path:
        messagebox.showwarning("Missing Input", "Please upload both Textbook and Syllabus PDFs.")
        return

    # Call the dummy processing function
    result_paths = process_pdfs(textbook_path, syllabus_path)
    
    # Clear the button frame before adding new buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Add a heading for "Generated Notes"
    notes_heading_label = tk.Label(button_frame, text="Generated Notes", bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"))
    notes_heading_label.pack(pady=10)

    # Dynamically create buttons for each file
    for file_path in result_paths:
        file_button = tk.Button(
            button_frame,
            text=os.path.basename(file_path),
            command=lambda p=file_path: open_file(p),
            bg="#3c3f41",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        file_button.pack(fill=tk.X, pady=5)

# Function to upload the textbook PDF
def upload_textbook():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        textbook_entry.delete(0, tk.END)
        textbook_entry.insert(0, file_path)
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file for the textbook.")
        
    return file_path

# Function to upload the syllabus PDF
def upload_syllabus():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        syllabus_entry.delete(0, tk.END)
        syllabus_entry.insert(0, file_path)
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file for the syllabus.")
    return file_path

# Simple chatbot function
def chatbot_response(input_text):
    """
    A dummy chatbot function that returns "Hello" for any input.
    """
    return "Hello"

# Function to handle chatbot interaction
def handle_chatbot_input(event=None):
    input_text = chatbot_entry.get().strip()
    if input_text:
        chatbot_entry.delete(0, tk.END)
        response = model(input_text)
        chatbot_output.configure(state=tk.NORMAL)
        chatbot_output.insert(tk.END, f"You: {input_text}\n")
        chatbot_output.insert(tk.END, f"Bot: {response}\n\n")
        chatbot_output.configure(state=tk.DISABLED)
        chatbot_output.see(tk.END)

# GUI setup
root = tk.Tk()
root.title("PDF Processor with Chatbot Interface")
root.geometry("800x600")
root.configure(bg="#2b2b2b")

# Textbook upload section
textbook_frame = tk.Frame(root, bg="#2b2b2b")
textbook_frame.pack(pady=10, fill=tk.X, padx=20)

textbook_label = tk.Label(textbook_frame, text="Textbook PDF:", bg="#2b2b2b", fg="white", font=("Arial", 10))
textbook_label.pack(side=tk.LEFT, padx=5)

textbook_entry = tk.Entry(textbook_frame, width=50, bg="#3c3f41", fg="#ffffff", font=("Arial", 10), insertbackground="#ffffff")
textbook_entry.pack(side=tk.LEFT, padx=5)

textbook_button = tk.Button(
    textbook_frame, text="Upload", command=upload_textbook, bg="#3498db", fg="white", font=("Arial", 10, "bold")
)
textbook_button.pack(side=tk.LEFT, padx=5)

# Syllabus upload section
syllabus_frame = tk.Frame(root, bg="#2b2b2b")
syllabus_frame.pack(pady=10, fill=tk.X, padx=20)

syllabus_label = tk.Label(syllabus_frame, text="Syllabus PDF:", bg="#2b2b2b", fg="white", font=("Arial", 10))
syllabus_label.pack(side=tk.LEFT, padx=5)

syllabus_entry = tk.Entry(syllabus_frame, width=50, bg="#3c3f41", fg="#ffffff", font=("Arial", 10), insertbackground="#ffffff")
syllabus_entry.pack(side=tk.LEFT, padx=5)

syllabus_button = tk.Button(
    syllabus_frame, text="Upload", command=upload_syllabus, bg="#3498db", fg="white", font=("Arial", 10, "bold")
)
syllabus_button.pack(side=tk.LEFT, padx=5)

# Process PDFs button
process_button = tk.Button(
    root, text="Process PDFs", command=process_files, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
)
process_button.pack(pady=20)

# Frame for dynamically created buttons
button_frame = tk.Frame(root, bg="#2b2b2b", relief=tk.GROOVE, borderwidth=2)
button_frame.pack(fill=tk.Y, side=tk.RIGHT, padx=10, pady=10)

# Chatbot interface
chatbot_frame = tk.Frame(root, bg="#2b2b2b", relief=tk.GROOVE, borderwidth=2)
chatbot_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

chatbot_label = tk.Label(chatbot_frame, text="Chatbot", bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"))
chatbot_label.pack(pady=5)

chatbot_output = tk.Text(chatbot_frame, width=40, height=20, bg="#3c3f41", fg="#ffffff", font=("Arial", 10), wrap=tk.WORD, state=tk.DISABLED)
chatbot_output.pack(pady=5)

chatbot_entry = tk.Entry(chatbot_frame, bg="#3c3f41", fg="#ffffff", font=("Arial", 10), insertbackground="#ffffff")
chatbot_entry.pack(fill=tk.X, padx=5, pady=5)

chatbot_button = tk.Button(
    chatbot_frame, text="Send", command=handle_chatbot_input, bg="#3498db", fg="white", font=("Arial", 10, "bold")
)
chatbot_button.pack(pady=5)

# Bind the Enter key to the chatbot input handler
chatbot_entry.bind("<Return>", handle_chatbot_input)

# Run the application
root.mainloop()


