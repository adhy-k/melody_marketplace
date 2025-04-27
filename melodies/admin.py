from django.contrib import admin
from .models import UserProfile, Melody, Purchase

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Melody)
admin.site.register(Purchase)
