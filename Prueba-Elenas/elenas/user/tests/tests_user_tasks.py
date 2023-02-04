from django.test import TestCase, Client
from rest_framework.test import APIClient
from user.models import User,TaskStatus,Task
from generator_coverage.viewsets import TestListViewsetMixin
import uuid
class UserTest(TestListViewsetMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.status_map = {
        1: {'admin': 200},
        2: {'admin':404},
        3: {'admin':201},
        4:{'admin':400},
        5:{'Hamilton':400},
        6:{'admin':204},
        7:{self.user.username:200}
        }

    def tests_login(self):
        data = {
            'username': "Hamilton",
            'password': "abcd.1234",
        }
        user_created = self.assert_viewset(1, "post", "/api/1.0/login/", "admin", data=data, format="json")
        self.assertIsInstance(user_created['content'], dict)

    def test_user_viewsets(self):
        self.assert_viewset(1, "get", "/api/1.0/user/", "admin")
        create_user ={
            "username":"lucas_2",
            "password":"abcd.1234",
            "first_name":"Alejandro",
            "last_name":"sanchez",
            "is_active":True,
            "email":"test@test.com"
        }
        create = self.assert_viewset(3, "post", "/api/1.0/user/", "admin",data=create_user,format='json')
    
    def test_task_status_viewset(self):
        create_task_status ={
            "id" : uuid.uuid4(),
            "name" : "Complete_task",
            "description" : "this task is completed successfully",
            "code_id" :"ok_code"
        }
        create = self.assert_viewset(3, "post", "/api/1.0/task_status/", "admin",data=create_task_status,format='json')
        self.assertIsInstance((create['content']), dict)

        listar = self.assert_viewset(1, "get", "/api/1.0/task_status/", "admin")
        self.assertIsInstance((listar['content']), list)
    

    def test_task_viewset(self):
        create_task = {
            "name" : "Login implementation task.",
            "description" : "this task is for login implementation",
            "task_status" :None,
            "user" : self.user.id
        }
        create_task_bad = {
            "task_status" :None,
            "user" : self.user.id
        }
        create_ok = self.assert_viewset(3, "post", "/api/1.0/task/", "admin",data=create_task,format='json')
        self.assertIsInstance((create_ok['content']), dict)
        
        create_bad = self.assert_viewset(4, "post", "/api/1.0/task/", "admin",data=create_task_bad,format='json')
        self.assertIsInstance((create_bad['content']), str)

        list_task_by_user = self.assert_viewset(1, "get", "/api/1.0/task/", "admin")
        self.assertIsInstance((list_task_by_user['content']), dict)

        id_update=str(create_ok['content']['id'])
        update_task_data = {
            "id": id_update,
            "name" : "Login implementation task updated hasala",
            "description" : "this task is for login implementation, was updated",
            "task_status" :None,
            "user" : str(self.user.id)
        }
        updated_task = self.assert_viewset(1, "put", "/api/1.0/task/{}/".format(str(id_update)), "admin",data=update_task_data,format='json')
        self.assertIsInstance((updated_task['content']), dict)
        
        updated_bad = self.assert_viewset(5, "put", "/api/1.0/task/{}/".format(str(self.task_login.id)),"Hamilton",data=update_task_data,format='json')
        self.assertIsInstance((updated_bad['content']), str)

        destroy_taks = self.assert_viewset(6, "delete", "/api/1.0/task/{}/".format(id_update), "admin")














