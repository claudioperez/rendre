PACKAGE = rendre
VRNPATN = '__version__ = "([^"]+)"'
VERSION = $(shell sed -nE 's:__version__ = "([^"]+)":\1:p' ./src/$(PACKAGE)/__init__.py)

test:
	echo $(VERSION)

install:
	pip install -e .

# docs:
# 	help2man aurore | pandoc -f man -t html > README.html


publish:
	python setup.py clean --all sdist bdist_wheel
	twine upload --skip-existing dist/*

	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags

