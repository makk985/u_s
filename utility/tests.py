from django.test import TestCase, Client
from django.urls import reverse
from .models import Service
from django.contrib.auth import get_user_model
User = get_user_model() 

#automated tests
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', util_acc_no='12345678', phone_number='1234567890')
        self.staff_user = User.objects.create_user(username='staffuser', email='staffuser@example.com', password='staffpassword', util_acc_no='12345679', phone_number='1234567899',is_staff=True)
        self.service = Service.objects.create(user=self.user, ser_req_no=12345, status='Pending')
        self.client.login(email='testuser@example.com', password='testpassword')
        

    def test_home_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'util_acc_no': '12345677'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_service_request_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('service_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_form.html')

    def test_service_request_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('service_request'), {
            'description': 'Test service request',
            'files': None
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_track_request_view_post(self):
        response = self.client.post(reverse('track_request'), {
            'search_query': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'track_request.html')

    def test_staff_dashboard(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_login.html')

    def test_service_update_view_post(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.post(reverse('service_update', args=[self.service.pk]), {
            'status': 'Completed',
            'note': 'Test note'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('staff_dashboard'))

    def test_service_docs(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('service_docs', args=[self.service.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('staff_dashboard'))
