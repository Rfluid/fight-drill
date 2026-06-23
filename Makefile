VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

.PHONY: help venv install install-dev test test-v test-k build validate serve dev clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

venv: ## Create virtual environment
	python3 -m venv $(VENV)

install: venv ## Install production dependencies
	$(PIP) install -r requirements.txt

install-dev: install ## Install dev dependencies (includes pytest)
	$(PIP) install -r requirements-dev.txt

test: install-dev ## Run all tests
	$(PYTEST) tests/

test-v: install-dev ## Run all tests with verbose output
	$(PYTEST) tests/ -v

test-k: install-dev ## Run tests matching pattern: make test-k K=<pattern>
	$(PYTEST) tests/ -v -k "$(K)"

build: ## Bundle src/ into src.zip + single-entry pyscript.toml (1 fetch, not 40)
	@rm -f src.zip
	@python3 -c "import zipfile, os; \
z = zipfile.ZipFile('src.zip', 'w', zipfile.ZIP_DEFLATED); \
[z.write(os.path.join(r, f)) for r, _, fs in os.walk('src') for f in fs \
if f.endswith('.py') and '__pycache__' not in r]; z.close()"
	@printf '[files]\n"./src.zip" = "./*"\n' > pyscript.toml
	@echo "[build] src.zip + pyscript.toml updated"
	@$(MAKE) --no-print-directory validate

validate: ## Validate pyscript.toml for TOML syntax errors (duplicate keys, etc.)
	@dupes=$$(grep -E '^"' pyscript.toml | sort | uniq -d); \
	if [ -n "$$dupes" ]; then \
		echo '[validate] pyscript.toml INVALID - duplicate keys:'; \
		echo "$$dupes"; \
		exit 1; \
	fi
	@echo '[validate] pyscript.toml OK'

serve: build ## Build and serve the app at http://localhost:8000
	python3 -m http.server 8000

dev: install-dev build ## Serve with auto-rebuild on src/ changes (reload browser manually)
	$(VENV)/bin/watchmedo shell-command \
		--patterns="*.py" \
		--recursive \
		--command='$(MAKE) build' \
		src/ &
	python3 -m http.server 8000

clean: ## Remove venv, caches, and build artifacts
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
