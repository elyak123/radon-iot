mkenv:
	@pip-compile --help > /dev/null
	@pip-sync requirements/local.txt

mkprod:
	@pip-compile --help > /dev/null
	@pip-sync requirements/production.txt

pipcompile:
	@pip-compile --help > /dev/null
	@pip-compile requirements/base.in --output-file requirements/base.txt
	@pip-compile requirements/local.in --output-file requirements/local.txt
	@pip-compile requirements/test.in --output-file requirements/test.txt
	@pip-compile requirements/production.in --output-file requirements/production.txt

shell:
	@docker-compose run django python manage.py shell

deploy:
	@docker-compose up -d

backup:
	@docker-compose exec postgis backup

listbackups:
	@docker-compose exec postgis list-backups