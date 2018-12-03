.PHONY: all dev lint test dist clean

all:

dev:
	pip3 install -r requirements.dev.txt
	pip3 install -e .

lint:
	pylint cnftools -v --reports=y --output-format=parseable || pylint-exit $$?

test:

dist:
	python3 setup.py sdist bdist_wheel

deploy: dist
	twine upload --verbose dist/*

clean:
	rm -rf dist/
