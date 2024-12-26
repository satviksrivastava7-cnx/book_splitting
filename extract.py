import google.generativeai as genai
import os
import glob
from dotenv import load_dotenv
import sys

load_dotenv()
gemini_api_key = os.getenv("API_KEY")
genai.configure(api_key=gemini_api_key)

def log_message(message):
    print(message)
    sys.stdout.flush() 

def send_to_llm_for_parsing(pdf_path, log_message):
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    book = genai.upload_file(pdf_path)
    prompt = (
        "Refer to the following PDF and go through it and return the chapter details, within the PDF, in a structured JSON format without any other text. "
        "The content should be in the following format: chapter_number, chapter_title, "
        "chapter_starting_page_number, chapter_ending_page_number, chapter_topics_list. "
        "Note: While fetching the chapter_starting number, make sure that it is the actual number of that page while traversing the PDF. "
        "Don't add JSON format text at the beginning or end of the response. Just return the JSON."
    )
    response = model.generate_content([prompt, book])
    return response.text

def process_books_in_directory(directory_path, parsed_dir, log_message, root):
    os.makedirs(parsed_dir, exist_ok=True)
    unparsed_file = os.path.join(parsed_dir, "unparsed_books.txt")
    parsed_file = os.path.join(parsed_dir, "parsed_books.txt")
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))

    log_message(f"Found {len(pdf_files)} PDF files to process in {directory_path}")
    root.update()
    with open(unparsed_file, "w") as unparsed:
        for pdf_path in pdf_files:
            book_name = os.path.splitext(os.path.basename(pdf_path))[0]
            try:
                log_message(f"Parsing: {book_name}")
                root.update()
                content = send_to_llm_for_parsing(pdf_path, log_message)
                if content: 
                    output_path = os.path.join(parsed_dir, f"{book_name}.txt")
                    with open(output_path, "w") as parsed_txt:
                        parsed_txt.write(content)
                    log_message(f"Successfully parsed: {book_name}")
                    root.update()
                else:
                    log_message(f"Failed to parse: {book_name} - Empty content returned")   
                    root.update()
                    unparsed.write(f"{book_name}\n")
            except Exception as e:
                log_message(f"Failed to parse: {book_name}. Error: {e}")
                root.update()
                unparsed.write(f"{book_name}\n")
    
    log_message("Processing complete.")
    root.update()
    return log_message

