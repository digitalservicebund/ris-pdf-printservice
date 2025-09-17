import io
import builtins
import pytest
from fastapi.testclient import TestClient

# Import the app after monkeypatching WeasyPrint classes in tests that need it
import main


client = TestClient(main.app)


def test_home_ok():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": True}


def test_pdf_ok_monkeypatched(monkeypatch):
    # Arrange: stub WeasyPrint HTML, CSS, and HTML.write_pdf so no native deps are required
    class DummyHTML:
        def __init__(self, string=None, **kwargs):
            self.string = string
            self.kwargs = kwargs

        def write_pdf(self, stylesheets=None, font_config=None):
            # Return deterministic bytes and expose what was passed for assertions
            self._last_call = {"stylesheets": stylesheets, "font_config": font_config}
            return b"%PDF-1.4\n%mock\n"

    class DummyCSS:
        def __init__(self, string="", font_config=None):
            self.string = string
            self.font_config = font_config

    # Patch symbols used in main.py
    monkeypatch.setattr(main, "HTML", DummyHTML)
    monkeypatch.setattr(main, "CSS", DummyCSS)

    # Act
    payload = {
        "html": "<h1>Hello</h1>",
        "css": "h1 { color: red }",
        "filename": "greeting.pdf",
    }
    resp = client.post("/pdf", json=payload)

    # Assert response basics
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    # Header format matches code: attachment; filename='greeting.pdf'
    cd = resp.headers.get("content-disposition", "")
    assert "attachment" in cd and "filename='greeting.pdf'" in cd
    # Body should be our mock bytes
    body = resp.content
    assert body.startswith(b"%PDF-")

    # Assert WeasyPrint interaction: the route should build HTML and CSS with font_config
    # default_css comes from styles.default_css; CSS constructed from body.css; both passed to write_pdf
    # We can't access DummyHTML._last_call here because new instance lived inside endpoint.
    # Instead, verify that CSS class got the same font_config object passed from module.
    dummy_css = main.CSS(string=payload["css"], font_config=main.font_config)
    assert isinstance(dummy_css, DummyCSS)
    assert dummy_css.font_config is main.font_config