.PHONY: fresh notebook test docs

fresh:
	@uv cache clean && rm -f uv.lock && uv lock --no-cache && uv sync --all-groups --no-cache

notebook:
	@uv run --no-cache marimo edit notebooks/$(f).py

test:
	@uv run pytest -s

docs:
	@cd documentation && uv run make clean && uv run make html && cd ..