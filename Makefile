mkenv:
	@pip-compile --help > /dev/null
	@pip-sync requirements/local.txt

pipcompile:
	@pip-compile --help > /dev/null
	@pip-compile --generate-hashes requirements/base.in --output-file requirements/base.txt
	@pip-compile --generate-hashes requirements/local.in --output-file requirements/local.txt
	@pip-compile --generate-hashes requirements/test.in --output-file requirements/test.txt

showvars:
	@sed -i.bak "s|SSL_CERT|$(SSL_CERT)|g" zappa_settings.json
	@sed -i.bak "s|ZAPPA_BUCKET|$(ZAPPA_BUCKET)|g" zappa_settings.json
	@sed -i.bak "s|AWS_SNS_ARN|$(AWS_SNS_ARN)|g" zappa_settings.json
	@sed -i.bak "s|AWS_REGION_DEPLOYMENT|$(AWS_REGION_DEPLOYMENT)|g" zappa_settings.json
	@sed -i.bak "s|DOMAIN_NAME|$(DOMAIN_NAME)|g" zappa_settings.json

hidevars:
	@sed -i.bak "s|$(SSL_CERT)|SSL_CERT|g" zappa_settings.json
	@sed -i.bak "s|$(ZAPPA_BUCKET)|ZAPPA_BUCKET|g" zappa_settings.json
	@sed -i.bak "s|"$(AWS_SNS_ARN)"|AWS_SNS_ARN|g" zappa_settings.json
	@sed -i.bak "s|$(AWS_REGION_DEPLOYMENT)|AWS_REGION_DEPLOYMENT|g" zappa_settings.json
	@sed -i.bak "s|$(DOMAIN_NAME)|DOMAIN_NAME|g" zappa_settings.json

dev:
	@zappa deploy dev

deploydev: showvars dev hidevars