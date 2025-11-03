.PHONY: help install dev test clean run lint format docs

# Variables
PYTHON := python3
PIP := pip3
PROJECT_NAME := project-wizard

help:  ## Show this help message
	@echo "$(PROJECT_NAME) - Makefile Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in production mode
	$(PIP) install .

dev:  ## Install package in development mode
	$(PIP) install -e .
	@echo "✓ Installed in development mode"
	@echo "Run: project-wizard init"

test:  ## Run tests
	$(PYTHON) -m pytest tests/ -v

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned build artifacts"

lint:  ## Run linting checks
	@echo "Running ruff..."
	ruff check app/ || true
	@echo "Running type checks..."
	$(PYTHON) -m mypy app/ || true

format:  ## Format code with black
	black app/ tests/
	@echo "✓ Code formatted"

init:  ## Run the project wizard
	project-wizard init

demo:  ## Run a demo project creation (non-interactive)
	@echo "Demo mode not yet implemented"
	@echo "Run: make init"

docs:  ## Generate documentation
	@echo "Documentation:"
	@cat README.md | head -50

github:  ## Create GitHub repo and push
	@echo "Creating GitHub repository..."
	gh repo create project_wizard --public --source=. --description="Interactive project management wizard with OpenProject integration"
	git remote add origin https://github.com/dollythedog/project_wizard.git
	git branch -M main
	git push -u origin main
	@echo "✓ Pushed to GitHub: https://github.com/dollythedog/project_wizard"

status:  ## Show git status
	@git status

commit:  ## Quick commit (use: make commit MSG="your message")
	@if [ -z "$(MSG)" ]; then \
		echo "Error: MSG is required. Usage: make commit MSG='your message'"; \
		exit 1; \
	fi
	git add .
	git commit -m "$(MSG)"
	@echo "✓ Committed: $(MSG)"

push:  ## Push to remote
	git push
	@echo "✓ Pushed to remote"

deps:  ## Show installed dependencies
	$(PIP) list | grep -E "(click|jinja2|pydantic|requests|rich|questionary)"

tree:  ## Show project structure
	@tree -L 3 -I '__pycache__|*.pyc' || ls -R

version:  ## Show version
	@grep "version=" setup.py | cut -d'"' -f2

update:  ## Update dependencies
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	@echo "✓ Dependencies updated"

uninstall:  ## Uninstall package
	$(PIP) uninstall -y $(PROJECT_NAME)
	@echo "✓ Uninstalled $(PROJECT_NAME)"

