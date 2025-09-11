LATEST_PYPI_VERSION = $(shell uv run pip index versions libsms 2>/dev/null | sed -n 's/^Available versions: //p' | awk -F', ' '{print $$1}')
CURRENT_VERSION = $(shell grep -E '^version\s*=' pyproject.toml | head -1 | sed -E 's/^version\s*=\s*"(.*)"/\1/' | sed 's/^version = //')

.PHONY: fresh notebook test docs publish check python commit version

fresh:
	@uv cache clean && rm -f uv.lock && uv lock --no-cache && uv sync --all-groups --no-cache

notebook:
	@uv run --no-cache marimo edit notebooks/$(f).py

test:
	@uv run pytest -s

commit:
	@now=$$(date '+%Y-%m-%d %H:%M:%S'); \
	if [ -z "$(message)" ]; then \
	  msg="Updates to repo $${now}"; \
	else \
	  msg="$(message)"; \
	fi; \
	git add --all && git commit -m "$$msg" && git push

check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --no-cache
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

docs:
	@now=$$(date '+%Y-%m-%d %H:%M:%S'); \
	if [ -z "$(message)" ]; then \
	  msg="Updates to documentation $${now}"; \
	else \
	  msg="$(message)"; \
	fi; \
	cd documentation && uv run make clean && uv run make html && cd .. && \
	make commit message="$$msg"

publish:
	@now=$$(date '+%Y-%m-%d %H:%M:%S'); \
	if [ -z "$(message)" ]; then \
	  msg="Publish new version $${now}"; \
	else \
	  msg="$(message)"; \
	fi; \
	if [ "${CURRENT_VERSION}" = "${LATEST_PYPI_VERSION}" ]; then \
		echo "This version already exists: ${CURRENT_VERSION}...exiting!"; \
		exit 1; \
	else \
		echo "Version is new!"; \
	fi;
	make fresh; \
	token=$$(cat ./assets/.pypi.token); \
	rm -rf dist/; \
	uv build; \
	uv publish --username "__token__" --password $$token; \
	make docs message="$$msg"

python:
	@uv run python -m asyncio
