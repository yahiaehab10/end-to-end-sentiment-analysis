.PHONY: help install dev prod build test clean deploy health logs
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := sentiment-analysis

help: ## Show this help message
	@echo "Sentiment Analysis ML Project"
	@echo "============================"
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Environment setup
install: ## Install project dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r src/api/requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -r src/api/requirements.txt
	$(PIP) install pytest flake8 black isort bandit pre-commit
	pre-commit install

# Docker commands
build: ## Build Docker images
	./scripts/docker-manage.sh build

dev: ## Start development environment
	./scripts/docker-manage.sh dev

prod: ## Start production environment
	./scripts/docker-manage.sh prod

stop: ## Stop all Docker services
	./scripts/docker-manage.sh stop

logs: ## Show logs (usage: make logs SERVICE=sentiment-api)
	./scripts/docker-manage.sh logs $(SERVICE)

health: ## Check service health
	./scripts/docker-manage.sh health

clean: ## Clean Docker resources
	./scripts/docker-manage.sh clean

# ML Pipeline commands
data-ingest: ## Run data ingestion
	$(PYTHON) src/data/data_ingestion.py

preprocess: ## Run data preprocessing
	$(PYTHON) src/data/data_preprocessing.py

train: ## Train the model
	$(PYTHON) src/model/model_building.py

evaluate: ## Evaluate the model
	$(PYTHON) src/model/model_evaluation.py

register: ## Register model to MLflow
	$(PYTHON) src/model/register_model.py

pipeline: data-ingest preprocess train evaluate register ## Run full ML pipeline

# Testing and Quality
test: ## Run tests
	pytest tests/ -v --cov=src --cov-report=html

test-api: ## Test API endpoints
	$(DOCKER_COMPOSE) exec sentiment-api pytest tests/ -v

lint: ## Run linting
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format: ## Format code
	black src/ tests/
	isort src/ tests/

security-check: ## Run security checks
	bandit -r src/ -f json -o security-report.json

quality: lint security-check ## Run all quality checks

# DVC commands
dvc-repro: ## Reproduce DVC pipeline
	dvc repro

dvc-metrics: ## Show DVC metrics
	dvc metrics show

dvc-plots: ## Show DVC plots
	dvc plots show

# API commands
serve-local: ## Serve API locally (development)
	cd src/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000

api-docs: ## Open API documentation
	@echo "API Documentation available at:"
	@echo "  - Interactive docs: http://localhost:8000/docs"
	@echo "  - ReDoc: http://localhost:8000/redoc"

# Deployment
deploy-staging: ## Deploy to staging
	@echo "Deploying to staging environment..."
	# Add your staging deployment commands here

deploy-prod: ## Deploy to production
	@echo "Deploying to production environment..."
	# Add your production deployment commands here

# Monitoring
monitor: ## Start monitoring stack
	$(DOCKER_COMPOSE) --profile monitoring up -d

monitor-stop: ## Stop monitoring stack
	$(DOCKER_COMPOSE) --profile monitoring down

# Database
db-start: ## Start database services
	$(DOCKER_COMPOSE) --profile database up -d

db-stop: ## Stop database services
	$(DOCKER_COMPOSE) --profile database down

# Utilities
jupyter: ## Start Jupyter notebook
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

mlflow-ui: ## Start MLflow UI
	mlflow ui --host 0.0.0.0 --port 5000

setup-git-hooks: ## Setup pre-commit git hooks
	pre-commit install
	pre-commit run --all-files

init-project: install-dev setup-git-hooks ## Initialize project for development
	@echo "Project initialized successfully!"
	@echo "Run 'make dev' to start development environment"