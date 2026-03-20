import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='testadmin').exists():
    admin_user = User.objects.create_user(
        username='testadmin',
        password='admin123',
        role='ADMIN'
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("Demo admin created")
else:
    print("Demo admin already exists")
