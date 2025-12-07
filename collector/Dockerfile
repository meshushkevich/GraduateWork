FROM ghcr.io/astral-sh/uv:alpine3.22
RUN apk add git

ADD . /app
WORKDIR /app
RUN uv sync
EXPOSE 8001
CMD ["uv", "run", "streamlit", "run", "src/ui/main.py", "--server.port", "8001"]
