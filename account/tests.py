from django.test import TestCase
from account.models import User


# Create your tests here.

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



