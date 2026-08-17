FROM cgr.dev/chainguard/python:latest-dev@sha256:5ae128eb5c1bec2d1dbad41edf009b8cf7475e473cbf5f2bb87c4baa2ded8e7c AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python@sha256:9c99be8c767aa0fd4bffbd92d32a192e43b4d3bed31f1a5dd33e836f921cd599 AS runtime
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
