.PHONY: all dev lint test dist clean

all:

dev:
	pip install -r requirements.dev.txt
	pip install -e .

lint: dev
	pylint cnftools -v --reports=y --output-format=parseable || pylint-exit $$?

test: lint

dist:
	python setup.py sdist bdist_wheel

deploy: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf dist/
