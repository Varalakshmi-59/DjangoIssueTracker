from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DEVELOPER', 'Developer'),
        ('TESTER', 'Tester'),
        ('PROJECT_MANAGER', 'Project Manager'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='DEVELOPER'
    )
    
    # Override email field to make it unique
    email = models.EmailField(unique=True)
    
    # Additional fields
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
