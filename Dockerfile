FROM cgr.dev/chainguard/wolfi-base AS build

WORKDIR /app

# Install system libs needed at runtime (Pango stack). Do this in both build and final.
RUN apk update && apk add --no-cache --update-cache \
    python-3.12 \
    py3.12-pip \
    pango \
    fontconfig \
    freetype \
    cairo \
    cairo-gobject \
    harfbuzz \
    curl \
    ca-certificates

# Set up a venv to isolate installed dependencies
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

COPY pyproject.toml ./
COPY uv.lock ./

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

RUN uv pip install --no-cache -r <(uv pip compile pyproject.toml)

FROM cgr.dev/chainguard/wolfi-base AS runtime
WORKDIR /app

# Install the same system libs required at runtime
RUN apk update && apk add --no-cache --update-cache \
    python-3.12 \
    py3.12-pip \
    pango \
    fontconfig \
    freetype \
    cairo \
    cairo-gobject \
    harfbuzz

USER nonroot

COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

COPY ./src ./app

EXPOSE 8080

CMD ["python", "-m", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]