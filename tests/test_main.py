import io
import builtins

import pikepdf
import pytest
from fastapi.testclient import TestClient

# Import the app after monkeypatching WeasyPrint classes in tests that need it
import main


client = TestClient(main.app)


def test_home_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": True}


def test_pdf_is_created():
    resp = client.post("/pdf", files={
        "html": ("law.html", "<h1>Hello</h1>", "text/html"),
        "css": ("style.css", "h1 { color: red }", "text/css"),
    })

    # Assert response basics
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.headers["content-disposition"] == "attachment; filename=\"download.pdf\""

    # Check the content looks like a pdf file in version 1.7
    assert resp.content.startswith(b"%PDF-1.7")

    print(resp.content)

    # check some metadata
    pdf = pikepdf.Pdf.open(io.BytesIO(resp.content))
    metadata = pdf.open_metadata()
    assert metadata.pdfa_status == "2A"
    assert pdf.pdf_version == "1.7"
    assert len(pdf.pages) == 1

def test_pdf_has_attachments():
    with open("./fixtures/attachment.pdf", "rb") as attachment:
        resp = client.post("/pdf", files=[
            ("html", ("law.html", "<h1>Hello</h1>", "text/html")),
            ("css", ("style.css", "h1 { color: red }", "text/css")),
            ("attachments", ("attachment-1.pdf", attachment, "application/pdf")),
            ("attachments", ("attachment-2.pdf", attachment, "application/pdf")),
        ])

    # Assert response basics
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.headers["content-disposition"] == "attachment; filename=\"download.pdf\""

    # check some metadata
    pdf = pikepdf.Pdf.open(io.BytesIO(resp.content))
    assert len(pdf.pages) == 21 # 1 for the generated pdf, and 10 for both of the attachments