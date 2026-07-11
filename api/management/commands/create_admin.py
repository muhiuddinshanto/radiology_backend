import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser, or rotates its password when explicitly requested.'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        reset_password = os.environ.get('RESET_SUPERUSER_PASSWORD', '').lower() in {
            '1', 'true', 'yes', 'on'
        }

        if not username or not password:
            self.stdout.write('Superuser environment variables are missing.')
            return

        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user is None:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        elif reset_password:
            user.email = email
            user.set_password(password)
            user.save(update_fields=['email', 'password'])
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" password rotated.'))
        else:
            self.stdout.write('Superuser already exists; password was not changed.')