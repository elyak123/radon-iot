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

static:
	#@python manage.py collectstatic --noinput --clear
	@python manage.py collectstatic --noinput
	@python manage.py compress --force
	@python manage.py collectstatic --noinput
	@python manage.py migrate

deploy: static
	@service apache2 restart