# Pdf print service
Rest API service that converts HTML and CSS into high‑quality PDFs.

## Usage

The service can create PDF files by rendering an HTML-file using CSS.
Additionally, attachments can be supplied that will be rendered to the end of the created PDF-file.
Files reverenced in the HTML (like images) also need to be sent to the service so they can be used during the rendering.

The request is sent to the `/pdf` endpoint and returns the created PDF-file. The rendering might take a while (especially for PDF files with many pages).

Example:
```bash
curl -X POST "$HOST/pdf" -F "html=@./sbgg.html" -F "css=@./norm.css" -F "attachments=@./sbgg-attachment-1.pdf" -F "attachments=@./sbgg-attachment-2.pdf" -F "files=@./sbgg-image-1.png" -F "files=@./sbgg-image-2.png" -o sbgg.pdf
```

## Prerequisites
To build and run the application, you'll need:

- Docker, for infrastructure or running a containerized version of the entire application locally
- A Python 3 Installation

If you would like to make changes to the application, you'll also need:

- [`talisman`](https://thoughtworks.github.io/talisman/), for preventing accidentially committing sensitive data
- [`lefthook`](https://lefthook.dev/), for running Git hooks
- [`gh`](https://cli.github.com/), for checking the pipeline status before pushing
- [`docker`](https://www.docker.com/), for running containers- 
- [`python`](https://www.python.org/) as runtime
- [`pango stack`](https://www.gtk.org/docs/architecture/pango) dependency of weasyprint
- [`uv`](https://github.com/astral-sh/uv) Python package and project manager


If you use [Homebrew](https://brew.sh/), you can install all of them like this:

```sh
brew install talisman lefthook gh
brew install python
brew install pango cairo harfbuzz fontconfig freetype pkg-config
brew install --cask docker # or `brew install docker` if you don't want the desktop app
```
Install uv by running:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or
```bash
brew install uv
```

Once you installed the prerequisites, make sure to initialize Git hooks. This will ensure any code you commit follows our coding standards, is properly formatted, and has a commit message adhering to our conventions:

```sh
lefthook install
```

## Developing

Download dependencies:
```bash
uv sync
```

Start dev server: 
```bash
uv run python -m fastapi dev src/main.py --host 0.0.0.0 --port 8080
```

Test manually:
```bash
curl -X POST http://localhost:8080/pdf  -F "html=@./sbgg.html" -F "css=@./style.css" -o sbgg.pdf
```

Run tests: 
```bash
uv run pytest
```

Run linter
```bash
uv run flake8 ./src
```

Run formatter
```bash
uv run black ./src
```

## Contributing

If you would like to contribute, check out [`CONTRIBUTING.md`](./CONTRIBUTING.md). Please also consider our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Documentation

- 🔒 [OpenAPI docs](https://pdf-service.ris.dev.ds4g.net/docs) or while the application is running locally under  http://localhost:8080/docs
- [How to use weasyprint with tailwind](./doc/how-to-use-weasyprint-with-tailwind.md)
- [Accessibility](./doc/accessibility.md)
- [PDF/A Conformance](./doc/adr/0002-pdf-variant.md)
