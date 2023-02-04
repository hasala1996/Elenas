from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from .models import Task
from .serializers import TaskSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SearchTaskView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        description = self.request.query_params.get('description', None)
        if description is not None:
            self.queryset = self.queryset.filter(description__contains=description)
        return self.list(request, *args, **kwargs)