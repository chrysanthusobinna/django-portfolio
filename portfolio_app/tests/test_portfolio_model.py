from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Portfolio
import datetime

class PortfolioModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_portfolio_creation(self):
        # Create a Portfolio instance
        portfolio = Portfolio.objects.create(
            user=self.user,
            title='My Portfolio',
            description='A description of my portfolio.',
            link='https://example.com'
        )
        self.assertEqual(portfolio.user, self.user)
        self.assertEqual(portfolio.title, 'My Portfolio')
        self.assertEqual(portfolio.description, 'A description of my portfolio.')
        self.assertEqual(portfolio.link, 'https://example.com')
        self.assertEqual(str(portfolio), 'My Portfolio')

    def test_portfolio_update(self):
        # Create and update a Portfolio instance
        portfolio = Portfolio.objects.create(
            user=self.user,
            title='My Portfolio',
            description='A description of my portfolio.',
            link='https://example.com'
        )
        portfolio.title = 'Updated Portfolio'
        portfolio.save()

        # Retrieve and check updated value
        updated_portfolio = Portfolio.objects.get(id=portfolio.id)
        self.assertEqual(updated_portfolio.title, 'Updated Portfolio')

    def test_portfolio_delete(self):
        # Create and delete a Portfolio instance
        portfolio = Portfolio.objects.create(
            user=self.user,
            title='My Portfolio',
            description='A description of my portfolio.',
            link='https://example.com'
        )
        portfolio_id = portfolio.id
        portfolio.delete()

        # Ensure the instance is deleted
        with self.assertRaises(Portfolio.DoesNotExist):
            Portfolio.objects.get(id=portfolio_id)
