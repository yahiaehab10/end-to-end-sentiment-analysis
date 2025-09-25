#!/bin/bash

# Docker management script for sentiment analysis project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the application
build() {
    print_status "Building Docker images..."
    docker-compose build --no-cache
    print_status "Build completed successfully!"
}

# Function to start development environment
dev() {
    print_status "Starting development environment..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    
    print_status "Development environment started!"
    echo "Services available at:"
    echo "  - API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - MLflow: http://localhost:5000"
    echo "  - Jupyter: http://localhost:8888"
}

# Function to start production environment
prod() {
    print_status "Starting production environment..."
    docker-compose up -d
    
    print_status "Production environment started!"
    echo "Services available at:"
    echo "  - API (via Nginx): http://localhost"
    echo "  - Direct API: http://localhost:8000"
    echo "  - MLflow: http://localhost/mlflow"
}

# Function to stop all services
stop() {
    print_status "Stopping all services..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
    print_status "All services stopped!"
}

# Function to view logs
logs() {
    service=${1:-sentiment-api}
    print_status "Showing logs for $service..."
    docker-compose logs -f $service
}

# Function to run tests
test() {
    print_status "Running tests..."
    docker-compose exec sentiment-api python -m pytest tests/ -v
}

# Function to check service health
health() {
    print_status "Checking service health..."
    
    # Check API health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✓ API service is healthy"
    else
        print_warning "✗ API service is not responding"
    fi
    
    # Check MLflow
    if curl -f http://localhost:5000 > /dev/null 2>&1; then
        print_status "✓ MLflow service is healthy"
    else
        print_warning "✗ MLflow service is not responding"
    fi
}

# Function to clean up
clean() {
    print_warning "This will remove all containers, networks, and volumes. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v
        docker system prune -f
        print_status "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show usage
usage() {
    echo "Usage: $0 {build|dev|prod|stop|logs|test|health|clean}"
    echo ""
    echo "Commands:"
    echo "  build    Build Docker images"
    echo "  dev      Start development environment"
    echo "  prod     Start production environment"
    echo "  stop     Stop all services"
    echo "  logs     Show logs (optional: specify service name)"
    echo "  test     Run tests"
    echo "  health   Check service health"
    echo "  clean    Remove all containers and volumes"
    echo ""
    echo "Examples:"
    echo "  $0 dev                    # Start development environment"
    echo "  $0 logs sentiment-api     # Show API logs"
    echo "  $0 health                 # Check all services"
}

# Main script logic
main() {
    check_docker
    
    case "${1:-}" in
        build)
            build
            ;;
        dev)
            dev
            ;;
        prod)
            prod
            ;;
        stop)
            stop
            ;;
        logs)
            logs $2
            ;;
        test)
            test
            ;;
        health)
            health
            ;;
        clean)
            clean
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"