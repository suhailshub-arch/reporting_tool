from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from config.configs import USER_CONFIG

class Command(BaseCommand):
    help = 'Creates a default superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(USER_CONFIG['default_admin_username'], USER_CONFIG['default_admin_email'], USER_CONFIG['default_admin_password'])
            self.stdout.write(self.style.SUCCESS('Successfully created a new superuser'))
        else:
            self.stdout.write(self.style.SUCCESS('Existing superuser found'))
