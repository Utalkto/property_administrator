# django 

from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.utils import timezone

# /users/ - to signup a new user,
# /users/me/ - to get user information,
# /token/login/ - to get token,
# /token/logout/ - to logout.


def seven_day_hence():
    return timezone.now() + timezone.timedelta(days=7)


class UserCountries(models.Model):
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.country


class UserCities(models.Model):
    # Foreign key
    country = models.ForeignKey(UserCountries, null=False, blank=False, on_delete=models.CASCADE)
    # --------------------------------
    # fields
    city = models.CharField(max_length=100)   

    def __str__(self) -> str:
        return self.city


class UserPlans(models.Model):
    plan = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    def __str__(self) -> str:
        return self.plan
    
    
class UserRoles(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.role 


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            plan=UserPlans.objects.get(id=1), 
            city=UserCities.objects.get(id=1), 
            role=UserRoles.objects.get(id=1),  
            **extra_fields)
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
    
    # foreignkeys 
    
    plan = models.ForeignKey(UserPlans, null=False, blank=False, on_delete=models.CASCADE, default=1) # default is 1 for free
    city = models.ForeignKey(UserCities, null=False, blank=False, on_delete=models.CASCADE, default=1)
    
    # roles
    # free > 1
    # landlord > 2
    # property_manager > 3
    # tenat > 4
    
    role = models.ForeignKey(UserRoles, null=False, blank=False, on_delete=models.CASCADE, default=1)
    
    # -----------------------------------------------------------
    # fields 
 
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
        
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    invited_by = models.IntegerField(null=False, default=-1) # if -1 then is a landlord
    
    last_name = models.CharField(max_length=255)
        
    objects = CustomUserManager()
    
    phone = models.CharField(max_length=120, default='')
    
    plan_status = models.BooleanField(default=True)
    
    plan_expired_on = models.DateTimeField(default=seven_day_hence) 
    registration_date = models.DateTimeField(default=timezone.now)
    
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.email} - {self.id}'


