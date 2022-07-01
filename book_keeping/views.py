# Django rest_framework

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# same app

from .models import BanksAccounts, Categories, Expenses
from .serializers import ExpensesGetSerializer, ExpensesPostSerializer, BankAccountSerializer, CategorySerializer


# Create your views here.


class ExpensesApi(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, request, expenses_id:str):
        
        if expenses_id == 'all':
            
            expenses = Expenses.objects.filter(unit__property_manager=request.user.id)
            
        else: 
            
            try:
                expenses = Expenses.objects.filter(id=int(expenses_id), unit__property_manager=request.user.id)
            except Expenses.DoesNotExist:
                
                return Response(
                    {
                        'error' : True,
                        'message_error' : 'There is no Expenses object with that id'
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExpensesGetSerializer(expenses, many=True)
        
        
        return Response(serializer.data)
    
    
    def post(self, request):
        
        serializer = ExpensesPostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            })    
            
    
    def put(self, request, expenses_id):
        
        try:
            expenses = Expenses.objects.get(id=int(expenses_id))
        except:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no Expenses object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        
        serializer = ExpensesPostSerializer(instance=expenses, data=request.data,)
        

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        else: 
            return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            }) 
        
    
    def delete(self, request, expenses_id):
        
        try:
            Expenses.objects.get(id=int(expenses_id)).delete()
        except:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no Expenses object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
                'success': True,
                'message' : 'Deleted',
            }) 


class BankAccountApi(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, request, bank_account_id:str):
        
        if bank_account_id == 'all':
            
            bank_accounts = BanksAccounts.objects.filter(landlord=request.user.id)
            
        else:
            try:
                bank_accounts = BanksAccounts.objects.filter(id=int(bank_account_id))
            except BanksAccounts.DoesNotExist:
                
                return Response(
                    {
                        'error' : True,
                        'message_error' : 'There is no BanksAccount object with that id'
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BankAccountSerializer(bank_accounts, many=True)
        
        
        return Response(serializer.data)
    
    
    def post(self, request):
        
        serializer = BankAccountSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            })    
            
    
    def put(self, request, bank_account_id):
        
        try:
            bank_account = BanksAccounts.objects.get(id=int(bank_account_id))
        except:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no BankAccount object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        
        serializer = BankAccountSerializer(instance=bank_account, data=request.data)
        

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        else: 
            return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            }) 
        
    
    def delete(self, request, bank_account_id):
        
        try:
            BanksAccounts.objects.get(id=int(bank_account_id)).delete()
        except BanksAccounts.DoesNotExist:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no BankAccount object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
                'success': True,
                'message' : 'Deleted',
            }) 


class CategoriesApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request):
        
        serializer = CategorySerializer(Categories.objects.all(), many=True)
        return Response(serializer.data)

