import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.JSONField(null=True)
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table  = 'user'
    


class TaskStatus(models.Model):
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name        = models.CharField(max_length=50,verbose_name='task name')
    description = models.CharField(max_length=100,verbose_name='task description')
    code_id     = models.CharField(max_length=100,blank=False,db_column='code_id',unique=True)

    class Meta: 
        db_table = "task_status"
        ordering =['id']

class Task(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length= 155,null=False)
    description = models.CharField(max_length=200,null=False)
    task_status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    
    class Meta: 
        db_table = "task"
        ordering =['id']
