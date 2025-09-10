
from __future__ import annotations
import re
from typing import Iterable, List, Optional
import pdfplumber

def _cleanup(text: str) -> str:
    lines_out = []
    for line in text.splitlines():
        s = line.strip()
        if re.fullmatch(r"\d{1,4}", s):  # "12"
            continue
        if re.fullmatch(r"(?i)page\s*\d{1,4}(?:\s*/\s*\d{1,4})?", s):  # "Page 3" / "Page 3/20"
            continue
        if re.fullmatch(r"\d{1,4}\s*/\s*\d{1,4}", s):  # "3/20"
            continue
        lines_out.append(line)
    text = "\n".join(lines_out)

    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def _remove_repeated_headers_footers(pages_text: List[str], min_repeat_frac: float = 0.2) -> List[str]:
    """Remove lines that repeat across many pages (likely header/footer)."""
    if not pages_text:
        return pages_text

    from collections import Counter
    line_counts = Counter()
    page_lines = []
    for p in pages_text:
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        page_lines.append(lines)
        line_counts.update(set(lines))  # count per page, not per occurrence

    threshold = max(2, int(len(pages_text) * min_repeat_frac))
    repeated = {l for l, c in line_counts.items() if c >= threshold and len(l) <= 120}

    cleaned_pages = []
    for lines in page_lines:
        cleaned = [l for l in lines if l not in repeated]
        cleaned_pages.append("\n".join(cleaned))
    return cleaned_pages

def load_pdf_as_block(
    pdf_path: str,
    *,
    max_pages: Optional[int] = None,
    ocr_mode: str = "auto",               
    poppler_path: Optional[str] = None,   
    tesseract_lang: str = "eng",
) -> str:
    """
    Returns the entire PDF as ONE cleaned text block.
    - Extracts embedded text per page (fast, low memory)
    - OCR only for pages with no text (auto), or force/disable via ocr_mode
    - Gracefully skips OCR if Poppler/Tesseract are missing
    """
    pages_text: List[str] = []
    ocr_needed: List[int] = []

   
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]
        for i, page in enumerate(pages):
            t = page.extract_text() or ""
            if t.strip():
                pages_text.append(t)
            else:
                pages_text.append("")  
                ocr_needed.append(i)

    should_ocr = (ocr_mode == "force") or (ocr_mode == "auto" and len(ocr_needed) > 0)
    if should_ocr:
        try:
            from pdf2image import convert_from_path
            from pdf2image.exceptions import PDFInfoNotInstalledError
            import pytesseract

            for i in ocr_needed:
                try:
                    imgs = convert_from_path(
                        pdf_path,
                        dpi=200,  
                        first_page=i + 1,
                        last_page=i + 1,
                        poppler_path=poppler_path,
                    )
                    if not imgs:
                        continue
                    ocr_conf = f"-l {tesseract_lang} --oem 1 --psm 3"
                    pages_text[i] = pytesseract.image_to_string(imgs[0], config=ocr_conf)
                except PDFInfoNotInstalledError:
                    break
                except Exception:
                    continue
        except Exception:
            pass

    pages_text = _remove_repeated_headers_footers(pages_text)
    big_text = _cleanup("\n\n".join(pages_text))
    return big_text
