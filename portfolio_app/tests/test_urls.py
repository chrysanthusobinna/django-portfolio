from django.test import SimpleTestCase
from django.urls import reverse, resolve
from portfolio_app import views   

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_user_profile_url_resolves(self):
        url = reverse('user_profile', kwargs={'username': 'testuser'})
        self.assertEqual(resolve(url).func, views.user_profile)

    def test_edit_user_profile_url_resolves(self):
        url = reverse('edit_user_profile', kwargs={'username': 'testuser'})
        self.assertEqual(resolve(url).func, views.edit_user_profile)

    def test_add_portfolio_url_resolves(self):
        url = reverse('add_portfolio')
        self.assertEqual(resolve(url).func, views.add_portfolio)

    def test_edit_portfolio_url_resolves(self):
        url = reverse('edit_portfolio', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.edit_portfolio)

    def test_delete_portfolio_url_resolves(self):
        url = reverse('delete_portfolio', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.delete_portfolio)

    def test_add_certification_url_resolves(self):
        url = reverse('add_certification')
        self.assertEqual(resolve(url).func, views.add_certification)

    def test_edit_certification_url_resolves(self):
        url = reverse('edit_certification', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.edit_certification)

    def test_delete_certification_url_resolves(self):
        url = reverse('delete_certification', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.delete_certification)

    def test_add_education_url_resolves(self):
        url = reverse('add_education')
        self.assertEqual(resolve(url).func, views.add_education)

    def test_edit_education_url_resolves(self):
        url = reverse('edit_education', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.edit_education)

    def test_delete_education_url_resolves(self):
        url = reverse('delete_education', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.delete_education)

    def test_add_employment_url_resolves(self):
        url = reverse('add_employment')
        self.assertEqual(resolve(url).func, views.add_employment)

    def test_edit_employment_url_resolves(self):
        url = reverse('edit_employment', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.edit_employment)

    def test_delete_employment_url_resolves(self):
        url = reverse('delete_employment', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, views.delete_employment)

    def test_save_about_url_resolves(self):
        url = reverse('save_about')
        self.assertEqual(resolve(url).func, views.save_about)

    def test_delete_about_url_resolves(self):
        url = reverse('delete_about')
        self.assertEqual(resolve(url).func, views.delete_about)

    def test_contact_update_url_resolves(self):
        url = reverse('contact_update')
        self.assertEqual(resolve(url).func, views.contact_update)

    def test_contact_delete_url_resolves(self):
        url = reverse('contact_delete')
        self.assertEqual(resolve(url).func, views.contact_delete)

    def test_save_profile_photo_url_resolves(self):
        url = reverse('save_profile_photo')
        self.assertEqual(resolve(url).func, views.save_profile_photo)

    def test_delete_profile_photo_url_resolves(self):
        url = reverse('delete_profile_photo')
        self.assertEqual(resolve(url).func, views.delete_profile_photo)
