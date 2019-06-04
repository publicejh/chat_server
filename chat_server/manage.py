#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # check manage env
    env = os.environ.get('CHAT_ENV', 'production')
    print("manage.py env: {}".format(env))

    if env == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.deploy')
    elif env == 'development':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.debug')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_server.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
