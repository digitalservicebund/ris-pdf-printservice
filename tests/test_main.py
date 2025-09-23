import io
import builtins
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
