.PHONY: help install run clean test

.DEFAULT_GOAL := help

help:  ## Show this help
	@echo "\033[36mProject Wizard Commands\033[0m"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[33mmake %-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Setup
install:  ## Install the tool
	pip3 install -e .
	@echo "\n✓ Installed! Try: make run"

# Usage  
run:  ## Start the project wizard
	project-wizard init

# Development
test:  ## Run tests
	python3 -m pytest tests/ -v

clean:  ## Clean build files
	rm -rf build/ dist/ *.egg-info __pycache__
	find . -name "*.pyc" -delete
	@echo "✓ Cleaned"

# Git
status:  ## Git status
	@git status -sb

git-push:  ## Commit and push (make git-push MSG="message")
	@if [ -z "$(MSG)" ]; then echo "Error: make git-push MSG='your message'"; exit 1; fi
	git add -A
	git commit -m "$(MSG)"
	git push
	@echo "✓ Pushed"

git-pull:  ## Pull latest changes
	git pull
	@echo "✓ Pulled"

# Info
tree:  ## Show project files
	@tree -L 2 -I '__pycache__|.git' 2>/dev/null || ls -R

version:  ## Show version  
	@grep version setup.py | cut -d'"' -f2
