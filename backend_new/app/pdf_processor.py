import re
from pathlib import Path

import fitz


def _extract_dwf_text(dwf_path):
    data = Path(dwf_path).read_bytes()
    decoded = data.decode("utf-8", errors="ignore")
    decoded += "\n" + data.decode("utf-16-le", errors="ignore")

    text_chunks = re.findall(r"[\x20-\x7e]{3,}", decoded)
    return "\n".join(text_chunks)


def extract_text(drawing_path):
    if Path(drawing_path).suffix.lower() == ".dwf":
        return _extract_dwf_text(drawing_path)

    doc = fitz.open(drawing_path)

    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    doc.close()

    return text