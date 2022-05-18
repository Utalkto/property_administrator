from faker import Faker
import random

from register.models import UserCountries, UserCities, UserPlans, UserRoles

from properties.models import PropertyTypes, UnitTypes, PropertyCountries, PropertyCities, Properties, Units, Tenants
from properties.serializers import TenantSerializer, UnitsSerializer, PropertiesSerializer

from candidates.models import Candidate, CandidateStatus
from candidates.serializers import CandiatesSerializer


from django.http import JsonResponse


fake = Faker('en_CA')
Faker.seed(1115)

class FillDataBase:
    
    def __init__(self, number_of_data:int = 10) -> None:
        
        country = UserCountries(country="Canada")
        country.save()
        p = UserPlans(plan='free', cost=0)
        p.save()

        for i in range(number_of_data):
            c = UserCities(country = country, city = fake.unique.city())
            c.save()
            up = UserPlans(plan=f'plan{i}', cost=random.choice([10, 20, 30]))
            up.save()
            us = UserRoles(role=f'role{i}')
            us.save()
        
        create_property_dependecy()
        
        crear_propiedades()

        for _ in range(10):
            crear_unidades()
            
        
        for _ in range(10):
            crear_candidatos()
            crear_inquilinos()
        
        
        
        

def fill_data_base(request):
    FillDataBase()
    
    return JsonResponse({"done": True})



def create_property_dependecy():
    c = PropertyCountries(country='canada')
    c.save()
    
    pt = PropertyTypes(property_type='appartment')
    pt.save()
    
    ut = UnitTypes(unit_type="first unit type")
    ut.save()
    
    
    for _ in range(10):
        ci = PropertyCities(country=c, city=fake.unique.city())
        ci.save()
        
    

def crear_propiedades():

    price_p = random.randrange(200, 400)
    year_bu  = random.randrange(1990,2000)
    year_bou = random.randrange(2005, 2018)

    data = {
        "landlord" : 1,
        "address" : "Nuevo Circo",
        "coordenates" : {"coordenadas": "coordenadas"},
        "country" : "Venezuela",
        "city" : 1,
        "maps" : [],
        "name" : "El Viento",
        "price_paid": price_p,
        "photos" : {"foto":"foto"},
        "property_type": 1,
        "year_built": year_bu,
        "year_bought": year_bou
    }

    serializer = PropertiesSerializer (data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print('------------------------')
        print('Property serializer')
        
        print(serializer.errors)
        print('------------------------')
       


def crear_unidades():
    """Crear datos de forma eleatorea en la tabla de Unidades"""

    resident= random.randrange(1,5)
    pet_f = random.randrange(200,400)
    number_pets = random.randrange(1,5)
    extra_r = random.randrange(1,5)
    deposit_amo = random.randrange(200,400)
    bathrooms = random.randrange(1,5)
    extra_resident_pri = random.randrange(100, 400)
    room = random.randrange(1,5)
    rent = random.randrange(1000, 1500)

    data = {
        "landlord" : 1,
        "property_manager" : 1,
        "property": 1,
        "air_conditioning": "false",
        "appliances" : {"fecha": "2024-05-09"},
        "bathrooms" : bathrooms,
        "deposit_amount" : deposit_amo,
        "details" : {"fecha": "2022-05-07"},
        "date_deposit_received" : "2022-05-07",
        "extra_resident_price": extra_resident_pri,
        "extra_resident" : extra_r,
        "heating_type": "texto aqui",
        "has_pet": "True",
        "lease_type": "texto aqui",
        "name": "nombre",
        "notes" : "notas",
        "services": {"1": "comida", "2":"wifi"},
        "unit_type": 1,
        "number_of_pets": number_pets,
        "number_of_residents" : resident,
        "payments_email": "ycabaniel@utalkto.com",
        "parking_available" : "True",
        "parking_type" : "texto aqui",
        "shed": "False",
        "pet_fee": pet_f,
        "pet_policy": "politicas",
        "pets_living": "pets",
        "rented" : True,
        "rent" : rent,
        "rooms" : room,
        "square_feet_area": 3.00,
        "tenant": 1
    }

    serializer = UnitsSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
       
    else:
        print('------------------------')
        print('Unit Serializer')
        print(serializer.errors)
        print('------------------------')


def crear_inquilinos():

    units = random.randrange(71,81)
    payments_del  = random.randrange(0, 5)
    payments_on_t = random.randrange(0, 5)
    standing_qualif = random.randrange(1, 10)
    

    data = {
        "landlord" : 1,
        "unit" : units,
        "date_deposit_received" :"2022-04-20",
        "email" : "andresruse18@gmail.com",
        "email2" : "email2qutalkto.com",
        "emergency_contact": "04168174690",
        "emergency_contact_name" : "karman the jewish",
        "lease_start_date" : "2020-02-10",
        "lease_expiration_date": "2025-02-10",
        "payments_delay" : payments_del ,
        "payments_on_time": payments_on_t,
        "name": fake.unique.name(),
        "phone": "+584129266703",
        "phone2" : "+544168174690",
        "preferred_communications": random.choice(['phone', 'email']),
        "role": "role",
        "secondary_communications": "correo",
        "standing_qualification" : standing_qualif,
        "tenant_type" : "tipo",
        
    }

    serializer = TenantSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


def crear_candidatos():
    
    unit = random.randrange(1, 9)

    data = {
        "property_manager": 1,
        "unit": unit,
        "availability_date": {"fecha": "2022-05-06"},
        "adults_information":  {"email": "ycabaniel@utalkto.com"},
        "appointment": "2022-04-06",
        "current_address": "caracas, Nuevo Circo",
        "current_landlord_name": "carmen",
        "current_landlord_phone": "04121419422",
        "duration_of_lease": "texto",
        "expected_renting_duration": "1",
        "family_income": "1",
        "length_of_time_at_current_address": "1",
        "max_score": 0,
        "number_of_adults": 3,
        "number_of_children": 1,
        "pets": "1",
        "previous_unit_time": "texto",
        "preferred_move_in_date": "2022-06-01",
        "reason_for_moving": "trabajo",
        "relevant_information": "responsable",
        "score": 0,
        "status": 0
    }

    serializer = CandiatesSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


def tickets():
    
    tipos_de_mantenimiento = ['appliance', 'electrical']
    
    
