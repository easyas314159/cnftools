.PHONY: all dev lint test dist clean

all:

dev:
	pip install -r requirements.dev.txt
	pip install -e .

lint:
	pylint cnftools -v --reports=y --output-format=parseable || pylint-exit $$?

test:

dist:
	python setup.py sdist bdist_wheel

deploy: dist
	twine upload --config-file ~/.pypirc --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf dist/
