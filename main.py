from transformers import LayoutLMForTokenClassification, LayoutLMTokenizer
from datasets import Dataset
import torch
from PIL import Image, ImageDraw
import pytesseract

# Function to preprocess the image for LayoutLM
def preprocess_image_layoutlm(image_path):
    image = Image.open(image_path).convert("RGB")
    return image

# Function to extract text and layout information using Tesseract
def extract_text_with_bbox(image):
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    words = ocr_data['text']
    bboxes = []
    normalized_bboxes = []
    for i in range(len(words)):
        if words[i].strip():  # If the word is not empty
            x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
            bboxes.append([x, y, x + w, y + h])

    # Normalize bounding boxes
    width, height = image.size
    for bbox in bboxes:
        normalized_bboxes.append([
            bbox[0] / width,
            bbox[1] / height,
            bbox[2] / width,
            bbox[3] / height
        ])

    return ocr_data['text'], bboxes

# Function to extract index using LayoutLM and return annotated image
def extract_index_with_layoutlm(image_path):
    image = preprocess_image_layoutlm(image_path)

    # Load LayoutLM model and tokenizer
    model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")
    tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")

    # Extract OCR text and bounding boxes
    words, bboxes = extract_text_with_bbox(image)

    # Tokenize input data
    encoded_inputs = tokenizer(
        words,
        boxes=[[bbox[0], bbox[1], bbox[2], bbox[3]] for bbox in bboxes],
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    # Get model predictions
    outputs = model(**encoded_inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)

    # Decode predictions and find chapters
    chapters = []
    current_chapter = {"Chapter Number": None, "Chapter Title": None, "Chapter Start Page": None}

    # Create a drawing context for annotation
    draw = ImageDraw.Draw(image)

    for i, label in enumerate(predictions[0]):
        token = tokenizer.decode(encoded_inputs.input_ids[0][i])
        bbox = bboxes[i]
        if label == 1:  # Chapter number
            if current_chapter["Chapter Number"]:
                chapters.append(current_chapter)
                current_chapter = {"Chapter Number": None, "Chapter Title": None, "Chapter Start Page": None}

            current_chapter["Chapter Number"] = token
            draw.rectangle(bbox, outline="blue", width=2)
        elif label == 2:  # Chapter title
            current_chapter["Chapter Title"] = token
            draw.rectangle(bbox, outline="green", width=2)
        elif label == 3:  # Start page
            current_chapter["Chapter Start Page"] = token
            draw.rectangle(bbox, outline="red", width=2)

    # Append last chapter if valid
    if current_chapter["Chapter Number"]:
        chapters.append(current_chapter)

    # Save annotated image
    annotated_image_path = image_path.replace(".png", "_annotated.png")
    image.save(annotated_image_path)

    return chapters, annotated_image_path

# Example usage
image_path = "/Users/satvik/Documents/Projects/Book_Splitter/images/book3.png"
details, annotated_image_path = extract_index_with_layoutlm(image_path)
print("Extracted Details:", details)
print("Annotated Image Saved at:", annotated_image_path)
