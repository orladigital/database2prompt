FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv pip install -r requirements.txt

# Expose the MCP server port
EXPOSE 8080

# Run the MCP server
CMD ["uv", "run", "python", "server.py"]
