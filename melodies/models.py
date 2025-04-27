from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({'Creator' if self.is_creator else 'Buyer'})"

class Melody(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_melodies')
    title = models.CharField(max_length=200)
    notes = models.TextField()  # Store melody notes as space-separated string
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.creator.username}"

class Purchase(models.Model):
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.melody.title} purchased by {self.buyer.username}"
