# Makefile for Kamugram (@kamugrambot)

.PHONY: help install run seed clean lint test docker-build docker-up docker-down

# Variables
PYTHONPATH := .
PYTHON := uv run
SRC_DIR := src
DB_SEED_SCRIPT := $(SRC_DIR)/database/seed.py
BOT_MAIN := $(SRC_DIR)/main.py

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## $$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

run: ## Run the Telegram bot
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(BOT_MAIN)

seed: ## Seed the database with the Kalebu dataset
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(DB_SEED_SCRIPT)

clean: ## Clean up temporary files, pycache, and logs
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .uv
	rm -rf .pytest_cache

lint: ## Run linting (requires ruff)
	uv run ruff check $(SRC_DIR)

format: ## Format code (requires ruff)
	uv run ruff format $(SRC_DIR)

test: ## Run tests
	PYTHONPATH=$(PYTHONPATH) uv run pytest

docker-build: ## Build the Docker image
	docker build -t kamugram .

docker-up: ## Start the services using Docker Compose
	docker-compose up -d

docker-down: ## Stop the services
	docker-compose down
