from .models import User,Task,TaskStatus
from .serializers import UserSerializer,TaskSerializer,TaskStatusSerializer
from task.task_serializer_list import TaskSerializerList
from rest_framework.permissions import IsAuthenticated
from rest_framework import  status,viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from elenas.pagination import StandardResultsSetPagination

class UserViewset(viewsets.ModelViewSet):
    """
        Viewset para administrar usuarios,
        se modifica metodo create para validar datos,
        delete,update,list disponibles desde viewset.
    """
    queryset=User.objects.all().order_by('id')
    serializer_class=UserSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Error creating user, reason : {e}",flush=True)
            return Response (f"{e}",status=status.HTTP_400_BAD_REQUEST)
        
        
class TaskStatusViewset(viewsets.ModelViewSet):
    queryset=TaskStatus.objects.all().order_by('id')
    serializer_class=TaskStatusSerializer
    permission_classes = (IsAuthenticated,) 


class TaskViewset(viewsets.ModelViewSet):
    queryset=Task.objects.all().order_by('id')
    serializer_class=TaskSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request,pk=None, *args, **kwargs):
        try:
            tasks = Task.objects.filter(user = request.user.id)
            page = self.paginate_queryset(tasks)
            response_serialized = TaskSerializerList(page)
            return self.get_paginated_response(response_serialized.data)
        except Exception as e :
            return Response (f"{e}",status=400)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Error creating task, reason : {e}",flush=True)
            return Response (f"{e}",status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request,*args, **kwargs):
          
        """
        Endpoint for update certain user data.
        """
        user = request.user
        instance = self.get_object()
        if user == instance.user:
            serializer = TaskSerializerList(instance,request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("you cant")
            return Response("You cannot edit tasks that are not yours.",status=status.HTTP_400_BAD_REQUEST) 

    def destroy(self, request,*args, **kwargs):
        """
        Endpoint for destroy tasks.
        """
        user = request.user
        instance = self.get_object()    
        if user == instance.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You cannot delete tasks that are not yours.",status=status.HTTP_400_BAD_REQUEST) 






