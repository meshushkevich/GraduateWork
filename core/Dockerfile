# Use Python base image
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml file
COPY pyproject.toml ./

# Install dependencies with uv
RUN uv pip install --system -e .

# Copy the rest of the application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
