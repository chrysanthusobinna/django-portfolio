from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Employment

class DeleteEmploymentViewTests(TestCase):
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

        # URL for deleting employment
        self.delete_url = reverse('delete_employment', kwargs={'id': self.employment.id})
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_delete_employment_valid(self):
        # Test deleting an employment entry with valid permissions
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the employment entry is deleted from the database
        with self.assertRaises(Employment.DoesNotExist):
            Employment.objects.get(id=self.employment.id)

    def test_delete_employment_no_permission(self):
        # Test deleting an employment entry without ownership
        self.client.logout()
        self.client.login(username='otheruser', password='password')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 404)

        # Verify the employment entry still exists
        self.assertTrue(Employment.objects.filter(id=self.employment.id).exists())

    def test_delete_employment_no_login(self):
        # Test deleting an employment entry without logging in
        self.client.logout()
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.delete_url}")

        # Verify the employment entry still exists
        self.assertTrue(Employment.objects.filter(id=self.employment.id).exists())

    def test_delete_employment_invalid_method(self):
        # Test deleting an employment entry using a GET request
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the employment entry still exists
        self.assertTrue(Employment.objects.filter(id=self.employment.id).exists())
