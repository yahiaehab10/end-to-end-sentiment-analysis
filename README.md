# End-to-End Sentiment Analysis

A production-ready machine learning pipeline for sentiment analysis featuring automated training, evaluation, model registry, and REST API deployment with CI/CD integration.

## Overview

This project implements a complete MLOps workflow for sentiment classification, including data preprocessing, model training with LightGBM, experiment tracking with MLflow, and a FastAPI service for real-time predictions. The system is fully containerized and includes automated testing and deployment pipelines.

## Quick Start

### Docker Deployment (Recommended)

```bash
# Start the development environment
make dev

# Test the API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this product!"}'
```

### Local Development

```bash
# Install dependencies
make install

# Run the complete ML pipeline
make pipeline

# Start the API server locally
make serve-local
```

## Project Structure

```
.
├── src/
│   ├── data/               # Data ingestion and preprocessing modules
│   ├── model/              # Model training, evaluation, and registration
│   └── api/                # FastAPI application for model serving
├── notebooks/              # Jupyter notebooks for experimentation
├── data/
│   ├── raw/                # Raw input data
│   └── interim/            # Processed data
├── .github/workflows/      # CI/CD pipeline definitions
├── scripts/                # Utility scripts
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Production container definition
├── requirements.txt        # Python dependencies
└── Makefile               # Project automation commands
```

## Key Features

### Machine Learning Pipeline

- Automated data preprocessing and feature extraction
- Model training with hyperparameter optimization
- Comprehensive model evaluation and metrics tracking
- Experiment tracking and versioning with MLflow

### REST API

- FastAPI-based service for real-time predictions
- Single and batch prediction endpoints
- Health monitoring and status checks
- Interactive API documentation (Swagger UI)

### Infrastructure

- Docker containerization for consistent deployments
- Docker Compose for multi-service orchestration
- Nginx reverse proxy with rate limiting
- Redis caching layer for improved performance

### CI/CD

- Automated testing and linting on pull requests
- Model training and registration pipeline
- Docker image building and publishing
- Security vulnerability scanning

## API Endpoints

| Endpoint         | Method | Description                      |
| ---------------- | ------ | -------------------------------- |
| `/`              | GET    | API information and version      |
| `/health`        | GET    | Service health status            |
| `/predict`       | POST   | Single text sentiment prediction |
| `/predict/batch` | POST   | Batch sentiment predictions      |
| `/model/info`    | GET    | Current model information        |
| `/docs`          | GET    | Interactive API documentation    |

### Request Examples

**Single Prediction:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "This product exceeded my expectations!"}'
```

**Batch Prediction:**

```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Great product!", "Terrible experience", "Average quality"]}'
```

## Available Commands

```bash
make help          # Display all available commands
make install       # Install Python dependencies
make dev           # Start development environment
make prod          # Start production environment
make build         # Build Docker images
make stop          # Stop all services
make test          # Run test suite
make lint          # Run code linting
make format        # Format code with black and isort
make pipeline      # Execute full ML pipeline
make health        # Check service health status
make logs          # View service logs
```

## Services and Ports

When running the full stack with `make dev`:

| Service     | Port | Description                     |
| ----------- | ---- | ------------------------------- |
| API Server  | 8000 | FastAPI application             |
| MLflow UI   | 5000 | Experiment tracking dashboard   |
| Jupyter Lab | 8888 | Interactive notebooks           |
| Nginx       | 80   | Reverse proxy and load balancer |
| Redis       | 6379 | Caching layer                   |

## Model Architecture

- **Task**: Multi-class sentiment classification
- **Classes**: Negative (-1), Neutral (0), Positive (1)
- **Algorithm**: LightGBM (Gradient Boosting)
- **Features**: TF-IDF vectorization with n-gram ranges
- **Tracking**: MLflow for experiment management and model versioning

## CI/CD Pipeline

The project includes automated GitHub Actions workflows:

### ML Pipeline Workflow

- Triggered on: Push to main/develop, Pull requests
- Code linting and formatting checks
- Unit and integration tests
- Data validation
- Model training and evaluation
- Model registration to MLflow
- Artifact preservation

### Docker Build Workflow

- Triggered on: Push to main, Version tags
- Multi-stage Docker image building
- Image publishing to GitHub Container Registry
- Automated deployment to staging environment

## Configuration

### Environment Variables

```bash
PYTHON_VERSION=3.10
MLFLOW_TRACKING_URI=http://localhost:5000
PORT=8000
HOST=0.0.0.0
```

### GitHub Secrets

Required repository secrets for CI/CD:

- `DAGSHUB_USERNAME`: DagsHub username for MLflow tracking
- `DAGSHUB_TOKEN`: DagsHub access token

## Dependencies

- Python 3.10+
- FastAPI 3.0+
- LightGBM 4.5+
- MLflow 2.17+
- scikit-learn 1.5+
- pandas 2.2+
- numpy 1.26+

See `requirements.txt` for complete dependency list.

## Documentation

For detailed guides, see:

- `.github/SETUP_GUIDE.md` - Step-by-step configuration
- `.github/WORKFLOW_FIXES.md` - CI/CD pipeline details

## License

This project is licensed under the MIT License.
