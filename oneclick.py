from datetime import datetime
from FiExt import extract_text_from_pdf
from ollmsyl import only_syll

from testbert import save_results
from FaissOllm import process_queries_from_file
from split_notes import split_text_by_modules

def oneclick(text_file,syl_file):
    start_time = datetime.now()
    text_file_t=extract_text_from_pdf(text_file,"output_text.txt")
    print("Completed1")
    syl_file_t=extract_text_from_pdf(syl_file,"syl_text.txt")
    print("Completed2")
    syllabus=only_syll("syl_text.txt")
    print("Completed3")
    embed_array,embed_json=save_results("output_text.txt")
    print("Completed4")
    
    process_queries_from_file("llmop.txt","llama3:latest",embed_array,embed_json,"final_notes.txt")
    print("Completed5")
    try:
        
        notes=split_text_by_modules("final_notes.txt")
        
    except:
        print("Splitting not working")
    
    end_time = datetime.now()
    print(f"Program started at: {start_time}")
    print(f"Program ended at: {end_time}")
    print(f"Total execution time: {end_time - start_time}")
    return notes

# oneclick("output_text.txt","syl_text")
    