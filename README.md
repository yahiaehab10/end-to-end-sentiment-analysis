# End-to-End Sentiment Analysis

A complete machine learning pipeline for sentiment analysis with automated training, evaluation, and deployment.

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Start development environment
make dev

# Access the API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this product!"}'
```

### Local Development
```bash
# Install dependencies
make install

# Run the ML pipeline
make pipeline

# Serve the API locally
make serve-local
```

## 📊 Project Structure

```
├── src/
│   ├── data/           # Data ingestion and preprocessing
│   ├── model/          # Model training, evaluation, and registration
│   └── api/            # FastAPI service for model serving
├── notebooks/          # Jupyter notebooks for experiments
├── .github/workflows/  # CI/CD pipelines
└── docker-compose.yml  # Container orchestration
```

## 🛠️ Features

- **ML Pipeline**: Automated data processing, training, and evaluation
- **Model Registry**: MLflow integration for experiment tracking
- **REST API**: FastAPI service for real-time predictions
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Containerization**: Docker setup for consistent environments
- **Monitoring**: Health checks and logging

## 📈 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Single text prediction |
| `/predict/batch` | POST | Batch predictions |
| `/health` | GET | Service health check |
| `/docs` | GET | Interactive API documentation |

## 🔧 Available Commands

```bash
make help          # Show all available commands
make dev           # Start development environment
make build         # Build Docker images
make test          # Run tests
make pipeline      # Run full ML pipeline
make health        # Check service health
```

## 🌐 Services

When running with `make dev`:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Jupyter**: http://localhost:8888

## 📝 Model Details

- **Task**: Sentiment classification (-1: negative, 0: neutral, 1: positive)
- **Model**: LightGBM with TF-IDF features
- **Tracking**: MLflow for experiment management
- **Registry**: Automated model registration and versioning

## 🚀 Deployment

The project includes automated CI/CD pipelines that:
- Run tests and quality checks on every PR
- Train and register models on main branch updates
- Build and deploy Docker containers automatically

For detailed setup instructions, see [DOCKER_README.md](DOCKER_README.md).
