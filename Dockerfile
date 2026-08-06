FROM cgr.dev/chainguard/python:latest-dev@sha256:062a24c85a047e797f25580694c17e1afc97ea46e305be8026b0d876f0c2f832 AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python@sha256:5128c3823542cfb27fd83c42ef9ee3bbbf3fdd0eb9190802e5fc119974c5f776 AS runtime
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
