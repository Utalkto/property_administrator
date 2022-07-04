# pandas
import pandas as pd

# django

from django.utils import timezone

#rest_framework

from rest_framework.serializers import ModelSerializer

# models 

from properties.models import Property, Tenants, Unit
from register.models import CustomUser, Organization, OrganizationClient

# serializers 

from properties.serializers import PropertySerializer, TenantSerializer, UnitSerializer

from tickets.models import Suppliers
from tickets.serializers import SupplierPostSerializer

FILE_TYPES = ['csv', 'xlsx']


GENERAL_FIELDS_TO_EXCLUDE = ['id', 'log', 'last_time_edited', 'last_edition_made_by', 'datetime_created', 'created_by']


TABLES = {
    
    'property': {
        'model': Property,
        'serializer': PropertySerializer,
        'fields_to_exclude': GENERAL_FIELDS_TO_EXCLUDE + ['client', 'unit', 'log','id', 'img', 'photos'],
    },
    
    'unit': {
        'model': Unit,
        'serializer': UnitSerializer,
        'fields_to_exclude': GENERAL_FIELDS_TO_EXCLUDE + ['availability', 'tenants', 'candidate', 'unitpayments', 
                                                          'unitmonthlypayments', 'ticket', 'expenses', 'paymentrent'],
    },
    
    'tenant': {
        'model': Tenants,
        'serializer': TenantSerializer,
        'fields_to_exclude': GENERAL_FIELDS_TO_EXCLUDE + ['conversation', 'ticket', 'paymentrent', 'client', 
                                                          'unitpayments', 'deleted']
    },
    
    'supplier': {
        'model': Suppliers,
        'serializer': SupplierPostSerializer,
        'fields_to_exclude': GENERAL_FIELDS_TO_EXCLUDE + ['conversation', 'ticket', 'expenses', 'organization']
    }
   
}


# function to upload the data to the database

class Uploader():
    
    def __init__(self, user:CustomUser, client:OrganizationClient) -> None:
        
        self.user = user
        self.client = client


    def upload_file_to_database(self, filename:str, file_type:str, table:str):
        
        
        if file_type not in FILE_TYPES:
            return f'file_type must be {FILE_TYPES}', False

        if table not in TABLES.keys():
            return f'the name of the file must be one of these {list(TABLES.keys())}', False
        
        
        if file_type == 'csv':
            file:pd.DataFrame = pd.read_csv(filename, sep=';')
        
        elif file_type == 'xlsx':
            file:pd.DataFrame = pd.read_excel(filename)
        
        

        fields_in_db = self.get_nessary_fields(table=table)

        
        list_of_keys = list(file.keys())
        if list_of_keys != fields_in_db:
            
            raise Exception(f'Invalid list, the parameters must match the list of fields that are \
                            in the db for the model wanted: fields: {fields_in_db} and yours were {list_of_keys}')
            

        # start_uploading the data to the database
        
        current_table:dict = TABLES[table]
        return self.serialize_data_and_upload(file, current_table['serializer'])
    
        
    def serialize_data_and_upload(self, df:pd.DataFrame, serializer_model:ModelSerializer) -> bool:
        
        list_of_serializers = list()
        
        current_index = 0
        
        while not df.empty:
            serializer_dict = dict(created_by=self.user.id, 
                                   datetime_created=timezone.now(),
                                   client=self.client.id)
            
            for key in (df.keys()):
                
                serializer_dict[key] = df[key][current_index]

            list_of_serializers.append(serializer_dict)
            df.drop(index=df.index[0], 
                    axis=0, 
                    inplace=True)
            
            current_index += 1
            
        
        
        serializer:ModelSerializer = serializer_model(data=list_of_serializers, many=True)
        
        
        if serializer.is_valid():
            #serializer.save()
            return serializer.data, True
        
        else:
            return serializer.errors, False


    def get_nessary_fields(self, table:str) -> list:
        
        current_table = TABLES[table]
        
        fields_in_db = [field.name for field in current_table['model']._meta.get_fields() 
                        if field.name not in current_table['fields_to_exclude']]
        
        return fields_in_db
    
# Token 43302189e044f29f641d6305804b2b865287f098