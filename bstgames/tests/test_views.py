from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from bstgames.models import GamePlatform


class HomeViewTestCase(TestCase):

    def setUp(self):
        for x in range(10):
            GamePlatform.objects.create(platform=f'platform_{x}')

    def test_get_context_data(self):
        request = self.client.get(reverse_lazy('bstgames:home'))
        platforms = GamePlatform.objects.all()
        self.assertEqual(request.status_code, 200)
        self.assertQuerysetEqual(list(request.context['platforms']), list(platforms))
        self.assertEqual(request.context['nbar'], 'home')


class SignUpViewTestCase(TestCase):

    def setUp(self):
        user_model = get_user_model()
        self.email = 'example@example.domain'
        self.password = user_model.objects.make_random_password()
        user_model.objects.create_user(
            username=self.email, email=self.email, password=self.password
        )

    def test_get(self):
        request = self.client.get(reverse_lazy('bstgames:signup'))
        self.assertEqual(request.status_code, 200)
        self.assertFalse(request.wsgi_request.user.is_authenticated)

        self.client.login(username=self.email, password=self.password)
        request = self.client.get(reverse_lazy('bstgames:signup'))
        self.assertEqual(request.status_code, 302)
        self.assertTrue(request.wsgi_request.user.is_authenticated)
        self.assertRedirects(request, reverse_lazy('bstgames:home'))

    def test_get_context_data(self):
        request = self.client.get(reverse_lazy('bstgames:signup'))
        self.assertEqual(request.context['nbar'], 'signup')
