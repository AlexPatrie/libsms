.PHONY: fresh notebook test docs publish

fresh:
	@uv cache clean && rm -f uv.lock && uv lock --no-cache && uv sync --all-groups --no-cache

notebook:
	@uv run --no-cache marimo edit notebooks/$(f).py

test:
	@uv run pytest -s

docs:
	@cd documentation && uv run make clean && uv run make html && cd ..

publish:
	@make fresh; \
	token=$$(cat ./assets/.pypi.token); \
	rm -rf dist/; \
	uv build; \
	uv publish --username "__token__" --password $$token;