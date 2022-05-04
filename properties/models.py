from django.db import models
from django.db.models.fields import CharField, BooleanField, IntegerField, TextField, DecimalField, DateField
from register.models import CustomUser

class Properties(models.Model):
    # foreign keys 
    landlord = models.ForeignKey(CustomUser, null=False, blank=False ,on_delete=models.CASCADE)
    
    # ------------------------------
    # fields 
    address = CharField(max_length=400)
    coordinates = models.JSONField()
    
    country = CharField(max_length=50)
    city = CharField(max_length=100)
    
    img = models.ImageField(upload_to='properties')
    maps_url =  models.URLField(default='')

    name = CharField(max_length=100, default='')
    
    price_paid = DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
    photos = models.JSONField()
    
    property_type = CharField(max_length=100)
    
    year_built = IntegerField()
    year_bought = IntegerField()
    


class Units(models.Model):
    # foreign keys 
    
    landlord = models.ForeignKey(CustomUser, null=False, blank=False ,on_delete=models.CASCADE)
    properties = models.ForeignKey(Properties, null=False, blank=False ,on_delete=models.CASCADE)
    
    #  ------------------------------------
    #  fields
    
    air_conditioning = BooleanField(default=False)
    appliances = models.JSONField()
    
    bathrooms = IntegerField(default=0)
    
    deposit_amount = DecimalField(max_digits=19, decimal_places=2)
    details = models.JSONField()
    date_deposit_received = DateField()
    
    extra_resident_price = DecimalField(max_digits=5, decimal_places=2, default=0)
    extra_resident = IntegerField(default=0)
    
    heating_type = CharField(max_length=50, default='')
    has_pet =  BooleanField(default=True)
    
    lease_type = CharField(max_length=100)
    
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
    
    rented = BooleanField(default=True) 
    rent = DecimalField(max_digits=19, decimal_places=2, default=0, null=False) 
    rooms = IntegerField(default=0)
    
    services = models.JSONField()
    square_feet_area = DecimalField(max_digits=19, decimal_places=2, default=0)
    shed = BooleanField(default=False)
    
    tenant = models.IntegerField(default=0)
    
    unit_type = CharField(max_length=100) 


class Tenants(models.Model):
    # foreign keys
    
    landlord = models.ForeignKey(CustomUser, default=1, null=False, blank=False ,on_delete=models.CASCADE)
    unit = models.ForeignKey(Units, null=False, blank=False ,on_delete=models.CASCADE)
    
    # -------------------------------------------------------
    # fields
    date_deposit_received = models.DateField(default=None ,null=True)
    
    email = CharField(max_length=50, default='')
    email2 = CharField(max_length=50 ,null=True)
    emergency_contact = CharField(max_length=50, default='phone')
    emergency_contact_name = CharField(max_length=50,default='', null=True)
    
    lease_start_date = models.DateField(default=None ,null=True)
    lease_expiration_date = models.DateField(default=None ,null=True)
    
    payments_delay = IntegerField(default=0)
    payments_on_time = IntegerField(default=0)
    
    name = CharField(max_length=50) 
    
    phone = CharField(max_length=50, null=False, default='')
    phone2 = CharField(max_length=50 ,null=True)
    preferred_communications = CharField(max_length=20, default='')
    
    role= CharField(max_length=50, default='')
    
    secondary_communications = CharField(max_length=20, default='')
    standing_qualification=models.IntegerField(default=0 )
    
    tenant_type = CharField(max_length=50, default='main')
    
    