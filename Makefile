# Run local development server
.PHONY: rundev
runlocal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf python manage.py runserver 127.0.0.1:8000

# Run server
.PHONY: run
run:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf python manage.py runserver 127.0.0.1:8000

# Make migrations
.PHONY: migrations
migrations:
	python manage.py makemigrations

# Apply migrations
.PHONY: migrate
migrate:
	python manage.py migrate

# Upload article as draft
.PHONY: upload
upload:
ifndef ARTICLE
	$(error Usage: make upload ARTICLE=/path/to/article.md)
endif
	python manage.py upload $(ARTICLE)

