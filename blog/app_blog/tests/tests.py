from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from app_blog.models import Profile, Post
from app_blog.views import PostCreateView


class CreatePostTest(TestCase):

    def setUp(self):
        """Создание юзера для тестов"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, name='Test User', email='test@example.com')
        self.factory = APIRequestFactory()

    def test_post_create_view(self):

        """Тест на создание нового поста"""

        self.client.force_login(self.user)

        data = {
            'profile': self.profile.id,
            'title': 'Test Post',
            'body': 'This is a test post body.',
        }

        request = self.factory.post('/create_post/', data)
        response = PostCreateView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(Post.objects.filter(title='Test Post').exists())

        created_post = Post.objects.get(title='Test Post')
        self.assertEqual(created_post.profile, self.profile)

    def test_post_delete_view(self):

        """Тест на удаление существующего поста"""

        post = Post.objects.create(profile=self.profile, title='Test Post', body='This is a test post.')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('app_blog:post_delete', args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())


class RegisterViewTest(TestCase):

    """Класс с двумя тестами на регистрацию"""

    def test_register_view(self):

        """Тест с валидными данными"""

        client = Client()

        data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'name': 'John Doe',
        }

        response = client.post('/register/', data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_authenticated)

    def test_register_view_invalid_form(self):
        """Тест с невалидными данными"""

        client = Client()

        data = {
            'username': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'name': 'John Doe',
        }

        response = client.post('/register/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertFalse(Profile.objects.filter(user__username='newuser').exists())
        user = User.objects.filter(username='newuser')
        self.assertFalse(user.exists() and user[0].is_authenticated)


class LoginViewTest(TestCase):

    """Класс с набором тестов для Логина"""

    def setUp(self):

        """Создание юзера для тестоа"""

        self.client = Client()
        self.login_url = reverse('app_blog:login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):

        """Тест на успешный логин зарегистрированного пользователя"""

        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app_blog:main'))

