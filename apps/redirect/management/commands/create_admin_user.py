from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@gmail.com"
    ADMIN_PASSWORD = "adminpassword"
    help = "Check and create default development admin user"

    def handle(self, *args, **options):
        user_class = get_user_model()

        user, _ = user_class.objects.update_or_create(
            username=self.ADMIN_USERNAME,
            defaults={
                "email": self.ADMIN_EMAIL,
                "first_name": "Admin",
                "last_name": "Test",
                "is_staff": True,
                "is_active": True,
                "is_superuser": True,
            },
        )
        user.set_password(self.ADMIN_PASSWORD)
        user.save()
        self.stdout.write(self.style.SUCCESS("Development admin user has been created!"))
