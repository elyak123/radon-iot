#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ


def settings_module_handler():
    ROOT_DIR = environ.Path(__file__) - 1
    env = environ.Env()
    # .env file, should load only in development environment
    READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

    if __name__ == "__main__":
        if READ_DOT_ENV_FILE:
            # Operating System Environment variables have precedence over variables defined in the .env file,
            # that is to say variables from the .env files will only be used if not defined
            # as environment variables.
            env_file = str(ROOT_DIR.path('.env'))
            env.read_env(env_file)
            os.environ.setdefault(
                "DJANGO_SETTINGS_MODULE",
                env('DJANGO_SETTINGS_MODULE')
            )
        else:
            os.environ.setdefault(
                "DJANGO_SETTINGS_MODULE", "radon.config.settings.production"
            )


def main():
    settings_module_handler()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
