from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_normaluser(self, name, surname, username, emailAddress, password=None):
        if not emailAddress:
            raise ValueError('User must have an emailAddress address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            emailAddress = self.normalize_email(emailAddress),
            username = username,
            name = name,
            surname = surname,
        )
# 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, emailAddress, username, password):
        user = self.create_normaluser(
            emailAddress = self.normalize_email(emailAddress),
            username = username,
            password = password,
            name = name,
            surname = surname,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    name      = models.CharField(max_length=50)
    surname       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    emailAddress           = models.EmailField(max_length=100, unique=True)
    contactNo    = models.CharField(max_length=50)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'emailAddress'
    REQUIRED_FIELDS = ['username', 'name', 'surname']

    objects = MyAccountManager()
    # 
    # def full_name(self):
    #     return f'{self.name} {self.surname}'

    def __str__(self):
        return self.emailAddress

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
