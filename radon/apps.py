from django.apps import AppConfig

class RadonConfig(AppConfig):
	name = 'radon'
	verbose_name = 'radon'

	def ready(self):
		pass