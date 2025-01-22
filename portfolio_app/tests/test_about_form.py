from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.forms import AboutForm
from portfolio_app.models import About

class AboutFormTests(TestCase):
    def setUp(self):
        # Create a test user to associate with the about section
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_about_form_valid(self):
        # Valid form data
        form_data = {
            'about': 'This is a test about section.'
        }
        form = AboutForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_about_form_invalid_missing_about(self):
        # Invalid form data (missing about field)
        form_data = {}
        form = AboutForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('about', form.errors)

    def test_about_form_save(self):
        # Test saving valid form data to the database
        form_data = {
            'about': 'This is a test about section.'
        }
        form = AboutForm(data=form_data)
        self.assertTrue(form.is_valid())
        about = form.save(commit=False)
        about.user = self.user  # Associate the about section with the test user
        about.save()

        # Verify the data is saved correctly
        saved_about = About.objects.get(id=about.id)
        self.assertEqual(saved_about.about, form_data['about'])
        self.assertEqual(saved_about.user, self.user)
