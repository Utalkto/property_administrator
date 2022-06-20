from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from to_do_list.models import ToDoList
from to_do_list.serializers import ToDoListSerializer


class ToDoListAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    
    def get(self, request):
        """Regresa las tareas indicadas

        Query parameters:
            tasks_completed (bool): por defecto es False, de ponerlo a True regresa solo las tareas marcadas como 
            completadas, si se marca como all, regresa todas las tareas
        """
        
        
        tasks_completed = request.GET.get('tasks_completed')
        
        if tasks_completed is None:
            tasks = ToDoList.objects.filter(onwer=request.user.id, completed=False)
        else:
            if tasks_completed.upper() == 'TRUE':
                tasks = ToDoList.objects.filter(onwer=request.user.id, completed=False)
            
            elif tasks_completed == 'all':
                tasks = ToDoList.objects.filter(onwer=request.user.id)
            
            else:
                return Response({'error': 'te dije que solo, all, True or False'})
        
        
        tasks_serializer = ToDoListSerializer(tasks)
        
        return Response(tasks_serializer.data)
            
    
    def post(self, request):
        
        request.data['owner'] = request.user.id
        todo_serializer = ToDoListSerializer(data=request.data)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(todo_serializer.data)
        else:
            return Response(todo_serializer.errors)
        
    
    def put(self, request):
        
        try:
            todo_list = ToDoList(id=(request.data['to_do_list_id'])).id
        except:
            return Response({'error': 'to_do_list_id: debe ser int'})
        
        request.data['owner'] = request.user.id
        todo_serializer = ToDoListSerializer(instance=todo_list, data=request.data)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(todo_serializer.data)
        else:
            return Response(todo_serializer.errors)