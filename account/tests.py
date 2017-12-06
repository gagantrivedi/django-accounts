from django.test import TestCase
from accounts.models import User


# Create your tests here.

class ModelTest(TestCase):
    """ Test suite for user model"""

    def setup(self):
        self.user_name = 'test'
        self.user_email = 'test@mail.com'
        self.password = '123456'
        self.user = User(user_name=self.user_name, email_id=self.user_email, password=self.password)
        self.user.save()

    def test_model_email(self):
        test= User.objects.get(email='test@mail.com')
        pass

