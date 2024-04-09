from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
import os
import random

def filename_ext(filepath):
    file_base = os.path.basename(filepath)
    filename, ext = os.path.splitext(file_base)
    return filename, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9498594795)
    name, ext = filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "pictures/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class MemberManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

    def active(self):
        return self.filter(active=True)

class Member(AbstractUser):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, default='default_surname')
    telephone = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    new_believer_school = models.BooleanField(max_length=255, blank=True, null=True, default='')
    pays_tithe = models.BooleanField(max_length=255, blank=True, null=True, default='')
    working = models.BooleanField(max_length=255, blank=True, null=True, default='')
    schooling = models.BooleanField(max_length=255, blank=True, null=True, default='')
    picture = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='member_groups',  # Add related_name to avoid clashes
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='member_user_permissions',  # Add related_name to avoid clashes
    )

    objects = MemberManager()

    def __str__(self):
        return self.username

class TestDb(models.Model):
    field = models.CharField(max_length=120)
