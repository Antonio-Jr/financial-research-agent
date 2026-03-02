# Makefile for Financial Research Agent

.PHONY: help install run build-docker run-docker compose-up compose-down test coverage lint format clean

# --- Variables ---
PYTHON = uv run python
PYTEST = uv run pytest
RUFF = uv run ruff

# --- Help ---
help:
	@echo "📑 Financial Research Agent - Available commands:"
	@echo ""
	@echo "🚀 Local Development:"
	@echo "  make install        - Install dependencies using uv"
	@echo "  make run            - Run the Gradio UI locally"
	@echo "  make clean          - Remove temporary files and caches"
	@echo ""
	@echo "🐳 Docker & Compose:"
	@echo "  make build-docker   - Build the Docker image"
	@echo "  make run-docker     - Run the container using Docker directly"
	@echo "  make compose-up     - Build and start the service with Docker Compose"
	@echo "  make compose-down   - Stop and remove Docker Compose services"
	@echo ""
	@echo "🧪 Quality & Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make coverage       - Run tests and show coverage report (aiming for 100%)"
	@echo "  make lint           - Check code style with Ruff"
	@echo "  make format         - Format code with Ruff"

# --- Local Development ---
install:
	uv sync

run:
	$(PYTHON) main.py

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +

# --- Docker ---
build-docker:
	docker build -t financial-agent .

run-docker:
	docker run -p 7860:7860 --env-file .env financial-agent

compose-up:
	docker-compose up --build

compose-down:
	docker-compose down

# --- Quality & Testing ---
test:
	$(PYTEST)

coverage:
	$(PYTEST) --cov=. --cov-report=term-missing

lint:
	$(RUFF) check .

format:
	$(RUFF) format .
