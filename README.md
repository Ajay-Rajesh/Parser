# Parser

An open-source multilingual OCR + NLP document parser for Government, Banking, and Educational forms.

## Features

* OCR using **Surya**
* Digital PDF text extraction with **PyMuPDF**
* Automatic OCR fallback for scanned documents
* Text cleaning pipeline
* Duplicate detection using SHA-256 hashing
* LangChain chunking
* Multilingual embeddings with Sentence Transformers
* Chroma vector database for RAG-ready retrieval

## Project Structure

```text
Parser/
├── backend/
│   ├── parser/
│   │   ├── upload.py
│   │   ├── extract.py
│   │   ├── cleaner.py
│   │   ├── chuncker.py
│   │   ├── pdf_reader.py
│   │   └── ocr.py
│   │
│   ├── knowledge_base/
│   │   ├── raw/
│   │   ├── extracted/
│   │   ├── user_kb/
│   │   └── vector_db/
│   │
│   └── user_uploads/
│
├── .gitignore
└── README.md
```

## Pipeline

```text
PDF Upload
    ↓
Extract (PyMuPDF)
    ↓
OCR (Surya if needed)
    ↓
Clean Text
    ↓
Duplicate Check
    ↓
Save JSON
    ↓
Chunk
    ↓
Embedding
    ↓
Chroma Vector DB
```

## Installation

```bash
git clone https://github.com/Ajay-Rajesh/Parser.git
cd Parser

python -m venv V1-venv
V1-venv\Scripts\activate

pip install -r requirements.txt
```

## Run

Start the drag-and-drop upload interface:

```bash
python backend/parser/upload.py
```

For one-time ingestion of the existing knowledge base:

```bash
python backend/parser/chuncker.py
```

## Tech Stack

* Python
* PyMuPDF
* Surya OCR
* LangChain
* Sentence Transformers
* ChromaDB
* PySide6

## Roadmap

* [x] PDF extraction
* [x] OCR fallback
* [x] Text cleaning
* [x] User document storage
* [x] Vectorization
* [ ] Retrieval pipeline
* [ ] RAG response generation
* [ ] Translation & voice support

## License

Released under the MIT License.
