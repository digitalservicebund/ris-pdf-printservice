FROM python:3.13-slim AS build

USER root
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system libs needed at runtime
RUN apt-get update -y && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM registry.opencode.de/open-code/oci/python3:3.13-oc.6-minimal AS runtime
WORKDIR /app

ARG TARGETPLATFORM
ENV LIB_FOLDER=${TARGETPLATFORM/linux\/amd64/x86_64-linux-gnu}
ENV LIB_FOLDER=${LIB_FOLDER/linux\/arm64/aarch64-linux-gnu}

# Copy libraries (this way we do not need to have apt-get in the image). It only works because the files from pango we
# need are all in the lib folder and both images use the same underlying OS.
COPY --from=build /usr/lib/${LIB_FOLDER} /usr/lib/${LIB_FOLDER}
# Copy python dependencies
COPY --from=build --chown=nonroot /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

COPY ./src ./src
COPY ./static ./static

EXPOSE 8080

ENTRYPOINT ["python", "-m", "fastapi"]
CMD ["run", "src/main.py", "--port", "8080", "--host", "0.0.0.0"]
