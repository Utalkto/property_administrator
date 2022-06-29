# python



# django 
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.forms import ValidationError

from django.utils import timezone

# from properties.models import Property, Tenants, Unit
# from tickets.models import Suppliers

# /users/ - to signup a new user,
# /users/me/ - to get user information,
# /token/login/ - to get token,
# /token/logout/ - to logout.

def seven_day_hence():
    return timezone.now() + timezone.timedelta(days=7)

# GENERAL TABLES THAT HAVE MANY RELATIONSHIPS WITH OTHERS


class Country(models.Model):
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.country}'


class City(models.Model):
    # Foreign key
    country = models.ForeignKey(Country, null=False, blank=False, on_delete=models.CASCADE)
    # --------------------------------
    # fields
    city = models.CharField(max_length=100)   

    def __str__(self) -> str:
        return f'{self.id} - {self.city}'

# ---------------------------------------------------
# ORGANIZATION TABLES 


class KumbioPlanPermission(models.Model):
    
    # This is going to be a list a list of modules, enumerated from 1 to N, 
    modules = models.CharField(max_length=120)
    
    number_of_clients_allowed = models.IntegerField()
    number_of_units_allowed = models.IntegerField()
    number_of_properties_allowed = models.IntegerField()
    number_of_users_allowed = models.IntegerField()


class KumbioPlan(models.Model):
    plan = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.plan}'


class Organization(models.Model): 
    # foreignkeys 

    country = models.ForeignKey(Country, null=False, blank=False, on_delete=models.CASCADE)
    plan = models.ForeignKey(KumbioPlan, null=False, blank=False, on_delete=models.CASCADE)

    # Fields
    # ---------------------------------------------------
    
    date_created = models.DateTimeField()
    due_date = models.DateTimeField()
    
    email_username = models.CharField(max_length=256, null=True, default=None)
    email_password = models.BinaryField(null=True, default=None)
    
    key = models.BinaryField(null=True, default=None)
    
    name = models.CharField(max_length=120)
    
    payment_status = models.BooleanField()
    
    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    
    
    # def save(self, **kwargs):
    #     some_salt = 'jksaof23w0923df32' 
    #     self.password_test = make_password(self.password_test, some_salt)
        
    #     if not self.id and self.services == 'Multiple' and not self.routing:
    #         raise ValidationError("You must have to provide routing for multiple services deployment.")
    #     super().save(**kwargs)



class OrganizationClient(models.Model):
    
    # Foreign key
    organization = models.ForeignKey(Organization, null=False, blank=False, on_delete=models.CASCADE)
    # --------------------------------
    # fields
    
    date_created = models.DateTimeField()
    
    email = models.EmailField()
    
    name = models.CharField(max_length=120)
    
    phone_number = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.name}'

# ---------------------------------------------------
# USER TABLES 


class UserRoles(models.Model):
    role = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.role}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            # plan=UserPlans.objects.get(id=1), 
            # city=UserCities.objects.get(id=1), 
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


def outer_json_is_object(value):
    if not isinstance(value, dict):
        raise ValidationError(('Outer JSON item should be an object'), code='invalid_json_object')


class IntKeyJSONField(models.JSONField):

    def __init__(self, *args, **kwargs):
        validators = kwargs.setdefault('validators', [])
        validators.append(outer_json_is_object)
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        if value is not None:
            return { int(k): v for k, v in value.items() }


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    # foreignkeys 
    
    organization = models.ForeignKey(Organization, null=False, blank=False, on_delete=models.CASCADE, default=1)
    country = models.ForeignKey(Country, null=True, blank=True, default=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, blank=True, default=True, on_delete=models.CASCADE)
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
    
    has_access = models.BooleanField(default=False)
    
    link_to_recover_password = models.CharField(max_length=35, null=True, default=None)
    time_recover_link_creation = models.DateTimeField(null=True, default=None)
    
    
    # USER PERMISSIONS 
    
    can_delete_data = models.BooleanField(default=True)
    can_edit_data = models.BooleanField(default=True)
    can_add_data = models.BooleanField(default=True)
    
    modules_access = models.CharField(default='1,2,3', max_length=120)    
    clients_access = IntKeyJSONField(default=dict)

    
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

    
    
    