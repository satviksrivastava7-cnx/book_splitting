from google.generativeai import Conversation, palm
import os
from PyPDF2 import PdfReader
import dotenv

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
palm.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def ask_gemini_question(context, question):
    """Use Gemini to ask a question based on the provided context."""
    try:
        conversation = Conversation(model="models/chat-bison-001")  
        conversation.append(text=context, role="user")
        conversation.append(text=question, role="user") 
        response = conversation.complete()
        return response[0].text or "No response from Gemini."
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return None

def main():
    pdf_path = "path_to_pdf.pdf"

    print("Extracting text from the PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text:
        print("Failed to extract text from the PDF.")
        return

    print("Text extracted successfully.")

    question = "Refer to the above book pdf and provide me with a list of chapters in the book along with their starting page number"
    answer = ask_gemini_question(context=pdf_text, question=question)

    if answer:
        print(f"Answer: {answer}")
    else:
        print("Failed to get an answer from Gemini.")

if __name__ == "__main__":
    main()
