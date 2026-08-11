FROM cgr.dev/chainguard/python:latest-dev@sha256:062a24c85a047e797f25580694c17e1afc97ea46e305be8026b0d876f0c2f832 AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python@sha256:69437de912cc3b5d36a2480b8fb0c3f658f151d8bc1978d19a6412be3a4983d5 AS runtime
WORKDIR /app

# Copy libraries from build stage.
COPY --from=build /usr/lib/lib* /usr/lib/
COPY --from=build /lib/lib* /lib/
COPY --from=build /etc/fonts /etc/fonts

# Copy python dependencies
COPY --from=build --chown=nonroot /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

COPY ./src ./src
COPY ./static ./static

EXPOSE 8080

ENTRYPOINT ["python", "-m", "fastapi"]
CMD ["run", "src/main.py", "--port", "8080", "--host", "0.0.0.0"]
