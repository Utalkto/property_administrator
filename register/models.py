from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# /users/ - to signup a new user,
# /users/me/ - to get user information,
# /token/login/ - to get token,
# /token/logout/ - to logout.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    city = models.CharField(null=False, max_length=120, default='')
    country = models.CharField(null=False, max_length=120, default='')
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
        
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    invited_by = models.IntegerField(null=False, default=-1) # if -1 then is a landlord
    
    last_name = models.CharField(max_length=255)
        
    objects = CustomUserManager()
    
    phone = models.CharField(max_length=120, default='')
    plan = models.IntegerField(default=0) # default is 0 for free
    plan_status = models.BooleanField(default=True)
    
    plan_expired_on = models.DateField(default='2022-05-03') 
    registration_date = models.DateField(default='2022-05-03')
    
    # roles
    # free > 0
    # landlord > 1
    # property_manager > 2
    # tenat > 3
    
    role = models.IntegerField(default=0) # default is 0 for demo
    
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


