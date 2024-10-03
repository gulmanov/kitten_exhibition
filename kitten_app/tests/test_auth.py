import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestAuthViews:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_user(self):
        def _create_user(username="testuser", password="password123"):
            user = User.objects.create_user(username=username, password=password)
            return user
        return _create_user

    def test_user_registration(self, api_client):
        # Arrange
        registration_url = reverse('register')  # Use the name of your registration URL
        user_data = {
            'username': 'newuser',
            'password': 'password123',
        }

        # Act
        response = api_client.post(registration_url, user_data, format='json')

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert 'username' in response.data  # Check if 'username' is returned
        assert response.data['username'] == 'newuser'  # Validate the correct username is returned


    def test_user_logout(self, api_client, create_user):
        # Arrange
        user = create_user()
        login_url = reverse('token_obtain_pair')  # Assuming this is your JWT login URL
        logout_url = reverse('logout')  # Use the name of your logout URL

        # Log in to get a JWT token
        login_data = {
            'username': 'testuser',
            'password': 'password123',
        }
        login_response = api_client.post(login_url, login_data, format='json')
        tokens = login_response.data
        refresh_token = tokens['refresh']

        # Act
        logout_response = api_client.post(
            logout_url, {'refresh_token': refresh_token}, format='json'
        )

        # Assert
        assert logout_response.status_code == status.HTTP_200_OK
        assert logout_response.data['message'] == 'Successfully logged out'

    def test_user_logout_invalid_token(self, api_client, create_user):
        # Arrange
        user = create_user()
        logout_url = reverse('logout')

        # Act
        invalid_token = "fake_token"
        response = api_client.post(logout_url, {'refresh_token': invalid_token}, format='json')

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
