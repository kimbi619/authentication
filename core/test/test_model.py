
from django.test import TestCase

from rest_framework.test import APITestCase
from core.models import User

class ModelTest(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(email="usertest@gmail.com", password="password123!@", username="tester")
        self.assertIsInstance(user, User) 
        self.assertEqual(user.email, "usertest@gmail.com")
        self.assertFalse(user.is_staff)

    def test_creates_super_user(self):
        user = User.objects.create_superuser(email="admintest@gmail.com", password="password123!@", username="admin001")
        self.assertIsInstance(user, User) 
        self.assertEqual(user.email, "admintest@gmail.com")
        self.assertTrue(user.is_staff)


    ################################
    # Tests for normal user
    ################################
    def test_raise_error_when_username_is_not_given(self):
        self.assertRaises(ValueError, User.objects.create_user, username="", email="usertest@gmail.com", password="password123!@")
    
    def test_raise_error_with_message_when_username_is_not_given(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(email="admintest@gmail.com", password="password123!@", username='')

    
    def test_raise_error_when_email_is_not_given(self):
        self.assertRaises(ValueError, User.objects.create_user, username="tester", email="", password="password123!@")


    def test_raise_error_with_message_when_email_is_not_given(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(email="", password="password123!@", username="tester")
    
    
    ################################
    # Tests for super user
    ################################
    def test_create_superuser_with_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(email="admintest@gmail.com", password="password123!@", username='tester', is_staff=False)
    
    
    def test_create_superuser_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(email="admintest@gmail.com", password="password123!@", username='tester', is_superuser=False)
    
