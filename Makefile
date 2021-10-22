.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

all: fastproaudio docs

fastproaudio: $(SRC)
	nbdev_build_lib
	touch fastproaudio

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

git_update: fastproaudio docs
	nbdev_build_lib
	nbdev_build_docs
	git add *.ipynb settings.ini README.md fastproaudio docs nbs
	git commit
	git push

test:
	nbdev_test_nbs

release: pypi conda_release
	nbdev_bump_version

conda_release:
	fastrelease_conda_package

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist
