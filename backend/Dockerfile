# FinSight Agent backend — Cloud Run image (Issue #23).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Upstream persona data: cloned at build time (not vendored in our repo),
# served in-process by the local transport (FI_MCP_MODE=local).
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && git clone --depth 1 https://github.com/epiFi/fi-mcp-dev.git /tmp/fi-mcp-dev \
    && mkdir -p /app/data && cp -r /tmp/fi-mcp-dev/test_data_dir /app/data/test_data_dir \
    && rm -rf /tmp/fi-mcp-dev \
    && apt-get purge -y git && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Install dependencies first for better layer caching.
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

# Copy application code.
COPY app ./app

# Cloud Run provides the port via $PORT (defaults to 8080).
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
