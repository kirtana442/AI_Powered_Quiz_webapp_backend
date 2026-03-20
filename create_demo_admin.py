import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

user, created = User.objects.get_or_create(
    username="testadmin",
    defaults={"password": "admin123", "email": ""}
)

if created:
    user.is_staff = True
    user.is_superuser = True
    user.set_password("admin123") 
    user.save()

profile, profile_created = UserProfile.objects.get_or_create(
    user=user,
    defaults={"role": "ADMIN"}
)

print("Demo admin ensured:")
print(f"- username: {user.username}")
print(f"- role: {profile.role}")
