# Professional FastAPI Monitoring Stack - Makefile

.PHONY: help build up down logs clean test lint format install-dev

# Default target
help: ## Show this help message
	@echo "FastAPI Monitoring Stack - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development Commands
install-dev: ## Install development dependencies
	cd app && pip install -r requirements.txt
	pip install black flake8 pytest pytest-asyncio

format: ## Format code with black
	cd app && black . --line-length 88

lint: ## Lint code with flake8
	cd app && flake8 . --max-line-length=88 --ignore=E203,W503

test: ## Run tests
	cd app && pytest -v

# Docker Commands
build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-app: ## Show FastAPI application logs
	docker-compose logs -f fastapi-app

logs-prometheus: ## Show Prometheus logs
	docker-compose logs -f prometheus

logs-grafana: ## Show Grafana logs
	docker-compose logs -f grafana

# Monitoring Commands
status: ## Check service status
	docker-compose ps

restart: ## Restart all services
	docker-compose restart

restart-app: ## Restart FastAPI application
	docker-compose restart fastapi-app

# Data Management
clean: ## Remove all containers and volumes
	docker-compose down -v
	docker system prune -f

backup-grafana: ## Backup Grafana data
	docker run --rm -v grafana_grafana_data:/data -v $(PWD):/backup alpine tar czf /backup/grafana-backup.tar.gz -C /data .

restore-grafana: ## Restore Grafana data
	docker run --rm -v grafana_grafana_data:/data -v $(PWD):/backup alpine tar xzf /backup/grafana-backup.tar.gz -C /data

# Testing Commands
load-test: ## Generate load for testing metrics
	@echo "Generating load test data..."
	@for i in {1..50}; do \
		curl -s http://localhost:8000/simulate/load > /dev/null; \
		curl -s -X POST http://localhost:8000/users/register \
			-H "Content-Type: application/json" \
			-d "{\"username\":\"user$$i\",\"email\":\"user$$i@test.com\"}" > /dev/null; \
		sleep 1; \
	done
	@echo "Load test completed!"

health-check: ## Check health of all services
	@echo "Checking service health..."
	@curl -s http://localhost:8000/health | jq .
	@curl -s http://localhost:9090/-/healthy && echo "Prometheus: Healthy"
	@curl -s http://localhost:3000/api/health | jq .

# Utility Commands
open-grafana: ## Open Grafana in browser
	open http://localhost:3000

open-prometheus: ## Open Prometheus in browser
	open http://localhost:9090

open-api-docs: ## Open FastAPI docs in browser
	open http://localhost:8000/docs

# Production Commands
prod-up: ## Start services in production mode
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
