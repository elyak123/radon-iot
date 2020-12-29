from django.core.management.base import BaseCommand
from radon.georadon.utils import create_estado


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('estado', type=str, help='Nombre del Estado a crear.')

    def handle(self, *args, **kwargs):
        estado = create_estado(kwargs['estado'])
        self.stdout.write(self.style.SUCCESS(f'Estado creado con id {estado.pk}.'))
