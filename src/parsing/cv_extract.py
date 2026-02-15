from pathlib import Path
from pypdf import PdfReader
import docx

def read_pdf(path: Path) -> str:
    r = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in r.pages)

def read_docx(path: Path) -> str:
    d = docx.Document(str(path))
    return "\n".join(p.text for p in d.paragraphs)

def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def read_cv(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return read_pdf(p)
    if p.suffix.lower() == ".docx":
        return read_docx(p)
    return read_txt(p)