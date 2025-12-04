# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install pip if not present (for slim images)
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -e ./predictor

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Run the predictor
CMD ["python", "predictor/main.py"]
