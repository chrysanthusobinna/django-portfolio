from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import About

class AboutModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_about_creation(self):
        # Create an About instance
        about = About.objects.create(
            user=self.user,
            about='This is a test about section.'
        )
        self.assertEqual(about.user, self.user)
        self.assertEqual(about.about, 'This is a test about section.')
        self.assertEqual(str(about), f"About {self.user.username}")

    def test_about_update(self):
        # Create and update an About instance
        about = About.objects.create(
            user=self.user,
            about='This is a test about section.'
        )
        about.about = 'Updated about section.'
        about.save()

        # Retrieve and check updated value
        updated_about = About.objects.get(id=about.id)
        self.assertEqual(updated_about.about, 'Updated about section.')

    def test_about_delete(self):
        # Create and delete an About instance
        about = About.objects.create(
            user=self.user,
            about='This is a test about section.'
        )
        about_id = about.id
        about.delete()

        # Ensure the instance is deleted
        with self.assertRaises(About.DoesNotExist):
            About.objects.get(id=about_id)
