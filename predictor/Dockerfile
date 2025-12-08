FROM ghcr.io/astral-sh/uv:debian-slim
RUN apt-get update && apt-get install -y git

# Copy manifest files for improving building speed
ADD pyproject.toml uv.lock /app/
WORKDIR /app
RUN uv sync

# Copy other files
COPY . /app
EXPOSE 8001
CMD ["uv", "run", "python", "main.py"]
