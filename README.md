# Pdf print service
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


If you use [Homebrew](https://brew.sh/), you can install all of them like this:

```sh
brew install talisman lefthook gh
brew install python
brew install pango cairo harfbuzz fontconfig freetype pkg-config
brew install --cask docker # or `brew install docker` if you don't want the desktop app
```

Once you installed the prerequisites, make sure to initialize Git hooks. This will ensure any code you commit follows our coding standards, is properly formatted, and has a commit message adhering to our conventions:

```sh
lefthook install
```

## Setup
We use uv as a dependency manager
Install by running:
```bash
brew install uv
```
or
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

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
curl -X POST http://localhost:8080/pdf -H "Content-Type: application/json" -d '{"html":"<h1>Hello</h1>","css":"h1 { color: red }","filename":"hello.pdf"}' -o hello.pdf
```

Run tests: 
```bash
uv run pytest
```

Run linter
```bash
uv run flake8 ./src
```

Fix linting errors
```bash
uv run black ./src
```