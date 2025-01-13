PY ?= python3

.PHONY: build test test-c
build:
	@true

test-c:
	@true

test:
	$(PY) manage.py test tests --settings=storefront.settings.test --noinput
