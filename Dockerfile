FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY . .
FROM python:3.13-slim AS release

COPY --from=builder /app /app

RUN pip install --no-cache-dir uv

WORKDIR /app

RUN uv sync --no-dev

ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"

EXPOSE 7860

CMD ["uv", "run", "--", "python", "main.py"]