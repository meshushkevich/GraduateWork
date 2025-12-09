FROM ghcr.io/astral-sh/uv:alpine3.22
RUN apk add git

ADD . /app
WORKDIR /app
RUN uv sync
EXPOSE 8002
CMD ["uv", "run", "uvicorn", "main:app", "--port", "8002"]
