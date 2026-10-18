import pytest

from ResearchSummarizer.utils.pdf_loader import _cleanup, _remove_repeated_headers_footers, load_pdf_as_block


def test_cleanup_drops_page_numbers_and_joins_hyphenation():
    text = "Intro-\nduction to models\n12\nPage 3 / 20\n3/20\n\n\n\nBody   text"
    assert _cleanup(text) == "Introduction to models\n\nBody text"


def test_repeated_headers_and_footers_are_removed():
    pages = [f"Journal of Things\nUnique content {i}\nPreprint - do not cite" for i in range(5)]
    cleaned = _remove_repeated_headers_footers(pages)
    assert cleaned == [f"Unique content {i}" for i in range(5)]


def test_remove_repeated_handles_empty_input():
    assert _remove_repeated_headers_footers([]) == []


@pytest.fixture
def sample_pdf(tmp_path):
    canvas = pytest.importorskip("reportlab.pdfgen.canvas")
    path = tmp_path / "paper.pdf"
    c = canvas.Canvas(str(path))
    for page in range(3):
        c.drawString(72, 800, "Proceedings of Testing")
        c.drawString(72, 700, f"Section {page}: transformers summarize long documents.")
        c.showPage()
    c.save()
    return path


def test_load_pdf_extracts_text_and_strips_running_header(sample_pdf):
    text = load_pdf_as_block(str(sample_pdf), ocr_mode="never")
    assert "Section 0: transformers summarize long documents." in text
    assert "Section 2" in text
    assert "Proceedings of Testing" not in text


def test_load_pdf_respects_max_pages(sample_pdf):
    text = load_pdf_as_block(str(sample_pdf), max_pages=1, ocr_mode="never")
    assert "Section 0" in text
    assert "Section 1" not in text
