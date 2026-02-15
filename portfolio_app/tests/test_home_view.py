from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class HomeViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home-page.html')

    @patch('portfolio_app.views.Template')
    def test_home_view_post_valid(self, mock_template):
        mock_template.objects.filter.return_value = []
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('portfolio_app.views.Template')
    def test_home_view_post_invalid(self, mock_template):
        mock_template.objects.filter.return_value = []
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
