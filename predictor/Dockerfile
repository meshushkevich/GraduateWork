FROM ghcr.io/astral-sh/uv:debian-slim
RUN apt-get update && apt-get install -y git

ADD . /app
WORKDIR /app
RUN uv sync
EXPOSE 8002
CMD ["uv", "run", "python", "core/run.py"]
