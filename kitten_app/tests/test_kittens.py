# kitten_app/tests/test_kittens.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from kitten_app.models import Kitten

@pytest.mark.django_db
class TestKittens:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        User = get_user_model()
        return User.objects.create_user(username='testuser', password='testpassword')

    @pytest.fixture
    def jwt_token(self, client, user):
        response = client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        return response.data['access']

    def test_create_kitten(self, client, jwt_token):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        response = client.post(reverse('kitten-list'), {
            'name': 'Fluffy',
            'age_months': 2,
            'breed': 'Persian',
            'color': 'White',
            'description': 'Persian white cute kitten'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Fluffy'

    def test_get_kitten(self, client, jwt_token, user):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        print(client)
        # user = self.context['request'].user

        kitten = Kitten.objects.create(name='Fluffy', age_months=2, breed='Persian', color='White', owner=user)
        
        response = client.get(reverse('kitten-detail', args=[kitten.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Fluffy'

    def test_update_kitten(self, client, jwt_token, user):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        kitten = Kitten.objects.create(name='Fluffy', age_months=2, breed='Persian', color='White', owner=user)
        
        response = client.patch(reverse('kitten-detail', args=[kitten.id]), {
            'name': 'Fluffy Updated',
            'age_months': 3,
            'breed': 'Siamese',
            'color': 'Black'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Fluffy Updated'

    def test_delete_kitten(self, client, jwt_token, user):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        kitten = Kitten.objects.create(name='Fluffy', age_months=2, breed='Persian', color='White', owner=user)

        response = client.delete(reverse('kitten-detail', args=[kitten.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Kitten.objects.filter(id=kitten.id).exists()
