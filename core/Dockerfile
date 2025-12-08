FROM ghcr.io/astral-sh/uv:alpine3.22
RUN apk add git

# Copy manifest files for improving building speed
ADD pyproject.toml uv.lock /app/
WORKDIR /app
RUN uv sync

# Copy other files
COPY . /app
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--port", "8000"]
