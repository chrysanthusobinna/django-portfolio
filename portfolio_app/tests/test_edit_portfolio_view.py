from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from portfolio_app.models import Portfolio
from django.contrib.messages import get_messages

class EditPortfolioViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.portfolio1 = Portfolio.objects.create(
            user=self.user1, 
            title="Portfolio 1", 
            description="Description 1"
        )
        self.edit_url = reverse("edit_portfolio", args=[self.portfolio1.id])

    def test_user_not_logged_in_redirect(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.edit_url}")

    def test_user_editing_another_users_portfolio(self):
        self.client.login(username="user2", password="password2")
        response = self.client.post(self.edit_url, {
            "title": "New Title",
            "description": "Updated Description",
        })
        self.assertEqual(response.status_code, 404)
        self.portfolio1.refresh_from_db()
        self.assertEqual(self.portfolio1.title, "Portfolio 1")

    def test_form_with_invalid_data(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(self.edit_url, {
            "title": "",
            "description": "Updated Description",
        })
        self.assertEqual(response.status_code, 302)
        self.portfolio1.refresh_from_db()
        self.assertEqual(self.portfolio1.description, "Description 1")
