.PHONY: all dev lint test dist clean

all:

dev:
	pip install -r requirements.dev.txt
	pip install -e .

lint: dev
	pylint cnftools -v --reports=y --output-format=parseable || pylint-exit $$?

test: lint

clean:
	rm -rf dist/
