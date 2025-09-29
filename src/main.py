import os
from io import BytesIO
from typing import Annotated

from fastapi import FastAPI, UploadFile, File
from weasyprint import HTML, CSS
from styles import default_css, font_config
import logging.config
import pikepdf
import tempfile
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

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

app = FastAPI(
    title="NeuRIS PDF Service",
    description="Rest API service that converts HTML and CSS into high‑quality accessible PDFs.",
    version="1.0.0",
    license_info={
        "name": "GPL-3.0",
        "url": "https://github.com/digitalservicebund/ris-pdf-printservice/blob/main/LICENSE"
    },
)

instrumentator = Instrumentator().instrument(app)

@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)

@app.get("/health")
def health():
    logger.info("request / endpoint!")
    return {"status": True}

with open(os.path.join(os.path.dirname(__file__), "fallback.png"), "rb") as file:
    fallback_image = file.read()

@app.post("/pdf", response_class=FileResponse)
def generate_pdf(
        html: Annotated[UploadFile, File(description="The HTML that should be rendered")],
        css: Annotated[UploadFile, File(description="The CSS that should be applied to the HTML for rendering it")],
        attachments: Annotated[list[UploadFile], File(description="Additional PDF-files that should be added to the end of the created PDF-file. If these files are not PDF-A/2a compliant the created PDF-file will not be compliant either.") ] = None,
        files: Annotated[list[UploadFile], File(description="Files references in the HTML that are needed for rendering. E.g. Images that are used in an <img>-tag. The filename must be the same as in the reference, the rest of the path is ignored.") ] = None
) -> FileResponse:
    def url_fetcher(url: str) -> dict[str, str]:
        for file in files:
            if url.endswith(file.filename):
                return {'file_obj': file.file, 'mime_type': file.content_type}
        logger.info(f"File for {url} not provided, using fallback image.")
        return { 'string': fallback_image, 'mime_type': 'image/png' }

    html = HTML(
        html.file,
        url_fetcher=url_fetcher,
        # we need to define a base url so the url_fetcher even tries to load relative paths
        base_url="https://testphase.rechtsinformationen.bund.de/"
    )
    css = CSS(css.file, font_config=font_config, url_fetcher=url_fetcher)

    pdf = html.write_pdf(stylesheets=[default_css, css], font_config=font_config, pdf_variant="pdf/a-2u", pdf_version="1.7", srgb=True, pdf_tags=True)

    ppdf = pikepdf.open(BytesIO(pdf))

    with ppdf.open_metadata() as meta:
        meta['pdfaid:conformance'] = "A"
        # We would need to also embedd the definition of the pdfuaid namespace into the pdf to still be PDF/A-2a compliant, thats not that simple so we do not do that at the moment
        # meta['pdfuaid:part'] = "1"

    if attachments:
        for attachment in attachments:
            attachment_pikepdf = pikepdf.open(attachment.file)

            with attachment_pikepdf.open_metadata() as metadata:
                if "A" not in metadata.pdfa_status:
                    logger.info("Attachment is not PDF/A compliant, removing metadata from final PDF.")
                    with ppdf.open_metadata() as meta:
                        if 'pdfaid:conformance' in meta:
                            del meta['pdfaid:conformance']
                        if 'pdfaid:part' in meta:
                            del meta['pdfaid:part']

            ppdf.pages.extend(attachment_pikepdf.pages)

    _, path = tempfile.mkstemp()
    ppdf.save(path)
    return FileResponse(path, media_type="application/pdf", filename="download.pdf", content_disposition_type="attachment")
    # todo: cleanup temp file
