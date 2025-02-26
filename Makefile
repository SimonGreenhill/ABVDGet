.PHONY: build release test clean

build:
	uv build

release:
	uv publish

test:
	uv run py.test --cov=abvdget


