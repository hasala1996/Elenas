
# from usuario.views import MyTokenObtainPairView, MyTokenRefreshPairView
from .viewsets import UserViewset,TaskViewset,TaskStatusViewset
from .views import MyTokenObtainPairView,SearchTaskView
from rest_framework.routers import SimpleRouter
from django.urls import path,include





router = SimpleRouter()
router.register(r'user', UserViewset, basename='managment user')
router.register(r'task', TaskViewset, basename='managment task')
router.register(r'task_status', TaskStatusViewset, basename='managment task_status')

urlpatterns = router.urls + [
    path('login/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('tasks/search/', SearchTaskView.as_view(), name='task_search'),
    
]
