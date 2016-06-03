.PHONY: build release test clean

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

test:
	rm -rf build
	py.test --cov=abvdget

clean:
	rm -rf build/*

