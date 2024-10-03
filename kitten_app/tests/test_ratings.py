# kitten_app/tests/test_ratings.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from kitten_app.models import Kitten, Rating

@pytest.mark.django_db
class TestRatings:
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
    
    @pytest.fixture
    def client2(self):
        return APIClient()

    @pytest.fixture
    def user2(self):
        User = get_user_model()
        return User.objects.create_user(username='testuser2', password='testpassword2')

    @pytest.fixture
    def jwt_token2(self, client2, user2):
        response = client2.post(reverse('token_obtain_pair'), {
            'username': 'testuser2',
            'password': 'testpassword2'
        })
        return response.data['access']    

    @pytest.fixture
    def kitten(self, client, jwt_token, user):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        return Kitten.objects.create(name='Fluffy', age_months=2, breed='Persian', color='White', owner=user)

    def test_kitten_owner_cannot_rate_own_kitten(self, client, jwt_token, kitten):
        """Ensure the kitten's owner cannot rate their own kitten."""
        url = reverse('rating-view', kwargs={'kitten_id': kitten.id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        response = client.post(url, {
            'score': 5
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "You cannot rate your own kitten."

    def test_other_user_can_rate_kitten(self, client2, jwt_token2, kitten):
        """Ensure another user can rate the kitten."""
        url = reverse('rating-view', kwargs={'kitten_id': kitten.id})
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token2)
        response = client2.post(url, {
            'score': 5  # Rating data
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['score'] == 5

    def test_get_rating(self, client, jwt_token, kitten, user2):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        rating = Rating.objects.create(kitten=kitten, score=5, user=user2)
        response = client.get(reverse('rating-view', kwargs={'kitten_id': kitten.id}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['score'] == 5

    def test_update_rating(self, client2, jwt_token2, kitten, user2):
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token2)
        rating = Rating.objects.create(kitten=kitten, score=5, user=user2)

        response = client2.put(reverse('rating-view', kwargs={'kitten_id': kitten.id}), {
            # 'kitten': kitten.id,
            'score': 4
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['score'] == 4

    def test_delete_rating(self, client2, jwt_token2, kitten, user2):
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token2)
        rating = Rating.objects.create(kitten=kitten, score=5, user=user2)

        response = client2.delete(reverse('rating-view', kwargs={'kitten_id': kitten.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Rating.objects.filter(id=rating.id).exists()
