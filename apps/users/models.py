from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('main_admin', 'Main Admin'),
        ('branch_admin', 'Branch Admin'),
        ('staff', 'Staff'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    country = models.ForeignKey('country.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_main_admin(self):
        return self.role == 'main_admin'
    
    def is_branch_admin(self):
        return self.role == 'branch_admin'
    
    def is_staff_user(self):
        return self.role == 'staff'
