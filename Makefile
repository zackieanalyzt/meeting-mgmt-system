# Meeting Management System - Development Commands

.PHONY: help build up down logs clean dev prod test

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev     - Start development environment"
	@echo "  make prod    - Start production environment"
	@echo "  make build   - Build all containers"
	@echo "  make up      - Start containers"
	@echo "  make down    - Stop containers"
	@echo "  make logs    - Show logs"
	@echo "  make clean   - Clean up containers and volumes"
	@echo "  make test    - Run tests"

# Development environment
dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Production environment
prod:
	docker-compose up --build -d

# Build containers
build:
	docker-compose build

# Start containers
up:
	docker-compose up -d

# Stop containers
down:
	docker-compose down

# Show logs
logs:
	docker-compose logs -f

# Clean up
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	docker-compose exec backend pytest
	docker-compose exec frontend npm test

# Database migration
migrate:
	docker-compose exec backend alembic upgrade head

# Create migration
migration:
	docker-compose exec backend alembic revision --autogenerate -m "$(name)"

# Reset database
reset-db:
	docker-compose down -v
	docker-compose up db mariadb -d
	sleep 10
	docker-compose up backend -d