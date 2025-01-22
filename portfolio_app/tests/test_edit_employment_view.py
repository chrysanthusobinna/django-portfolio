from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Employment

class EditEmploymentViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create another user
        self.other_user = User.objects.create_user(username='otheruser', password='password')

        # Create an employment entry for the test user
        self.employment = Employment.objects.create(
            user=self.user,
            employer_name='Tech Corp',
            job_title='Software Engineer',
            description_of_duties='Developed software applications.',
            start_date='2020-01-01',
            end_date='2023-01-01',
        )

        # URL for editing employment
        self.edit_url = reverse('edit_employment', kwargs={'id': self.employment.id})
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_edit_employment_valid(self):
        # Test editing an employment entry with valid data
        form_data = {
            'employer_name': 'Updated Corp',
            'job_title': 'Senior Software Engineer',
            'description_of_duties': 'Managed software projects.',
            'start_date': '2019-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify the employment entry is updated in the database
        self.employment.refresh_from_db()
        self.assertEqual(self.employment.employer_name, 'Updated Corp')
        self.assertEqual(self.employment.job_title, 'Senior Software Engineer')

    def test_edit_employment_invalid(self):
        # Test editing an employment entry with invalid data (missing employer_name)
        form_data = {
            'employer_name': '',
            'job_title': 'Senior Software Engineer',
            'description_of_duties': 'Managed software projects.',
            'start_date': '2019-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify the employment entry is not updated in the database
        self.employment.refresh_from_db()
        self.assertNotEqual(self.employment.employer_name, '')

    def test_edit_employment_no_permission(self):
        # Test editing an employment entry that does not belong to the user
        self.client.logout()
        self.client.login(username='otheruser', password='password')
        form_data = {
            'employer_name': 'Unauthorized Edit',
            'job_title': 'Senior Software Engineer',
            'description_of_duties': 'Managed software projects.',
            'start_date': '2019-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertEqual(response.status_code, 404)

        # Verify the employment entry is not updated in the database
        self.employment.refresh_from_db()
        self.assertNotEqual(self.employment.employer_name, 'Unauthorized Edit')

    def test_edit_employment_no_login(self):
        # Test editing an employment entry without logging in
        self.client.logout()
        form_data = {
            'employer_name': 'No Login Edit',
            'job_title': 'Senior Software Engineer',
            'description_of_duties': 'Managed software projects.',
            'start_date': '2019-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.edit_url}")
