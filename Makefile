mkenv:
	@pip-compile --help > /dev/null
	@pip-sync requirements/local.txt

pipcompile:
	@pip-compile --help > /dev/null
	@pip-compile --generate-hashes requirements/base.in --output-file requirements/base.txt
	@pip-compile --generate-hashes requirements/local.in --output-file requirements/local.txt
	@pip-compile --generate-hashes requirements/test.in --output-file requirements/test.txt
	@pip-compile --generate-hashes requirements/production.in --output-file requirements/production.txt

static:
	#@python manage.py collectstatic --noinput --clear
	@python manage.py collectstatic --noinput
	@python manage.py compress --force
	@python manage.py collectstatic --noinput
	@python manage.py migrate

deploy: static
	@service apache2 restart