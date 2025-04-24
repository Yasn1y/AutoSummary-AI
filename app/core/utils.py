import os
import PyPDF2
from typing import Optional, Union

def read_text_file(filepath: str) -> Optional[str]:
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf_file(filepath: str) -> Optional[str]:
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        print(f"Ошибка чтения PDF: {e}")
        return None

def get_file_content(filepath: str) -> Union[str, None]:
    if filepath.endswith(".pdf"):
        return read_pdf_file(filepath)
    elif filepath.endswith(".txt"):
        return read_text_file(filepath)
    else:
        print("Неподдерживаемый формат файла")
        return None