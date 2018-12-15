.PHONY: all dev lint test dist clean

all:

dev:
	pip3 install --upgrade -r requirements.dev.txt
	pip3 install -e .

lint:
	pylint cnftools -v --reports=y --output-format=parseable || pylint-exit $$?

test:
	nose2 -v --with-coverage --coverage cnftools --coverage-report term-missing --coverage-report html tests

dist:
	python3 setup.py sdist bdist_wheel

deploy: dist
	twine upload --verbose dist/*

clean:
	rm -rf dist/
