.PHONY: install test run lint format clean help

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies from requirements.txt"
	@echo "  make test     - Run pytest suite with coverage"
	@echo "  make run      - Start the development server with auto-reload"
	@echo "  make lint     - Check code with flake8"
	@echo "  make format   - Format code with black and sort imports with isort"
	@echo "  make clean    - Remove cache files and build artifacts"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=app --cov-report=html

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	flake8 app tests

format:
	black app tests
	isort app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
