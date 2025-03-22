
pull:
	git pull --rebase

deps:
	pip install -U -r requirements.txt

static:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

update: pull deps migrate static
	@echo "Update steps completed successfully."


.PHONY: pull deps static migrate prefupdatelight
