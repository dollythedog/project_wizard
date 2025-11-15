.PHONY: help lint lint-fix format check install run clean

help:
	@echo "Project Wizard - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  make lint       - Run ruff linter (check only)"
	@echo "  make lint-fix   - Run ruff and auto-fix issues"
	@echo "  make format     - Format code with ruff"
	@echo "  make check      - Run all checks (lint + format check)"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the Streamlit app"
	@echo "  make clean      - Clean Python cache files"

# Install dependencies
install:
	pip install -r requirements.txt

# Run linter (check only)
lint:
	@echo "Running ruff linter..."
	ruff check app/ app.py

# Run linter and auto-fix issues
lint-fix:
	@echo "Running ruff linter with auto-fix..."
	ruff check --fix app/ app.py

# Format code
format:
	@echo "Formatting code with ruff..."
	ruff format app/ app.py

# Check formatting without making changes
format-check:
	@echo "Checking code formatting..."
	ruff format --check app/ app.py

# Run all checks
check: lint format-check
	@echo "✓ All checks passed!"

# Run the app
run:
	streamlit run app.py

# Clean Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned cache files"
