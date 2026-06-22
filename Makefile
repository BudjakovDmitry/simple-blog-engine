PYTHON ?= .venv/bin/python

# Run development server
.PHONY: run
run:
	$(PYTHON) manage.py runserver

# Make migrations
.PHONY: migrations
migrations:
	$(PYTHON) manage.py makemigrations

# Apply migrations
.PHONY: migrate
migrate:
	$(PYTHON) manage.py migrate

# Upload article as draft
.PHONY: upload
upload:
ifndef ARTICLE
	$(error Usage: make upload ARTICLE=/path/to/article.md)
endif
	$(PYTHON) manage.py upload $(ARTICLE)

