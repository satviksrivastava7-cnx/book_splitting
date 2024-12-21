import fitz 
import pytesseract
from pytesseract import Output
from PIL import Image
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    return images

def extract_text_with_boxes(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    words = []
    boxes = []
    for i, word in enumerate(data['text']):
        if word.strip():
            words.append(word)
            boxes.append((data['left'][i], data['top'][i],
                           data['left'][i] + data['width'][i],
                           data['top'][i] + data['height'][i]))
    return words, boxes

def query_gemini_api(text, query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"The table of contents is: {text}.\nQuery: {query}")
    return response.text

def process_pdf(pdf_path, query):
    images = convert_pdf_to_images(pdf_path)
    content_image = images[8]
    text, _ = extract_text_with_boxes(content_image) 
    combined_query = " ".join(text) + f"\nQuery: {query}"
    response = query_gemini_api(combined_query, query)
    print(f"Content from the image: {response}")

if __name__ == "__main__":
    pdf_path = "/Users/satvik/Documents/Projects/Book_Splitter/Geography.pdf"
    query = "Describe the chapter details like chapter name, page number, and content from the image. The details should be like this: Chapter Number,  Chapter Name, Chapter Starting Page Number, Chapter Ending Page Number."
    process_pdf(pdf_path, query)