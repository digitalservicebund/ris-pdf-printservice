FROM cgr.dev/chainguard/python:latest-dev@sha256:78b681a40e3ebb5049773123e7e7d277b2578712e23b32df5cb5213b4123509d AS build

USER root
WORKDIR /app

# Install system libs needed at runtime
RUN apk update && apk add pango

COPY pyproject.toml ./
COPY uv.lock ./

# Install python dependencies to .venv
RUN uv sync --locked --compile-bytecode --no-editable

FROM cgr.dev/chainguard/python@sha256:8fab86fb761aeb18723f4f1b1baa330bd59d64e92abdc5b980d1bbd9399c297d AS runtime
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
