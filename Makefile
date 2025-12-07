# ---------------------------------------------------------------------
# 🧙 Makefile — project_wizard
# ---------------------------------------------------------------------
# Usage: run `make help` to list available commands.
# ---------------------------------------------------------------------
MAKEFLAGS += --no-print-directory
.SILENT:
SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

# ---------------------------------------------------------------------
# Paths and Environment
# ---------------------------------------------------------------------

PROJECT_DIR := $(shell pwd)
VENV ?= venv
PYTHON := $(VENV)/Scripts/python.exe
PIP := $(VENV)/Scripts/pip.exe

# Variables for commit message
MSG ?=

# ---------------------------------------------------------------------
# PHONY targets
# ---------------------------------------------------------------------
.PHONY: help venv install \
        run restart-web test lint lint-fix \
        git-pull git-push git-status \
        clean clean-all \
        tree version

# ---------------------------------------------------------------------
# 🧭 HELP
# ---------------------------------------------------------------------

help:
	@echo "==================== Project Wizard ===================="
	@echo ""
	@echo "Setup:"
	@echo "  make venv                  Create local Python virtual environment"
	@echo "  make install               Install project in editable mode"
	@echo ""
	@echo "Usage:"
	@echo "  make run                   Start project wizard (init command)"
	@echo "  make restart-web           Kill all Python & restart web server (background)"
	@echo ""
	@echo "Development:"
	@echo "  make test                  Run tests"
	@echo "  make lint                  Run ruff linter"
	@echo "  make lint-fix              Run ruff linter and auto-fix issues"
	@echo ""
	@echo "Git / Maintenance:"
	@echo "  make git-pull              Pull latest changes from GitHub"
	@echo "  make git-push MSG='msg'    Add, commit, and push changes"
	@echo "  make git-status            Show git status"
	@echo "  make clean                 Remove Python caches"
	@echo "  make clean-all             Deep clean (caches + venv)"
	@echo ""
	@echo "Info:"
	@echo "  make tree                  Show project file structure"
	@echo "  make version               Show current version"
	@echo "========================================================"

# ---------------------------------------------------------------------
# 🐍 Python environment
# ---------------------------------------------------------------------

venv:
	@echo "[INFO] Creating virtual environment..."
	python -m venv $(VENV)
	@echo "[INFO] Virtual environment created at $(VENV)"
	@echo "[INFO] Activate with: .\venv\Scripts\Activate.ps1"


install: venv
	@echo "[INFO] Upgrading pip..."
	$(PIP) install --upgrade pip
	@echo "[INFO] Installing project in editable mode..."
	$(PIP) install -e .
	@echo "[INFO] Installation complete. Try: make run"

# ---------------------------------------------------------------------
# 🚀 Usage
# ---------------------------------------------------------------------

run:
	@echo "[INFO] Starting project wizard..."
	$(PYTHON) -m app.main init

restart-web:
	@echo "[INFO] Killing all Python processes..."
	-taskkill /F /IM python.exe 2>$$null
	@echo "[INFO] Starting web server in background (http://localhost:8000)..."
	start python run_web.py
	@echo "[INFO] Server started in background"
	@echo "[INFO] Wait ~3-5 seconds for server to be ready, then refresh browser"
	@echo "[INFO] If needed, check console for any errors"

# ---------------------------------------------------------------------
# 🧪 Testing & Quality
# ---------------------------------------------------------------------

test:
	@echo "[INFO] Running tests..."
	$(PYTHON) -m pytest tests/ -v

lint:
	@echo "[INFO] Running ruff linter..."
	$(PYTHON) -m ruff check app/

lint-fix:
	@echo "[INFO] Running ruff linter with auto-fix..."
	$(PYTHON) -m ruff check app/ --fix
	@echo "[INFO] Lint fixes applied"

# ---------------------------------------------------------------------
# 🔧 Git & Cleanup
# ---------------------------------------------------------------------

git-status:
	@git status

git-pull:
	@echo "[INFO] Pulling latest changes from GitHub..."
	git pull
	@echo "[INFO] Pull complete"

git-push:
	@if ("$(MSG)" -eq "") { echo "[ERROR] Must pass MSG='commit message'"; exit 1 }
	@echo "[INFO] Adding all changes..."
	git add .
	@echo "[INFO] Committing with message: $(MSG)"
	git commit -m "$(MSG)"
	@echo "[INFO] Pushing to GitHub..."
	git push
	@echo "[INFO] Push complete"

clean:
	@echo "[INFO] Cleaning Python caches..."
	Get-ChildItem -Path . -Include __pycache__,*.pyc,.pytest_cache,*.egg-info -Recurse -Force | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
	@echo "[INFO] Clean complete"

clean-all: clean
	@echo "[INFO] Removing virtual environment..."
	Remove-Item -Path $(VENV) -Recurse -Force -ErrorAction SilentlyContinue
	@echo "[INFO] Deep clean complete"

# ---------------------------------------------------------------------
# 📊 Info
# ---------------------------------------------------------------------

tree:
	@echo "[INFO] Project structure:"
	@tree /F /A app 2>$$null || Get-ChildItem -Recurse -Directory | Select-Object FullName

version:
	@echo "[INFO] Current version:"
	@Select-String -Path setup.py -Pattern 'version="([^"]+)"' | ForEach-Object { $$_.Matches.Groups[1].Value }
