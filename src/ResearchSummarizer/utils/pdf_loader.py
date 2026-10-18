from __future__ import annotations

import re
from collections import Counter

import pdfplumber

from ResearchSummarizer.logging import logger


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


def _remove_repeated_headers_footers(pages_text: list[str], min_repeat_frac: float = 0.2) -> list[str]:
    """Remove lines that repeat across many pages (likely header/footer)."""
    if not pages_text:
        return pages_text

    line_counts = Counter()
    page_lines = []
    for p in pages_text:
        lines = [line.strip() for line in p.splitlines() if line.strip()]
        page_lines.append(lines)
        line_counts.update(set(lines))  # count per page, not per occurrence

    threshold = max(2, int(len(pages_text) * min_repeat_frac))
    repeated = {line for line, c in line_counts.items() if c >= threshold and len(line) <= 120}

    cleaned_pages = []
    for lines in page_lines:
        cleaned = [line for line in lines if line not in repeated]
        cleaned_pages.append("\n".join(cleaned))
    return cleaned_pages


def _ocr_pages(
    pdf_path: str, pages_text: list[str], page_indices: list[int], poppler_path: str | None, lang: str
) -> None:
    """OCR the given pages in place. Skips OCR (with a warning) if Poppler/Tesseract are missing."""
    try:
        import pytesseract
        from pdf2image import convert_from_path
        from pdf2image.exceptions import PDFInfoNotInstalledError
    except ImportError:
        logger.warning("pdf2image/pytesseract not installed; skipping OCR")
        return

    for i in page_indices:
        try:
            images = convert_from_path(pdf_path, dpi=200, first_page=i + 1, last_page=i + 1, poppler_path=poppler_path)
            if images:
                pages_text[i] = pytesseract.image_to_string(images[0], config=f"-l {lang} --oem 1 --psm 3")
        except (PDFInfoNotInstalledError, pytesseract.TesseractNotFoundError):
            logger.warning("Poppler or Tesseract not found on PATH; skipping OCR")
            return
        except Exception:
            logger.exception(f"OCR failed on page {i + 1}")


def load_pdf_as_block(
    pdf_path: str,
    *,
    max_pages: int | None = None,
    ocr_mode: str = "auto",
    poppler_path: str | None = None,
    tesseract_lang: str = "eng",
) -> str:
    """
    Returns the entire PDF as ONE cleaned text block.
    - Extracts embedded text per page (fast, low memory)
    - OCR only for pages with no text (auto), or force/disable via ocr_mode
    - Gracefully skips OCR if Poppler/Tesseract are missing
    """
    pages_text: list[str] = []
    ocr_needed: list[int] = []

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]
        for i, page in enumerate(pages):
            t = page.extract_text() or ""
            if t.strip():
                pages_text.append(t)
            else:
                pages_text.append("")
                ocr_needed.append(i)

    if ocr_mode == "force":
        ocr_needed = list(range(len(pages_text)))
    if ocr_mode != "never" and ocr_needed:
        _ocr_pages(pdf_path, pages_text, ocr_needed, poppler_path, tesseract_lang)

    pages_text = _remove_repeated_headers_footers(pages_text)
    big_text = _cleanup("\n\n".join(pages_text))
    return big_text
