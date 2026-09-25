# Stage 1: Build stage
FROM python:3.14-alpine AS build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1

WORKDIR /code

# Install dependencies first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Install the project itself
COPY . .
RUN uv sync --frozen --no-dev

# Stage 2: Runtime stage
FROM python:3.14-alpine AS runtime

RUN adduser -D appuser
WORKDIR /code

COPY --from=build --chown=appuser:appuser /code /code

ENV PATH="/code/.venv/bin:$PATH"
USER appuser
ENTRYPOINT ["app"]
