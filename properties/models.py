# django
from django.db import models
from django.db.models.fields import CharField, BooleanField, IntegerField, TextField, DecimalField, DateField

from django.utils import timezone

from register.models import CustomUser, OrganizationClient

# main tables 

class Team(models.Model):

    landlord = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE)

    name = models.CharField(max_length=120, default='')
    email = models.EmailField(max_length=120, default='')
    phone = models.CharField(max_length=120, default='')
    address = models.CharField(max_length=120, default='')
    role = models.CharField(max_length=120, default='')
    
    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    

class PropertyType(models.Model):
    property_type = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.property_type}'


class UnitType(models.Model):
    unit_type = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.unit_type}' 


class PropertyCountries(models.Model):
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.country}' 
    

class PropertyCities(models.Model):
    # Foreign key
    country = models.ForeignKey(PropertyCountries, null=False, blank=False, on_delete=models.CASCADE)
    # --------------------------------
    # fields
    
    city = models.CharField(max_length=100)   
    
    def __str__(self) -> str:
        return f'{self.id} - {self.city}' 


class Property(models.Model):
    # foreign keys 
    client = models.ForeignKey(OrganizationClient, null=False, blank=False, on_delete=models.CASCADE, default=1)
    city = models.ForeignKey(PropertyCities, null=False, blank=False ,on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, null=False, blank=False, on_delete=models.CASCADE)
    
    # ------------------------------
    # fields 
    
    address = CharField(max_length=400)
    coordinates = models.JSONField(null=True)
    
    img = models.ImageField(upload_to='properties', null=True)
    maps_url =  models.URLField(default='')

    name = CharField(max_length=100, default='')
    number_of_units = IntegerField(default=0)
    
    price_paid = DecimalField(max_digits=19, decimal_places=2, default=0, null=True)
    photos = models.JSONField(null=True)
    
    year_built = IntegerField(null=True)
    year_bought = IntegerField(null=True)
    
    datetime_created = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(CustomUser, default=1, on_delete=models.PROTECT, related_name='property_create_by')
    
    last_time_edited = models.DateTimeField(null=True, default=None)
    last_edition_made_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT, 
                                             default=None, related_name='property_last_edited_by')

    
    def __str__(self) -> str:
        return f'{self.id} - {self.name}' 
    

class UnitContractType(models.Model):
    contract_type = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.contract_type}' 


class PetType(models.Model):
    pet_type = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.pet_type}'


