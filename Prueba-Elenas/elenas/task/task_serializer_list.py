from rest_framework import serializers
import json
from rest_framework.exceptions import APIException
from user.serializers import TaskSerializer


class Http400(APIException):
    status_code = 400


class TaskSerializerList(serializers.Serializer):
    id                = serializers.CharField(max_length=150)
    name              = serializers.CharField(max_length=150)
    description       = serializers.CharField(max_length=150)
    task_status       = serializers.UUIDField(required=False,allow_null=True)

    def save(self, **kwargs):
      self.update(self.instance, self.validated_data)


    def update(self, instance, validated_data):
      instance.name = validated_data["name"]
      instance.description = validated_data["description"]
      instance.task_status = validated_data["task_status"]
      instance.save()

    @property
    def data(self):
      info = self.instance
      if str(type(info)) == "<class 'list'>":	
        data_users = list(map(lambda t: TaskSerializerList(t).data,info))
      else:   
        data_users = super().data
        data_users['id'] = str(info.id)
        data_users['name'] =info.name
        data_users['description'] =info.description
        data_users['task_status'] =info.task_status
      return data_users

