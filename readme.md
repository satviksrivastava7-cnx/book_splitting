## Content Curator

This is python application is designed to preprocess and curate unstructured PDF books into structured JSON files, meanwhile maintaining the original structure of the book and splitting the content into chapter specific PDF files. This aims to be used for the data curation of the books, for the purpose of creating a structured dataset for the AI models to learn from, in regards to BrightClass AI.

---

## **Pipeline Workflow**

### **1. PDF Splitting**

- **Objective**: Divide a multi-chapter PDF into individual chapters or sections based on page numbers or markers.

- **Steps**:
  1. Read the input PDF file.
  2. Split the file into smaller PDFs using predefined page ranges.
  3. Save the output PDFs in a structured folder hierarchy.
- **Tools**: `PyPDF2`, `pdfplumber`

### **2. Information Extraction**
- **Objective**: Extract chapter titles, topics, and other metadata from the individual PDFs.
- **Steps**:
  1. Parse each split PDF for text using OCR (if needed).
  2. Extract chapter titles, topic names, and other metadata.
  3. Store the extracted data in a JSON format.
- **Tools**: `pdfplumber`, `PyPDF2`, `Tesseract OCR` (for scanned PDFs)

### **3. Post-Processing**
- **Objective**: Clean, validate, and organize the extracted data into a standard syllabus format.
- **Steps**:
  1. Read parsed JSON files containing chapter data.
  2. Map the chapter and topic information into a structured syllabus.
  3. Add metadata like board, class, and book name.
  4. Output a `syllabus.json` file for each subject.
- **Tools**: `Python`, JSON manipulation

---

## **Project Features**
- **Automated PDF Splitting**: Handles large educational resources and divides them into manageable files.
- **Metadata Extraction**: Extracts titles, topics, and hierarchical information from PDFs.
- **Standardized Output**: Produces JSON files formatted for easy integration into other platforms.
- **Error Handling**: Logs errors and skips invalid files to ensure smooth execution.

---

## Instructions

1. Clone the repository
```bash     
    git clone https://github.com/satviksrivastava-cnx/book-curator.git
```
2. Create a virtual environment
```bash 
    python -m venv env
```
3. Activate the virtual environment
```bash
    source env/bin/activate
```
4. Install the required packages using 
```bash 
    pip install -r requirements.txt
```
5. Create a `.env` file in the project root and store your gemini api key inside it.
6. Run the `main.py` file to start the application.
```bash
    python3 main.py
```

---

## How to Use

1. Place the raw PDFs in the input/PDFs folder.
2. Define chapter ranges and metadata in input/metadata.json.
3. Run the scripts sequentially or integrate them into a single script.
4. The curated contents are saved in provided output folder. 