class Unit(models.Model):
    # foreign keys 
     
    property = models.ForeignKey(Property, null=False, blank=False, on_delete=models.CASCADE)
    unit_type = models.ForeignKey(UnitType, null=False, blank=False, on_delete=models.CASCADE)
    
    #  ------------------------------------
    #  fields
    
    air_conditioning = BooleanField(null=True, default=None)
    appliances = models.JSONField()
    
    bathrooms = IntegerField()
    
    deposit_amount = DecimalField(max_digits=19, decimal_places=2)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    details = models.TextField(null=True, default=None)
    date_deposit_received = DateField(null=True, default=None)
    
    extra_resident_price = DecimalField(max_digits=5, decimal_places=2)
    extra_resident = IntegerField(null=True, default=None)
    
    heating_type = CharField(max_length=50, null=True, default=None)
    has_pet =  BooleanField(null=True, default=None)
    
    lease_typee = models.ForeignKey(UnitContractType, null=True, default=None, on_delete=models.CASCADE)
    lease_start_date = models.DateField(default=None, null=True, blank=True, )
    lease_expiration_date = models.DateField(default=None, null=True, blank=True)
    
    main_tenant_name = CharField(max_length=150, null=True, default=None)
    
    name = CharField(max_length=100, null=True, default=None)
    notes = TextField(null=True, default=None)
    number_of_pets = IntegerField(null=True, default=None)
    number_of_residents = IntegerField(null=True, default=None)
    
    payments_email = CharField(max_length=100, null=True, default=None)
    parking_available = BooleanField()
    parking_type = CharField(max_length=50, null=True, default=None)
    
    pet_fee = DecimalField(max_digits=19, decimal_places=2, null=True, default=None)
    pet_policy= CharField(max_length=100)
    pets_living = models.CharField(max_length=50, null=True, default=None)
    
    rented = BooleanField(default=False) 
    rent = DecimalField(max_digits=19, decimal_places=2, null=True, default=None) 
    rooms = IntegerField()
    
    servicesss = models.JSONField(null=True, default=dict)
    square_feet_area = DecimalField(max_digits=19, decimal_places=2)
    shed = BooleanField(default=False)

    pet_typee = models.ForeignKey(PetType, null=True, default=None, on_delete=models.CASCADE)
    
    unit_number = models.IntegerField(default=1)
    
    availability = models.DateField(null=True, blank=True, default=None)

    balcony = models.BooleanField(null=True, blank=True, default=False)

    lease_information = models.TextField(null=True, blank=True, default=None)
    video_tour = models.BooleanField(null=True, blank=True, default=False)
    private_unit = models.BooleanField(null=True, blank=True, default=True)

    yard = models.BooleanField(null=True, blank=True, default=False)

    outdoor_storage = models.BooleanField(null=True, blank=True, default=False)
    basement_unit = models.BooleanField(null=True, blank=True, default=False)
    people_above = models.BooleanField(null=True, blank=True, default=False)
    unemployed_people = models.BooleanField(null=True, blank=True, default=False)
    kids = models.BooleanField(null=True, blank=True, default=False)
    pet_friendly = models.BooleanField(null=True, blank=True, default=False)
    
    utilities_cost = models.CharField(max_length=120, null=True, blank=True, default='')
    utilities_included = models.TextField(null=True, blank=True, default='')
    can_utilities_be_included = models.TextField(null=True, blank=True, default='')
    
    max_weeks_to_move = models.IntegerField(null=True, default=0)
    
    datetime_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, default=1, on_delete=models.PROTECT, related_name='unit_create_by')
    
    last_time_edited = models.DateTimeField(null=True, default=None)
    last_edition_made_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT, 
                                             default=None, related_name='unit_last_edited_by')
    
    accessibility_features = models.BooleanField(default=False)
    ad_title = models.CharField(max_length=120, default='')
    description = models.TextField(default='')
    
    smoking_permitted = models.BooleanField(default=False)
    
    is_school_near = models.BooleanField(default=False)
    is_hospital_near = models.BooleanField(default=False)
    is_mall_near = models.BooleanField(default=False)
    is_store_near = models.BooleanField(default=False)
    is_bus_stop_near = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f'{self.id} - {self.property.name} - {self.property.id}' 

    
class TenantType(models.Model):
    tenan_type = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.tenan_type}'


class Tenants(models.Model):
    # foreign keys
    
    client = models.ForeignKey(OrganizationClient, default=1, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='tenants', null=False, blank=False ,on_delete=models.CASCADE)
    
    # -------------------------------------------------------
    # fields
    date_deposit_received = models.DateField(default=None ,null=True)
    
    email = CharField(max_length=50)
    email2 = CharField(max_length=50, null=True, default=None, blank=True)
    emergency_contact = CharField(max_length=50, null=True, default=None, blank=True)
    emergency_contact_name = CharField(max_length=50, null=True, default=None, blank=True)
    
    payments_delay = IntegerField(default=0)
    payments_on_time = IntegerField(default=0)
    
    name = CharField(max_length=50) 
    
    phone = CharField(max_length=50, null=False)
    phone2 = CharField(max_length=50, null=True, default=None, blank=True)
    preferred_communications = CharField(max_length=20)
    
    secondary_communications = CharField(max_length=20, null=True, default=None, blank=True)
    standing_qualification=models.IntegerField(default=0)
    
    tenant_type = models.ForeignKey(TenantType, null=True, default=None, on_delete=models.CASCADE)
    
    datetime_created = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(CustomUser, default=1, on_delete=models.PROTECT, related_name='tenant_create_by')
    
    last_time_edited = models.DateTimeField(null=True, default=None)
    last_edition_made_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT, 
                                             default=None, related_name='tenant_last_edited_by')

    
    deleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    

class Links(models.Model):
    # Foreign key
    owner = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, default=1)
    # --------------------------------
    # fields
    
    link = models.CharField(max_length=500)
    link_name = models.CharField(max_length=150)
    link_type = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.link_name}'
    
