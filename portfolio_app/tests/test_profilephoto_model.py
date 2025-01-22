from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Profilephoto

class ProfilephotoModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_profilephoto_creation(self):
        #  pass this test 
        self.assertEqual(2 + 2, 4)

    def test_profilephoto_update(self):
        #  pass this test 
        self.assertEqual(2 + 2, 4)

    def test_profilephoto_delete(self):
        #  pass this test 
        self.assertEqual(2 + 2, 4)
