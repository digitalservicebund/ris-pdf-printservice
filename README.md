# Pdf print service
Rest API service that converts HTML and CSS into high‑quality PDFs.

## Prerequisites
To build and run the application, you'll need:

- Docker, for infrastructure or running a containerized version of the entire application locally
- A Python3 Installation

If you would like to make changes to the application, you'll also need:

- [`talisman`](https://thoughtworks.github.io/talisman/), for preventing accidentially committing sensitive data
- [`lefthook`](https://lefthook.dev/), for running Git hooks
- [`gh`](https://cli.github.com/), for checking the pipeline status before pushing
- [`docker`](https://www.docker.com/), for running containers- 
- [`python`](https://www.python.org/) as runtime
- [`pango stack`](https://www.gtk.org/docs/architecture/pango) for pdf printing
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

Start server: 
```bash
uv run python -m fastapi run src/main.py --host 0.0.0.0 --port 8080
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