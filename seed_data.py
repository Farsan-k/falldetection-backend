"""
Seed script to create initial admin, doctor, and user accounts.
Run with: python seed_data.py
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'falldetectionusingai.settings')
django.setup()

from django.contrib.auth.models import User as AuthUser
from myapp.models import Login, Doctor, User as AppUser, Patient

def seed():
    print("Seeding initial data...")

    # 1. Django Superuser
    if not AuthUser.objects.filter(username='admin').exists():
        AuthUser.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
        print("[+] Created Django superuser (admin / admin12345)")
    else:
        print("[+] Django superuser already exists")

    # 2. Portal Admin Login
    admin_login, created = Login.objects.get_or_create(
        Username='admin1@gmail.com',
        defaults={'Password': 'admin11', 'Type': 'admin'}
    )
    if created:
        print("[+] Created Portal Admin (admin1@gmail.com / admin11)")
    else:
        print("[+] Portal Admin already exists")

    # 3. Doctor Login and Profile
    doc_login, created = Login.objects.get_or_create(
        Username='doctor2@gmail.com',
        defaults={'Password': 'doctor2', 'Type': 'Doctor'}
    )
    if created:
        Doctor.objects.create(
            Name='Dr. Smith',
            Email='doctor2@gmail.com',
            Phone=9876543210,
            Photo='/media/doc.jpg',
            Qualification='MBBS, MD',
            Department='General Medicine',
            Gender='Male',
            DOB=date(1985, 5, 20),
            Place='City Hospital',
            City='Metropolis',
            State='State',
            Pincode='123456',
            Status='Approve',
            LOGIN=doc_login
        )
        print("[+] Created sample Doctor (doctor2@gmail.com / doctor2)")
    else:
        print("[+] Doctor account already exists")

    # 4. User and Patient Account
    user_login, created = Login.objects.get_or_create(
        Username='user1@gmail.com',
        defaults={'Password': 'user1', 'Type': 'User'}
    )
    if created:
        app_user = AppUser.objects.create(
            Name='John Doe',
            Email='user1@gmail.com',
            Phone=9123456789,
            Photo='/media/user.jpg',
            Gender='Male',
            Place='Main Street',
            City='Metropolis',
            State='State',
            Pincode='123456',
            DOB=date(1990, 1, 1),
            LOGIN=user_login
        )
        Patient.objects.create(
            Name='Patient One',
            Email='patient1@gmail.com',
            Phone=9123456780,
            Photo='/media/patient.jpg',
            Gender='Male',
            Place='Main Street',
            City='Metropolis',
            State='State',
            Pincode='123456',
            DOB=date(1950, 1, 1),
            USER=app_user
        )
        print("[+] Created sample User & Patient (user1@gmail.com / user1)")
    else:
        print("[+] User account already exists")


    print("\nDatabase seeding completed successfully!")

if __name__ == '__main__':
    seed()
