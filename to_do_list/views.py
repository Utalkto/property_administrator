from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from to_do_list.models import Task, ToDoList
from to_do_list.serializers import TaskSerializer

from drf_yasg.utils import swagger_auto_schema


class ToDoListAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: TaskSerializer()})
    def get(self, request, list_id):
        """Regresa las tareas indicadas

            Query parameters:
                tasks_completed (bool): por defecto es False, de ponerlo a True regresa solo las tareas marcadas como 
                completadas, si se marca como all, regresa todas las tareas
        """
        
        tasks_completed = request.GET.get('tasks_completed')
        
        try: ToDoList.objects.get(owner=request.user.id)
        except:
            
            t = ToDoList(
                owner = request.user,
                name = 'ToDoList'
            )
            
            t.save()
            
        
        if tasks_completed is None:
            tasks = Task.objects.filter(to_do_list__owner=request.user.id, completed=False)
        else:
            if tasks_completed == 'all':
                tasks = Task.objects.filter(to_do_list__owner=request.user.id)
                
            elif tasks_completed:
                tasks = Task.objects.filter(to_do_list__owner=request.user.id, completed=True)
            else:
                return Response({'error': 'te dije que solo, all, True or False'})
        
        
        tasks_serializer = TaskSerializer(tasks, many=True)
        
        return Response(tasks_serializer.data)
            
    
    def post(self, request, list_id):
        
        request.data['to_do_list'] = list_id
 
        todo_serializer = TaskSerializer(data=request.data)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(todo_serializer.data)
        else:
            return Response(todo_serializer.errors)
        
    
    def put(self, request, list_id):
        
        try:
            task:Task = Task.objects.get(id=(request.data['task_id']))
        except:
            return Response({'error': 'task_id: debe ser int'})
        
        request.data['task'] = task.task
        
        
        todo_serializer = TaskSerializer(instance=task, data=request.data)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(todo_serializer.data)
        else:
            return Response(todo_serializer.errors)
        
    
    def delete(self, request, list_id):
        try:
            task:Task = Task.objects.get(id=(request.data['task_id']))
        except:
            return Response({'error': 'task_id: debe ser int'})
        
        task.delete()
        