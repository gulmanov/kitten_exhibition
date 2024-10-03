
import re
from rest_framework import serializers
from .models import Kitten, Rating
from django.contrib.auth.models import User

class KittenSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')  # Make owner read-only
    class Meta:
        model = Kitten
        fields = '__all__'

    def validate_breed(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Breed must have at least 2 characters.")
        if not re.match(r'^[A-Za-z\s\-]+$', value):
            raise serializers.ValidationError("Breed must contain only alphabetic characters, spaces, or dashes.")
        return value

    def validate_color(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Color must have at least 2 characters.")
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Color must contain only alphabetic characters or spaces.")
        return value

    def validate_age_months(self, value):
        if value < 0:
            raise serializers.ValidationError("Age must be a positive number.")
        return value
    
    
    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return Kitten.objects.create(name=validated_data['name'], age_months=validated_data['age_months'], description=validated_data['description'], breed=validated_data['breed'], color=validated_data['color'], owner=user)
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'kitten', 'score', 'created_at']
        read_only_fields = ['id', 'user','kitten', 'created_at']

    def create(self, validated_data):
        rating = Rating.objects.create(**validated_data)
        rating.kitten.update_average_rating()  # Update the kitten's average rating on create
        return rating

    def update(self, instance, validated_data):
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        instance.kitten.update_average_rating()  # Update the kitten's average rating on update
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
