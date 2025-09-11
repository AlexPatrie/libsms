.PHONY: fresh notebook test docs publish check python commit

fresh:
	@uv cache clean && rm -f uv.lock && uv lock --no-cache && uv sync --all-groups --no-cache

notebook:
	@uv run --no-cache marimo edit notebooks/$(f).py

test:
	@uv run pytest -s

commit:
	@git add --all && git commit -m $(message) && git push

docs:
	@now=$$(date '+%Y-%m-%d %H:%M:%S'); \
	if [ -z "$(message)" ]; then \
	  msg="Updates to documentation $${now}"; \
	else \
	  msg="$(message)"; \
	fi; \
	cd documentation && uv run make clean && uv run make html && cd .. && \
	git add --all && git commit -m "$$msg" && git push


publish:
	@[ -z "$(message)" ] && port="Publish update" || message=$(message); \
	make fresh; \
	token=$$(cat ./assets/.pypi.token); \
	rm -rf dist/; \
	uv build; \
	uv publish --username "__token__" --password $$token; \
	make docs

check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --no-cache
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

python:
	@uv run python -m asyncio
