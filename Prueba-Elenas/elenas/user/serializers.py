from rest_flex_fields import FlexFieldsModelSerializer
from .models import User,Task,TaskStatus
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


UserModel = get_user_model()

class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name',
                  'last_name','is_active','password','email')
        
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TaskSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Task
        fields = ('id','name','description','task_status','user')

        def create(self, validated_data):
            task = Task.objects.create(
            name = validated_data['name'],
            description=validated_data['description'],
            task_status=validated_data['task_status'],
            user=validated_data['user'],
            )
            task.save()
            return task


class TaskStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ('id','name','description','code_id')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer para la customizar los parámetros encriptados en el JWT. 
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.last_login:
            token['last_login'] = user.last_login.strftime("%Y/%m/%d - %H:%M:%S")
        user.last_login = datetime.now()
        user.save()
        return token

