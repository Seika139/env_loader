#########################
# For Local Development #
#########################
.PHONY: check
check:
	@echo "Running checks..."
	-poetry run black --check src/ tests/
	-poetry run isort --check src/ tests/
	-poetry run flake8 src/ tests/
	-poetry run mypy src/ tests/

.PHONY: format
format:
	@echo "Running formatters..."
	poetry run isort src/ tests/
	poetry run black src/ tests/

.PHONY: test-local
test-local:
	@echo "Running tests in local..."
	poetry run pytest tests

######################
# For test in Docker #
######################
DOCKER_COMPOSE := docker compose --file Docker/compose.yml
MODULE_NAME := $(shell basename $(CURDIR))
CACHE_HOME := $(if $(XDG_CACHE_HOME), $(XDG_CACHE_HOME)/$(MODULE_NAME), $(CURDIR)/.cache)
BUILD_CACHE_FILE := $(CACHE_HOME)/build_cache
RUN_CACHE_FILE := $(CACHE_HOME)/run_cache
PYTHON_VERSIONS := 3.9 3.10 3.11 3.12 3.13
SERVICES := $(foreach ver,$(PYTHON_VERSIONS),python_$(subst .,_,$(ver)))

.PHONY: build
build: $(BUILD_CACHE_FILE)
$(BUILD_CACHE_FILE): Docker/Dockerfile Docker/compose.yml
	@mkdir -p $(CACHE_HOME)
	@$(DOCKER_COMPOSE) build
	@date >$(@)

# --volumes option deletes the volumes
# --remove-orphans option removes the containers that are not defined in the compose file
.PHONY: up
up: $(RUN_CACHE_FILE)
$(RUN_CACHE_FILE): $(BUILD_CACHE_FILE)
	@mkdir -p $(CACHE_HOME)
	-@rm -f $(RUN_CACHE_FILE)
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans
	@$(DOCKER_COMPOSE) up --detach --wait
	@date >$(@)

.PHONY: test-docker
test-docker: up
	@echo "Running tests in Docker..."
	@$(foreach service,$(SERVICES), \
		echo "--- Testing $(service) ---"; \
		$(DOCKER_COMPOSE) exec $(service) poetry run isort --check src/ tests/ || exit 1; \
		$(DOCKER_COMPOSE) exec $(service) poetry run black --check src/ tests/ || exit 1; \
		$(DOCKER_COMPOSE) exec $(service) poetry run flake8 src/ tests/ || exit 1; \
		$(DOCKER_COMPOSE) exec $(service) poetry run mypy src/ tests/ || exit 1; \
		$(DOCKER_COMPOSE) exec $(service) poetry run pytest tests || exit 1; \
	)
	@echo ""
	@echo "All tests in Docker passed!"
	@echo ""

.PHONY: down
down:
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans
	-@rm -f $(RUN_CACHE_FILE)

.PHONY: clean
clean:
	@$(MAKE) down
	@$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	-@rm -r $(CACHE_HOME)

#########################
# Test Local And Docker #
#########################
.PHONY: test
test: test-local test-docker
