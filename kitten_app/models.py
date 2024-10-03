from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_age(value):
    if value < 0:
        raise ValidationError('Age must be a positive number.')

def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError('Rating must be between 1 and 5.')

class Kitten(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=51)
    age_months = models.IntegerField(validators=[validate_age])
    description = models.TextField()
    average_rating = models.FloatField(default=0)
    inserted_time = models.DateTimeField(auto_now_add=True)

    def update_average_rating(self):
        total_rating = sum([rating.score for rating in self.ratings.all()])
        rating_count = self.ratings.count()
        self.average_rating = total_rating / rating_count if rating_count > 0 else 0
        self.save()

    def __str__(self):
        return f'{self.name} ({self.breed})'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kitten = models.ForeignKey(Kitten, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[validate_rating])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'kitten')  # Each user can only rate a kitten once

    def __str__(self):
        return f'{self.user.username} rated {self.kitten.name}:  {self.score}'
