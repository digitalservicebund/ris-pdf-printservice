FROM cgr.dev/chainguard/python:latest-dev AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add --no-cache --update-cache pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python:latest AS runtime
WORKDIR /app

# Copy libraries (this way we do not need to have apk in the image). It only works because the files from pango we need
# are all in the lib folder and both images use the same underlying OS.
COPY --from=build /usr/lib /usr/lib
# Copy python dependencies
COPY --from=build --chown=nonroot /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

COPY ./src ./src
COPY ./static ./static

EXPOSE 8080

ENTRYPOINT ["python", "-m", "fastapi"]
CMD ["run", "src/main.py", "--port", "8080", "--host", "0.0.0.0"]
