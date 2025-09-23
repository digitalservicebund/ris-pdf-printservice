from io import BytesIO

from fastapi import FastAPI, UploadFile
from weasyprint import HTML, CSS
from styles import default_css, font_config
import logging.config
import pikepdf
import tempfile
from fastapi.responses import FileResponse

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def home():
    logger.info("request / endpoint!")
    return {"status": True}

@app.post("/pdf")
def generate_pdf(html: UploadFile, css: UploadFile, attachments: list[UploadFile] | None = None):
    html = HTML(html.file)
    css = CSS(css.file, font_config=font_config)

    # See https://doc.courtbouillon.org/weasyprint/stable/api_reference.html#weasyprint.HTML.write_pdf
    pdf = html.write_pdf(stylesheets=[default_css, css], font_config=font_config, pdf_variant="pdf/a-2u", pdf_version="1.7", srgb=True, pdf_tags=True)

    ppdf = pikepdf.open(BytesIO(pdf))

    with ppdf.open_metadata() as meta:
        meta['pdfaid:conformance'] = "A"

    if attachments:
        for attachment in attachments:
            attachment_pikepdf = pikepdf.open(attachment.file)
            ppdf.pages.extend(attachment_pikepdf.pages)

    _, path = tempfile.mkstemp()
    ppdf.save(path)
    return FileResponse(path, media_type="application/pdf", filename="download.pdf", content_disposition_type="attachment")
    # todo: cleanup temp file
