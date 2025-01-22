from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Education

class DeleteEducationViewTests(TestCase):
    def setUp(self):
        # Create test users and an education entry
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

        self.delete_url = reverse('delete_education', kwargs={'id': self.education.id})
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_delete_education_valid(self):
        # Test deleting an education entry with valid request
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify that the education entry is deleted
        self.assertFalse(Education.objects.filter(id=self.education.id).exists())

    def test_delete_education_invalid_method(self):
        # Test deleting an education entry with a GET request
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify that the education entry is not deleted
        self.assertTrue(Education.objects.filter(id=self.education.id).exists())

    def test_delete_education_not_owner(self):
        # Test that a user cannot delete another user's education entry
        self.client.logout()
        self.client.login(username='otheruser', password='password')

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 404)  # Unauthorized users get a 404 response

        # Verify that the education entry is not deleted
        self.assertTrue(Education.objects.filter(id=self.education.id).exists())
