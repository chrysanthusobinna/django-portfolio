from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio_app.forms import ProfilephotoForm
from portfolio_app.models import Profilephoto

class ProfilephotoFormTests(TestCase):
    def setUp(self):
        # Create a test user to associate with the profile photo
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_profilephoto_form_valid(self):
        # Simulate a valid image file
        image = SimpleUploadedFile("image.jpg", b"image content", content_type="image/jpeg")
        form_data = {
            'profile_photo': image
        }
        form = ProfilephotoForm(data={}, files=form_data)
        self.assertTrue(form.is_valid())
