from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, KittenListCreateView, KittenDetailView,  DistinctColorsView, DistinctBreedsView, RatingView

urlpatterns = [
    # User registration, login and logout
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Kittens management
    path('kittens/', KittenListCreateView.as_view(), name='kitten-list'),
    path('kittens/<int:pk>/', KittenDetailView.as_view(), name='kitten-detail'),

    # Distinct colors and breeds for filtering
    path('kittens/colors/', DistinctColorsView.as_view(), name='kitten-colors'),
    path('kittens/breeds/', DistinctBreedsView.as_view(), name='kitten-breeds'),

    # Ratings management for a specific kitten
    path('kittens/<int:kitten_id>/ratings/', RatingView.as_view(), name='rating-view'),
]