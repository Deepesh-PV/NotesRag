
# NotesRAG

## Automated Syllabus-Aligned Notes Generation

### 📌 Overview
NotesRAG is an AI-powered system that automates the process of generating syllabus-aligned study notes from textbooks. It leverages Retrieval-Augmented Generation (RAG) along with Context-Based Extraction of Concepts (**COBEC**) to extract and generate relevant educational content efficiently. The system helps students and educators save time by transforming textbooks into structured, concise notes while ensuring alignment with syllabus requirements.to run the file run gui12.

### 🚀 Features
- **Automated Note Generation** – Extracts syllabus-aligned notes from textbooks.
- **AI-Powered Concept Extraction** – Identifies and ranks key concepts.
- **RAG for Content Retrieval** – Ensures high-quality, syllabus-relevant content.
- **COBEC** – Automatically ranks concepts in each module using DBpedia Spotlight.
- **Custom Syllabus Extraction** – Uses tailored functions to extract syllabus based on **VTU (Visvesvaraya Technological University)** format.
- **Interactive Chatbot** – Provides real-time answers based on extracted knowledge.
- **Scalable & Efficient** – Handles large datasets and diverse academic domains.

### 🏗️ System Architecture
1. **Textbook & Syllabus Upload** – Users upload PDFs for processing.
2. **PDF Extraction** – The system extracts text from uploaded files.
3. **Custom Syllabus Extraction** – A custom function tailored for **VTU** syllabus format extracts syllabus topics. **Users must edit this function according to their syllabus format for optimal performance.**
4. **Semantic Embeddings** – Uses **sBERT** to create meaningful representations of text.
5. **Similarity Search** – **FAISS** identifies the most relevant textbook content for syllabus topics.
6. **Notes Generation** – **Llama3** generates structured and concise notes. **Users can customize this component to integrate any large language model (LLM) of their choice.**
7. **Concept Ranking & Enrichment (COBEC)** – **DBpedia Spotlight** extracts key concepts and automatically ranks them by relevance within each module.
8. **Interactive Chatbot** – Uses retrieved content to generate contextually rich responses.

### 🛠️ Tech Stack
- **Python** – Core programming language
- **sBERT** – Semantic text embeddings
- **FAISS** – Fast similarity search
- **Llama3** – Language model for text generation (customizable for other LLMs)
- **DBpedia Spotlight** – Concept extraction and ranking
- **MuPDF** – PDF text extraction
- **Tkinter** – User-friendly GUI

### 📥 Installation & Setup
#### Prerequisites
- Python 3.x +
- pip (Python package manager)

#### Installation
Clone the repository:
```bash
git clone https://github.com/your-username/NotesRAG.git
cd NotesRAG
```
Install dependencies:
```bash
pip install -r requirements.txt
```

#### Running the Application
```bash
python main.py
```

### 🎯 How It Works
1. Upload textbook and syllabus PDFs through the UI.
2. Process the documents to extract relevant sections.
3. Extract syllabus topics using **Custom Syllabus Extraction** tailored for **VTU**. **Users must customize this function to suit their institution's syllabus format.**
4. Generate concise study notes aligned with the syllabus using **Llama3** or any other preferred LLM.
5. Automatically rank key concepts using **COBEC**.
6. Interact with the chatbot for additional explanations.
7. Download structured notes for easy study and reference.

### 📊 Future Enhancements
- Multi-language support for global accessibility.
- Real-time curriculum updates using APIs.
- Advanced AI chatbot for deeper topic understanding.
- Cloud-based deployment for seamless access.

### 🤝 Contributors
- Deepesh P V
- Dhanvith Shetty
- M D Keerthan Kumar
- Maneesh Anchan B  
Under the guidance of **Prof. Abhishek Kumar**

### 📜 License
This project is licensed under the MIT License. See LICENSE for more details.

