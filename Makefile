# ============================
# Makefile Settings
# By: Abraão V. S. Santos
# ============================
COMPOSE_DIR := compose
COMPOSE_FILE := source/docker/$(COMPOSE_DIR)/docker-compose.yml
ENV_FILE := source/docker/$(COMPOSE_DIR)/.env

# Docker Compose project name (to isolate containers)
PROJECT_NAME := pizza-management-system

# ============================
# Docker Compose Commands
# ============================
up:
	@echo "Starting containers..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d

down:
	@echo "Stopping and removing containers..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down

stop:
	@echo "Stopping containers (without removing)..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop

start:
	@echo "Starting stopped containers..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) start

restart: down up

logs:
	@echo "Showing service logs..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) logs -f

ps:
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) ps

build:
	@echo "Building images..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) build

# ============================
# Cleanup
# ============================
clean:
	@echo "Cleaning containers, volumes, and orphan images..."
	docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f

# ============================
# Help
# ============================
help:
	@echo ""
	@echo "  Available commands:"
	@echo ""
	@echo "  make up        -> Start containers"
	@echo "  make down      -> Stop and remove containers"
	@echo "  make stop      -> Stop containers (keep them)"
	@echo "  make start     -> Start stopped containers"
	@echo "  make restart   -> Restart containers (down + up)"
	@echo "  make logs      -> Show real-time logs"
	@echo "  make ps        -> List active containers"
	@echo "  make build     -> Build images"
	@echo "  make clean     -> Remove containers, volumes, and orphan images"
	@echo ""

# Default target when running only `make`
.DEFAULT_GOAL := help
