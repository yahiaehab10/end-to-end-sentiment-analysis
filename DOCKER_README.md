# Docker and CI/CD Setup

## GitHub Actions Workflows

### ML Pipeline (`ml-pipeline.yml`)

- **Triggers**: Push to main/develop, PRs to main, manual dispatch
- **Jobs**:
  - Linting and testing with flake8, black, isort
  - Data validation
  - Model training and registration
  - Security scanning with Bandit

### Docker Build (`docker-build.yml`)

- **Triggers**: Push to main, tags, PRs
- **Features**:
  - Multi-platform builds (AMD64, ARM64)
  - GitHub Container Registry integration
  - Automated deployment to staging

## Docker Setup

### Production Deployment

```bash
# Build and start production environment
make build
make prod

# Services will be available at:
# - API: http://localhost (via Nginx)
# - MLflow: http://localhost/mlflow
```

### Development Environment

```bash
# Start development with hot reload
make dev

# Services available at:
# - API: http://localhost:8000
# - MLflow: http://localhost:5000
# - Jupyter: http://localhost:8888
```

### Docker Services

#### Core Services

- **sentiment-api**: FastAPI application for model serving
- **mlflow**: MLflow tracking server for experiment management
- **redis**: Caching layer for predictions
- **nginx**: Reverse proxy with rate limiting

#### Optional Services (Profiles)

- **monitoring**: Prometheus + Grafana for metrics
- **database**: PostgreSQL for storing predictions

### Management Commands

Use the provided scripts for easy management:

```bash
# Using the management script
./scripts/docker-manage.sh dev    # Start development
./scripts/docker-manage.sh health # Check service health
./scripts/docker-manage.sh logs   # View logs

# Using Makefile
make help          # Show all available commands
make dev           # Start development environment
make test-api      # Run API tests
make health        # Check service health
```

### Environment Variables

Set these in your GitHub repository secrets:

- `DAGSHUB_USERNAME`: Your DagsHub username
- `DAGSHUB_TOKEN`: Your DagsHub token
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Local Development Setup

1. **Prerequisites**:

   ```bash
   # Install Docker and Docker Compose
   # macOS: brew install docker docker-compose
   ```

2. **Initialize project**:

   ```bash
   make init-project  # Install dependencies and setup hooks
   ```

3. **Start development**:
   ```bash
   make dev          # Start all services
   make api-docs     # View API documentation
   ```

### API Endpoints

Once running, access the API:

- **Health Check**: `GET /health`
- **Single Prediction**: `POST /predict`
- **Batch Prediction**: `POST /predict/batch`
- **Model Info**: `GET /model/info`
- **Documentation**: `GET /docs`

### Monitoring and Observability

Enable monitoring services:

```bash
make monitor       # Start Prometheus + Grafana
# Access Grafana at http://localhost:3000 (admin/admin)
```

### Deployment

The Docker workflow automatically:

1. Builds multi-platform images on push to main
2. Pushes to GitHub Container Registry
3. Deploys to staging environment
4. Runs health checks

For production deployment, update the workflow with your specific deployment commands.
