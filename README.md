# Parser

> **Open-source multilingual OCR + NLP document parser for Government, Banking & Educational PDFs.**

Parser is an offline document ingestion and retrieval pipeline that extracts text from digital and scanned PDFs, builds a multilingual vector knowledge base, and answers questions using RAG with English and Tamil voice output.

**Status:** Core pipeline completed • UI & model fine-tuning are the next phase.

---

## Features

* 📄 Digital PDF extraction with **PyMuPDF**
* 🌍 Multilingual OCR using **Surya OCR** (English + Tamil)
* 🔁 Automatic OCR fallback for scanned documents
* 🧹 Text cleaning & normalization
* 🔒 SHA-256 duplicate document detection
* ✂️ LangChain recursive text chunking
* 🧠 Sentence Transformer multilingual embeddings
* 🗂️ ChromaDB vector database
* 💬 Offline RAG document retrieval
* 🔊 English & Tamil Text-to-Speech (Piper ONNX)

---

## Pipeline

```text
PDF Upload
    │
    ▼
PyMuPDF Extraction
    │
    ├── Digital PDF
    └── Scanned PDF → Surya OCR
                │
                ▼
      Clean & Normalize
                │
                ▼
   SHA-256 Duplicate Check
                │
                ▼
        Structured JSON
                │
                ▼
     LangChain Chunking
                │
                ▼
SentenceTransformer Embeddings
                │
                ▼
     Chroma Vector Database
                │
                ▼
      Retrieve + Generate
                │
                ▼
    English / Tamil Speech
```

---

## Project Structure

```text
Parser/
├── backend/
│   ├── parser/
│   │   ├── upload.py
│   │   ├── process_upload.py
│   │   ├── extract.py
│   │   ├── cleaner.py
│   │   ├── chuncker.py
│   │   ├── retrieve.py
│   │   ├── generate.py
│   │   ├── chat.py
│   │   ├── speech.py
│   │   ├── pdf_reader.py
│   │   └── ocr.py
│   │
│   ├── Voices/
│   ├── knowledge_base/
│   │   ├── raw/
│   │   ├── extracted/
│   │   ├── user_kb/
│   │   └── vector_db/
│   │
│   └── user_uploads/
│
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/Ajay-Rajesh/Parser.git
cd Parser

python -m venv V1-venv
V1-venv\Scripts\activate

pip install -r requirements.txt
```

---

## Usage

### Upload & Process PDFs

```bash
python backend/parser/upload.py
```

### Build / Update Vector Database

```bash
python backend/parser/chuncker.py
```

### Chat with Documents

```bash
python backend/parser/chat.py
```

---

## Tech Stack

| Component  | Technology               |
| ---------- | ------------------------ |
| Language   | Python                   |
| PDF Parser | PyMuPDF                  |
| OCR        | Surya OCR                |
| Chunking   | LangChain                |
| Embeddings | Sentence Transformers    |
| Vector DB  | ChromaDB                 |
| RAG        | Local Retrieval Pipeline |
| TTS        | Piper ONNX               |

---

## Current Progress

| Module                 | Status         |
| ---------------------- | -------------- |
| PDF Extraction         | ✅ Complete     |
| OCR Fallback           | ✅ Complete     |
| Text Cleaning          | ✅ Complete     |
| Duplicate Detection    | ✅ Complete     |
| JSON Storage           | ✅ Complete     |
| LangChain Chunking     | ✅ Complete     |
| Embeddings             | ✅ Complete     |
| Chroma Vector Database | ✅ Complete     |
| Retrieval Pipeline     | ✅ Complete     |
| RAG Answer Generation  | ✅ Complete     |
| English & Tamil TTS    | ✅ Complete     |
| Desktop / Web UI       | ❎ In Progress |

---

## Future Roadmap

### UI

* Drag-and-drop desktop interface
* Chat interface with document history
* Progress indicators & upload manager
* Searchable knowledge base viewer

### Model Fine-Tuning

* Fine-tune on **50+ Government & Banking form types**
* Improve key-value field extraction (Name, DOB, Account No., IFSC, etc.)
* Better multilingual understanding for Indian regional documents
* Domain-specific instruction tuning for form assistance
* Expand supported languages beyond English & Tamil

---

## License

Released under the **MIT License**.

### Author

**Ajay Rajesh**
