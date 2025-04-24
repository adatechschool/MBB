# authentication\service\tests\authentication_service_tests.py

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from unittest.mock import patch, MagicMock

from authentication.service.exceptions import UserAlreadyExists, AuthenticationFailed, TokenBlacklistError
from authentication.service.infrastructure.django_auth_repository import DjangoAuthRepository
from common.models import User, Role
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterControllerTests(APITestCase):
    @patch('authentication.service.interface_adapters.controllers.publish_event')
    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.register')
    def test_register_success(self, mock_register, mock_publish_event):
        mock_register.return_value = 42
        url = '/api/auth/register/'
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'pass1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('detail', response.data['data'])
        mock_publish_event.assert_called_once_with(
            'user.registered',
            {'user_id': 42, 'username': 'testuser', 'email': 'test@example.com'}
        )

    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.register')
    def test_register_conflict(self, mock_register):
        mock_register.side_effect = UserAlreadyExists('Username exists')
        url = '/api/auth/register/'
        data = {'username': 'existing', 'email': 'exist@example.com', 'password': 'pass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['status'], 'error')
        self.assertIsNotNone(response.data['error'])
        self.assertEqual(response.data['error']['message'], 'Username exists')


class LoginControllerTests(APITestCase):
    @patch('authentication.service.interface_adapters.controllers.SessionClient.create_session')
    @patch('authentication.service.interface_adapters.controllers.publish_event')
    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.login')
    def test_login_success(self, mock_login, mock_publish_event, mock_create_session):
        mock_login.return_value = MagicMock(access='acc', refresh='ref')
        url = '/api/auth/login/'
        data = {'email': 'user@example.com', 'password': 'pass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['access'], 'acc')
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        mock_create_session.assert_called_once_with(refresh_token='ref', access_token='acc')
        mock_publish_event.assert_called_once_with('user.logged_in', {'email': 'user@example.com'})

    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.login')
    def test_login_failed(self, mock_login):
        mock_login.side_effect = AuthenticationFailed('Invalid')
        url = '/api/auth/login/'
        data = {'email': 'invalid@example.com', 'password': 'wrong'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['error']['message'], 'Invalid')


class LogoutControllerTests(APITestCase):
    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.logout')
    @patch('authentication.service.interface_adapters.controllers.publish_event')
    def test_logout_no_token(self, mock_publish_event, mock_logout):
        url = '/api/auth/logout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['error']['message'], 'Refresh token not provided.')

    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.logout')
    @patch('authentication.service.interface_adapters.controllers.publish_event')
    def test_logout_success(self, mock_publish_event, mock_logout):
        role = Role.objects.create(role_name='user')
        user = User.objects.create(username='u', email='e', role=role)
        self.client.force_authenticate(user=user)
        # Set refresh cookie
        self.client.cookies['refresh_token'] = 'some_token'
        url = '/api/auth/logout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure cookies are deleted
        self.assertNotIn('access_token', response.cookies)
        self.assertNotIn('refresh_token', response.cookies)
        mock_logout.assert_called_once_with('some_token')
        mock_publish_event.assert_called_once_with('user.logged_out', {'user_id': user.user_id})

    @patch('authentication.service.interface_adapters.controllers.AuthUseCase.logout')
    def test_logout_blacklist_error(self, mock_logout):
        role = Role.objects.create(role_name='user')
        user = User.objects.create(username='u2', email='e2', role=role)
        self.client.force_authenticate(user=user)
        self.client.cookies['refresh_token'] = 'bad_token'
        mock_logout.side_effect = TokenBlacklistError('Already blacklisted')
        url = '/api/auth/logout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['message'], 'Already blacklisted')


class DjangoAuthRepositoryTests(TestCase):
    def setUp(self):
        self.repo = DjangoAuthRepository()

    def test_register_and_duplicate(self):
        uid = self.repo.register('test', 'test@example.com', 'password')
        self.assertIsInstance(uid, int)
        user = User.objects.get(user_id=uid)
        self.assertEqual(user.username, 'test')
        with self.assertRaises(UserAlreadyExists):
            self.repo.register('test', 'test@example.com', 'password2')

    def test_authenticate_success_and_failure(self):
        role, _ = Role.objects.get_or_create(role_name='user')
        user = User(username='t2', email='t2@example.com', role=role)
        user.set_password('pwd')
        user.save()
        auth = self.repo.authenticate('t2', 'pwd')
        self.assertTrue(hasattr(auth, 'access'))
        self.assertTrue(hasattr(auth, 'refresh'))
        with self.assertRaises(AuthenticationFailed):
            self.repo.authenticate('t2', 'wrong')

    def test_blacklist_and_error(self):
        role, _ = Role.objects.get_or_create(role_name='user')
        user = User(username='t3', email='t3@example.com', role=role)
        user.set_password('pwd3')
        user.save()
        refresh = RefreshToken.for_user(user)
        token_str = str(refresh)
        # Should succeed
        self.repo.blacklist(token_str)
        # Blacklisting again should raise
        with self.assertRaises(TokenBlacklistError):
            self.repo.blacklist(token_str)
