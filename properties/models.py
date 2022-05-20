from operator import truediv
from django.db import models
from django.db.models.fields import CharField, BooleanField, IntegerField, TextField, DecimalField, DateField
from register.models import CustomUser

# main tables 

class PropertyTypes(models.Model):
    property_type = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.property_type


class UnitTypes(models.Model):
    unit_type = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.unit_type


class PropertyCountries(models.Model):
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.country
    

class PropertyCities(models.Model):
    # Foreign key
    country = models.ForeignKey(PropertyCountries, null=False, blank=False, on_delete=models.CASCADE)
    # --------------------------------
    # fields
    
    city = models.CharField(max_length=100)   
    
    def __str__(self) -> str:
        return self.city 


class Properties(models.Model):
    # foreign keys 
    landlord = models.ForeignKey(CustomUser, null=False, blank=False ,on_delete=models.CASCADE)
    city = models.ForeignKey(PropertyCities, null=False, blank=False ,on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyTypes, null=False, blank=False, on_delete=models.CASCADE)
    
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
    

class Units(models.Model):
    # foreign keys 
     
    property_manager = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, null=False, blank=False, on_delete=models.CASCADE)
    unit_type = models.ForeignKey(UnitTypes, null=False, blank=False, on_delete=models.CASCADE)
    
    
    #  ------------------------------------
    #  fields
    
    air_conditioning = BooleanField(default=False)
    appliances = models.JSONField()
    
    bathrooms = IntegerField()
    
    deposit_amount = DecimalField(max_digits=19, decimal_places=2)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    details = models.JSONField(null=True)
    date_deposit_received = DateField(null=True)
    
    extra_resident_price = DecimalField(max_digits=5, decimal_places=2, default=0)
    extra_resident = IntegerField(default=0)
    
    heating_type = CharField(max_length=50, default='')
    has_pet =  BooleanField(default=True)
    
    lease_type = CharField(max_length=100)
    
    main_tenant_name = CharField(max_length=150, default='Homero el griego')
    
    name = CharField(max_length=100, default='')
    notes = TextField(default='')
    number_of_pets = IntegerField(default=0)
    number_of_residents = IntegerField(default=0)
    
    payments_email = CharField(max_length=100, default='')
    parking_available = BooleanField(default=False)
    parking_type = CharField(max_length=50, default='')
    
    shed = models.BooleanField()
    pet_fee = DecimalField(max_digits=19, decimal_places=2, default=0)
    pet_policy= CharField(max_length=100, default='')
    pets_living = models.CharField(max_length=50, default='')
    
    rented = BooleanField(default=False) 
    rent = DecimalField(max_digits=19, decimal_places=2, default=0, null=False) 
    rooms = IntegerField(default=0)
    
    services = models.JSONField()
    square_feet_area = DecimalField(max_digits=19, decimal_places=2, default=0)
    shed = BooleanField(default=False)
    
    unit = IntegerField(default=1)
    
    
class Tenants(models.Model):
    # foreign keys
    
    landlord = models.ForeignKey(CustomUser, default=1, null=False, blank=False, on_delete=models.CASCADE)
    unit = models.ForeignKey(Units, null=False, blank=False ,on_delete=models.CASCADE)
    
    # -------------------------------------------------------
    # fields
    date_deposit_received = models.DateField(default=None ,null=True)
    
    email = CharField(max_length=50, default='')
    email2 = CharField(max_length=50, null=True)
    emergency_contact = CharField(max_length=50, default='')
    emergency_contact_name = CharField(max_length=50, default='', null=True)
    
    lease_start_date = models.DateField(default=None, null=True)
    lease_expiration_date = models.DateField(default=None, null=True)
    
    payments_delay = IntegerField(default=0)
    payments_on_time = IntegerField(default=0)
    
    name = CharField(max_length=50) 
    
    phone = CharField(max_length=50, null=False)
    phone2 = CharField(max_length=50 ,null=True, default=None)
    preferred_communications = CharField(max_length=20, default='')
    
    role = CharField(max_length=50, default='')
    
    secondary_communications = CharField(max_length=20, null=True, default=None)
    standing_qualification=models.IntegerField(default=0)
    
    tenant_type = CharField(max_length=50, default='main')
    

class Links(models.Model):
    
    # Foreign key
    owner = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, default=1)
    # --------------------------------
    # fields
    
    link = models.CharField(max_length=500)
    link_name = models.CharField(max_length=150)
    link_type = models.CharField(max_length=150)
    