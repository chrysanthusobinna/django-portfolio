from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Education

class EditEducationViewTests(TestCase):
    def setUp(self):
        # Create a test user and an education entry
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='testuser', password='password')

        self.education = Education.objects.create(
            user=self.user,
            qualification='BSc Computer Science',
            institution_name='University of Test',
            start_date='2020-01-01',
            end_date='2023-01-01',
        )

        self.edit_url = reverse('edit_education', kwargs={'id': self.education.id})
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_edit_education_valid(self):
        # Test editing an education entry with valid data
        form_data = {
            'qualification': 'MSc Computer Science',
            'institution_name': 'University of Updated',
            'start_date': '2021-01-01',
            'end_date': '2024-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify the updated education entry
        self.education.refresh_from_db()
        self.assertEqual(self.education.qualification, 'MSc Computer Science')
        self.assertEqual(self.education.institution_name, 'University of Updated')
        self.assertEqual(str(self.education.start_date), '2021-01-01')
        self.assertEqual(str(self.education.end_date), '2024-01-01')

    def test_edit_education_invalid(self):
        # Test editing an education entry with invalid data
        form_data = {
            'qualification': '',  # Missing required field
            'institution_name': 'University of Test',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertRedirects(response, self.redirect_url)

        # Verify that the education entry is not updated
        self.education.refresh_from_db()
        self.assertEqual(self.education.qualification, 'BSc Computer Science')  # Original value

    def test_edit_education_not_owner(self):
        # Test that a user cannot edit another user's education entry
        self.client.logout()
        self.client.login(username='otheruser', password='password')

        form_data = {
            'qualification': 'MSc Computer Science',
            'institution_name': 'University of Updated',
            'start_date': '2021-01-01',
            'end_date': '2024-01-01',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertEqual(response.status_code, 404)  # Not found for unauthorized user

        # Verify that the education entry is not updated
        self.education.refresh_from_db()
        self.assertEqual(self.education.qualification, 'BSc Computer Science')  # Original value
