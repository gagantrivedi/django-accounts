from django.test import TestCase
from account.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from rest_framework import status


class UserModelTest(TestCase):
    """ Test suite for user model"""

    def setUp(self):
        self.user_name = 'test'
        self.user_email_id = 'test@test.com'
        self.password = '123456'
        self.user = User(username=self.user_name, email_id=self.user_email_id, password=self.password)
        self.user.save()
        print ('user object created')

    def test_model_user(self):
        test = User.objects.get(email_id='test@test.com')
        self.assertEqual(self.user, test)


class RegisterUserProfileApiTest(TestCase):
    """Test suite for user registration api"""

    def setUp(self):
        self.client = APIClient()
        self.response = self.client.post(reverse('register'),
                                         {'username': 'bill', 'email_id': 'mail@me.com', 'password': '123456',
                                          'profile_picture_url': 'ww.'},
                                         format='json')

    def test_user_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
