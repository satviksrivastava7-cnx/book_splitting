import fitz
import pytesseract
from pytesseract import Output
from PIL import Image
import io

def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append((page_num, img))
    return images

def extract_text_from_image(image):
    data = pytesseract.image_to_string(image)
    return data.lower()

def find_page_with_keywords(images, keywords):
    for page_num, image in images:
        text = extract_text_from_image(image)
        if any(keyword in text for keyword in keywords):
            return page_num, image
    return None, None

def get_page_with_content(pdf_path, keywords=["index", "content", "chapter list", "chapter", "lesson", "lesson name"]):
    images = convert_pdf_to_images(pdf_path)
    page_num, page_image = find_page_with_keywords(images, keywords)
    if page_image:
        page_image.show()
        return page_num, page_image
    else:
        print("No matching page found.")
        return None, None

if __name__ == "__main__":
    pdf_path = "/Users/satvik/Documents/Projects/Book_Splitter/Mathematics.pdf" 
    page_num, page_image = get_page_with_content(pdf_path)
    if page_image:
        print(f"Page {page_num + 1} contains the relevant content.")
