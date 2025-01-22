from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Employment

class AddEmploymentViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.add_url = reverse('add_employment')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_add_employment_valid(self):
        # Test adding an employment entry with valid data
        form_data = {
            'employer_name': 'Tech Corp',
            'job_title': 'Software Engineer',
            'description_of_duties': 'Developed software applications.',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.add_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify that the employment entry is created in the database
        self.assertTrue(Employment.objects.filter(user=self.user, employer_name='Tech Corp').exists())

    def test_add_employment_invalid(self):
        # Test adding an employment entry with invalid data (missing employer_name)
        form_data = {
            'job_title': 'Software Engineer',
            'description_of_duties': 'Developed software applications.',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.add_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify that no employment entry is created in the database
        self.assertFalse(Employment.objects.filter(user=self.user, job_title='Software Engineer').exists())

    def test_add_employment_no_login(self):
        # Test adding an employment entry without logging in
        self.client.logout()
        form_data = {
            'employer_name': 'Tech Corp',
            'job_title': 'Software Engineer',
            'description_of_duties': 'Developed software applications.',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.add_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.add_url}")
