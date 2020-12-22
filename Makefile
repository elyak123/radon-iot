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
dev:
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=radon.config.settings.production/DJANGO_SETTINGS_MODULE=radon.config.settings.local/g .env
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=radon.config.settings.test/DJANGO_SETTINGS_MODULE=radon.config.settings.local/g .env
	@sed -i.bak s/DJANGO_DEBUG=False/DJANGO_DEBUG=True/g .env
	@docker-compose -f docker-compose-dev.yml up

buildev:
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=radon.config.settings.production/DJANGO_SETTINGS_MODULE=radon.config.settings.local/g .env
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=radon.config.settings.test/DJANGO_SETTINGS_MODULE=radon.config.settings.local/g .env
	@sed -i.bak s/DJANGO_DEBUG=False/DJANGO_DEBUG=True/g .env
	@docker-compose -f docker-compose-dev.yml up --build

shell:
	@docker-compose run django python manage.py shell

deploy:
	@docker-compose up -d

backup:
	@docker-compose exec postgis backup

restore:
	@docker-compose exec postgis restore

localbackup:
	@pg_dump -U ${POSTGRES_USER} | gzip -c > docker/production/postgis/backups/backup_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz

listbackups:
	@docker-compose exec postgis list-backups