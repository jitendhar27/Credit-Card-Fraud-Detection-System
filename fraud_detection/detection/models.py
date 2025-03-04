from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(auto_now_add=True)  # Fixed

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="admin_users_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="admin_users_permissions",
        blank=True
    )

    def __str__(self):
        return self.username
