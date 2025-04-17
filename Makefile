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

.PHONY: test
test:
	@echo "Running tests..."
	poetry run pytest tests
