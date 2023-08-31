install: ## Install project
	pip install --editable .

test: ## Run tests
	python -m pytest -v

lint: .clean ## Run linter
	python -m black .
	python -m ruff --fix .
	python -m mypy .

tool: install ## Install development tools
	python -m pip install  ".[dev]"

.clean:
	rm -rf build/

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
