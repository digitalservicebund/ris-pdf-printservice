# Pdf print service

## Setup
We use uv as a dependency manager
Install by running:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Download dependencies:
```bash
uv sync
```

Start server: 
```bash
python -m fastapi run app/main.py --host 0.0.0.0 --port 8080
```

Test manually:
```bash
curl -X POST http://localhost:8080/pdf -H "Content-Type: application/json" -d '{"html":"<h1>Hello</h1>","css":"h1 { color: red }","filename":"hello.pdf"}' -o hello.pdf\n\n
```

Run tests: 
```bash
uv run pytest
```