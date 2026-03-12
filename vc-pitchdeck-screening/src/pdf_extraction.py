from pathlib import Path

import fitz


def extract_pitchdeck_text(pdf_path: str) -> str:
    """Extract text from all pages in a pitch deck PDF."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    page_texts = []
    with fitz.open(path) as doc:
        for page in doc:
            page_texts.append(page.get_text("text"))

    return "\n".join(page_texts).strip()
