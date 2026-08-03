FROM cgr.dev/chainguard/python:latest-dev@sha256:1937c8994699b16ee74e11cb1d88e744270b51fa4b06aa4f83dae78d15067cbe AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python@sha256:b3d3fbb8b9fe48950bab73d49bffa7496ff6f8a46ba570b302fc366f1396011a AS runtime
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
