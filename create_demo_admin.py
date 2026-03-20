# create_demo_admin.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile 


if not User.objects.filter(username="testadmin").exists():
    
    user = User.objects.create_user(
        username="testadmin",
        password="admin123",
        email=""
    )
    
    profile = UserProfile.objects.create(
        user=user,
        role="ADMIN"
    )
   
    user.is_staff = True
    user.is_superuser = True
    user.save()

    print("Demo admin created: username='testadmin', password='admin123'")
else:
    print("Demo admin already exists")
