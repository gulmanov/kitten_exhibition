from rest_framework import generics, permissions, serializers, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Kitten, Rating
from .serializers import KittenSerializer, RatingSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404


# User registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# Logout view
class LogoutView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Enforce JWT 

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class KittenListCreateView(generics.ListCreateAPIView):

    queryset = Kitten.objects.all().order_by('-inserted_time')
    serializer_class = KittenSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['inserted_time']
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]  # Enforce JWT 

    def get_queryset(self):
        queryset = Kitten.objects.all().order_by('-inserted_time')
        
        # Handle case-insensitive filtering for breed and color
        breed = self.request.query_params.get('breed')
        color = self.request.query_params.get('color')
        
        if breed:
            queryset = queryset.filter(breed__iexact=breed)  # Case-insensitive exact match
        if color:
            queryset = queryset.filter(color__iexact=color)  # Case-insensitive exact match


        # Handle age filtering
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        if min_age and max_age and min_age == max_age:
            queryset = queryset.filter(age_months=min_age)
        elif min_age and max_age:
            queryset = queryset.filter(age_months__gte=min_age, age_months__lte=max_age)
        elif min_age:
            queryset = queryset.filter(age_months__gte=min_age)
        elif max_age:
            queryset = queryset.filter(age_months__lte=max_age)

        return queryset

    def perform_create(self, serializer):        
        try:
            serializer.save(owner=self.request.user)
        except Exception as e:
            print(f"Error: {e}", flush=True)

    
class DistinctColorsView(generics.ListAPIView):
    def get(self, request):
        # Case-insensitive distinct colors
        colors = Kitten.objects.annotate(color_lower=Lower('color')).values_list('color_lower', flat=True).distinct()
        return Response(sorted(colors))

class DistinctBreedsView(generics.ListAPIView):
    def get(self, request):
        # Case-insensitive distinct breeds
        breeds = Kitten.objects.annotate(breed_lower=Lower('breed')).values_list('breed_lower', flat=True).distinct()
        return Response(sorted(breeds))

# Kitten Detail, Update, Delete View
class KittenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]  # Enforce JWT 


class RatingView(generics.GenericAPIView):
    serializer_class = RatingSerializer
#     # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Enforce JWT 

    def get(self, request, kitten_id):
        """Get all ratings for a specific kitten."""
        ratings = Rating.objects.filter(kitten__id=kitten_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

    def post(self, request, kitten_id):
        """Create a rating for a specific kitten."""
        kitten = get_object_or_404(Kitten, id=kitten_id)

        # Check if the user is the owner of the kitten
        if request.user == kitten.owner:
            return Response({"error": "You cannot rate your own kitten."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rated this kitten
        if Rating.objects.filter(user=request.user, kitten=kitten).exists():
            return Response({"error": "You have already rated this kitten."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the rating
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, kitten=kitten)
        kitten.update_average_rating()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, kitten_id):
        """Update the user's rating for a specific kitten."""
        kitten = get_object_or_404(Kitten, id=kitten_id)
        
        # Find the rating by the user for this specific kitten
        rating = get_object_or_404(Rating, user=request.user, kitten=kitten)

        # Update the rating
        serializer = self.get_serializer(rating, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        kitten.update_average_rating()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, kitten_id):
        """Delete the user's rating for a specific kitten."""
        kitten = get_object_or_404(Kitten, id=kitten_id)

        # Find the rating by the user for this specific kitten
        rating = get_object_or_404(Rating, user=request.user, kitten=kitten)

        # Delete the rating
        rating.delete()
        kitten.update_average_rating()

        return Response({"message": "Rating deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
