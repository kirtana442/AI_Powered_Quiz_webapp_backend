import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

user, created = User.objects.get_or_create(username="testadmin")
if created:
    user.is_staff = True
    user.is_superuser = True
    user.set_password("admin123")  
    user.save()
else:
    
    user.is_staff = True
    user.is_superuser = True
    user.save()

profile, _ = UserProfile.objects.get_or_create(user=user)
profile.role = "ADMIN"  
profile.save()

print("Demo admin ensured:")
print(f"- username: {user.username}")
print(f"- role: {profile.role}")
