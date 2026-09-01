import json
import hashlib
from pathlib import Path
import sys
from extract import extract_pdf
from cleaner import clean_pages
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from chuncker import ingest_kb

from extract import extract_pdf

USER_KB = Path(r"backend\knowledge_base\user_kb")


def save_if_new(data):
        USER_KB.mkdir(parents=True, exist_ok=True)

        text = "\n".join(
            page["text"]
            for page in data["pages"]
        )


        doc_hash = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

        for file in USER_KB.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    existing = json.load(f)

                if existing.get("doc_hash") == doc_hash:
                    print("Already exists in user_kb.")
                    return False

            except (json.JSONDecodeError, OSError):
                continue

        data["doc_hash"] = doc_hash

        filename = Path(data["source"]).stem + ".json"
        output_path = USER_KB / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"Added to user_kb: {output_path}")
        return True


class DropBox(QLabel):
    def __init__(self):
        super().__init__("Drop PDF Here")

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(400, 220)

        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #888;
                border-radius: 12px; 
                font-size: 20px;
            }
        """)
    

    


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()

        if file_path.lower().endswith(".pdf"):
            self.setText("PDF received ✓")

            result = process_upload(file_path)

            saved = save_if_new(result)

            if saved:
                ingest_kb(result,is_user=True)

            print(result)

def process_upload(pdf_path: str):

    pages = extract_pdf(pdf_path)
    pages = clean_pages(pages)



    data = {
        "source": pdf_path,
        "pages": pages
    }

    return data

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DropBox()
    window.show()

    sys.exit(app.exec())