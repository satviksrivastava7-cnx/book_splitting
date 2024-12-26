import os
import json
from PyPDF2 import PdfReader, PdfWriter
import sys

def log_message(message):
    print(message)
    sys.stdout.flush()

def split_pdf_by_chapters(book_pdf, chapter_metadata, output_dir, log_message, root):
    reader = PdfReader(book_pdf)
    num_pages = len(reader.pages)
    log_message(f"Total pages in PDF {os.path.basename(book_pdf)}: {num_pages}")
    root.update()

    for i, chapter in enumerate(chapter_metadata):
        chapter_name = chapter['chapter_title'].replace('/', '-')
        try:
            start_page = int(chapter['chapter_starting_page_number']) - 1
            end_page = (
                int(chapter_metadata[i + 1]['chapter_starting_page_number']) - 1
                if i + 1 < len(chapter_metadata)
                else int(chapter['chapter_ending_page_number'])
            )
        except ValueError as e:
            log_message(f"Skipping chapter due to invalid page numbers: {chapter_name}. Error: {e}")
            root.update()
            continue

        chapter_dir = os.path.join(output_dir, chapter_name)
        os.makedirs(chapter_dir, exist_ok=True)

        chapter_pdf_path = os.path.join(chapter_dir, f"{chapter_name}.pdf")
        writer = PdfWriter()

        for page_num in range(start_page, end_page):
            if (page_num + 1) % 2 == 0:
                writer.add_page(reader.pages[page_num])

        if len(writer.pages) > 0:
            with open(chapter_pdf_path, 'wb') as chapter_pdf:
                writer.write(chapter_pdf)

            log_message(f"Created chapter PDF (odd pages only): {chapter_name} at {chapter_pdf_path}")
        else:
            log_message(f"No odd pages found for chapter: {chapter_name}, skipping.")
        
        root.update()

def organize_books(input_pdf_dir, input_json_dir, output_dir, log_message, root):
    os.makedirs(output_dir, exist_ok=True)
    for subject_file in os.listdir(input_pdf_dir):
        if subject_file.endswith('.pdf'):
            subject_name = os.path.splitext(subject_file)[0]
            subject_pdf = os.path.join(input_pdf_dir, subject_file)
            json_file = os.path.join(input_json_dir, f"{subject_name}.json")

            if os.path.exists(json_file):
                log_message(f"Processing book: {subject_name}")
                root.update()
                with open(json_file, 'r') as f:
                    chapter_metadata = json.load(f)

                subject_dir = os.path.join(output_dir, subject_name)
                os.makedirs(subject_dir, exist_ok=True)

                split_pdf_by_chapters(subject_pdf, chapter_metadata, subject_dir, log_message, root)
            else:
                log_message(f"JSON metadata not found for: {subject_name}")
                root.update()
