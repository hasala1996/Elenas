import uuid,json
from collections import OrderedDict
from rest_framework.test import APIClient
from django.utils.http import urlencode
from user.models import User,TaskStatus,Task
from .core import TestMixin, TestSingleObjectMixin



class TestViewsetMixin(TestMixin):
    def setUp(self):
        self.client = APIClient()
        # Configuración previa para cada prueba
        self.user = User.objects.create_superuser(
            username="Hamilton",
            password="abcd.1234"
        )

        self.user_test = User.objects.create(
            id = uuid.uuid4(),
            username="Testing",
            password="abcd.1234",
            is_active=True,
            last_name="Testing",
            email="Testing@1.com"
        )
        self.task_status_complete = TaskStatus.objects.create(
            id = uuid.uuid4(),
            name = "Complete",
            description = "this task is completed successfully",
            code_id ="ok"
        )

        self.task_login = Task.objects.create(
            id = uuid.uuid4(),
            name = "Login implementation task.",
            description = "this task is for login implementation",
            task_status = None,
            user = self.user_test
        )

        self.login_url = '/api/1.0/login/'
        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': "abcd.1234"
            },
            format='json'
        )
        self.jwt = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt)


    
    def assert_viewset(self, key, method, route, username, kwargs={}, query_params={}, data={},format=None):

        status_map = self.status_map[key]

        url = route

        if method == 'get':
            response = self.client.get(url, query_params)
        else:
            if query_params:
                url += '?' + urlencode(query_params)

            if method == 'post':
                response = self.client.post(url, data,format=format)
            elif method == 'put':
                response = self.client.put(url, json.dumps(
                    data), content_type='application/json')
            elif method == 'patch':
                response = self.client.patch(url, json.dumps(
                    data), content_type='application/json')
            elif method == 'delete':
                response = self.client.delete(url,data,format=format)
            else:
                raise RuntimeError('method \'%s\' not supported' % method)

        content_type = response.get('Content-Type')

        if content_type == 'text/html':
            content = response.content
        elif content_type == 'application/json':
            content = response.json()
        elif content_type == 'application/zip':
            content = '<zip>'
        else:
            content = None

        msg = OrderedDict((
            ('username', username),
            ('url', url),
            ('method', method),
            ('data', data),
            ('status_code', response.status_code),
            ('content_type', content_type),
            ('content', content)
        ))

        self.assertEqual(response.status_code, status_map[username], msg=msg)
        return msg

    def assert_list_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('list_viewset', 'get', 'list', username, kwargs=kwargs, query_params=query_params)

    def assert_detail_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('detail_viewset', 'get', 'detail', username, kwargs=kwargs, query_params=query_params)

    def assert_create_viewset(self, username, kwargs={}, query_params={}, data={}):
        return self.assert_viewset('create_viewset', 'post', 'list', username, kwargs=kwargs, query_params=query_params, data=data)

    def assert_update_viewset(self, username, kwargs={}, query_params={}, data={}):
        return self.assert_viewset('update_viewset', 'put', 'detail', username, kwargs=kwargs, query_params=query_params, data=data)

    def assert_delete_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('delete_viewset', 'delete', 'detail', username, kwargs=kwargs, query_params=query_params)


class TestListViewsetMixin(TestViewsetMixin):

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username)


class TestCreateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(
                username, data=self.get_instance_as_dict(instance))


class TestDetailViewsetMixin(TestViewsetMixin):

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, kwargs={'pk': instance.pk})


class TestUpdateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_update_viewset(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_update_viewset(
                username, kwargs={'pk': instance.pk}, data=data)


class TestDeleteViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={'pk': instance.pk})
            instance.save(update_fields=None)


class TestReadOnlyModelViewsetMixin(TestListViewsetMixin,
                                    TestDetailViewsetMixin):
    pass


class TestModelViewsetMixin(TestListViewsetMixin,
                            TestDetailViewsetMixin,
                            TestCreateViewsetMixin,
                            TestUpdateViewsetMixin,
                            TestDeleteViewsetMixin):
    pass
